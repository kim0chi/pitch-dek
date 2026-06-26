"""
Rolling one-step-ahead backtest: forecast + newsvendor vs day-blind 'gut-feel' prep.
Reports accuracy (WAPE), service level and spoilage FOR BOTH gut-feel and the system
(so the availability/waste trade-off is explicit), plus the profit uplift.
Per-SKU model is chosen once (on the warm-up window) and reused — no look-ahead, and the
same model the morning dashboard deploys. Distribution-aware prep (Poisson/NegBin/Normal).
"""
import numpy as np
import forecast, newsvendor
from config import WARMUP_DAYS, GUT_OVERPREP, FULL_SCALE


def _spoil_rate(spoiled_units, prepared_units):
    return spoiled_units / prepared_units if prepared_units else 0.0


def backtest_sku(series, dows, price, cost, dist, paydays=None, model=None):
    n = len(series)
    if model is None:
        model = forecast.select_model(series[:WARMUP_DAYS], dows[:WARMUP_DAYS],
                                      paydays[:WARMUP_DAYS] if paydays is not None else None)
    s = dict(profit=0.0, spoil=0.0, prep=0.0, abserr=0.0, act=0.0, soldout=0)
    g = dict(profit=0.0, spoil=0.0, prep=0.0, soldout=0)
    days = 0
    for t in range(WARMUP_DAYS, n):
        train, dtr, actual = series[:t], dows[:t], series[t]
        ip = int(paydays[t]) if paydays is not None else 0
        mean, sd = forecast.forecast_with(model, train, dtr, dows[t],
                                          paydays[:t] if paydays is not None else None, ip)
        sprep, _ = newsvendor.optimal_prep(mean, sd, price, cost, dist, 0.0, samples=train)
        gprep = max(0, round(float(np.mean(train)) * GUT_OVERPREP))
        rs = newsvendor.evaluate(sprep, actual, price, cost)
        rg = newsvendor.evaluate(gprep, actual, price, cost)
        s["profit"] += rs["profit"]; s["spoil"] += rs["spoiled"]; s["prep"] += rs["prepared"]
        s["abserr"] += abs(mean - actual); s["act"] += actual; s["soldout"] += rs["lost"] > 0
        g["profit"] += rg["profit"]; g["spoil"] += rg["spoiled"]; g["prep"] += rg["prepared"]
        g["soldout"] += rg["lost"] > 0
        days += 1
    d = days or 1
    return {
        "model": model, "days": days,
        "wape": s["abserr"] / s["act"] if s["act"] else 0.0,
        "service_sys": 1 - s["soldout"] / d,
        "service_gut": 1 - g["soldout"] / d,
        "spoil_sys": _spoil_rate(s["spoil"], s["prep"]),
        "spoil_gut": _spoil_rate(g["spoil"], g["prep"]),
        "uplift_day": (s["profit"] - g["profit"]) / d,
    }


def compare_models(series, dows, paydays=None, holdout=21):
    """WAPE of each candidate model (incl. LightGBM) over the last `holdout` days —
    the honest 'we tested N models' table."""
    y = list(map(float, series)); n = len(y); out = {}
    start = max(WARMUP_DAYS, n - holdout)
    if start >= n:
        return out
    for m in forecast.candidate_models(paydays, include_ml=True):
        err = act = 0.0
        for t in range(start, n):
            ip = int(paydays[t]) if paydays is not None else 0
            mean, _ = forecast.forecast_with(m, y[:t], dows[:t], dows[t],
                                             paydays[:t] if paydays is not None else None, ip)
            err += abs(mean - y[t]); act += y[t]
        out[m] = err / act if act else float("inf")
    return out


def run(items, series_by_sku, dows, paydays=None, models=None):
    rows, tot_uplift = [], 0.0
    for it in items:
        m = (models or {}).get(it["sku_id"])
        r = backtest_sku(series_by_sku[it["sku_id"]], dows, it["unit_price"], it["unit_cost"],
                         it["dist"], paydays, m)
        r["sku"] = it["name"]; rows.append(r); tot_uplift += r["uplift_day"]
    month = tot_uplift * 30
    agg = lambda k: float(np.mean([r[k] for r in rows]))
    return {
        "rows": rows,
        "uplift_day": tot_uplift, "uplift_month": month,
        "uplift_year_staged": month * 12,                 # year = month × 12 (consistent)
        "uplift_year_full": month * 12 * FULL_SCALE,
        "spoil_sys": agg("spoil_sys"), "spoil_gut": agg("spoil_gut"),
        "service_level": agg("service_sys"), "service_gut": agg("service_gut"),
        "wape": agg("wape"),
    }
