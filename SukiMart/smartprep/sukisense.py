"""
SukiSense — the predictive engine inside Tina's POS.   ·   one engine, many modules

ONE ENGINE (shared core): forecast.py (Holt-Winters) · distributions.py · newsvendor.py
                          · censoring.py · events.py · backtest.py · config.py
MANY MODULES that plug into it:
    Smart-Prep    [BUILT]      perishable spoilage forecasting     (run.py / report.py)
    Smart Reorder [PROTOTYPE]  (s,S) reorder points for ~900 SKUs  (reorder.py)
    Utang Score   [PROTOTYPE]  explainable credit-risk scoring     (utang.py)
    Basket Lift   [PROTOTYPE]  market-basket cross-sell            (basket.py)

`python sukisense.py` prints the engine status board (one line per module).
Honesty: only Smart-Prep is built & backtested today; the rest are working prototypes that run
on the SAME engine — they switch on as the POS fills with real data (the SukiSense roadmap).
"""
import os, sys, warnings, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # siblings import by bare name


def _smartprep_summary():
    """Smart-Prep: run the rolling backtest and report spoilage + profit uplift + accuracy.
    Mirrors run.main() exactly (one model per SKU, same backtest call) so numbers reconcile."""
    import run, backtest, forecast
    items, series, dows, paydays, _tdow, _tpay = run.load()
    models = {it["sku_id"]: forecast.select_model(series[it["sku_id"]], dows, paydays) for it in items}
    s = backtest.run(items, series, dows, paydays, models)
    return (f"spoilage {s['spoil_gut']*100:.0f}%->{s['spoil_sys']*100:.0f}% · "
            f"+PHP {s['uplift_year_staged']:,.0f}/yr · WAPE {s['wape']*100:.0f}%")


def _reorder_summary():
    """Smart Reorder: how many grocery SKUs are at/below their reorder point right now."""
    import reorder
    with open(reorder.generate_sample()) as f:
        items = list(csv.DictReader(f))
    on_hand = {it["sku_id"]: int(it["on_hand"]) for it in items}
    orders = reorder.suggest_orders(items, on_hand)
    return f"{len(orders)} of {len(items)} SKUs need reorder today"


def _utang_summary():
    import utang
    return utang.summary()


def _basket_summary():
    import basket
    return basket.summary()


MODULES = [
    ("Smart-Prep",    "BUILT",     _smartprep_summary),
    ("Smart Reorder", "PROTOTYPE", _reorder_summary),
    ("Utang Score",   "PROTOTYPE", _utang_summary),
    ("Basket Lift",   "PROTOTYPE", _basket_summary),
]


def main():
    warnings.filterwarnings("ignore")   # keep the board clean (sklearn/statsmodels chatter)
    line = "=" * 78
    print(line)
    print("SukiSense — the predictive engine inside Tina's POS    ·    one engine, many modules")
    print(line)
    print(f"{'MODULE':15}{'STATUS':12}RESULT")
    print("-" * 78)
    for name, status, fn in MODULES:
        try:
            res = fn()
        except Exception as e:                 # one broken module must not blank the board
            res = f"(could not run: {e})"
        tag = ("BUILT ✓" if status == "BUILT" else status)
        print(f"{name:15}{tag:12}{res}")
    print("-" * 78)
    print("Only Smart-Prep is built & backtested today; the rest are prototypes on the same engine.")
    print("Detail per module:  python run.py  ·  python reorder.py  ·  python utang.py  ·  python basket.py")


if __name__ == "__main__":
    main()
