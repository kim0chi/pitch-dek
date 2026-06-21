# PopCart PH — Deck Content & Build Guide
### LAMBO 2026 Qualifying Case | "Fix the Engine Before You Grow the Body"

> **How to use this document.** This is your slide-by-slide build spec. Copy the **On-slide content** into Canva/PowerPoint. The **🎓 AI note** and **📊 Data viz** lines are coaching for you (the team) — they do NOT go on the slide. **🎤 Talk track** is for the June 24 semifinal pitch, not the written deck.
>
> Limit: **15 content slides** (cover + appendix don't count). We use all 15.
> Deadline: **June 22, 11:59 PM**. File name: `SchoolName_TeamName_LAMBO2026.pdf`
>
> **⚠️ Team decisions flagged inline** — search for `⚠️` and fill those in / vote as a team.

---

## PART 0 — Two primers (read once, applies to every slide)

### 🎓 How we leverage AI in this competition (the *process* judges reward)
The rubric gives **×5 for "AI woven into your own work"** and the case says *"AI use is expected and encouraged. Hiding it counts against you."* So we use AI openly, at five points, and disclose all of it:

1. **Understand the data** — we fed the case exhibits to AI to extract and structure them into one money-leak model (turned 4 scattered exhibits into 1 ranked table). *You should re-read the exhibits yourself to verify — AI can misread a number.*
2. **Build the math** — AI wrote our financial model ([popcart_model.py](popcart_model.py)) so every peso is reproducible and we can re-run scenarios in seconds.
3. **Stress-test** — we asked AI to *attack* our own recommendation (the "red-team") so we're ready for Q&A.
4. **Draft & tighten** — AI helps turn topic titles into "so-what" headlines and cut wordy bullets.
5. **Design** — AI suggests the right chart per slide and drafts the appendix disclosure.

**Golden rule from the case:** *"passing off unverified output as fact counts against you."* Every number on a slide must trace to an exhibit or our model. When in doubt, cite the exhibit.

### 📊 Data-presentation principles (how fresh grads look like pros)
- **Headline = the conclusion, not the topic.** ✅ "Stockouts cost 68% of profit" ❌ "Stockout Analysis". The judge should get your point from the title alone.
- **One message per slide.** If you're explaining two things, it's two slides (or one is appendix).
- **Make the hero number huge.** PHP 7.35M in 60pt; the supporting detail small.
- **Color = meaning.** Red = loss/problem. Green = our fix/gain. Grey = context. Be consistent across all 15 slides.
- **Pick the right object:** *comparison* → table; *magnitude* → bar chart; *over time* → timeline; *process* → flow diagram; *part-of-whole* → single stacked bar (avoid pie charts — judges find them hard to read).
- **Cite the source** on every data point: small "Exhibit C" tag. This directly earns the "grounded in the data" rubric points.
- **≤ 6 lines of text per slide.** White space reads as confidence.

---

## COVER (not counted toward 15)

**Title:** PopCart PH: Fix the Engine Before You Grow the Body
**Subtitle:** A 12-Month Growth Strategy Led by Operations
**Footer:** ⚠️ `[School Name]` · ⚠️ `[Team Name]` · LAMBO 2026 — Pagtubo sa Negosyo

🎓 *AI note:* ask AI for 5 title options, then pick the one that states a point of view. A title that takes a stance ("Fix the engine first") beats a neutral one ("PopCart Growth Strategy").
📊 *Data viz:* clean cover, one product photo or a simple engine/gear icon. No clutter.

---

## SLIDE 1 — Executive Summary

**Headline:** Stop a PHP 7.35M profit leak first — then earn the right to expand.

**On-slide content:**
- **Recommendation:** Lead with an **operations fix** (a forecasting + reorder control system). Then expand only in sequence — *not all at once*.
- **3 proof points:**
  - Stockouts silently cost **PHP 7.35M/yr in gross profit = 68% of net profit** (Exhibit C)
  - Fixing it recovers **~PHP 1.0–1.6M/yr** for a small, reversible **PHP 1.4M** outlay — the **only option with a positive floor in every scenario**
  - Year 1 is a low-risk **investment year**; the cash and data it creates make Year-2 expansion safe
- **The sequence:** ① Fix operations (Mo 1–6) → ② Cebu 3PL pilot, *gated on a partner quote* (Mo 7+) → ③ defer kiosk & owned hubs to Year 2

📊 *Data viz:* 3 big stat-cards (PHP 7.35M leak / only positive-floor option / PHP 1.4M to fix). A tiny 3-step arrow for the sequence.
🎓 *AI note:* write this slide LAST — it's a summary of 2–15. Ask AI: "compress this into 3 honest numbers a busy owner remembers," and resist rosy single-point figures; a range reads as credible.
🎤 *Talk track:* "PopCart is profitable but leaking. Before betting millions on a hub, close a PHP 7.35M leak that costs almost nothing to fix."

---

## SLIDE 2 — Main Problem Diagnosis

**Headline:** PopCart's biggest leak isn't shipping — it's invisible stockouts.

**On-slide content:**
- The founders worry about 5 problems. We ranked them by **recoverable peso**, not by how loud they are:

| Problem | Annual impact | Cost to fix | Verdict |
|---|---|---|---|
| **Stockouts** | **PHP 7.35M lost GP** | PHP 1.4M setup + PHP 0.9M/yr | 🟢 **Fix first** |
| Shipping cost | PHP 24M spent; ~PHP 2.4M recoverable via hub | PHP 9M/yr | 🔴 Costs more than it saves |
| Damage in transit | ~PHP 1.7M | bundled w/ hub | 🟡 Secondary |
| Channel dependence (90% TikTok) | existential, not yet a cash loss | cheap webstore | 🟡 Hedge now |

- **Key distinction:** shipping is the biggest *cost*; stockouts are the biggest *recoverable opportunity*.

📊 *Data viz:* the table, with the stockout row highlighted green. Put a red "biggest cost ≠ biggest opportunity" callout beside the shipping row.
🎓 *AI note:* this "rank by recoverable money, not by noise" framing is the move that earns the ×4 "pinpoints the real core problem" points. Ask AI to sanity-check that your ranking logic is consistent.

---

## SLIDE 3 — Key Insights From the Case Data

**Headline:** Three numbers force the strategy.

**On-slide content:**
- **① 68%** — stockouts cost 68% of net profit, yet inventory is tracked by manual Excel twice a day (Exhibit C + D).
- **② PHP 2.4M vs PHP 9M** — a Cebu hub saves ~PHP 2.4M in shipping but costs ~PHP 9M/yr to run. *The case's own example admits shipping savings can't cover a hub* (Exhibit B, Assumption C).
- **③ 9% margin** — too thin to afford a fix that costs more than it saves (Exhibit A interpretation guide).

- **The logic:** cheap + high-return + low-risk = fix operations first. Expensive + uncertain = earn it later.

📊 *Data viz:* three columns, each a giant number + one line. This is a "rule of three" slide — very memorable.
🎓 *AI note:* we found insight ② by having AI compare Exhibit B against Assumption C — the case *plants* this contradiction and rewards teams who catch it. Always ask AI: "what two exhibits, read together, change the answer?"

---

## SLIDE 4 — Customer & Market Opportunity

**Headline:** The demand is already there — PopCart just can't keep it in stock or get it there.

**On-slide content:**
- **Proven demand:** freeze-dried candy sells **300 units/day even while out of stock 11 days/month**. People want it; PopCart isn't capturing it.
- **Underserved regions:** Central Visayas + Davao = **43% of orders** but slowest (5–10 days), priciest (PHP 155–185), most damaged (4.2–5.0%) — Exhibit B.
- **Channel reality:** 90% from TikTok Shop — the growth engine *and* the single biggest risk.
- **The opportunity:** recapture demand we already lose, then protect the channel that creates it.

📊 *Data viz:* PH map with CV + Davao shaded (43% callout). Small bar chart: damage rate by region (MM 1.5% vs Davao 5.0%) to show the regional gap.
🎓 *AI note:* ask AI to pull *public* context (TikTok Shop PH growth, snack e-commerce trends) to size the market — but label it clearly as external research in the appendix, per the rules.

---

## SLIDE 5 — Option Comparison (benefit / cost / risk) ★ analytical centerpiece

**Headline:** Only one option has a positive floor — it can't lose, even in its worst case.

**On-slide content** — **recurring** (steady-state) net per year:

| Option | Worst case | Base case | Best case | Risk |
|---|---|---|---|---|
| **D — Fix Operations First** | **+PHP 0.20M** 🟢 | **+PHP 0.97M** | +PHP 3.51M | Low, reversible |
| A — Cebu hub (owned) | −PHP 6.88M 🔴 | −PHP 3.96M 🔴 | +PHP 1.00M | High fixed cost |
| C — Mall kiosk | −PHP 2.52M 🔴 | +PHP 0.12M | +PHP 3.00M | Foot-traffic bet |

- **Decision rule:** *on a 9% margin, you maximize the FLOOR, not the ceiling.* Ops-fix is the only option whose worst case stays positive.
- **Honest accounting:** ops-fix is valued at a conservative **30% contribution margin** (recovered sales still pay fees + shipping); the hub's growth is credited *generously* at 50% — and it **still** loses in the base case.
- **Caveat (state it):** these are recurring figures. Year 1 for ops-fix is an *investment year* (~−PHP 0.67M cash after the PHP 1.4M setup); net-positive in ~17 months.

📊 *Data viz:* a **floating-bar / range chart** — one bar per option from worst→best, with a line at PHP 0. Ops-fix sits entirely right of zero; the others cross into red. This single chart *is* the argument.
🎓 *AI note:* straight from [popcart_model.py](popcart_model.py). In the live round, offer to show the model run — "AI woven into your own work" made visible.
🎤 *Talk track:* "We didn't pick the highest upside. We picked the one a thin-margin business can't lose on — and we handicapped its rival in its own favour to prove it."

---

## SLIDE 6 — Recommended Strategy

**Headline:** Fix the engine first, then expand asset-light — never all at once.

**On-slide content:**
- **PRIMARY MOVE → Fix Operations First** (forecasting + reorder control system). Recovers ~PHP 1.0–1.6M/yr recurring; ~13–20 mo payback; the only positive-floor option.
- **THEN, in sequence:**
  - **Cheap hedge (by Mo 6):** launch a low-cost **own webstore** — the one second-channel spend in Year 1.
  - **Phase 2 (Mo 7+, gated on a 3PL quote):** asset-light **Cebu 3PL** — only if it beats ~PHP 56/order.
  - **Year 2:** evaluate kiosk / owned hub — *deferred, not in Year 1.*
- **The discipline:** one lead move, a clear order, *never funding everything in Year 1* (the case penalizes "do everything").
- **The principle:** *earn the right to expand.* Year 1 builds the cash and the data that make Year 2 expansion safe.

📊 *Data viz:* a 3-phase horizontal timeline with a **decision-gate diamond** at Month 7. Phase 1 big and bold; phases 2–3 lighter (they're conditional).
🎓 *AI note:* ⚠️ *Team review point — this is THE recommendation. Read it aloud together: does "earn the right to expand" feel true to you? If you'd rather lead with the Cebu 3PL (Raj's instinct), tell me and I'll re-sequence — but the model shows leading with the hub risks a −PHP 6.88M floor.*

---

## SLIDE 7 — Location & Channel Recommendation

**Headline:** Stay online in Year 1; pilot Cebu via 3PL only if a partner quote clears the unit-economics bar.

**On-slide content:**
- **Year 1 base:** online-only + a low-cost **own webstore** (~PHP 50–150K) — the case notes PopCart has "almost no presence on its own website." Cheap channel insurance, and the *one* second-channel move in Year 1.
- **Cebu, not Davao, first:** higher volume, shorter distance, better economics. Davao waits.
- **3PL, not an owned hub:** converts the PHP 9M/yr fixed cost (the −PHP 6.88M floor) into pay-per-use variable cost.
- **The decision gate (corrected):** proceed only if a real 3PL quote costs **less than ~PHP 56/order** (shipping saved + damage avoided, *before* any growth). Gate on quoted unit economics — **not** on a hoped-for growth %.

📊 *Data viz:* decision tree — "Month 7: Does a 3PL quote beat ~PHP 56/order on current volume? → Yes: pilot top SKUs / No: stay online, re-quote later."
🎓 *AI note:* ⚠️ *Optional analogy — team's call (see checklist). MrBeast's virtual-kitchen model scaled fast by decentralizing to 3rd-party kitchens, then hit quality-control disputes + litigation and was unwound — lesson: "decentralize only with a control system." Powerful but factually delicate: state it exactly or drop it. **Never say it "collapsed."** Always ask AI for the full arc of an example — half a story is a Q&A trap.*

---

## SLIDE 8 — Supply Chain & Inventory Solution

**Headline:** Reorder *before* you run out — not after the shelf is empty.

**On-slide content:**
- **Today:** founders reorder on "gut feel + visual shelf checks" (Exhibit D). With 14–30 day lead times, by the time a shelf looks empty, it's already too late.
- **The fix — a reorder point per SKU:** `reorder when stock ≤ (daily sales × lead time) + safety stock`
  - *Example:* Freeze-dried candy = 300/day × 14-day lead + buffer → reorder at ~5,000 units, weeks before stockout.
- **Long-lead items (ramen, 30 days):** pre-order viral SKUs + add a 2nd supplier (case risk mitigation).
- **Target:** stockout days **11 → 4–7 per month** (case KPI).

📊 *Data viz:* a "sawtooth" inventory line chart — stock falling, hitting the reorder line, replenishing — with the danger zone (stockout) shaded red. Very intuitive.
🎓 *AI note:* the reorder-point formula is standard ops math; we used AI to apply it to each SKU's real lead time from Exhibit C. Ask AI to compute the trigger level for all 5 SKUs so you can show a table in the appendix.

---

## SLIDE 9 — Forecasting & Reorder Control System + Workflow ★ highest-weighted (×5)

**Headline:** A forecasting & reorder control system a 3-person admin team can actually run.

**On-slide content — the workflow (left → right):**
1. **INGEST** — orders flow from the **TikTok Shop Orders API** via a connector (or a scheduled export, 2–3×/day) into Google Sheets — replacing the manual 2×/day Excel.
2. **FORECAST** — weighted **7/14/28-day** sales trend + lead-time demand + safety stock, with a **viral-trend multiplier** from TikTok views/add-to-cart + Google Trends.
3. **COMPUTE** — a reorder point per SKU + a daily fast-mover ranking + viral watchlist.
4. **ALERT** — automatic reorder alerts + a one-screen dashboard.
5. **DECIDE** — founder reviews alerts **daily**; parameters tuned **weekly**. **System recommends; humans decide.**

- **Tools (cheap, low-code):** Google Sheets + Power Query (or Airtable) + a barcode scan app + an API connector / Apps Script. No engineers, no app to build.
- **✅ WE BUILT IT.** A live, formula-driven prototype exists — drop in the **Dashboard screenshot** ([screenshot_3_dashboard.png](screenshot_3_dashboard.png)) as the hero image: *3 SKUs to reorder, ₱55,410/day at risk, 1 viral item rising.* Back it with the **Control Panel** ([screenshot_2_control_panel.png](screenshot_2_control_panel.png)).

📊 *Data viz:* put the **Dashboard screenshot** centre-stage (proof, not promise); the 5-box flow runs small underneath as the legend. Callout "recommends → human decides."
🎓 *AI note:* the **make-or-break slide (×5)** — and we turned it from *told* to *shown*. The working file ([PopCart_Reorder_System.xlsx](PopCart_Reorder_System.xlsx)) uploads straight to Google Sheets and recalculates live; in Q&A you can change a stock number and watch a 🟢 flip to 🔴. Real data path (TikTok Orders API), real method (weighted 7/14/28-day + safety stock 1.65·σ·√LT + viral multiplier), real cadence (daily alerts, weekly tuning). That beats "AI brain" buzz, which the rubric penalizes.

---

## SLIDE 10 — Financial Logic, Part 1: The Leak

**Headline:** PHP 7.35M of gross profit lost a year — recoverable cheaply, but valued honestly.

**On-slide content:**

| SKU | Lost units/yr | Lost GP/yr (gross) |
|---|---|---|
| Freeze-Dried Candy | 39,600 | PHP 3.56M |
| Spicy Korean Ramen | 14,400 | PHP 2.30M |
| Chocolate Crunch | 13,440 | PHP 1.01M |
| Giant Bubble Gum | 4,320 | PHP 0.48M |
| **Total** | | **PHP 7.35M** |

- **The honest adjustment:** recovered sales still pay platform fees + shipping, so we value recovery at **contribution margin (~30% conservative)**, not the 50% gross margin. That's the real net opportunity (sized on Slide 11).
- **Cost to capture it:** **PHP 1.4M setup + PHP 0.9M/yr** (cheap, low-code tools).

📊 *Data viz:* horizontal bar of lost GP by SKU (freeze-dried candy dominates — that's the visual point). Cite Exhibit C.
🎓 *AI note:* show your work — the case rewards "numbers that reconcile." We deliberately value recovery at *contribution*, not gross; judges trust teams that discount their own upside. Full audit trail in the appendix via [popcart_model.py](popcart_model.py).

---

## SLIDE 11 — Financial Logic, Part 2: Payback & ROI

**Headline:** ~13–20 month payback on honest assumptions — and the only option that can't lose.

**On-slide content** — recovery held at 42.5%; sensitivity on **contribution margin** (the honest swing factor):

| Contribution margin | Recurring net/yr | Calendar payback* |
|---|---|---|
| 20% (harsh) | +PHP 0.35M | ~51 mo |
| **30% (base)** | **+PHP 0.97M** | **~20 mo** |
| 40% (realistic) | +PHP 1.60M | ~13 mo |
| 50% (full gross) | +PHP 2.22M | ~11 mo |

- *Calendar payback includes the 3-month build before benefits flow.*
- **Year 1 is an investment year:** ~−PHP 0.67M cash after the PHP 1.4M setup; net-positive thereafter.
- **Honest per the case rules:** payback may exceed 12 months at conservative margins — *and that's fine*. The outlay is tiny and reversible; the hub never pays back in its base case (−PHP 3.96M/yr), the kiosk's base payback is 115 months.

📊 *Data viz:* the sensitivity table + a small "Year-1 = investment" note box. The honesty (discounting our own case to contribution margin) is the selling point.
🎓 *AI note:* this table is the review correction made visible. Showing a *down*side sensitivity on your *own* recommendation reads as integrity, not weakness — and it still wins. Always have AI give conservative/base/optimistic, never one rosy number.

---

## SLIDE 12 — 12-Month Roadmap

**Headline:** One primary move, one cheap hedge, one *conditional* pilot — never everything at once.

**On-slide content:**

| Month | Phase | Output |
|---|---|---|
| 1 | Data cleanup | Clean sales/inventory/supplier baseline |
| 2–3 | Build + pilot the control system | Live reorder alerts; overselling drops |
| 4–6 | Optimize reorder points + launch webstore | Stockout days 11 → ~6; cheap 2nd channel live |
| **7** | **★ DECISION GATE** | **3PL quote beats ~PHP 56/order? → go/no-go** |
| 8–10 | *(only if gate passes)* Cebu 3PL pilot, top SKUs | Faster delivery, measured |
| 10–12 | Review & Year-2 plan | SOPs; decide kiosk/owned hub **for Year 2** |

- **What we deliberately DON'T do in Year 1:** owned hubs, permanent kiosks. The webstore is the *only* second-channel spend (trivial cost); the 3PL is *conditional*, not committed.

📊 *Data viz:* Gantt bars; Month-7 gate as a bright diamond. **Grey-out** the conditional 3PL row to show it's gated, not guaranteed.
🎓 *AI note:* this resolves the "do everything" trap the case penalizes — Year 1 = one real investment (the system) + one near-free hedge (webstore) + one *gated* pilot. Have AI re-check the roadmap commits to nothing the Year-1 budget can't fund.

---

## SLIDE 13 — Risks & Mitigation

**Headline:** Every major risk has a cheap, specific mitigation.

**On-slide content:**

| Risk | Mitigation |
|---|---|
| Staff won't adopt the tool | Low-code tools (Sheets/Airtable) + training; that's why we avoid enterprise software |
| Long supplier lead times (ramen 30d) | Pre-order viral SKUs; add a 2nd supplier |
| Recovery / margin lower than modeled | We already model a harsh 20–30% contribution; recurring still positive (Slide 11) |
| Year-1 cash dip (−PHP 0.67M) | Small, reversible; funded from current PHP 10.8M profit |
| Channel shock (TikTok change) | Low-cost webstore live by Mo 6; kiosk evaluated for Year 2 |
| Hub never utilized | Deferred behind a unit-economics gate; 3PL, not owned |

📊 *Data viz:* 2-column table. Keep it tight — reassurance, not a wall of text.
🎓 *AI note:* this table IS our red-team — we had AI attack the plan, then turned each attack into a row. Have AI fire these at you aloud for Q&A practice.

---

## SLIDE 14 — Expected Impact

**Headline:** Stockouts roughly halved, a second channel live, and net margin climbing toward the 10% target.

**On-slide content:**

| KPI (case targets) | Baseline | After Year 1 |
|---|---|---|
| Stockout days/month (viral) | 11 | ~6 (range 4.4–8.3) ✅ meets 4–7 target in base case |
| Inventory update frequency | 2×/day | every 2 hrs ✅ |
| Recovered profit (recurring) | — | +PHP 1.0–1.6M/yr |
| Net profit margin | 9.0% | 9.3–10.3% in Yr 1 (by contribution margin); toward 10–13% target as it compounds |
| Channel share (TikTok) | 90% | webstore live; diversification begun |

📊 *Data viz:* before→after arrows. Green-check **only** where we genuinely hit the case target; show margin as a *trend arrow*, not a hard number.
🎓 *AI note:* mirror the case's exact KPI names (case p.14). Note we softened "10.3%" to "trending to ~10%" — the margin claim must use contribution, not gross, so we present it as a trajectory, honestly.

---

## SLIDE 15 — Closing Pitch

**Headline:** Fix the engine. Earn the growth. Decentralize with control.

**On-slide content:**
- **The leak is the opportunity:** PHP 7.35M of gross profit lost yearly, closed for a PHP 1.4M outlay.
- **The discipline is the edge:** one lead move, small and reversible, with a positive floor in every scenario.
- **The growth is sequenced, not gambled:** expand to Cebu only once the data earns it — asset-light, with a control tower, learning from MrBeast's mistake.
- **Closing line:** *"PopCart doesn't need to bet the margin to grow. It needs to stop the leak, then let the data point the way."*

📊 *Data viz:* minimal — the closing line big and centered, the 3 phase icons small underneath. End on confidence, not clutter.
🎤 *Talk track:* land the last line slowly, then stop. Don't add a "thank you" slide that dilutes it.

---

## APPENDIX (not counted — required by the case)

**A. AI-Use Disclosure** *(name every tool + where used — the case requires this)*

| AI / tool | Where we used it |
|---|---|
| ⚠️ `[Claude / ChatGPT / etc.]` | Extracted & structured the exhibits; ranked the money leaks; drafted slide copy & headlines; red-teamed the recommendation |
| Python (models we wrote w/ AI help) | `popcart_model.py` — scenario financials, payback, margins; `build_prototype.py` — generates the live reorder system |
| Google Trends / public web | Market context on TikTok Shop PH & snack e-commerce |
| ⚠️ `[Canva / PowerPoint / Gamma]` | Slide design & charts |

> Statement: *"AI was used as an analytical and drafting partner. Every figure was verified against the case exhibits by the team. No output was presented as fact without checking."*

**B. Supporting Calculations** — paste the full output of `popcart_model.py` (stockout table, all scenario grids, the downside test). Optionally include a screenshot of the working reorder prototype (`PopCart_Reorder_System.xlsx`) — README tab documents every formula.

**C. Key Assumptions** — AOV PHP 650; gross margin 50%; **contribution margin ~30% (conservative) on recovered sales** — nets out platform fees + shipping; this is the honest value of recovery, *not* the 50% gross; stockout recovery 25–60% (Assumption D); damage loss/order ~PHP 480 (COGS + wasted shipping); **hub growth credited generously at 50%** (we handicap the option we reject); 3-month build before benefits flow; tool costs at MSME low-end (Sheets/Airtable, no enterprise software).

---

## 🗣️ ANALOGY BANK — make the numbers stick (storytelling, ×4)

> Rule: every analogy must stay true to the *corrected* numbers. Never use one that re-inflates the recovery we discounted to contribution margin.

| # | Number / concept | Analogy | Use it on |
|---|---|---|---|
| 1 | PHP 7.35M leak = 68% of net profit | **The empty-shelf bucket** — best-seller sold out 1 day in 3; for every ₱3 of take-home profit, ~₱2 more walks out as customers leave. (Add: "we won't recover all of it.") | 🟢 Slides 2 & 10 |
| 2 | Reorder point = sales × lead time + safety stock | **The low-fuel light** — don't wait for the engine to die when the next station is a 14-day drive; the reorder point warns you with road left to refill. | 🟢 Slide 8 |
| 3 | Contribution vs gross margin (~30% not 50%) | **Gross salary vs take-home pay** — ₱180 candy nets ~₱54 after TikTok's cut + courier; budget on take-home, not gross. | 🟢 Slides 10–11 |
| 4 | Maximize the floor, not the ceiling | **Don't bet the rent on lotto** — hub: win ₱1M or lose ₱6.9M; ops-fix: reliably +₱0.2–3.5M, never loses. On a 9% margin, take the sure gain. | 🟢 Slide 5 |
| 5 | Owned hub vs 3PL (fixed vs variable cost) | **Buying a car vs taking Grab** — pay for the car whether you drive or not; pay Grab only when you ride. Take Grab until you're driving daily. | 🟢 Slide 7 |
| 6 | Hub ₱9M/yr cost vs ₱2.4M shipping saving | **A ₱9M truck to save ₱2.4M in fares** — only worth it if you fill it. | 🎤 Slide 6/7 pitch |
| 7 | Year 1 = −PHP 0.67M, positive after | **Planting a fruit tree** — spend to plant Year 1, harvest every year after. Payback >12 mo = farming, not gambling. | 🎤 Slide 11 pitch |
| 8 | 90% TikTok dependence | **A house on rented land** — landlord can change rent/rules/locks overnight; the webstore is buying your own small lot. | 🎤 Slide 4/7 pitch |
| 9 | Manual 2×/day inventory | **Checking your bank balance only at 8am & 5pm**, then spending blind; the system is online banking — always on, alerts when low. | 🎤 Slide 9 pitch |
| 10 | AI's role (recommends, human decides) | **GPS, not a self-driving car** — smart dashboard warns; founder still drives and can overrule. | 🎤 Slide 9 pitch |
| 11 | Cebu gate (~PHP 56/order budget) | **A house-hunting budget** — quote ₱50, move in; quote ₱80, walk away — don't bank on a future raise. | 🎤 Slide 7 pitch |

🎓 *AI note:* analogies are where AI helps you *translate*, not invent. Ask AI: "give me 5 everyday Filipino analogies for [this number], then flag any that distort the math." Keep only the ones that survive the honesty check.

---

## ⚠️ Team review checklist (do this before submitting)
1. Fill every `⚠️` (school name, team name, AI tools used, design tool).
2. **Slide 6** — agree on the lead move as a team (ops-first vs Raj's hub-first). Current deck = ops-first.
3. **Slide 9** — decide: diagram, or a real prototype-Sheet screenshot? (Strongest scoring lever.)
4. **Slide 7** — vote: keep the MrBeast analogy (stated *exactly*, never "collapsed") or drop it.
5. Read each headline alone — does it state a conclusion? If it's a topic, rewrite it.
6. Check every number on a slide traces to an exhibit or the model — *and uses contribution margin, not gross, for recovered sales.*
7. Count content slides = 15 exactly. Cover + appendix excluded.

## 📌 Changelog — what the review fixed (so you can defend it in Q&A)
- **Contribution margin, not gross:** recovered sales valued at ~30% (pays fees + shipping), not 50%. Recurring benefit now ~PHP 1.0–1.6M/yr.
- **Payback honesty:** ~13–20 months calendar (incl. 3-mo build), not 7.6; Year 1 is an investment year (−PHP 0.67M cash).
- **Cost stated fully:** PHP 1.4M setup + PHP 0.9M/yr, not "~PHP 1M".
- **Cebu gate fixed:** unit economics (3PL < ~PHP 56/order), not "15% growth".
- **Roadmap de-loaded:** kiosk deferred to Year 2; webstore is the only 2nd-channel spend → no "do everything" contradiction.
- **Workflow tightened:** "control system" not "AI brain"; TikTok Orders API (not magic no-code); daily alerts + weekly tuning; weighted 7/14/28-day trends.
- **Stockout target honest:** ~6 days base (range 4.4–8.3), hits 4–7 target in base/optimistic, not always.
- **MrBeast:** softened from "collapsed" to "disputes + litigation, unwound."
