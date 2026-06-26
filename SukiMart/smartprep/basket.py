"""
SukiSense · Basket Lift  [PROTOTYPE]
Market-basket analysis: find items frequently bought together, to drive cross-sell, bundles,
and shelf placement — lifting the average basket (the case: ~PHP 62 today vs the ~PHP 120 the
break-even needs). Classic, explainable association metrics, no black box:

    support(A,B)     = share of baskets containing BOTH A and B
    confidence(A->B) = P(B | A) = baskets(A,B) / baskets(A)
    lift(A->B)       = confidence(A->B) / P(B)      (lift > 1 => bought together MORE than chance)

We filter to a minimum support (so a one-off fluke pair doesn't top the list), then rank by lift.
"""
import os, csv
from itertools import combinations
from collections import Counter

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
MIN_SUPPORT = 0.12   # a pair must appear in >=12% of baskets to count (filters single-basket flukes)


def associations(baskets, min_support=MIN_SUPPORT):
    """Return cross-sell rules (both directions) sorted by lift, then antecedent.
    baskets: list of iterables of item names (one per transaction)."""
    n = len(baskets)
    if n == 0:
        return []
    sets = [set(b) for b in baskets]
    item_ct, pair_ct = Counter(), Counter()
    for s in sets:
        for it in s:
            item_ct[it] += 1
        for a, b in combinations(sorted(s), 2):
            pair_ct[(a, b)] += 1
    rules = []
    for (a, b), c in pair_ct.items():
        support = c / n
        if support < min_support:
            continue
        for x, y in ((a, b), (b, a)):                       # both directions
            confidence = c / item_ct[x]
            lift = confidence / (item_ct[y] / n)
            rules.append(dict(antecedent=x, consequent=y, support=round(support, 3),
                              confidence=round(confidence, 2), lift=round(lift, 2)))
    rules.sort(key=lambda r: (-r["lift"], r["antecedent"]))  # stable: alpha tiebreak
    return rules


def generate_sample(path=None):
    """Write illustrative transaction baskets (one row per basket, items pipe-separated)."""
    path = path or os.path.join(DATA_DIR, "baskets.csv")
    baskets = [
        "coffee|pandesal", "coffee|pandesal", "coffee|pandesal", "coffee|pandesal|egg",
        "rice|sardines", "rice|sardines", "rice|egg", "rice|softdrink",
        "sardines|softdrink", "siomai|softdrink", "siomai|rice", "cigarette|load",
        "cigarette|softdrink", "load|snack", "softdrink|snack",
    ]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["basket_id", "items"])
        for i, b in enumerate(baskets, 1):
            w.writerow([i, b])
    return path


def _load(path):
    with open(path) as f:
        return [row["items"].split("|") for row in csv.DictReader(f)]


def summary():
    """One-line module summary for the SukiSense status board."""
    rules = associations(_load(generate_sample()))
    if not rules:
        return "no strong pairs at this support"
    t = rules[0]
    return (f"top pair: {t['antecedent']} -> {t['consequent']} "
            f"(lift {t['lift']}, conf {int(t['confidence']*100)}%) · {len(rules)} rules")


if __name__ == "__main__":
    rules = associations(_load(generate_sample()))
    print(f"{'if buys':12}{'also buys':12}{'lift':>6}{'conf':>7}{'support':>9}")
    for r in rules[:10]:
        print(f"{r['antecedent']:12}{r['consequent']:12}{r['lift']:>6}"
              f"{str(int(r['confidence']*100))+'%':>7}{r['support']:>9}")
    # self-test: the tightly-paired coffee/pandesal must surface as the top rule
    assert rules and {rules[0]["antecedent"], rules[0]["consequent"]} == {"coffee", "pandesal"}, \
        "coffee<->pandesal should be the top association"
    print("\n[self-test] OK — coffee <-> pandesal is the top pair")
