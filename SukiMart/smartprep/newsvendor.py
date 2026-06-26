"""
Newsvendor optimizer — the prep-quantity decision under uncertainty.
Optimal prep Q* = F^-1(CR), CR = Cu/(Cu+Co):
  Cu = margin lost if you run out (under-prep)   = price - cost
  Co = cost lost if it spoils    (over-prep)     = cost
High critical ratio (high margin) -> prep above the mean; low CR -> below.
A service-level FLOOR (config.SERVICE_FLOOR_CR) lifts the CR so we never run out too often.
"""
import numpy as np
from scipy.stats import norm, poisson
import config


def critical_ratio(price, cost, penalty=0.0):
    Cu = (price - cost) + penalty   # underage = lost margin (+ optional premium, default 0)
    Co = cost                       # overage  = spoiled cost
    return Cu / (Cu + Co), Cu, Co


def optimal_prep(mean, std, price, cost, dist="normal", penalty=0.0, samples=None):
    """Return (prep_qty, effective_CR).
    The critical ratio is floored at config.SERVICE_FLOOR_CR (availability guard, read live
    so it can be tuned). If `samples` (recent demand history) are given, the demand
    distribution is auto-selected (Poisson / Negative-Binomial / Normal); else use `dist`."""
    cr_raw, Cu, Co = critical_ratio(price, cost, penalty)
    CR = max(cr_raw, config.SERVICE_FLOOR_CR)         # service-level floor (live)
    if samples is not None and len(samples) >= 10:
        import distributions
        q = distributions.optimal_quantity(mean, max(std, 1e-6) ** 2, CR, list(samples))
        return max(0, int(q)), CR
    if dist == "poisson":
        q = poisson.ppf(CR, max(mean, 0.1))
    else:
        q = norm.ppf(CR, loc=mean, scale=max(std, 1e-6))
    q = float(q)
    if not np.isfinite(q):                             # CR -> 1 (cost 0) can give inf
        q = mean
    return max(0, int(np.ceil(q))), CR


def evaluate(prep, demand, price, cost):
    """One day's outcome for a given prep vs realized demand."""
    sold = min(prep, demand)
    spoiled = max(0, prep - sold)
    lost = max(0, demand - prep)
    profit = sold * (price - cost) - spoiled * cost      # margin earned minus spoiled cost
    return dict(sold=sold, spoiled=spoiled, lost=lost, profit=profit, prepared=prep,
                spoil_value=spoiled * cost, sales_value=sold * price)
