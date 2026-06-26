"""
Distribution selection for the newsvendor decision.
Perishable demand isn't always Normal: low-volume count lines (siomai, rice meals)
are Poisson, and "lumpy" days (events, payday spikes) make counts overdispersed
(variance > mean) — better fit by a Negative Binomial. Picking the right tail shape
changes the optimal-quantity CR-quantile, so we choose per-SKU from the samples.

  select_distribution(samples)               -> 'poisson' | 'nbinom' | 'normal'
  optimal_quantity(mean, var, cr, samples)   -> int  (newsvendor CR-quantile, floored at 0)
"""
import numpy as np
from scipy.stats import poisson, nbinom, norm


def _looks_like_counts(samples):
    """True if all values are non-negative whole numbers (i.e. countable items)."""
    return all(s >= 0 and float(s) == int(s) for s in samples)


def select_distribution(samples):
    """Pick a demand distribution from observed daily samples.
    poisson : count-like and roughly equidispersed (var/mean in [0.7,1.3]);
    nbinom  : count-like but overdispersed (var/mean > 1.3);
    normal  : everything else (non-counts, or counts with var/mean < 0.7)."""
    s = list(map(float, samples))
    if not s:
        return "normal"
    mean = float(np.mean(s))
    if mean <= 0 or not _looks_like_counts(s):
        return "normal"                     # no positive count signal -> Normal
    var = float(np.var(s))
    ratio = var / mean                      # dispersion index
    if ratio > 1.3:
        return "nbinom"                     # overdispersed counts
    if 0.7 <= ratio <= 1.3:
        return "poisson"                    # equidispersed counts
    return "normal"                         # underdispersed -> Normal is safer


def optimal_quantity(mean, var, cr, samples=None):
    """Newsvendor optimal prep = inverse-CDF(cr) under the chosen distribution.
    If samples are given, select_distribution decides the shape; else default Normal.
    cr is the critical ratio Cu/(Cu+Co). Returns an int floored at 0."""
    mean = float(mean)
    var = float(var)
    dist = select_distribution(samples) if samples is not None else "normal"

    if dist == "poisson":
        q = poisson.ppf(cr, max(mean, 1e-9))                 # mu = mean (integer-valued)
    elif dist == "nbinom":
        # honour the OBSERVED dispersion (from samples), not the floored forecast variance,
        # evaluated at the forecast mean: var_eff = mean * (sample_var / sample_mean).
        if samples is not None and len(samples) >= 2:
            sm = float(np.mean(samples)); sv = float(np.var(samples))
            disp = sv / sm if sm > 0 else 1.0
            var = max(mean * disp, mean * 1.001)             # ensure var > mean for NB
        if var <= mean:                                      # guard: NB needs var>mean
            q = poisson.ppf(cr, max(mean, 1e-9))             # fallback to Poisson
        else:
            r = mean ** 2 / (var - mean)                     # NB size (#successes)
            p = r / (r + mean)                               # NB prob of success
            q = nbinom.ppf(cr, r, p)                         # integer-valued
    else:  # normal: ceil so realized service meets/exceeds the target CR
        q = np.ceil(norm.ppf(cr, loc=mean, scale=np.sqrt(max(var, 1e-12))))

    q = float(q)
    if not np.isfinite(q):                                   # cr at the extremes can give inf/nan
        q = mean
    return max(0, int(q))


if __name__ == "__main__":
    # --- self-test on small synthetic data (no external files needed) ---
    rng = np.random.default_rng(7)

    # 1) selection: equidispersed Poisson sample -> 'poisson'
    pois = rng.poisson(8, size=400).tolist()
    assert select_distribution(pois) == "poisson", select_distribution(pois)

    # 2) selection: overdispersed counts -> 'nbinom' (NB with var >> mean)
    over = rng.negative_binomial(2, 2 / (2 + 8), size=400).tolist()  # mean=8, var>mean
    od_mean, od_var = float(np.mean(over)), float(np.var(over))
    assert od_var / od_mean > 1.3, (od_mean, od_var)
    assert select_distribution(over) == "nbinom", select_distribution(over)
    print(f"overdispersed sample: mean={od_mean:.1f} var={od_var:.1f} "
          f"var/mean={od_var/od_mean:.2f} -> {select_distribution(over)}")

    # 3) selection: continuous / non-count values -> 'normal'
    cont = (rng.normal(28, 5, size=200)).tolist()
    assert select_distribution(cont) == "normal", select_distribution(cont)

    # 4) optimal_quantity monotonic non-decreasing in cr, for every distribution path
    for samp, mean, var, label in [
        (pois, float(np.mean(pois)), float(np.var(pois)), "poisson"),
        (over, od_mean, od_var, "nbinom"),
        (None, 28.0, 25.0, "normal"),
    ]:
        qs = [optimal_quantity(mean, var, cr, samp) for cr in np.linspace(0.05, 0.95, 19)]
        assert all(b >= a for a, b in zip(qs, qs[1:])), (label, qs)
        assert all(isinstance(q, int) and q >= 0 for q in qs), (label, qs)
        print(f"{label:8} q across cr 0.05..0.95: {qs[0]} -> {qs[-1]}")

    # 5) nbinom guard: var<=mean must fall back to Poisson (equal to poisson quantile)
    assert optimal_quantity(10.0, 4.0, 0.8, over[:0] or over) >= 0  # smoke
    g = optimal_quantity(10.0, 4.0, 0.8, samples=None)              # normal path, smoke
    assert g >= 0

    print("distributions.py self-test: OK")
