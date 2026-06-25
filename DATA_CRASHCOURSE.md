# PopCart PH — Data Crashcourse
### Know every number cold. Defend every claim. (UCLM · SiXeven)

> **Purpose:** so any team member can explain *where each number comes from, how it's calculated, and why it holds* — exactly what your mentor asked for ("make sure you can explain/defend this"). Read top-to-bottom once; then drill the **🎯 Defend it** lines and the rapid-fire at the end.

---

## 0 · The 60-second mental model
PopCart earns **₱120M** but keeps only **9%** (₱10.8M). The loudest problem (shipping) is *not* the most expensive — **stockouts** quietly lose **₱7.35M of gross profit a year**. A Cebu hub to cut shipping is a **₱9M-to-save-₱2.4M trap**. So: **fix the inventory engine first** (cheap, recovers ~₱0.6M/yr net, the only option with a positive floor), then **earn expansion** via an asset-light 3PL gated at Month 7. Every number below supports that one story.

## 1 · The exhibits (where everything comes from)
| Exhibit | Contains | We use it for |
|---|---|---|
| **A** | FY2025 financials: ₱120M rev, 50% gross margin, 20% logistics, 9% net | The 9% constraint; margins; the hub-cost reality |
| **B** | Region: % orders, ₱/order, delivery days, damage % | Shipping cost, the 43% CV+Davao, damage |
| **C** | 5 SKUs: units/day, price, out-of-stock days/mo, lead time | The ₱7.35M leak; reorder points; lead times |
| **D** | Ops: 90% TikTok, manual Excel 2×/day, gut-feel ordering | The root cause; the channel risk; what we automate |
| **Assumptions A–F** | AOV ₱650, 185k orders, expansion costs, savings %, growth %, kiosk revenue | The hub model, recovery %, the gate |

---

## 2 · The baseline & the 9% margin  *(Exhibit A)*
- Revenue **₱120.0M** · COGS ₱60.0M (50%) · Gross profit **₱60.0M** · Platform+marketing ₱12.0M (10%) · **Logistics & shipping subsidies ₱24.0M (20%)** · Warehouse ₱10.0M · Admin ₱3.2M · **Net profit ₱10.8M = 9%**.
- 🎯 **Defend the 9%:** "It's thin — every ₱1 of avoidable cost matters, and we can't fund a fix that costs more than it saves. That single fact rules out the hub and favours the cheap operations fix."

## 3 · The ₱7.35M leak — and the gross-vs-net answer  *(Exhibit C × A)* — **mentor note 3**
Per SKU: `units/day × out-of-stock days/mo × 12 × price × 50% gross margin`
| SKU | units/day | out days/mo | lost units/yr | × price | **lost gross profit** |
|---|---|---|---|---|---|
| Freeze-dried candy | 300 | 11 | 39,600 | ₱180 | **₱3.56M** |
| Spicy Korean ramen | 240 | 5 | 14,400 | ₱320 | ₱2.30M |
| Chocolate crunch | 160 | 7 | 13,440 | ₱150 | ₱1.01M |
| Bubble gum | 180 | 2 | 4,320 | ₱220 | ₱0.48M |
| Sour belts | 120 | 0 | 0 | ₱120 | ₱0 |
| **Total lost revenue ₱14.7M** | | | | | **₱7.35M gross** |
- **68%** = ₱7.35M ÷ ₱10.8M net profit.
- 🎯 **Defend gross-vs-net (the mentor's flag):** "₱7.35M is gross profit *lost*. We compare it to *net* profit only to show scale — it's about two-thirds the size of net profit. We never add ₱7.35M to net income; the amount we'd actually *keep* is far smaller and is valued separately at contribution margin (Section 5)."

## 4 · Why recovery ≠ the leak: contribution margin  *(Exhibit A)*
A recovered sale still pays platform fees and shipping, so it doesn't drop at 50% gross.
- ₱180 candy → **−₱90** COGS (50%) → **−₱36** shipping (~20%) → **₱54 take-home = 30% contribution.**
- 🎯 **Defend it:** "Gross margin is 50%; *contribution* margin is ~30% after the variable costs every order still incurs. Budgeting on take-home, not gross, is why our benefit number is honest and small."

## 5 · The recovery → +₱0.6M/yr net  *(the Fix-Ops bar)*
Chain: `₱14.7M lost rev × 42.5% recovery × ~80% captured × 30% contribution = ₱1.5M − ₱0.9M/yr run cost = +₱0.6M/yr net (base).`
The deck's worst→best range is a sensitivity on those three levers:
| Case | recovery × capture × contribution | gross recovery | − run | **net/yr** |
|---|---|---|---|---|
| Worst | 25% × 70% × 20% | ₱0.51M | −₱0.9M | **−₱0.5M** |
| **Base** | **42.5% × 80% × 30%** | **₱1.5M** | −₱0.9M | **+₱0.6M** |
| Best | 60% × 90% × 40% | ₱3.18M | −₱0.9M | **+₱2.2M** |
- 🎯 **Defend it:** "Even our *worst* case (−₱0.5M) is a small, recoverable miss — and the base and best are positive. No other option has a floor that shallow."

## 6 · Safety stock & reorder points  *(Exhibit C)* — **mentor note 7 (the big one)**
The slide shows **lead-time demand** (e.g., candy `300/day × 14-day lead = 4,200`). The full rule adds a buffer:
> **Reorder point = (avg daily sales × lead time) + safety stock**
> **Safety stock = Z × σ_daily × √(lead time)** — Z = 1.65 for a 95% service level.
Worked, assuming ~30% demand variability (σ = 0.30 × daily) for volatile viral snacks:
| SKU | lead-time demand | safety stock (1.65·0.3·daily·√LT) | **full reorder point** |
|---|---|---|---|
| Candy (14d) | 4,200 | ≈ 555 | **≈ 4,755** |
| Ramen (30d) | 7,200 | ≈ 650 | **≈ 7,850** |
| Chocolate (21d) | 3,360 | ≈ 365 | **≈ 3,725** |
- 🎯 **Defend it (kills the "placeholder?" question):** "The reorder points on the slide are the lead-time-demand component. Safety stock is calculated, not guessed: Z × variability × √lead-time. At 95% service and ~30% demand swing, that's ~550 units on candy. For a *confirmed* viral spike we'd lift the service level to 97–98%. Our stop-rule (slide 13) is: don't inflate safety stock blindly."

## 7 · The ₱9M hub trap  *(Exhibit B + Assumptions C/D/E)* — **mentor note 1**
- Shipping saved: 48,100 CV orders × ₱50/order saved = **₱2.4M**.
- Damage avoided (base): ≈ **₱0.29M**. Growth GP at 15% (Assumption E): ≈ **₱2.34M**.
- Base benefit ≈ **₱5.04M** vs operating cost **₱9M/yr** (Assumption C) → base **−₱3.96M/yr**.
- Break-even needs ≈ **40% regional growth** — above the case's 15–30% range.
- 🎯 **Defend it:** "We gave the hub every benefit — full shipping saving, damage reduction, and the case's growth — and it still loses ~₱4M a year and needs 40% growth to break even. It's a bet, not a plan."

## 8 · The asymmetry — all nine numbers  *(model on Exhibit C + Assumptions C/D/E/F)*
| Option | worst | **base** | best |
|---|---|---|---|
| **Fix Operations** | −₱0.5M | **+₱0.6M** | +₱2.2M |
| Cebu hub (owned) | −₱6.9M | **−₱4.0M** | +₱1.0M |
| Mall kiosk | −₱2.5M | **+₱0.1M** | +₱3.0M |
- 🎯 **Defend it:** "Recurring net profit per year. Fix-Ops has by far the smallest downside and a positive base — the others can lose ₱2.5–6.9M. On a 9% margin you pick the smallest downside."

## 9 · Payback  *(model)* — **mentor note 11 (chart scaling)**
- ~**31 months** at 30% contribution (incl. 3-month build). At 40% → 18 mo; 50% → 14 mo; **20% → ~14 years (effectively never)**.
- Year 1 = investment year: **−₱1.18M cash**; net-positive after.
- 🎯 **Defend the chart (the "14yr vs 31mo same height" flag):** "The 20% bar is greyed and intentionally *not to scale* — it's a 'never pays back' marker, not a height comparison. We'd rather flag the bad case honestly than hide it. Real payback at our base margin is ~31 months."

## 10 · The ₱56/order gate  *(Assumption D)*
- Before any growth, a 3PL must cost **less than ~₱56/order** to beat status quo: ₱50 shipping saved + ~₱6 damage avoided per order.
- 🎯 **Defend it:** "It's the unit-economics break-even *before* counting growth. If a real quote — including storage, pick-pack, transfer, returns, and minimums — beats ₱56, we pilot for 8 weeks. If not, we walk."

## 11 · Forecast methodology — honest  *(Exhibit C/D)* — **mentor note 8**
- It's **weighted moving averages** (7/14/28-day) × a viral multiplier + a safety-stock formula. **Not** machine learning.
- 🎯 **Defend it:** "We deliberately chose transparent math over a black-box model. A 3-person team must trust and tune it, and the case rewards a workflow a real MSME can run. AI assisted our *analysis and build* — disclosed in the appendix — but the operating logic is simple by design."

## 12 · The connector reality  *(Exhibit D)* — **mentor note 8**
- TikTok Shop has **no free native connector** to Sheets/Airtable. Options: a paid third-party connector (~low monthly fee) or a free scheduled CSV export.
- 🎯 **Defend it:** "We don't assume magic. Our ₱0.9M/yr operating line covers a low-cost connector or a scheduled daily export. Worst case, an admin exports once a day — still a massive upgrade on twice-a-day manual."

## 13 · Buy vs build — the webstore  *(Exhibit D)* — **mentor note 9**
- We **buy** (off-the-shelf low-code D2C, ₱50–150K), not build. It's a **hedge**, not a growth engine.
- 🎯 **Defend it (the McDo-on-Grab point):** "Most volume stays on TikTok — like McDo leaning on Grab's existing users. We're not betting on D2C traffic; the webstore is cheap insurance against an algorithm change and it lets us own customer data. Target is <75% channel concentration, not zero."

## 14 · Roadmap sequencing  *(case template)* — **mentor note 13**
- M1 baseline → M2–3 pilot warning system → M3–6 stabilise + webstore → **M7 decision gate** → M8+ 3PL pilot (if it clears the gate) → M10–12 scale.
- 🎯 **Defend the "compressed?" critique:** "The Month-7 gate is the buffer. The webstore (4–6) and the 3PL pilot (post-gate) don't overlap — we sequence on purpose so execution friction in one phase doesn't sink the next."

## 15 · Assumptions & sources (quick reference)
AOV ₱650 · 185,000 orders/yr (MM 77.7k / CV 48.1k / Davao 31.5k / Rest 27.8k) — *Assumption A/B* · gross margin 50%, contribution ~30% — *Exhibit A* · recovery 25–60%, base 42.5% — *Assumption D* · hub setup ₱2.5–4M, run ₱7.2–10.8M/yr — *Assumption C* · regional growth 15–30% — *Assumption E* · prototype daily-sales & TikTok index are **illustrative samples** (logic is the deliverable).

---

## 16 · Rapid-fire — 15 questions, 15 answers
1. **Biggest problem?** Stockouts, ₱7.35M/yr gross-profit leak (Exhibit C).
2. **Gross or net?** Gross lost; ~68% the *size* of net; never added to net.
3. **Why not the hub?** ₱9M to save ₱2.4M; base −₱4M; needs 40% growth.
4. **Recovery amount?** ~₱0.6M/yr net base (₱0.1–1.6M range), at 30% contribution.
5. **Why 30% not 50%?** Recovered sales still pay fees + shipping.
6. **Safety stock value?** Z×σ×√LT; ~550 on candy at 95% service — calculated, not placeholder.
7. **Is it AI?** No — weighted averages + safety stock. Transparent by design.
8. **TikTok connector?** No free native one; budgeted connector or daily export.
9. **Why a webstore? Buy vs build?** Buy off-the-shelf; a hedge, not a growth bet (McDo/Grab).
10. **Payback?** ~31 months base; Year-1 −₱1.18M; case allows >12 mo.
11. **The 14-yr bar?** Greyed, not-to-scale; "never pays back" marker.
12. **The ₱56 gate?** Unit-economics break-even before growth; pilot 8 weeks.
13. **Roadmap too tight?** M7 gate is the buffer; phases are sequenced.
14. **Worst case for Fix-Ops?** −₱0.5M — smallest downside of any option.
15. **What if recovery underperforms?** Stop-rule: cut scope if economics turn negative.
