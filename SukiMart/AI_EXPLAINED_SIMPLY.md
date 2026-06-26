# Smart-Prep, Explained From Zero
## A plain-language lecture on the AI we built — for every teammate, no background needed

> **The goal of this document.** By the end, you can explain our AI to your *lola* — and to a judge. We assume you know **nothing** about business math or AI. Every hard word is explained with an everyday example *before* we name it. Read it slowly, once. Then read §9 (the 5-sentence version) and §11 (your rehearsal lines) until you can say them without looking.
>
> **First, the only scary word, removed:** a **"model"** is just a **recipe** — a fixed set of steps a computer follows to turn information into an answer. Not a robot. Not magic. A recipe. We use a few small recipes that work together. That's the whole "AI."
>
> **A note on the two names:** the whole predictive engine is called **SukiSense**. **Smart-Prep** is its *first part* — the spoilage one — and it's the part this lecture explains. So when you hear "SukiSense," think *the engine*; when you hear "Smart-Prep," think *the first thing it does.*

---

## §1 · The one job (everything starts here)

Every single morning, Tina has to answer one question for her cooked food:

> **"How many should I make today?"** — how many siomai, cups of coffee, rice meals, pandesal, lumpia.

It sounds small. It is actually where the most money is won or lost, because:
- Cooked food (ready-to-eat) earns the **best profit** in the store — **45% to 55%**.
- But it **spoils fast.** If she makes too much, the leftover is thrown away — **money in the trash.**
- If she makes too little, she **sells out** and turns customers away — **money she never earned.**

So she's trapped between two mistakes every day:

| Mistake | What happens | What it costs |
|---|---|---|
| **Cook too much** | leftovers spoil | she loses the **cost** of making them |
| **Cook too little** | sells out early | she loses the **profit** she would have made |

**Our AI, Smart-Prep, has exactly one job: help Tina pick the number that loses the least money** — for each item, every day. That's it. If you remember nothing else, remember this paragraph.

---

## §2 · The big picture (the whole AI in 4 simple steps)

Smart-Prep answers the morning question in four steps. The rest of this lecture is just these four steps, slowed down:

1. **GUESS** how many will sell today. *(called "forecasting")*
2. **ADMIT the guess isn't exact** — figure out the realistic range (could be a little more, could be a little less). *(called "uncertainty")*
3. **DECIDE the smart number to cook** — using which mistake is more expensive for that item. *(called the "newsvendor" decision)*
4. **LEARN from what really happened** tonight, so tomorrow's guess is better. *(the "learning loop")*

Picture an experienced *tindera* in her head: *"Fridays are busy, it's payday, looks like rain… I'll make a bit extra coffee but go easy on the pandesal."* **She is already doing all four steps in her head.** Smart-Prep just does the same thinking with memory and math — consistently, for every item, without forgetting or guessing wrong on a tired morning.

> **Say this on stage:** *"Our AI doesn't replace Tina's instinct — it's her instinct, written down as math, so it never has a bad morning and never forgets a pattern."*

---

## §3 · STEP 1 — Guessing how many will sell (forecasting)

**The problem:** before the day starts, we need a best guess of today's demand for each item.

**The everyday version:** how would *you* guess today's bread sales? You'd think about three things:
1. **What sells on a normal day** — "lately, about 40 pandesal a day."
2. **Whether business is slowly growing or shrinking** — "this month feels a bit busier than last."
3. **The weekly rhythm** — "Saturdays are always biggest, Sundays quietest."

That's exactly what our main forecasting recipe tracks. Its name is **Holt-Winters** (just two inventors' names — don't be scared of it).

### 3.1 What Holt-Winters actually does

It keeps a running estimate of those same three things and combines them:
- **The usual level** — roughly how much sells on an ordinary day. It updates this constantly: recent days matter more, old days matter less (but aren't forgotten).
- **The trend** — is the usual level slowly drifting up or down over weeks?
- **The weekly rhythm** — the repeating shape across Monday→Sunday. *(The fancy word for "a pattern that repeats on a fixed cycle" is **seasonality**. A week is our cycle.)*

> **One more term, made easy — "exponential smoothing."** It just means: **"trust recent days more than old days, but don't throw the old days away."** Last week tells you more about tomorrow than three months ago — but the old months still shaped the overall pattern. That's all "smoothing" means: gently blending the past, weighted toward what's recent.

So when someone says our model is **"triple exponential smoothing,"** they're saying the *same thing* as Holt-Winters — "triple" because it smooths **three** things (level, trend, weekly rhythm). **Same recipe, two names.** If a judge uses either name, you nod — they mean the same model.

### 3.2 The payday nudge

In the Philippines, the **15th and 30th** (payday) change everything — people have cash. So we added one nudge: around payday, **push the forecast up.** And the model **learns how big** that bump usually is from past paydays, instead of us guessing. We call it **"payday-aware Holt-Winters"** — Holt-Winters, plus it watches the calendar for payday.

### 3.3 The backup recipe for week one (the "seasonal baseline")

Holt-Winters needs a few weeks of history to learn the rhythm. **On day one, there is no history.**

**Everyday version:** a brand-new helper on their first week doesn't know the store's rhythm yet. So they use the simplest sensible rule: *"To guess this Friday, look at the last few Fridays and copy that, then adjust for payday."* Plain, but it works from day one.

That simple rule is our **seasonal baseline** — the fallback. Once 3–4 weeks of data exist, the smarter Holt-Winters takes over. **Smart-Prep automatically uses whichever one has been more accurate lately** — you don't choose.

> **Say it simply:** *"To guess demand, we use Holt-Winters — it learns the normal level, the slow trend, the weekly rhythm, and the payday bump. Before there's enough data, it falls back to a simple 'same-weekday average.'"*

---

## §4 · STEP 2 — Knowing how wrong the guess could be (uncertainty)

Here is the idea most people miss, and it's simple:

> **A forecast of "30 coffees" is a best guess — not a promise.** Some days 26 sell. Some days 35. We must know the **realistic range**, not just the middle number — because we cook *before* we know.

**Everyday version:** the weather app doesn't say "it will rain." It says **"30% chance of rain."** It gives you the *odds and the range* so you can decide whether to bring an umbrella. Same here: Smart-Prep says *"probably about 30 coffees, realistically somewhere from 25 to 36."* That **range** is what lets us safely cook a little extra to cover the busy-day chance.

### 4.1 Why we use different "shapes" of range

Different items vary in different ways, so the *shape* of their range differs. We pick the shape that fits each item. There are three, and you only need the intuition:

| Shape (the name) | Use it for | Everyday picture |
|---|---|---|
| **Normal** ("bell curve") | **big, steady sellers** — coffee (~28/day), pandesal (~40/day) | like people's heights: most cluster near the average, a few higher/lower, **evenly balanced** both sides |
| **Poisson** | **small-count items** — rice meals (~8/day) | like **counting how many tricycles pass in 10 minutes**: small whole numbers, can't go below zero, naturally a bit lopsided |
| **Negative Binomial** | small-count items that are **extra jumpy** | a usually-quiet item that **sometimes gets a surprise group order** — bigger swings than Poisson expects |

**Why this matters in one line:** you can't measure a big steady seller (coffee) and a tiny jumpy one (rice meals) with the same ruler. Smart-Prep picks the right ruler per item, **automatically**, from each item's own history.

> **You do NOT need to do any of this math.** The computer chooses the shape. You only need to be able to *say why*: **big steady sellers → bell curve; small counts → Poisson; jumpy small counts → Negative Binomial.** That sentence alone answers the judge.

> **Say it simply:** *"We don't just predict an average — we estimate the realistic range of demand, and we use the right kind of range for each item depending on whether it sells in big steady numbers or small jumpy ones."*

---

## §5 · STEP 3 — Deciding the smart number to cook (the newsvendor)

This is the **heart** of the AI and the part judges love. It's built on one insight:

> **The two mistakes do NOT cost the same.** So the smart amount to cook depends on *which mistake is more expensive for that specific item.*

**The classic everyday version (this is literally where the name comes from):** a man sells **newspapers** on the corner. Each morning he buys his stack. Papers unsold by night = wasted money. But if he runs out by noon, he misses sales he could've had. **How many should he buy?** It depends on his profit per paper versus his loss per unsold paper. That puzzle is called the **"newsvendor problem,"** and it's the standard, textbook method for anything that spoils — bread, coffee, newspapers, flowers. **We're using a 70-year-old, proven business formula — not a buzzword.**

### 5.1 Watch it decide, with Tina's real numbers

The rule: **if missing a sale hurts more than wasting one → cook a bit MORE than the average. If wasting hurts more than missing → cook a bit LESS.**

**☕ Coffee** — sells ₱30, costs ₱12.
- Miss a sale → lose the **profit, ₱18.**
- Waste a cup → lose the **cost, ₱12.**
- Missing (₱18) **hurts more** than wasting (₱12). → **Cook a little MORE than average.** (If the guess is 32, cook ~33 — *"cook 33, not 34."*)

**🥖 Pandesal** — sells ₱4, costs ₱2.40.
- Miss a sale → lose the **profit, ₱1.60.**
- Waste one → lose the **cost, ₱2.40.**
- Wasting (₱2.40) **hurts more** than missing (₱1.60). → **Cook a little LESS than average.**

**Same store, opposite decisions — and both are correct.** That's the magic sentence: **Smart-Prep makes a different, money-based decision for every item.** It is the opposite of "cook 20% extra of everything."

### 5.2 The one number behind it (optional, for the curious)

Smart-Prep turns "which mistake costs more" into a score between 0 and 1 called the **critical ratio** — *the share of the total mistake-cost that comes from missing a sale.*

> critical ratio = **profit-if-sold ÷ (profit-if-sold + cost-if-spoiled)**

- Coffee: 18 ÷ (18 + 12) = **0.60** → high → aim **above** average (cook generously).
- Pandesal: 1.60 ÷ (1.60 + 2.40) = **0.40** → low → aim **below** average (cook lean).

**Plain meaning:** a higher score = "this item is worth protecting against sell-outs, so cook more." A lower score = "this item is cheap to miss but costly to waste, so cook less." You don't need the formula on stage — just *"high-margin items we cook generously, cheap-to-waste items we cook lean, and the model calculates exactly how much."*

> **Say it simply:** *"The newsvendor model picks the prep quantity that loses the least money — balancing the cost of waste against the cost of a missed sale, separately for each item."*

---

## §6 · STEP 4 — It gets smarter every day (the learning loop)

The AI is not "set once." It improves nightly. Here's the loop:

- **Morning:** Smart-Prep recommends — *"make 33 coffee, 25 siomai, 8 rice meals…"*
- **During the day:** customers buy.
- **At close (30 seconds):** Tina records four things — **made, sold, spoiled, and did it sell out? (and what time).** *(This little daily record is the single most important habit — without it, nothing can learn.)*
- **Overnight:** the AI compares its guess to what really happened and adjusts:
  - Made too much, lots spoiled → **aim lower** tomorrow.
  - Sold out early → **aim higher** tomorrow.
  - Payday clearly spiked sales → **remember that** for next payday.

So it learns from its own mistakes, a little every day. **That's the honest meaning of "the AI learns" — not a brain, just a recipe that corrects itself with new data.**

### 6.1 The clever bit: the "sold-out trap" (censoring)

Here's a subtle problem that separates a real system from a toy:

> If Tina made **30** coffees and they **sold out by 2pm**, how many did people actually *want*? We don't know — maybe 30, maybe 45. **We only saw the ones who got served.**

**Everyday version:** a jeepney passes your stop already **full.** How many *more* people wanted to ride? You can't see them — they're left at the curb. If you only count who fit, you'll always **underestimate** demand.

If the AI naively learns "sold 30," it thinks demand was 30, so it suggests ~30 again, sells out again, and **spirals downward forever.** Smart-Prep avoids this: when an item **sells out**, it flags it and **estimates the demand it didn't get to see** (using the sell-out time). In our testing, ignoring this made demand look **17% too low**; correcting it brought the estimate **within about 1%** of the truth.

> **Say it simply:** *"When an item sells out, the real demand was higher than what we sold — like a full jeepney passing a crowded stop. We correct for that, so the forecast doesn't shrink itself into a corner."*

---

## §7 · The fancy AI we tested — and chose NOT to use (this is a strength)

You will be asked: *"Why not use real machine learning / deep learning / AI like ChatGPT?"* Here's the honest, confident answer.

We **did** test a modern machine-learning model — it's called **LightGBM** (a popular, powerful "learns-from-many-clues" model). The catch: powerful models like that need **lots and lots** of data to shine — years of it, ideally many stores.

Tina has about **four months** of data from **one** store. With that little, LightGBM actually did **worse** than our simple Holt-Winters. So we kept the simpler recipe — because here it is **both more accurate AND explainable** (we can tell Tina exactly *why* it recommended a number; a big ML model is a "black box" that can't).

> **Say it on stage (this scores points):** *"We tested a modern machine-learning model, LightGBM. With Tina's small dataset it performed worse than the simpler method, so we chose the simpler, explainable one. We used the right-sized tool — and we proved it by testing, instead of using fancy AI just to sound impressive."*

This is exactly the maturity the case asks for: *"Buzzwords score nothing."*

---

## §8 · How good is it? (the results, in plain words)

We **backtested** it — meaning we replayed history and checked the AI's guesses against what *actually* sold (a fair, honest exam). The headline results:

| Plain question | Answer |
|---|---|
| How accurate is the forecast? | On average it's off by about **19%** *(lower is better; the simple model beat LightGBM's 20%)* |
| How much less food is wasted? | Spoilage drops from about **16% → 9%** of what's prepped |
| How much money does that protect? | about **₱24,000/year** now, **~₱47,000/year** at full SukiMart size |
| What does it cost to run? | **₱0 extra** — it's a feature of the POS she's buying anyway |

> **"WAPE"** is just the accuracy score — *"on average, how far off were our guesses, as a percentage."* 19% off. Lower is better. You can say "our average forecast error" instead of the acronym.

---

## §9 · The whole thing in 5 sentences (memorize this)

1. Every morning Tina must decide how much cooked food to make — too much spoils, too little sells out.
2. **Smart-Prep guesses tomorrow's demand** for each item using **Holt-Winters**, which learns the normal level, the weekly rhythm, and the payday bump.
3. It then estimates a **realistic range** around that guess (a bell curve for big sellers, a counting model for small-count items).
4. It picks the **profit-smart amount to cook** with the **newsvendor model** — cook *more* of high-margin items like coffee, *less* of cheap-to-waste items like pandesal.
5. Every night it **learns** from what sold and spoiled (and corrects for sell-outs), getting better over time — and we proved fancier AI wasn't worth it here.

---

## §10 · Glossary — every scary word in one plain line

| Word | What it really means |
|---|---|
| **Model** | a recipe: fixed steps that turn data into an answer |
| **Forecast** | a best guess of how many will sell |
| **Holt-Winters** | the forecasting recipe that learns level + trend + weekly rhythm |
| **Triple exponential smoothing** | the *exact same thing* as Holt-Winters (three things smoothed) |
| **Exponential smoothing** | "trust recent days more than old days, but don't forget the old ones" |
| **Seasonality** | a pattern that repeats on a cycle (for us, the weekly Mon→Sun shape) |
| **Seasonal baseline** | the simple backup forecast for week one ("average the last few same-weekdays") |
| **Uncertainty / distribution** | the realistic *range* of demand, not just the average |
| **Normal (bell curve)** | the range-shape for big, steady sellers |
| **Poisson** | the range-shape for small whole-number counts (e.g., 8 rice meals) |
| **Negative Binomial** | like Poisson but for small counts that swing more than expected |
| **Newsvendor model** | the decision recipe: cook the amount that loses the least money |
| **Critical ratio** | a 0–1 score for "how generously to cook this item" (high = cook more) |
| **Censoring / the sold-out trap** | sell-outs hide true demand (the full-jeepney problem); we correct for it |
| **Backtest** | replaying history to fairly test how good the guesses were |
| **WAPE** | the accuracy score: average forecast error as a % (lower is better) |
| **LightGBM** | a powerful machine-learning model we tested but didn't use (needs more data) |

---

## §11 · Your turn — rehearsal lines (say these out loud)

**If a teammate or judge asks "what is the AI?":**
> *"It's called Smart-Prep. Every morning it tells Tina how many of each ready-to-eat item to cook — enough to not lose customers, but not so much that food gets wasted. It guesses demand, estimates the range, then picks the money-smart amount to cook."*

**If asked "is it really AI, or just an average?":**
> *"Not an average. It learns weekly and payday patterns, estimates the realistic range per item, and makes a different cost-based decision for each one — more coffee because a missed sale costs more, less pandesal because waste costs more. And it improves every day from what actually sold."*

**If asked "what models?":**
> *"Holt-Winters to forecast demand, a Normal or Poisson range to handle uncertainty, and the newsvendor model to choose the profit-best quantity. We tested LightGBM too, but it didn't beat the simpler model on Tina's data."*

**The 3 things to NEVER forget:**
1. **One job:** how much to cook — waste vs. sell-out.
2. **Three steps:** guess (Holt-Winters) → range (Normal/Poisson) → decide (newsvendor).
3. **Per-item, money-based:** cook *more* coffee, *less* pandesal — and it learns nightly.

> *You don't need to be a data scientist. You need to explain a smart morning decision in plain Filipino. If you can tell the jeepney story and the coffee-vs-pandesal story, you understand our AI better than most people in the room.*
