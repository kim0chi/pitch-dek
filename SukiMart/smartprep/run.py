"""
SukiMart Smart-Prep — end-to-end run (v2).
  1) load data (+ payday calendar)          2) per-SKU model selected ONCE, used everywhere
  3) distribution-aware newsvendor prep      4) Morning Dashboard (xlsx + phone HTML)
  5) backtest (accuracy + spoilage & service BOTH ways + profit uplift)
  6) honest model comparison (incl. LightGBM)   7) censoring validation (preprocessing step)
Run from repo root:  ./.venv/bin/python SukiMart/smartprep/run.py
"""
import os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
import config, datagen, forecast, newsvendor, backtest, report, html_report, censoring


def load():
    if not os.path.exists(os.path.join(config.DATA_DIR, "sample_sales.csv")):
        datagen.generate()
    items = pd.read_csv(os.path.join(config.DATA_DIR, "items.csv")).to_dict("records")
    sales = pd.read_csv(os.path.join(config.DATA_DIR, "sample_sales.csv"), parse_dates=["date"]).sort_values("date")
    cal = pd.read_csv(os.path.join(config.DATA_DIR, "calendar.csv"), parse_dates=["date"]).set_index("date")
    dates = sorted(sales["date"].unique())
    dows = [pd.Timestamp(d).strftime("%a") for d in dates]
    paydays = [int(cal.loc[pd.Timestamp(d), "is_payday"]) for d in dates]
    series = {it["sku_id"]: sales[sales.sku_id == it["sku_id"]].set_index("date")["qty"].reindex(dates).fillna(0).tolist()
              for it in items}
    tomorrow = pd.Timestamp(dates[-1]) + dt.timedelta(days=1)
    return items, series, dows, paydays, tomorrow.strftime("%a"), int(tomorrow.day in (15, 16, 30, 31, 1))


def censoring_check():
    """Preprocessing validation: on real POS data you only see SOLD (censored on sell-outs);
    de-censoring recovers demand from an imperfect sell-out-time signal. Show it beats naive 'sold'."""
    p = os.path.join(config.DATA_DIR, "prep_log.csv"); s = os.path.join(config.DATA_DIR, "sample_sales.csv")
    if not (os.path.exists(p) and os.path.exists(s)):
        return None
    m = pd.read_csv(p, parse_dates=["date"]).merge(
        pd.read_csv(s, parse_dates=["date"]), on=["date", "sku_id"]).rename(columns={"qty": "true_demand"})
    so = m[m.sold_out == 1]
    if so.empty:
        return None
    est = np.array([censoring.decensor(r.sold, True, r.frac_remaining) for r in so.itertuples()])
    naive = (so["sold"].sum() - so["true_demand"].sum()) / so["true_demand"].sum()
    dec = (est.sum() - so["true_demand"].sum()) / so["true_demand"].sum()
    return dict(soldout_rate=len(so) / len(m), naive_bias=naive, decensored_bias=dec)


def main():
    items, series, dows, paydays, tdow, tpay = load()
    # one model per SKU, selected on full history, used for BOTH the dashboard and the backtest
    models = {it["sku_id"]: forecast.select_model(series[it["sku_id"]], dows, paydays) for it in items}

    print("=" * 78); print(f"SUKIMART SMART-PREP v2  —  forecast for tomorrow ({tdow}{', PAYDAY' if tpay else ''})"); print("=" * 78)
    print(f"{'Item':16}{'model':12}{'forecast':>9}{'PREP':>6}   service-floor sizing")
    recs = []
    for it in items:
        mdl = models[it["sku_id"]]
        mean, sd = forecast.forecast_with(mdl, series[it["sku_id"]], dows, tdow, paydays, tpay)
        prep, CR = newsvendor.optimal_prep(mean, sd, it["unit_price"], it["unit_cost"],
                                           it["dist"], 0.0, samples=series[it["sku_id"]])
        cr_raw = (it["unit_price"] - it["unit_cost"]) / it["unit_price"]
        why = f"CR {cr_raw:.2f} -> serve {CR*100:.0f}%"
        recs.append(dict(name=it["name"], prep=prep, forecast=round(mean), method=mdl, why=why))
        print(f"{it['name']:16}{mdl:12}{mean:>9.1f}{prep:>6}   {why}")

    s = backtest.run(items, series, dows, paydays, models)
    print("-" * 78)
    print("BACKTEST (rolling one-step-ahead, gut-feel vs forecast+newsvendor):")
    print(f"  forecast accuracy  : WAPE {s['wape']*100:.0f}%")
    print(f"  service level      : {s['service_gut']*100:.0f}% (gut-feel)  ->  {s['service_level']*100:.0f}% (Smart-Prep)")
    print(f"  spoilage of prep   : {s['spoil_gut']*100:.0f}% (gut-feel)  ->  {s['spoil_sys']*100:.0f}% (Smart-Prep)")
    print(f"  PROFIT UPLIFT      : PHP {s['uplift_month']:,.0f}/mo  =  PHP {s['uplift_year_staged']:,.0f}/yr (staged)")
    print(f"                       PHP {s['uplift_year_full']:,.0f}/yr at full SukiMart")
    print(f"  model / SKU        : {', '.join(r['sku'].split()[0]+':'+r['model'] for r in s['rows'])}")

    cmps = [backtest.compare_models(series[it["sku_id"]], dows, paydays) for it in items]
    avg = {m: float(np.mean([c[m] for c in cmps if m in c])) for m in cmps[0]}
    print("-" * 78)
    print("MODEL COMPARISON (avg WAPE across SKUs, incl. ML):  "
          + "  ".join(f"{m} {w*100:.0f}%" for m, w in sorted(avg.items(), key=lambda kv: kv[1])))

    cc = censoring_check()
    if cc:
        print(f"CENSORING CHECK    : sell-outs on {cc['soldout_rate']*100:.0f}% of item-days · "
              f"naive 'sold' under-counts demand by {abs(cc['naive_bias'])*100:.0f}% · "
              f"de-censored to within {abs(cc['decensored_bias'])*100:.0f}% (imperfect sell-out timing)")

    out = report.write(recs, s, tdow); html = html_report.write_html(recs, s, tdow)
    print(f"\nWrote {out}\n      {html}")


if __name__ == "__main__":
    main()
