"""
Payday / holiday demand multipliers — a calendar lens the smoother can't see.
Holt-Winters tracks weekly seasonality but is blind to pay-cycle spikes (15th/30th).
We learn one multiplicative factor from history and apply it to tomorrow's mean
ONLY when tomorrow is a payday, leaving the std untouched (the decision layer
re-derives the prep quantity from the bumped mean).
"""
import numpy as np


def learn_event_factors(qty, is_payday):
    """Learn payday demand bump: mean(payday days)/mean(non-payday days).

    qty        : list[float]  daily sold/realized quantity
    is_payday  : list[int]    1 if that day is a payday, else 0 (aligned to qty)
    Returns {'payday_mult': r} clipped to [1.0, 2.0]; defaults to 1.0 (neutral)
    when there are fewer than 3 payday samples or the baseline is degenerate.
    """
    q = np.asarray(qty, dtype=float)
    p = np.asarray(is_payday)
    pay, non = q[p == 1], q[p == 0]
    if pay.size < 3 or non.size == 0:        # too little payday signal -> stay neutral
        return {"payday_mult": 1.0}
    base = non.mean()
    if base <= 0:                            # avoid divide-by-zero on a dead baseline
        return {"payday_mult": 1.0}
    mult = pay.mean() / base
    mult = float(min(2.0, max(1.0, mult)))   # clip: never shrink, cap the spike at 2x
    return {"payday_mult": mult}


def apply_event(mean, is_payday_next, factors):
    """Scale tomorrow's forecast mean by the payday factor if tomorrow is payday."""
    mult = factors.get("payday_mult", 1.0) if is_payday_next else 1.0
    return float(mean) * mult


if __name__ == "__main__":
    # Self-test: synthetic payday-boosted demand. Non-payday ~20, payday ~32 (1.6x).
    rng = np.random.default_rng(7)
    n = 60
    is_pay = [(1 if i % 15 in (0, 1) else 0) for i in range(n)]
    qty = [float(rng.poisson(32 if pd else 20)) for pd in is_pay]

    f = learn_event_factors(qty, is_pay)
    print("learned:", f)
    assert f["payday_mult"] > 1.0, "expected a payday bump > 1"
    assert 1.0 <= f["payday_mult"] <= 2.0, "factor must be clipped to [1,2]"

    # apply: payday scales, non-payday is identity
    assert apply_event(100.0, 1, f) == 100.0 * f["payday_mult"]
    assert apply_event(100.0, 0, f) == 100.0

    # default path: fewer than 3 payday samples -> neutral
    assert learn_event_factors([10, 11, 12, 13], [1, 0, 0, 0]) == {"payday_mult": 1.0}
    # clipping: huge ratio is capped at 2.0
    assert learn_event_factors([100, 100, 100, 1, 1], [1, 1, 1, 0, 0])["payday_mult"] == 2.0

    print("events.py self-test OK")
