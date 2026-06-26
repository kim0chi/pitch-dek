"""Smart-Prep configuration & SKU master (the perishable ready-to-eat lines)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")

WARMUP_DAYS  = 35      # history before backtest starts forecasting
HISTORY_DAYS = 120     # length of the sample log datagen creates
GUT_OVERPREP = 1.15    # baseline 'gut-feel': day-blind flat prep ~15% over avg (keeps the
                       # baseline's spoilage inside the case's stated 8-15% — a FAIR comparator)
SERVICE_FLOOR_SD = 0.20  # floor on forecast std (as fraction of mean) to avoid overconfidence

# Optional service-level floor (min critical-ratio quantile). Default 0.0 = OFF: we prep the
# PROFIT-OPTIMAL pure-newsvendor quantity per item (replaces the earlier intangible 'goodwill'
# premium, so the decision and the profit accounting stay consistent). Raising this trades
# profit for availability (a knob the owner can turn); at 0.80 it over-preps cheap lines.
SERVICE_FLOOR_CR = 0.0

# day-of-week & event demand shape (used only to GENERATE illustrative data)
DOW_INDEX = {"Mon":0.95,"Tue":0.90,"Wed":0.95,"Thu":1.00,"Fri":1.15,"Sat":1.25,"Sun":0.85}
PAYDAY_BUMP = 1.20     # 15th & 30th (+/-1 day)

# SKU master: id, name, category, price, cost, mean_daily, distribution
SKUS = [
    ("SIO", "Siomai (4pc)",   "ready-to-eat", 45,  22.0, 22, "poisson"),
    ("COF", "Hot coffee",     "ready-to-eat", 30,  12.0, 28, "normal"),
    ("RIC", "Rice meal",      "ready-to-eat", 65,  35.0,  8, "poisson"),
    ("PAN", "Pandesal (pc)",  "bakery",        4,   2.4, 40, "normal"),
    ("LUM", "Lumpia (pc)",    "ready-to-eat", 15,   8.0, 15, "poisson"),
]
FULL_SCALE = 158_000 / 80_510   # ratio: full SukiMart perishable vs staged (for annual scaling)
