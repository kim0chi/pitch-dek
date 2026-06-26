"""
Generate illustrative sample data (the LOGIC is the deliverable, not these numbers).
Writes: data/items.csv, data/calendar.csv, data/sample_sales.csv (= true demand),
        data/prep_log.csv (operational log: prepared/sold/spoiled/sold-out — what a POS sees).
Demand = mean × day-of-week shape × payday bump × noise, drawn from each SKU's distribution.
"""
import os, csv
from datetime import date, timedelta
import numpy as np
from config import SKUS, DOW_INDEX, PAYDAY_BUMP, HISTORY_DAYS, DATA_DIR, GUT_OVERPREP

START = date(2026, 2, 1)


def _payday(d): return d.day in (15, 16, 30, 31, 1)


def generate(seed=7):
    np.random.seed(seed)
    os.makedirs(DATA_DIR, exist_ok=True)
    dates = [START + timedelta(days=i) for i in range(HISTORY_DAYS)]

    with open(os.path.join(DATA_DIR, "items.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["sku_id","name","category","unit_price","unit_cost","mean_daily","dist"])
        for s in SKUS: w.writerow(s)

    with open(os.path.join(DATA_DIR, "calendar.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["date","dow","is_payday"])
        for d in dates: w.writerow([d.isoformat(), d.strftime("%a"), int(_payday(d))])

    # true demand
    demand = {}
    with open(os.path.join(DATA_DIR, "sample_sales.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["date","sku_id","qty"])
        for i, d in enumerate(dates):
            dow = d.strftime("%a")
            shape = DOW_INDEX[dow] * (PAYDAY_BUMP if _payday(d) else 1.0) * (1 + 0.0006 * i)
            for sku_id, name, cat, price, cost, mean, dist in SKUS:
                lam = max(0.1, mean * shape)
                qty = np.random.poisson(lam) if dist == "poisson" else max(0, round(np.random.normal(lam, lam*0.16)))
                qty = int(qty); demand[(d, sku_id)] = qty
                w.writerow([d.isoformat(), sku_id, qty])

    # operational prep_log: a day-blind 'gut-feel' prep -> sales are CENSORED on sold-out days
    means = {s[0]: s[5] for s in SKUS}
    with open(os.path.join(DATA_DIR, "prep_log.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["date","sku_id","prepared","sold","spoiled","sold_out","frac_remaining"])
        for d in dates:
            for sku_id in means:
                dem = demand[(d, sku_id)]
                prepared = max(0, round(means[sku_id] * GUT_OVERPREP))
                sold = min(prepared, dem); spoiled = max(0, prepared - dem); so = dem > prepared
                # demand arrives ~uniformly: it sells out after (prepared/dem) of the day, so the
                # true fraction of day REMAINING at sell-out is 1 - prepared/dem. The RECORDED
                # sell-out time is noisy (staff don't log the exact minute) -> de-censoring must
                # recover demand from an IMPERFECT signal, so the validation isn't circular.
                if so and dem:
                    frac_true = 1.0 - prepared / dem
                    frac = float(np.clip(frac_true + np.random.normal(0, 0.06), 0.0, 0.95))
                    frac = round(frac, 2)
                else:
                    frac = 0.0
                w.writerow([d.isoformat(), sku_id, prepared, sold, spoiled, int(so), frac])
    return DATA_DIR


if __name__ == "__main__":
    print("Wrote sample data to", generate())
