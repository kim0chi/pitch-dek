"""
Phase-3 gradient-boosted forecaster — WITH HONEST EVALUATION.

The whole point of this module is to TEST whether ML (LightGBM) actually beats
the simple seasonal methods on SukiMart's tiny, single-store, ~120-day history.
On data this small it very often does NOT, and saying so out loud is the win:
trees need many rows to learn seasonality that Holt-Winters already encodes for free.

Features (per day, engineered from the series + calendar):
  - day-of-week one-hot (Mon..Sun, 7 cols)
  - is_payday (0/1)
  - lag-1            (yesterday)
  - lag-7           (same weekday last week)
  - rolling-7 mean  (last 7 days, trailing)

Public API:
  lgbm_next(series, dows, paydays) -> float
      Train LightGBM on engineered features, predict the next day's demand.
      Falls back to a seasonal average if LightGBM is missing or history too short.
  compare(series, dows, paydays) -> dict
      Honest holdout: WAPE of LightGBM vs a seasonal baseline (avg of last 4
      same-weekdays), rolling one-step-ahead over a tail holdout. Tells you which won.
"""
import numpy as np

_DOW_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]  # matches config.DOW_INDEX

# minimum engineered rows we want before bothering to fit a tree (lag-7 + rolling-7
# eat the first 7 days; trees below this are essentially memorising noise).
_MIN_TRAIN_ROWS = 14


def _features(series, dows, paydays):
    """Build (X, y) of engineered rows. Row t predicts series[t]; uses only info < t.
    The first 7 days are dropped (need lag-7 and a full rolling-7 window)."""
    y = list(map(float, series))
    n = len(y)
    X, target = [], []
    for t in range(7, n):                       # need t-7 available
        roll7 = float(np.mean(y[t - 7:t]))      # trailing 7-day mean (excludes today)
        onehot = [1.0 if dows[t] == d else 0.0 for d in _DOW_ORDER]
        feat = onehot + [float(paydays[t]), y[t - 1], y[t - 7], roll7]
        X.append(feat); target.append(y[t])
    return np.asarray(X, dtype=float), np.asarray(target, dtype=float)


def _next_feature_row(series, dows, paydays, next_dow, next_payday):
    """Engineered feature row for the (unseen) next day given history + its calendar."""
    y = list(map(float, series))
    roll7 = float(np.mean(y[-7:]))              # trailing 7-day mean over last 7 actuals
    lag1 = y[-1]
    lag7 = y[-7] if len(y) >= 7 else y[0]
    onehot = [1.0 if next_dow == d else 0.0 for d in _DOW_ORDER]
    return np.asarray([onehot + [float(next_payday), lag1, lag7, roll7]], dtype=float)


def _seasonal_next(series, dows, next_dow, k=4):
    """Baseline: average of the last k same-weekday observations (else overall mean)."""
    y = list(map(float, series))
    idx = [i for i in range(len(y)) if dows[i] == next_dow][-k:]
    if not idx:
        return float(np.mean(y)) if y else 0.0
    return float(np.mean([y[i] for i in idx]))


def _fit_lgbm(X, y):
    """Fit a small LightGBM regressor tuned for tiny data. Returns model or raises."""
    import lightgbm as lgb                       # local import: handled by callers
    model = lgb.LGBMRegressor(
        n_estimators=120,
        learning_rate=0.05,
        num_leaves=7,            # shallow: tiny data, avoid overfitting
        min_child_samples=3,     # allow small leaves but not size-1
        subsample=0.9, colsample_bytree=0.9,
        reg_lambda=1.0,
        random_state=7, n_jobs=1, verbosity=-1,
    )
    model.fit(X, y)
    return model


_AVAIL = None
def available():
    """True only if LightGBM can actually FIT here (lightgbm + scikit-learn present).
    Cached. Used to gate the 'lgbm' candidate so we never label a fallback as ML."""
    global _AVAIL
    if _AVAIL is None:
        try:
            X = np.arange(20, dtype=float).reshape(-1, 1); y = np.arange(20, dtype=float)
            _fit_lgbm(X, y)
            _AVAIL = True
        except Exception:
            _AVAIL = False
    return _AVAIL


def lgbm_next(series, dows, paydays, next_is_payday=0, next_dow=None):
    """Predict next-day demand with LightGBM (falls back to seasonal avg on failure).

    series  : list[float]  daily quantities, oldest..newest
    dows    : list[str]    weekday per day (aligned with series)
    paydays : list[int]    1 if that day is a payday else 0 (aligned with series)
    next_is_payday : 0/1   whether the day being forecast is a payday (avoids train/serve skew)
    next_dow : str|None    weekday of the forecast day; if None, inferred from the cycle
    """
    series = list(map(float, series))
    if next_dow is None:
        next_dow = _DOW_ORDER[(_DOW_ORDER.index(dows[-1]) + 1) % 7]
    X, y = _features(series, dows, paydays)
    if len(X) < _MIN_TRAIN_ROWS:
        return _seasonal_next(series, dows, next_dow)   # too little to train a tree
    try:
        model = _fit_lgbm(X, y)
    except Exception:
        return _seasonal_next(series, dows, next_dow)   # missing dep / fit failure -> safe fallback
    row = _next_feature_row(series, dows, paydays, next_dow, int(next_is_payday))
    return max(0.0, float(model.predict(row)[0]))


def _wape(pred, actual):
    pred, actual = np.asarray(pred, float), np.asarray(actual, float)
    denom = actual.sum()
    return float(np.abs(pred - actual).sum() / denom) if denom else 0.0


def compare(series, dows, paydays, holdout=None):
    """Honest rolling holdout: LightGBM vs seasonal baseline (avg of last 4 same-wd).

    Walks forward over the tail `holdout` days; at each step trains on the past only,
    predicts that one day with BOTH methods, scores WAPE over all holdout days.
    Returns a dict with both WAPEs, the winner, the margin, and whether LightGBM helped.
    """
    series = list(map(float, series))
    n = len(series)
    if holdout is None:
        holdout = max(7, min(21, n // 4))       # ~last quarter, clamped to a sane window
    start = n - holdout
    lgb_ok = True
    try:
        import lightgbm  # noqa: F401
    except ImportError:
        lgb_ok = False

    lgb_pred, base_pred, actual = [], [], []
    for t in range(start, n):
        hist, dh, ph = series[:t], dows[:t], paydays[:t]
        nd = dows[t]
        actual.append(series[t])
        base_pred.append(_seasonal_next(hist, dh, nd, k=4))
        if not lgb_ok:
            lgb_pred.append(base_pred[-1]); continue
        X, y = _features(hist, dh, ph)
        if len(X) < _MIN_TRAIN_ROWS:
            lgb_pred.append(base_pred[-1])      # cold-start: defer to baseline
            continue
        try:
            model = _fit_lgbm(X, y)
            row = _next_feature_row(hist, dh, ph, nd, paydays[t])
            lgb_pred.append(max(0.0, float(model.predict(row)[0])))
        except Exception:
            lgb_pred.append(base_pred[-1])

    w_lgb, w_base = _wape(lgb_pred, actual), _wape(base_pred, actual)
    margin = w_base - w_lgb                       # positive => LightGBM lower error (better)
    ml_helped = lgb_ok and margin > 0.005         # >0.5pp WAPE improvement to count as "helped"
    return {
        "wape_lightgbm": w_lgb,
        "wape_seasonal": w_base,
        "winner": "lightgbm" if w_lgb < w_base else "seasonal",
        "margin_wape": margin,
        "ml_helped": ml_helped,
        "holdout_days": holdout,
        "n_train_start": start,
        "lightgbm_available": lgb_ok,
        "verdict": (
            "LightGBM beat the seasonal baseline at this size."
            if ml_helped else
            "ML did NOT beat the simple seasonal baseline at this data size — "
            "stick with Holt-Winters / seasonal averaging."
        ),
    }


if __name__ == "__main__":
    # --- self-test on small synthetic data shaped like SukiMart's log -------------
    rng = np.random.default_rng(7)
    DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    shape = {"Mon": .95, "Tue": .90, "Wed": .95, "Thu": 1.0, "Fri": 1.15, "Sat": 1.25, "Sun": .85}
    N = 120
    dows = [DOW[i % 7] for i in range(N)]
    paydays = [1 if (i % 30) in (14, 15, 29, 0) else 0 for i in range(N)]   # ~15th & 30th
    mean = 22.0
    series = []
    for i in range(N):
        lam = mean * shape[dows[i]] * (1.20 if paydays[i] else 1.0) * (1 + 0.0006 * i)
        series.append(float(rng.poisson(max(0.1, lam))))

    print("=" * 64)
    print("LightGBM Phase-3 forecaster — HONEST self-test")
    print("=" * 64)
    nxt = lgbm_next(series, dows, paydays)
    print(f"lgbm_next() -> next-day forecast = {nxt:.1f}  (last actual {series[-1]:.0f})")

    res = compare(series, dows, paydays)
    print(f"\nHoldout = last {res['holdout_days']} days, rolling one-step-ahead")
    print(f"  WAPE  LightGBM : {res['wape_lightgbm']*100:5.1f}%")
    print(f"  WAPE  seasonal : {res['wape_seasonal']*100:5.1f}%  (avg of last 4 same-weekdays)")
    print(f"  winner         : {res['winner']}  (margin {res['margin_wape']*100:+.1f} pp WAPE)")
    print(f"  lightgbm avail : {res['lightgbm_available']}")
    print("\nVERDICT:")
    print(f"  {res['verdict']}")
    print("\nPlain-English takeaway:")
    if res["ml_helped"]:
        print("  ML helped here — but margins this thin rarely justify the added "
              "complexity/opacity vs Holt-Winters in production.")
    else:
        print("  ML did NOT help at ~120 days of single-store data. Gradient boosting "
              "needs many more rows to learn the weekly + payday pattern that "
              "Holt-Winters models structurally. Keep the simple forecaster.")
    print("=" * 64)
