"""
Demand forecasting for the next day, with AUTOMATIC model selection.
Candidate models:
  baseline   exponentially-weighted same-weekday average (robust on short history)
  hw         Holt-Winters (triple exponential smoothing), weekly seasonality (period 7)
  hw_events  hw, then multiply by a learned payday factor (events.py)
  lgbm       gradient-boosted trees (lightgbm_model.py) — only offered for the honest
             model COMPARISON, never auto-deployed (it doesn't beat HW at this data size).
select_model() picks the lowest-WAPE deployable model on a holdout; forecast_with() runs one.
"""
import warnings
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from config import SERVICE_FLOOR_SD
import events
import lightgbm_model


def candidate_models(paydays=None, include_ml=False):
    """Deployable models. `include_ml` adds 'lgbm' (only for comparison, and only if it
    can actually fit here) — it is never selected for deployment."""
    base = ["baseline", "hw"] if paydays is None else ["baseline", "hw", "hw_events"]
    if include_ml and paydays is not None and lightgbm_model.available():
        base = base + ["lgbm"]
    return base


def _seasonal_baseline(y, dows, next_dow, k=6, alpha=0.45):
    """Mean AND std from the same-weekday observations (so cross-weekday seasonal swing
    doesn't inflate next-day uncertainty)."""
    idx = [i for i in range(len(y)) if dows[i] == next_dow][-k:]
    if not idx:
        return float(np.mean(y)), float(np.std(y))
    vals = [y[i] for i in idx]
    w = [(1 - alpha) ** (len(vals) - 1 - j) for j in range(len(vals))]
    mean = sum(v * wi for v, wi in zip(vals, w)) / sum(w)
    sd = float(np.std(vals)) if len(vals) > 1 else float(np.std(y))
    return float(mean), sd


def _hw(y):
    with warnings.catch_warnings():                       # scope the noise to this fit only
        warnings.simplefilter("ignore")
        fit = ExponentialSmoothing(y, trend="add", seasonal="add", seasonal_periods=7,
                                   initialization_method="estimated").fit()
        mean = float(fit.forecast(1)[-1])
        sd = float(np.std(np.asarray(y) - np.asarray(fit.fittedvalues)))
    return mean, sd


def _floor_sd(sd, mean):
    return max(sd or 0.0, SERVICE_FLOOR_SD * max(mean, 1.0), float(np.sqrt(max(mean, 1.0))))


def forecast_with(model, y, dows, next_dow, paydays=None, next_is_payday=0):
    """Forecast next-day demand with a SPECIFIC model. Returns (mean, sd)."""
    y = list(map(float, y))
    mean = sd = None
    try:
        if model in ("hw", "hw_events") and len(y) >= 21:
            mean, sd = _hw(y)
            if model == "hw_events" and paydays is not None:
                f = events.learn_event_factors(y, list(paydays))
                mean = events.apply_event(mean, next_is_payday, f)
        elif model == "lgbm" and lightgbm_model.available() and len(y) >= 21 and paydays is not None:
            mean = float(lightgbm_model.lgbm_next(y, list(dows), list(paydays),
                                                  next_is_payday, next_dow))
            _, sd = _seasonal_baseline(y, dows, next_dow)
    except Exception:
        mean = None
    if mean is None or not np.isfinite(mean) or mean < 0:
        mean, sd = _seasonal_baseline(y, dows, next_dow)
        if model == "hw_events" and paydays is not None:     # keep the payday signal on fallback
            mean = events.apply_event(mean, next_is_payday, events.learn_event_factors(y, list(paydays)))
    return max(0.0, mean), _floor_sd(sd, mean)


def select_model(y, dows, paydays=None, holdout=14):
    """Pick the deployable model with the lowest WAPE on a rolling holdout of the last
    `holdout` days. Call on TRAINING data only (avoids look-ahead)."""
    y = list(map(float, y)); n = len(y)
    if n < holdout + 21:
        return "hw" if n >= 21 else "baseline"
    best, best_wape = "hw", float("inf")
    for m in candidate_models(paydays):                      # ml excluded from deployment
        err = act = 0.0
        for t in range(n - holdout, n):
            ip = int(paydays[t]) if paydays is not None else 0
            mean, _ = forecast_with(m, y[:t], dows[:t], dows[t],
                                    paydays[:t] if paydays is not None else None, ip)
            err += abs(mean - y[t]); act += y[t]
        wape = err / act if act else float("inf")
        if wape < best_wape - 1e-9:
            best_wape, best = wape, m
    return best


def forecast_next(y, dows, next_dow, paydays=None, next_is_payday=0, model="hw"):
    """Backward-compatible entry. Returns (mean, sd, model_used).
    model='hw' preserves the original behaviour; model='auto' selects the best deployable."""
    if model == "auto":
        model = select_model(y, dows, paydays)
    mean, sd = forecast_with(model, y, dows, next_dow, paydays, next_is_payday)
    used = model if (model in ("hw", "hw_events", "lgbm") and len(y) >= 21) else "seasonal-baseline"
    return mean, sd, used
