# SukiMart — Three-Path Pressure Test & Verdict  (v2, review-corrected)
### The financial case for the recommendation (spine of the finals deck)

> Modeled all three paths over 12 months with ramp-up and downside. Full math: [sukimart_three_paths.py](sukimart_three_paths.py). All figures use one consistent definition — **economic profit = cash to Tina − ₱16,000 fair wage** (Exhibit A memo). Baseline today = **₱9,800/mo** (not the ₱25,800 Tina believes — [BUSINESS_CRASHCOURSE.md](BUSINESS_CRASHCOURSE.md) §4).

## The verdict in one honest line
**Take the staged transition** — but say the trade-off plainly: it **gives up ~₱77k of first-year cash** versus just optimizing the sari-sari, *in exchange for* nearly **3× the monthly run-rate, twelve months of demand data, and protection from an irreversible loan.**

## The three paths, side by side (consistent economics)
| Path | Mo-12 run-rate (econ profit/mo) | Year-1 cash to Tina (after capex) | Capital needed | Loan | Downside |
|---|---|---|---|---|---|
| **3 · Disciplined sari-sari** | ₱15,936 (+63%) | **₱353,232** ← highest Yr-1 cash | ₱24k | No | ≈ the ₱24k — essentially none |
| **2 · Staged transition** ✅ | **₱27,200 (≈ 3×)** | ₱275,825 | ₱150k | No | ≈ ₱150k capex; **savings safe** |
| **1 · Full jump (base)** | ₱27,800 | needs ₱1.35M upfront | **₱1,350,000** | ₱750k | savings at risk; **~₱389k extra liquidity** if sales come in low |

## The single most important insight
**Full-jump (base) run-rate ≈ ₱27,800/mo — barely above staged's ₱27,200 — yet it costs 9× the capital and a ₱750k loan.** The full jump only *meaningfully* wins in its **optimistic** case (₱128,000/mo). So the question isn't "which earns more?" — base case, staged and full jump are a tie. The question is **"is the optimistic case worth betting her ₱600k savings + a loan on, at a corner that is 'real but not a flood'?"** The honest answer is no — not until the data proves it.
> *Consistency note (cash vs P&L): all run-rates here are **cash-basis** — the full-jump figure is after repaying ~₱12k/mo of loan principal. On a pure **P&L** basis (principal isn't an expense) the full-jump base reads ~**₱39,800/mo** vs staged's ₱27,200. We compare on cash because survival is a cash test and that's where the downside risk lives; the verdict turns on risk, not on the profit being equal.*

## Why not the full jump (stated defensibly)
- Break-even is **₱612,000/mo (₱20,400/day, ~170 txns)** — a **3.4× jump** from today's ₱180k, with **6 rival sari-sari within 300m**.
- **Pessimistic (150 txns/day):** run-rate **−₱46,000/mo**; Year-1 operating cash **−₱484k**. Her ₱600k savings are already sunk as capital, so the model shows she would need **~₱389,000 of additional liquidity within the first year** to keep the doors open.
- *(Honest caveat for Q&A: the assets keep residual value and the loan principal amortizes, so this isn't "₱600k vaporized" — but it does **put her ₱600k at risk and demand ~₱389k more cash in the downside**, with a loan due regardless.)*
- She keeps **no digital records today** and would jump from **160 → ~900 SKUs**, 3 staff, perishables, and a loan — heavy execution risk on day one.
> *No prize for the most ambitious option; a prize for being right and honest about the risk.* — the case itself.

## Why staged wins (capture the upside, cap the downside)
- Add **high-margin, low-capex** pieces, each self-funding: **ready-to-eat** (45–55%), **services** (bills/e-wallet/padala, near-pure fee margin, draws traffic), **1–2 chillers**.
- Run-rate climbs ₱9,800 → **~₱27,200/mo** on **₱150k of her own cash, no loan** — *the same run-rate as the full-jump base case, without the ₱1.35M and the debt.*
- **Honest cost of this choice:** ~₱77k less first-year cash than Path 3 (you're reinvesting into the ramp). We accept that for the higher run-rate, the learning, and the optionality.
- It **generates the demand data** to answer "can this corner support ₱612k/mo?" — so any future loan is **gated on proof, not hope.**

## The honest rebuttal (rehearse for Q&A)
**"Path 3 makes more cash in year one — why not just optimize the sari-sari?"**
→ *"Path 3 wins the first year by ~₱77k, but it caps Tina at ₱16k/mo and leaves the convenience opportunity on the table. Staged reaches a ₱27k/mo run-rate and — critically — builds the data and the muscle to go further. We're trading a one-year cash bump for a durable, higher engine and a safe path to the full store."*

**"Aren't you just avoiding the real decision (the full build)?"**
→ *"No — we're sequencing it. Staged is the on-ramp. After 12 months we'll have proven demand and ₱450k savings intact. If the data shows the corner carries ₱612k/mo, Tina draws the loan **then** and builds the full SukiMart from a position of proof. Same destination, safer route."*

## Where AI earns its place (the role-of-AI question, 25 pts)
**One use, costed, payback-proven: perishable spoilage forecasting in the POS.**
- Ready-to-eat is the **highest-margin and highest-loss** line — 8–15% spoilage if demand is misjudged (Exhibit F).
- A **payday-aware Holt-Winters + newsvendor** model backtested on sample data cuts spoilage **16% → 9%**:
  - **At staged scale: ~₱24,000/yr protected.**
  - **At full SukiMart (~₱720k/mo): ~₱47,000/yr.**
- **Cost is already in the plan:** POS feature, ₱0 incremental. Backtested WAPE ~19%; payday-HW beat LightGBM (18% vs 20%). *Specific. Costed. Defensible.* It's also the **data engine** for the go/no-go gate. (Fixes the PopCart "is this really AI?" weakness — it's genuine demand forecasting + operations research, not a moving average.)

## The 12-month roadmap (phased, with buffer; NO loan drawn this year)
- **M1–2 · Baseline & books:** put the store on a cheap POS; start capturing sales/SKU/utang data (end the notebook).
- **M3–5 · Add services + ready-to-eat:** expand bills/e-wallet/padala; launch coffee + siomai; switch on spoilage forecasting from the first day of perishables.
- **M6–8 · Add chillers + mix shift:** chilled beverages; push the mix toward fat-margin lines.
- **M9 · DECISION GATE:** does the data show a credible path to ₱612k/mo? **Go / refine / hold.**
- **M10–12 · Prepare, don't borrow:** if the gate passes, **assemble the loan package and full-build plan for Year 2** (lease the adjacent lot, get 3 contractor quotes) — but **the ₱750k loan is not drawn inside this 12-month plan.** If the gate fails, bank a ~₱27k/mo store with savings intact. *(This keeps the "no loan, savings safe" claim true for the whole modeled year.)*

## Three biggest risks → how Tina manages each
1. **Perishable spoilage** (highest-margin line bleeds) → AI demand forecast + start small, scale to demand.
2. **Demand never reaches break-even** → that's *why* we stage; the M9 gate stops the loan before it's ever taken.
3. **Owner overload** (one person, growing SKUs) → POS + one trained helper before scope grows; sequence, don't stack.
