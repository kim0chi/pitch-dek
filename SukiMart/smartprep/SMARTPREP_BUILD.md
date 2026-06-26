# SukiMart Smart-Prep — Prototype Build Document
### The buildable spec: exact model, exact data, tech stack, and repo plan

> **Audience:** whoever builds it (your team / a dev / Claude). This is the engineering design behind the pitch artifact. Two tiers: **Tier-0** is the spreadsheet Tina actually runs day-one ([SukiMart_SmartPrep.xlsx](SukiMart_SmartPrep.xlsx)); **Tier-1** is the Python engine in this repo that proves, backtests, and improves the model. The pitch shows Tier-0; this doc builds Tier-1.
>
> **System framing — SukiSense (*one engine, many modules*):** the engine is **SukiSense**. This doc specs the shared core + the **built** module, **Smart-Prep** (spoilage). Sibling **prototype** modules reuse the same engine: `reorder.py` (Smart Reorder), `utang.py` (Utang Score), `basket.py` (Basket Lift) — run them all via `python sukisense.py`. **Only Smart-Prep is built & backtested today**; the rest switch on as the POS fills with real data.

---

## 1 · What it does (scope)
**Input:** a few weeks of daily ready-to-eat sales. **Output, every morning:** "prepare *this many* of each item today" — the quantity that **maximizes expected profit**, balancing spoilage against lost sales. It also tracks how well it's doing (spoilage %, sell-out %, accuracy) and improves weekly.

**In scope (MVP, BUILT):** Smart-Prep over the 5–15 perishable ready-to-eat SKUs (siomai, coffee, rice meals, pandesal, lumpia). **Now also prototyped as sibling modules on the same engine:** the ~900 grocery SKUs → **Smart Reorder** (`reorder.py`, classic (s,S) reorder points — they don't spoil, so newsvendor doesn't apply); the utang ledger → **Utang Score** (`utang.py`); cross-sell → **Basket Lift** (`basket.py`). See `sukisense.py` for the combined status board.

---

## 2 · THE FORECASTING MODEL (specific)

This is a **two-model pipeline**: forecast the demand *distribution*, then choose the prep quantity by *optimization*. We name the exact methods and when each applies.

### 2.1 Why this class of model (the constraints decide it)
- **Daily data, strong weekly seasonality** (weekends/paydays spike — Exhibit G) → need a model with **day-of-week seasonality**.
- **Short history** at launch (weeks, not years) → classic statistical models, **not** deep learning.
- **Low, count-based volume** for some items (8 rice meals/day) → demand is a **count**, model it as one.
- **Perishable + a prep decision** → we need a **quantity decision under uncertainty** → the **newsvendor model**.
- **Demand is censored** (if you sell out, you don't see true demand) → must be handled or the model under-forecasts forever.

### 2.2 Step A — forecast the MEAN demand (per SKU, per day)
| Phase | Model | When to use | Library |
|---|---|---|---|
| **MVP (Phase 1)** | **Seasonal baseline:** exponentially-weighted average of the last 4–8 *same-weekdays* × event multiplier (payday/holiday) | < 3 weeks of data, or to run in Sheets | pure pandas / Sheets formula |
| **Phase 2** | **Holt-Winters (Triple Exponential Smoothing)** — level + trend + **weekly seasonality (period = 7)**, multiplicative | ≥ 3–4 weeks of data; the default engine | `statsmodels.tsa.ExponentialSmoothing` |
| **Phase 3 (later)** | **Gradient-boosted trees (LightGBM)** with features: day-of-week, payday, holiday, school-day, weather, lagged sales, promo | only at ≥ 3–6 months data, if it beats Phase 2 on backtest | `lightgbm` |
- **Event adjustments** (all phases): multiplicative factors for **payday (15th/30th ±1), holidays, school in/out, rain**. Learned from history once enough data exists; set manually at cold-start.

### 2.3 Step B — model the UNCERTAINTY (so we can choose a safe quantity)
The newsvendor needs the *distribution*, not just the mean. Pick by item volume:
- **High-volume items** (coffee, pandesal): **Normal(μ = forecast, σ = forecast-error std)** — σ estimated from recent residuals (rolling).
- **Low-volume count items** (rice meals, siomai batches): **Poisson(λ = forecast)**; if variance > mean (overdispersed), **Negative Binomial**. This is the statistically correct choice for counts and is genuinely defensible.

### 2.4 Step C — the DECISION (newsvendor optimization)
> Optimal prep `Q* = F⁻¹(CR)` — the demand-distribution quantile at the **critical ratio** `CR = Cu / (Cu + Co)`, where `Cu` = margin lost if you run out, `Co` = cost lost if it spoils.
- Normal: `Q* = μ + z·σ`, `z = Φ⁻¹(CR)` (`scipy.stats.norm.ppf`).
- Poisson: `Q* = scipy.stats.poisson.ppf(CR, μ)`. NegBin: `nbinom.ppf(CR, r, p)`.
- *Worked (coffee, Sat):* μ≈32, CR = 18/(18+12)=0.60, z=0.25 → **Q\*≈33**. High margin → prep above the mean. Pandesal CR=0.40 → z<0 → **prep below** the mean. (Matches the [xlsx](SukiMart_SmartPrep.xlsx).)

### 2.5 Handling demand censoring (the detail that makes it real)
When an item **sells out**, the recorded sale is a floor, not the true demand. If ignored, the forecast spirals down. Fix:
- Log a **sell-out flag + time**. On sold-out days, treat demand as **right-censored** (demand ≥ sold) and inflate the estimate (e.g., scale by the fraction of the day remaining at sell-out, or use the prep_log's prepared qty as the observed ceiling).

### 2.6 Continuous improvement (the learning loop)
Each night: record **prepared / sold / spoiled** → update residual σ and event factors → **weekly backtest** (one-step-ahead) → if Phase-3 model beats Phase-2 on WAPE, promote it. *Honest framing for the pitch: "it improves as data arrives," not "it's a neural network."*

### 2.7 What we deliberately do NOT do (don't over-engineer)
No deep learning, no cloud GPUs, no real-time streaming. The case rewards *affordable and believable.* Holt-Winters + newsvendor runs on a phone in milliseconds and is fully explainable — that's the point.

---

## 3 · THE DATA IT NEEDS (exact schema)

Five small tables. **The one most teams forget is `prep_log`** — without logging what was *prepared* and *spoiled*, you can never measure spoilage or learn. That table is the heart of the system.

```
items
  sku_id (PK) · name · category · is_perishable(bool)
  unit_price · unit_cost · shelf_life_hours · batch_size · active(bool)

sales            -- from the POS, one row per line item
  id (PK) · datetime · sku_id (FK) · qty · unit_price · unit_cost

prep_log         -- entered once daily (or by the POS) — THE learning loop
  date · sku_id (FK) · qty_prepared · qty_sold · qty_spoiled
  · sold_out_flag(bool) · sold_out_time(nullable)

calendar         -- features that drive demand
  date (PK) · dow · is_payday · is_holiday · is_school_day · weather

forecasts        -- written by the engine (audit trail)
  date · sku_id · forecast_mean · forecast_std · prep_recommended · model_version
```

**Sources & collection:**
- `sales` → POS export (CSV/API). If no POS yet (today she uses a notebook), MVP starts with a **manual daily tally** of the ~10 ready-to-eat items — that's realistic and cheap.
- `prep_log` → 30 seconds at close: "made 30, sold 26, threw 4." This is the discipline that powers everything.
- `calendar` → generated automatically (PH holidays, paydays) + a one-tap weather/rain note.

**Data volume needed:** ~**3–4 weeks** to estimate weekly seasonality (Phase 2). **Cold-start (week 1–2):** use category priors + Tina's gut as the mean, wide σ; the newsvendor still beats pure guessing, and accuracy climbs fast.

---

## 4 · TECH STACK
| Layer | Choice | Why |
|---|---|---|
| Language | **Python 3.11** | free, ubiquitous, the model libraries live here |
| Data | **pandas, numpy** | tabular wrangling |
| Forecasting | **statsmodels** (Holt-Winters), **scipy.stats** (Poisson/NegBin/Normal quantiles) | named, standard, lightweight |
| (later) ML | **lightgbm** | only when data justifies |
| Storage | **SQLite** (`smartprep.db`) or CSV | zero-config, single file, runs on a laptop |
| Report/UI | **openpyxl** (Excel morning report) + optional **Streamlit** dashboard | matches the pitch artifact; Streamlit = a real clickable UI |
| Charts | **matplotlib** | backtest + accuracy plots |
| Delivery to Tina | Google Sheet + **Apps Script**, or a phone-friendly **HTML/PDF** morning report | affordable; no app store needed |

**Production reality for Tina:** an affordable POS with CSV export + this engine running nightly (cron/Apps Script), pushing the prep list to her phone each morning. No POS budget? The whole MVP runs in **Google Sheets** (the seasonal baseline + newsvendor are spreadsheet formulas — that's the [xlsx](SukiMart_SmartPrep.xlsx) we built).

---

## 5 · ARCHITECTURE / DATA FLOW
```
POS export / manual tally
        │  ingest.py        (load sales, build calendar, join events)
        ▼
   clean daily series  ──►  forecast.py   (Holt-Winters → mean; residuals → σ;
        │                                   Poisson/NegBin for counts; de-censor)
        ▼
   demand distribution ──►  newsvendor.py (Q* = F⁻¹(Cu/(Cu+Co)) per SKU)
        ▼
   prep recommendations ─►  report.py     (Morning Dashboard: xlsx / HTML / Sheet)
        ▼
   (end of day) record prepared/sold/spoiled ─► prep_log ─► backtest.py (weekly)
```

## 6 · PROPOSED REPO STRUCTURE (the "rearrange")
The repo currently mixes PopCart and SukiMart. Clean split:
```
business-ai/
  README.md
  archive/popcart/                 # ← move all PopCart files here (keep, don't delete)
  SukiMart/
    case/                          # the 2 case PDFs
    analysis/                      # sukimart_model.py, three_paths, crashcourse, verdict
    deck/                          # SUKIMART_FINALS_DECK.md, screenshots, illustrations
    smartprep/                     # ★ THE PROTOTYPE (Tier-1)
      README.md  ·  requirements.txt
      data/        sample_sales.csv, items.csv, calendar.csv, smartprep.db
      smartprep/   __init__.py, ingest.py, forecast.py, newsvendor.py,
                   report.py, backtest.py, cli.py, config.py
      tests/       test_newsvendor.py, test_forecast.py
      notebooks/   exploration.ipynb
```
**CLI feel:** `python -m smartprep forecast --date 2026-06-28` → prints the prep list + writes `morning_report.xlsx`. `python -m smartprep backtest` → accuracy + spoilage metrics.

## 7 · BUILD MILESTONES
- **M0 — Scaffold + MVP (½ day):** folder, sample data, **seasonal-baseline forecast + newsvendor**, CLI prints prep list. (Python version of the xlsx — real, testable.)
- **M1 — Real forecasting (1 day):** Holt-Winters; Poisson/NegBin distributions; censoring handling; per-SKU config (Cu/Co).
- **M2 — Proof it works (1 day):** backtest harness + metrics (WAPE, service level, spoilage%); the Excel/HTML Morning Report; charts for the deck.
- **M3 — Usable (1–2 days):** Streamlit dashboard *or* Google-Sheets connector; daily prep_log entry flow.
- **M4 — Later:** LightGBM + event-factor learning once ≥ 3 months of data.

## 8 · HOW WE KNOW IT WORKS (metrics)
- **Forecast accuracy:** WAPE / MAE, one-step-ahead backtest.
- **Service level:** % of days an item did *not* sell out (target ~90–95%).
- **Spoilage rate:** spoiled value ÷ perishable sales (backtested: 16% → 9%, profit-optimal).
- **Profit:** gross profit per SKU vs the gut-feel baseline (the ₱24k/yr number).

## 9 · COST & FEASIBILITY (MSME-honest)
- Software: **₱0 extra** — runs in Google Sheets, or as a feature of the POS already in the operating plan (~₱3–4k/mo, Exhibit D).
- Skill: Tina reads one number per item each morning. The engine is dev-built once; she just runs it.
- Compute: a phone or any laptop. No cloud needed.

## 10 · SAY IT SIMPLY (for the pitch / Q&A)
> *"The forecasting model is Holt-Winters — exponential smoothing with a weekly pattern — and for the low-volume items we model demand as a Poisson count. On top, the newsvendor model picks the prep quantity that maximizes profit. It needs only daily sales plus what was prepared and spoiled. It runs in a spreadsheet today and improves as data comes in. That's specific, affordable, and we've built a working version."*
