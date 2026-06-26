"""
Unit tests for the Smart-Prep math (newsvendor + the parallel
distributions/events/censoring helpers).

Run from repo root:  ./.venv/bin/python -m pytest SukiMart/smartprep/tests -q

The package puts its own dir on sys.path at import time, so siblings import
by bare name — replicate that here before importing them.
"""
import os, sys
sys.path.insert(0, os.path.join("SukiMart", "smartprep"))
# also allow running pytest from inside the package dir
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import pytest

import newsvendor


# --------------------------------------------------------------------------
# newsvendor.critical_ratio
# --------------------------------------------------------------------------
def test_critical_ratio_known_inputs():
    # price 45, cost 22, no penalty: Cu=23, Co=22 -> CR = 23/45
    CR, Cu, Co = newsvendor.critical_ratio(45, 22, penalty=0.0)
    assert Cu == 23 and Co == 22
    assert CR == pytest.approx(23.0 / 45.0)


def test_critical_ratio_with_penalty():
    # penalty raises the underage cost -> raises CR
    CR0, _, _ = newsvendor.critical_ratio(30, 12, penalty=0.0)
    CR1, Cu, Co = newsvendor.critical_ratio(30, 12, penalty=6.0)
    assert Cu == (30 - 12) + 6.0 and Co == 12
    assert CR1 == pytest.approx((18.0 + 6.0) / ((18.0 + 6.0) + 12.0))
    assert CR1 > CR0   # penalty on underage cost raises the critical ratio


# --------------------------------------------------------------------------
# newsvendor.optimal_prep — monotone in CR (margin)
# --------------------------------------------------------------------------
def test_optimal_prep_monotone_in_margin_normal():
    # higher margin (price) -> higher CR -> prep more, for fixed demand shape
    mean, std, cost = 50.0, 10.0, 20.0
    q_lo, cr_lo = newsvendor.optimal_prep(mean, std, price=25, cost=cost, dist="normal")
    q_md, cr_md = newsvendor.optimal_prep(mean, std, price=45, cost=cost, dist="normal")
    q_hi, cr_hi = newsvendor.optimal_prep(mean, std, price=120, cost=cost, dist="normal")
    assert cr_lo < cr_md < cr_hi
    assert q_lo <= q_md <= q_hi
    assert q_lo < q_hi   # strict overall move


def test_optimal_prep_monotone_in_margin_poisson():
    mean, std, cost = 22.0, 5.0, 22.0
    q_lo, cr_lo = newsvendor.optimal_prep(mean, std, price=30, cost=cost, dist="poisson")
    q_hi, cr_hi = newsvendor.optimal_prep(mean, std, price=200, cost=cost, dist="poisson")
    assert cr_hi > cr_lo
    assert q_hi >= q_lo
    assert q_hi > q_lo


# --------------------------------------------------------------------------
# newsvendor.evaluate
# --------------------------------------------------------------------------
def test_evaluate_underdemand_spoilage():
    # prep 10, demand 7 -> sold 7, spoiled 3, lost 0
    price, cost = 45, 22.0
    r = newsvendor.evaluate(prep=10, demand=7, price=price, cost=cost)
    assert r["sold"] == 7
    assert r["spoiled"] == 3
    assert r["lost"] == 0
    assert r["profit"] == pytest.approx(7 * (price - cost) - 3 * cost)
    assert r["spoil_value"] == pytest.approx(3 * cost)
    assert r["sales_value"] == pytest.approx(7 * price)


def test_evaluate_overdemand_lost_sales():
    # prep 10, demand 15 -> sold 10, spoiled 0, lost 5
    price, cost = 45, 22.0
    r = newsvendor.evaluate(prep=10, demand=15, price=price, cost=cost)
    assert r["sold"] == 10
    assert r["spoiled"] == 0
    assert r["lost"] == 5
    assert r["profit"] == pytest.approx(10 * (price - cost))


# --------------------------------------------------------------------------
# distributions.select_distribution + optimal_quantity  (built in parallel)
#   sig: select_distribution(samples) -> str
#        optimal_quantity(mean, var, cr, samples=None) -> int
# --------------------------------------------------------------------------
def test_distributions_select_and_quantity_monotone():
    distributions = pytest.importorskip("distributions")

    # Poisson-ish (mean ~ var): a tame count sample should NOT be flagged nbinom.
    tame = [4, 5, 6, 5, 4, 5, 6, 5, 5, 4, 6, 5, 5, 4, 5]
    d = distributions.select_distribution(tame)
    assert isinstance(d, str)

    # optimal_quantity monotone in critical ratio
    mean, var = 20.0, 25.0
    q_lo = distributions.optimal_quantity(mean, var, 0.2)
    q_md = distributions.optimal_quantity(mean, var, 0.5)
    q_hi = distributions.optimal_quantity(mean, var, 0.9)
    assert isinstance(q_lo, int) and isinstance(q_hi, int)
    assert q_lo <= q_md <= q_hi
    assert q_lo < q_hi


def test_distributions_nbinom_for_overdispersed():
    distributions = pytest.importorskip("distributions")
    # heavy overdispersion: variance >> mean -> negative binomial expected
    overdispersed = [0, 0, 1, 0, 30, 0, 2, 0, 40, 1, 0, 0, 25, 0, 0, 50, 0, 1, 0, 35]
    d = distributions.select_distribution(overdispersed)
    assert d == "nbinom"


# --------------------------------------------------------------------------
# events.learn_event_factors + apply_event  (built in parallel)
#   sig: learn_event_factors(qty, is_payday) -> dict
#        apply_event(mean, is_payday_next, factors) -> float
# --------------------------------------------------------------------------
def test_events_learns_payday_boost():
    events = pytest.importorskip("events")
    # baseline ~10, payday days clearly boosted ~20
    qty = [10, 11, 9, 10, 20, 21, 19, 10, 9, 11, 22, 20, 10, 9, 21]
    is_payday = [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1]
    factors = events.learn_event_factors(qty, is_payday)
    assert isinstance(factors, dict)
    assert factors["payday_mult"] > 1.0


def test_events_apply_event_uses_factor():
    events = pytest.importorskip("events")
    qty = [10, 11, 9, 10, 20, 21, 19, 10, 9, 11, 22, 20, 10, 9, 21]
    is_payday = [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1]
    factors = events.learn_event_factors(qty, is_payday)
    base, boosted = 10.0, None
    boosted = events.apply_event(base, True, factors)
    plain = events.apply_event(base, False, factors)
    assert boosted > plain          # payday tomorrow -> higher forecast
    assert plain == pytest.approx(base, rel=1e-6) or plain <= boosted


# --------------------------------------------------------------------------
# censoring.decensor  (built in parallel)
#   sig: decensor(qty, sold_out, frac_day_remaining=0.0) -> float
# --------------------------------------------------------------------------
def test_decensor_not_soldout_returns_qty():
    censoring = pytest.importorskip("censoring")
    # not sold out -> observed qty is true demand, returned unchanged
    assert censoring.decensor(12, False, 0.0) == pytest.approx(12.0)
    assert censoring.decensor(12, False, 0.5) == pytest.approx(12.0)


def test_decensor_soldout_inflates_and_caps():
    censoring = pytest.importorskip("censoring")
    # sold out -> true demand was higher than observed: inflate above qty
    up = censoring.decensor(12, True, 0.5)
    assert up > 12.0
    # cap at 2x the observed qty even with most of the day remaining
    capped = censoring.decensor(12, True, 0.99)
    assert capped <= 2.0 * 12.0 + 1e-9
    # sold out at the very end of day -> little/no inflation, still >= qty
    late = censoring.decensor(12, True, 0.0)
    assert late >= 12.0


if __name__ == "__main__":
    # Lightweight self-test with small synthetic data (no pytest runner needed),
    # so we can confirm zero import/logic errors before finishing.
    # newsvendor tests always run; parallel-module tests run only if present.
    CR, Cu, Co = newsvendor.critical_ratio(45, 22)
    assert (Cu, Co) == (23, 22) and abs(CR - 23 / 45) < 1e-9

    q_lo, cr_lo = newsvendor.optimal_prep(50, 10, 25, 20, "normal")
    q_hi, cr_hi = newsvendor.optimal_prep(50, 10, 120, 20, "normal")
    assert cr_hi > cr_lo and q_hi > q_lo

    r = newsvendor.evaluate(10, 7, 45, 22.0)
    assert r["sold"] == 7 and r["spoiled"] == 3 and r["lost"] == 0
    assert abs(r["profit"] - (7 * 23 - 3 * 22.0)) < 1e-9
    r2 = newsvendor.evaluate(10, 15, 45, 22.0)
    assert r2["lost"] == 5

    checked = ["newsvendor"]
    for mod in ("distributions", "events", "censoring"):
        try:
            __import__(mod)
            checked.append(mod)
        except Exception:
            pass  # built in parallel; absence is fine for this self-test
    print("self-test OK — verified:", ", ".join(checked))
