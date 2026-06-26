"""
SukiMart Smart-Prep — DEV dashboard (Streamlit).
  Loads data/*.csv the same way run.py does, builds per-SKU daily series + dows,
  lets you pick tomorrow's weekday and tune the profit-vs-availability dial (SERVICE_FLOOR_CR),
  then shows per-SKU forecast + newsvendor prep decision + rolling backtest.

Run with:  ./.venv/bin/streamlit run SukiMart/smartprep/app.py
"""
import os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from scipy.stats import norm, poisson
import config, datagen, forecast, newsvendor, backtest

DOW_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def load():
    """Same load path as run.py: items + per-SKU daily series aligned to a shared date axis."""
    if not os.path.exists(os.path.join(config.DATA_DIR, "sample_sales.csv")):
        datagen.generate()
    items = pd.read_csv(os.path.join(config.DATA_DIR, "items.csv")).to_dict("records")
    sales = pd.read_csv(os.path.join(config.DATA_DIR, "sample_sales.csv"), parse_dates=["date"])
    sales = sales.sort_values("date")
    dates = sorted(sales["date"].unique())
    dows = [pd.Timestamp(d).strftime("%a") for d in dates]
    series = {it["sku_id"]: sales[sales.sku_id == it["sku_id"]].set_index("date")["qty"].reindex(dates).fillna(0).tolist()
              for it in items}
    tomorrow = (pd.Timestamp(dates[-1]) + dt.timedelta(days=1))
    return items, series, dows, tomorrow.strftime("%a")


def build_dashboard(items, series, dows, tdow, service_floor):
    """Per-SKU forecast + newsvendor prep for the chosen tomorrow weekday.
    service_floor sets the minimum critical ratio (0.0 = profit-optimal; higher = more availability)."""
    rows = []
    for it in items:
        mean, sd, method = forecast.forecast_next(series[it["sku_id"]], dows, tdow)
        prep = newsvendor.optimal_prep(mean, sd, it["unit_price"], it["unit_cost"], it["dist"])
        cr_raw, Cu, Co = newsvendor.critical_ratio(it["unit_price"], it["unit_cost"])
        cr = max(cr_raw, service_floor)
        if dist := it["dist"]:
            if dist == "poisson":
                from scipy.stats import poisson as _p
                q = _p.ppf(cr, max(mean, 0.1))
            else:
                q = norm.ppf(cr, loc=mean, scale=max(sd, 1e-6))
            prep = max(0, int(np.ceil(float(q) if np.isfinite(q) else mean)))
        why = "prep MORE — high margin" if cr > 0.55 else ("prep LESS — spoils cheap" if cr < 0.45 else "match demand")
        rows.append(dict(
            Item=it["name"], Category=it["category"], Method=method,
            Forecast=round(mean, 1), Std=round(sd, 1),
            CR=round(cr, 2), PREP=prep, Why=why,
        ))
    return pd.DataFrame(rows)


def main():
    import streamlit as st
    st.set_page_config(page_title="SukiMart Smart-Prep (dev)", layout="wide")
    st.title("SukiMart Smart-Prep — dev dashboard")
    st.caption("Perishable demand forecast + newsvendor prep decision. Logic is the deliverable, not the numbers.")

    items, series, dows, default_tdow = load()

    with st.sidebar:
        st.header("Controls")
        tdow = st.selectbox("Tomorrow's weekday", DOW_ORDER,
                            index=DOW_ORDER.index(default_tdow) if default_tdow in DOW_ORDER else 3)
        service_floor = st.slider(
            "Service-floor CR (profit-vs-availability dial)",
            0.0, 0.95, float(config.SERVICE_FLOOR_CR), 0.05,
            help="0.0 = profit-optimal (default). Raise to guarantee more availability at the cost of profit.",
        )

    df = build_dashboard(items, series, dows, tdow, service_floor)

    st.subheader(f"Tomorrow's prep plan ({tdow})")
    st.dataframe(df, use_container_width=True, hide_index=True)
    c1, c2 = st.columns(2)
    c1.metric("SKUs", len(df))
    c2.metric("Total units to prep", int(df["PREP"].sum()))

    st.subheader("Backtest — rolling one-step-ahead (gut-feel vs Smart-Prep)")
    bt = backtest.run(items, series, dows)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("WAPE (accuracy)", f"{bt['wape']*100:.0f}%")
    m2.metric("In-stock (system)", f"{bt['service_level']*100:.0f}%",
              delta=f"{(bt['service_level']-bt['service_gut'])*100:+.0f}% vs gut")
    m3.metric("Spoilage (system)", f"{bt['spoil_sys']*100:.0f}%",
              delta=f"{(bt['spoil_sys']-bt['spoil_gut'])*100:+.0f}% vs gut", delta_color="inverse")
    m4.metric("Profit uplift / mo", f"PHP {bt['uplift_month']:,.0f}")
    st.caption(
        f"Annual uplift: PHP {bt['uplift_year_staged']:,.0f} (staged)  |  "
        f"PHP {bt['uplift_year_full']:,.0f} at full SukiMart"
    )


if __name__ == "__main__":
    main()
