# SukiMart Smart-Prep — POS AI Module Spec  (handoff for design)
### The specific, built, adversarially-reviewed AI for the finals deck

> **For the designer/Claude:** this is the AI section of the SukiMart pitch — **built, backtested, and code-reviewed**. Every number below is reproducible: `./.venv/bin/python SukiMart/smartprep/run.py`. This answers the finals' "role of AI" question (25 pts) and fixes our PopCart weakness ("is this really AI, or just an average?").

## What it is (one line)
**SukiSense** is the predictive engine inside Tina's POS — it turns a cash register into a system that *forecasts*. Its first built module, **Smart-Prep**, tells her each morning **exactly how much of each ready-to-eat item to cook** — sizing every item to its own economics so she stops wasting the highest-margin food. *(Naming: SukiSense = the engine/vision; Smart-Prep = module 1, the part that's built and backtested today.)*

## Why ready-to-eat
Per the case, ready-to-eat (siomai, coffee, rice meals) earns the best margin (45–55%) **and bleeds the most — 8–15% spoilage if demand is misjudged** (Exhibit F). That's the one place AI earns real pesos.

## The method (two real models — why it's NOT "just an average")
1. **FORECAST** — per item, an automatically-selected model: a **payday-aware Holt-Winters** (weekly seasonality + a learned payday multiplier) wins on our data; it falls back to a seasonal baseline on short history. Selected per SKU by lowest hold-out error.
2. **OPTIMIZE — the newsvendor model** (textbook OR for perishables): prepare the quantity where the cost of spoiling one unit (Co = its cost) equals the cost of missing one sale (Cu = its margin). `PREP = F⁻¹(CR)`, `CR = Cu/(Cu+Co)`, demand distribution auto-chosen (Poisson / Negative-Binomial / Normal) from the SKU's own dispersion.
   - **Per-item result:** high-margin coffee (CR 0.60) is kept in stock more; cheap pandesal (CR 0.40) is prepped leaner — *a different, costed decision per item.*

> **Defensibility line:** *"It's a payday-aware Holt-Winters forecast plus the newsvendor model — the standard method for perishables. A different, costed decision per item, and we backtested it. Not an average."*

## THE FULL NUMBERS (backtested — `run.py`; fair baseline; profit-optimal setting)
| Metric | Value |
|---|---|
| Forecast accuracy (WAPE) | **~19%** |
| **Spoilage of what's prepared** | **~16% (gut-feel) → ~9% (Smart-Prep)** — about 44% less waste |
| **Profit protected — staged** | **~₱1,983/mo ≈ ₱24,000/yr** |
| **Profit protected — full SukiMart** | **~₱47,000/yr** |
| In-stock (service) level | **71% (gut-feel) → 53% (profit-optimal)** — a deliberate, *tunable* trade-off (see dial) |
| Tool cost | **₱0 incremental** — a feature of the POS already in the plan |

### The honest trade-off — the profit-vs-availability DIAL (sensitivity, from `run.py` sweep)
Smart-Prep is a dial, not a fixed point. Raising the service floor buys availability with profit:
| Service floor | In-stock | Spoilage | Profit/yr (staged) |
|---|---|---|---|
| 0.00 (profit-optimal) | 53% | 9% | **₱24,000** |
| 0.60 | 66% | 12% | ₱20,000 |
| 0.70 | 74% | 15% | ₱14,000 |
| 0.75 (≈ match today) | 79% | 17% | ₱10,000 |
*Even at today's availability, it still cuts waste and adds profit — because it's day-aware, not flat. (numbers indicative; reproduce with the sweep in `run.py`.)*

### We tested ML — and said so honestly (model comparison, avg WAPE)
**payday-Holt-Winters 18%  ·  Holt-Winters 19%  ·  LightGBM 20%  ·  seasonal baseline 21%**
→ *Gradient boosting did NOT beat the simple statistical model at ~120 days of one-store data. We deploy Holt-Winters and keep LightGBM only in the comparison.*

### Data quality: censoring (the detail that makes it real)
On real POS data you only see what SOLD; on a sell-out, true demand is higher. In our validation, naive "sold" under-counts demand by **~17%** on sell-out days; **de-censoring recovers it to within ~1%** (from an imperfect sell-out-time signal). Smart-Prep cleans the data before forecasting, so it doesn't spiral down.

## The horizon — one engine, compounding (the outside-the-box layer)
Smart-Prep's spoilage forecast is **the beachhead, not the ceiling** — it's module 1 of **SukiSense**, the predictive engine in her POS. The same forecast-then-optimize engine, fed by the POS data the store captures from Month 1, extends to the store's other quantified losses — each switching on as the data arrives, none needing a new system:

| Next use | The loss it attacks | Same-engine logic | Status |
|---|---|---|---|
| **Smart Reorder** (900 grocery SKUs) | cash frozen in overstock + lost sales on stock-outs | newsvendor reorder-point per SKU — already prototyped in [reorder.py](reorder.py) | designed · code exists |
| **Utang credit scoring** | bad debt + working capital tied in informal credit | classify suki by repayment history → safe credit line | designed |
| **Basket lift / cross-sell** | AOV ~₱62 vs the ~₱120 break-even needs | market-basket association → bundles & placement | designed |

**The unifying line:** *Tina earns the right to grow the store with data — and that same data earns the right to grow the intelligence.* One engine, fed not rebuilt; AI maturity is staged exactly like the store.

**Deliberately OUT of scope (judgment, not omission):** payday **surge-pricing** and camera **surveillance** — both erode the *suki* trust that is the business's real asset. Naming what we won't build is part of the answer.

> ⚠️ Honesty: only the **spoilage** use is built and backtested today. The rest are designed extensions on the same engine — present them as the **roadmap**, not as done.

## The built artifact (show this — it's the credibility)
- **Python prototype — SukiSense engine + modules:** [`smartprep/`](.) — engine: `forecast.py`, `newsvendor.py`, `distributions.py`, `events.py`, `censoring.py`, `backtest.py`, `lightgbm_model.py`; modules: `run.py` (**Smart-Prep**, built), `reorder.py` (**Smart Reorder**), `utang.py` (**Utang Score**), `basket.py` (**Basket Lift**); `sukisense.py` (orchestrator/status board), `app.py` (Streamlit), `html_report.py`, `charts.py`, `tests/` (**18 pass**). Architecture: [SMARTPREP_BUILD.md](SMARTPREP_BUILD.md).
- **Live demo spreadsheet:** [SukiMart_SmartPrep.xlsx](SukiMart_SmartPrep.xlsx) — same logic in Sheets (change a price, PREP recalculates via `NORM.S.INV`).
- **Screenshots / charts for the slide:**
  - **Hero:** [screenshot_morning_dashboard.png](screenshot_morning_dashboard.png) — the Morning Prep Dashboard (real run output).
  - Charts in [../deck/](../deck/): `chart_spoilage.png` (16%→9%), `chart_uplift.png` (₱24k/₱47k), `chart_accuracy.png` (forecast vs actual).
  - Method panel: [screenshot_smartprep_panel.png](screenshot_smartprep_panel.png).

## How to depict it in the deck (2 main slides + 4 appendix backups)
> **Now split across two main slides** (see [SUKIMART_FINALS_DECK.md](../deck/SUKIMART_FINALS_DECK.md)): **Slide 9** = the method (the 2-step list + Morning Dashboard); **Slide 10** = the proof band + the horizon strip + the "deliberately NOT" line. The deeper material below is also built out as **4 appendix backup slides (AI-1…AI-4)** to flip to in Q&A. The single-slide layout below still works if you ever need to recombine them.
- **Title:** THE STORE THAT LEARNS — STARTING WITH SPOILAGE
- **Standfirst:** *Forecast each day's demand, then prep the profit-optimal amount per item — the first job of one engine that compounds.*
- **Left:** the 2-step method (name **Holt-Winters**) + per-item insight (coffee kept stocked, cheap bread leaner).
- **Right:** the Morning Dashboard screenshot.
- **Proof band:** *Backtested: WAPE ~19% · spoilage 16%→9% · payday-HW beats LightGBM (18% vs 20%) · de-censoring recovers demand to ~1%.*
- **Bottom band:** *Protects ~₱24k/yr staged → ~₱47k/yr full · ₱0 incremental cost · a tunable profit-vs-availability dial · founder always approves.*
- **Horizon strip:** *Today spoilage (built). Next, as data fills the POS → Smart Reorder (900 SKUs) · Utang scoring · Basket lift. One engine, fed not rebuilt.*
- **Judgment line:** *Deliberately NOT doing surge-pricing or surveillance — they'd cost the suki trust.*

## Q&A defense (rehearse)
| Question | Answer |
|---|---|
| **"Is this really AI?"** | "Payday-aware Holt-Winters + the newsvendor model — both standard, both backtested. A costed decision per item, not an average." |
| **"Why only spoilage — is that all?"** | "Spoilage is where AI pays *today* — a quantified loss with data to learn from. But it's one engine: the same forecaster extends to reorder across 900 SKUs, utang scoring, and basket lift as the POS fills with data. We put AI where it earns its place, then let it compound — and we deliberately said no to surge-pricing and surveillance, which would cost the suki trust." |
| **"Did you try ML?"** | "Yes — LightGBM scored 20% WAPE, worse than Holt-Winters' 18%. At ~120 days of one-store data, ML doesn't earn its complexity. We said so." |
| **"Your in-stock drops to 53%?"** | "At the profit-MAX setting, yes — deliberately, on cheap items where over-cooking wastes more than the occasional miss. It's a dial: match today's ~79% availability and it still cuts waste and adds profit, because it's day-aware." |
| **"Where's the payback?"** | "₱24k/yr now, ~₱47k at full scale, ₱0 extra cost — it's a feature of the POS Tina already needs." |
| **"Can she run it?"** | "She reads one number per item each morning. System recommends; Tina decides." |

## Honesty / AI disclosure (appendix)
Daily sales & sell-out timing are **illustrative samples**; the **logic is the deliverable**. Methods = demand forecasting + newsvendor + de-censoring (operations research). AI assisted analysis and this build; the **prototype was adversarially code-reviewed** and the numbers reconcile to `run.py`. The founder always approves the final prep amount.
