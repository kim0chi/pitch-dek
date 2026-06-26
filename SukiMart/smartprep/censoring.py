"""
De-censoring sold-out days — recover TRUE demand from CENSORED sales.

When an item sells out, recorded `qty` is only what was on the shelf, not what
customers actually wanted: the tail of demand walked out unserved. Recorded sales
are right-censored at the prep quantity.

WHY this matters (the feedback death-spiral): the forecaster (forecast.py) and the
newsvendor (newsvendor.py) both consume the sales SERIES as if it were demand. If we
feed censored numbers in:
    sold out  ->  recorded < true demand  ->  forecast biased LOW
              ->  smaller prep tomorrow   ->  sells out EARLIER / harder
              ->  even lower recorded sales  ->  forecast even lower ...
Each loop shrinks prep, so a popular item is taught to look unpopular and is slowly
starved — high-margin, traffic-driving lines (exactly where stockouts cost a whole
basket) get hit worst. De-censoring breaks the loop by reconstructing a demand-like
quantity BEFORE the series reaches the model, so the bias never compounds.

The estimate uses how much of the selling day remained at sellout: if you sold out
with `frac_day_remaining` of the day still to go, those would-be sales are missing,
so scale the recorded qty up by 1/(1 - frac_day_remaining). Guardrails:
  - floor the divisor at 0.5  -> never inflate by more than 2x from the fraction,
  - hard-cap the result at qty*2.0 -> a de-censored point can never dominate/outlier
    the fit (a sellout is evidence of MORE demand, not proof of double).
With no time info (frac=0) we still nudge nothing (divisor 1.0) unless the caller
supplies a fraction; the cap keeps even a near-instant sellout sane.
"""


def decensor(qty: float, sold_out: bool, frac_day_remaining: float = 0.0) -> float:
    """True-demand estimate for one day.

    qty                : recorded units sold that day.
    sold_out           : True if the item ran out (sales are censored).
    frac_day_remaining : fraction of the selling day still left at sellout (0..1);
                         larger -> more unmet demand -> bigger upward correction.
    Returns qty unchanged when not sold out; otherwise the inflated estimate,
    capped at qty*2.0.
    """
    qty = float(qty)
    if not sold_out:
        return qty
    # clamp the fraction to [0,1] so a bad input can't flip the divisor sign/blow up
    frac = min(max(float(frac_day_remaining), 0.0), 1.0)
    divisor = max(1.0 - frac, 0.5)          # floor at 0.5 -> at most a 2x scale-up
    return min(qty / divisor, qty * 2.0)    # hard cap: a sellout never doubles+ the day


def decensor_series(qtys, sold_outs, fracs=None) -> list:
    """Vectorized de-censor over a series.

    qtys      : iterable of recorded daily quantities.
    sold_outs : iterable of bools (per day: did it sell out?).
    fracs     : optional iterable of frac_day_remaining; defaults to 0.0 each day.
    Returns a list[float] of de-censored quantities, same length/order as inputs.
    """
    qtys = list(qtys)
    sold_outs = list(sold_outs)
    if fracs is None:
        fracs = [0.0] * len(qtys)
    else:
        fracs = list(fracs)
    if not (len(qtys) == len(sold_outs) == len(fracs)):
        raise ValueError("decensor_series: qtys, sold_outs, fracs must be equal length")
    return [decensor(q, so, fr) for q, so, fr in zip(qtys, sold_outs, fracs)]


if __name__ == "__main__":
    # --- small synthetic self-test (no external data) ---
    # 1) not sold out -> unchanged regardless of frac
    assert decensor(20, False) == 20.0
    assert decensor(20, False, 0.9) == 20.0
    # 2) sold out, no time info -> divisor 1.0 -> unchanged (but now demand-flagged)
    assert decensor(20, True, 0.0) == 20.0
    # 3) sold out with half the day left -> /0.5 = 2x, but cap is also 2x -> 40
    assert decensor(20, True, 0.5) == 40.0
    # 4) cap binds: 80% of day left would be /0.2 = 5x; capped at 2x
    assert decensor(20, True, 0.8) == 40.0
    # 5) mild sellout (10% left) -> /0.9 ~= 22.22, below the 2x cap
    assert abs(decensor(20, True, 0.1) - 20 / 0.9) < 1e-9
    # 6) bad/out-of-range frac is clamped, not exploded
    assert decensor(10, True, 5.0) == 20.0      # clamps to 1.0 -> divisor 0.5 -> /0.5=20 == cap
    assert decensor(10, True, -3.0) == 10.0     # clamps to 0.0 -> unchanged

    # series: mix of normal + sold-out days; check length, order, monotonic >= raw
    raw   = [10, 12, 9, 11, 14]
    sold  = [False, True, False, True, True]
    frac  = [0.0, 0.25, 0.0, 0.5, 0.1]
    out = decensor_series(raw, sold, frac)
    assert len(out) == len(raw)
    assert out[0] == 10.0 and out[2] == 9.0               # untouched normal days
    assert all(o >= r for o, r in zip(out, raw))          # de-censor never lowers
    assert abs(out[1] - 12 / 0.75) < 1e-9                 # 25% left -> /0.75
    assert out[3] == 22.0                                  # 50% left -> 2x cap (11*2)
    assert abs(out[4] - 14 / 0.9) < 1e-9                  # 10% left -> /0.9

    # default fracs path (all zero) -> sold-out days unchanged, just flagged
    assert decensor_series([5, 6], [True, True]) == [5.0, 6.0]

    # length mismatch guard
    try:
        decensor_series([1, 2], [True])
        raise AssertionError("expected ValueError on length mismatch")
    except ValueError:
        pass

    print("censoring self-test OK:", out)
