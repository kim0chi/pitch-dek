# SukiMart Smart-Prep — prototype

POS module that tells Tina **how much ready-to-eat to cook each day** to maximize profit:
**Holt-Winters demand forecast → newsvendor optimal prep**. Built to prove the AI is real and defensible.

## Run it (from the repo root)
```bash
./.venv/bin/python SukiMart/smartprep/run.py          # forecast tomorrow + backtest + write morning_report.xlsx
./.venv/bin/python SukiMart/smartprep/datagen.py      # regenerate the illustrative sample data
./.venv/bin/python SukiMart/smartprep/build_smartprep.py   # the spreadsheet (Google-Sheets) version
```
Deps (already in the repo `.venv`): `pip install -r requirements.txt` (pandas, numpy, scipy, statsmodels, openpyxl).

## Backtested results (sample data)
- Forecast accuracy **WAPE ~19%** · payday-HW beats LightGBM (18% vs 20%)
- Spoilage **~16% → ~9%** (gut-feel baseline → Smart-Prep, profit-optimal)
- In-stock 71% (gut) → 53% (profit-optimal) — tunable dial, see spec
- Profit protected **~₱1,983/mo ≈ ₱24k/yr (staged)**, **~₱47k/yr (full SukiMart)**
- Cost: **₱0 incremental** — a feature of the POS already in the plan

## Files
| File | What |
|---|---|
| `config.py` | SKU master, day-of-week shape, service-floor dial |
| `datagen.py` | writes `data/{items,calendar,sample_sales}.csv` (illustrative) |
| `forecast.py` | Holt-Winters (weekly seasonality) + seasonal-baseline fallback |
| `newsvendor.py` | critical ratio → optimal prep (Normal / Poisson) |
| `backtest.py` | rolling one-step-ahead: gut-feel vs forecast+newsvendor |
| `report.py` | writes `morning_report.xlsx` (the dashboard) |
| `run.py` | orchestrates all of the above |
| `build_smartprep.py` | the Google-Sheets demo version (`SukiMart_SmartPrep.xlsx`) |
| `SMARTPREP_BUILD.md` | full architecture / model / data / tech-stack spec |
| `SMARTPREP_AI_SPEC.md` | the pitch handoff (numbers + how to draw the slide) |

## Method (one line)
Demand forecasting (Holt-Winters / Poisson for counts) + the **newsvendor model** — the standard operations-research method for perishables. Not a moving average; it makes a costed, per-item decision and improves with data. The founder always approves the final prep amount.

> Sample data is illustrative — the **logic** is the deliverable. To use real data, replace `data/sample_sales.csv` with the POS export (same columns: `date,sku_id,qty`).
