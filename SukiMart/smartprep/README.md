# SukiSense — the predictive engine inside Tina's POS

> **One engine, many modules.** A shared forecasting + optimization core, with modules that plug into it.
> Module 1 (**Smart-Prep**) is **built & backtested**; the rest are working **prototypes** on the same engine.
> *(The folder is still named `smartprep/` so existing paths keep working — think of it as the SukiSense package.)*

```bash
./.venv/bin/python SukiMart/smartprep/sukisense.py     # the engine status board (all modules)
```

## The modules

| Module | Status | What it does | Run it |
|---|---|---|---|
| **Smart-Prep** | **BUILT ✓** | perishable spoilage forecasting (Holt-Winters → newsvendor) | `python SukiMart/smartprep/run.py` |
| **Smart Reorder** | prototype | (s,S) reorder points for the ~900 grocery SKUs | `python SukiMart/smartprep/reorder.py` |
| **Utang Score** | prototype | explainable credit-risk score → safe credit line per suki | `python SukiMart/smartprep/utang.py` |
| **Basket Lift** | prototype | market-basket cross-sell (support / confidence / lift) | `python SukiMart/smartprep/basket.py` |

## Smart-Prep — backtested results (sample data)
- Forecast accuracy **WAPE ~19%** · payday-HW beats LightGBM (18% vs 20%)
- Spoilage **~16% → ~9%** (gut-feel baseline → Smart-Prep, profit-optimal)
- In-stock 71% (gut) → 53% (profit-optimal) — tunable dial, see spec
- Profit protected **~₱1,983/mo ≈ ₱24k/yr (staged)**, **~₱47k/yr (full SukiMart)**
- Cost: **₱0 incremental** — a feature of the POS already in the plan

## Files
| File | What |
|---|---|
| **ENGINE (shared core)** | |
| `forecast.py` | Holt-Winters (weekly seasonality) + seasonal-baseline fallback |
| `distributions.py` | Normal / Poisson / Negative-Binomial demand distributions |
| `newsvendor.py` | critical ratio → optimal prep quantity |
| `censoring.py` · `events.py` | sell-out de-censoring · payday/holiday factors |
| `backtest.py` | rolling one-step-ahead: gut-feel vs forecast+newsvendor |
| `lightgbm_model.py` | the ML benchmark (tested, doesn't beat HW at this scale) |
| `config.py` | SKU master, day-of-week shape, service-floor dial |
| **MODULES** | |
| `run.py` · `report.py` | **Smart-Prep** orchestrator + Morning Dashboard (`morning_report.xlsx`) |
| `reorder.py` | **Smart Reorder** (grocery reorder points) |
| `utang.py` | **Utang Score** (credit-risk scoring) |
| `basket.py` | **Basket Lift** (cross-sell association) |
| `sukisense.py` | the engine **orchestrator** — runs every module, prints the status board |
| **SUPPORT** | |
| `datagen.py` | writes `data/{items,calendar,sample_sales}.csv` (illustrative) |
| `build_smartprep.py` | the Google-Sheets demo version (`SukiMart_SmartPrep.xlsx`) |
| `tests/` | 18 tests (engine math + each module) |
| `SMARTPREP_BUILD.md` · `SMARTPREP_AI_SPEC.md` | architecture/tech spec · pitch handoff |

## Method (one line)
Demand forecasting (Holt-Winters / Poisson for counts) + the **newsvendor model** — the standard operations-research method for perishables. Not a moving average; it makes a costed, per-item decision and improves with data. **The same engine powers every module.** The founder always approves the final decision.

> Sample data is illustrative — the **logic** is the deliverable. Only **Smart-Prep is built & backtested**; reorder/utang/baskets are prototypes that switch on as the POS fills with real data.
