"""
SukiSense · Utang Score  [PROTOTYPE]
Explainable credit-risk scoring for a sari-sari's utang (informal credit) ledger.

Why it matters: the case ledger is PHP 12,000 with ~6% never recovered (~PHP 720/mo of bad
debt). This module scores each suki on repayment behaviour and recommends a SAFE credit line
so Tina extends more to the reliable and tightens up on the risky — transparently, not a
black box. With real ledger data the weights would be calibrated; here they are sensible
defaults so the logic is fully auditable.

Trust score (0-100, higher = safer):
    + 100 x on-time payment rate     (the backbone signal)
    -   2 x average days late
    -  20 x past defaults (never repaid)   (a hard red flag)
    +   1 x times borrowed, capped at +10  (tenure / earned trust)
Recommended credit line scales with the score AND tenure.
"""
import os, csv

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
MAX_LINE = 1000  # peso ceiling for a fully-trusted, long-tenure suki (prototype assumption)


def score_suki(on_time_rate, avg_days_late, defaults, times_borrowed):
    """Return a 0-100 trust score (higher = safer) from one suki's repayment history."""
    s = 100.0 * float(on_time_rate)              # on-time rate is the backbone
    s -= 2.0 * float(avg_days_late)              # each average day late costs 2 points
    s -= 20.0 * float(defaults)                  # a never-repaid loan is a big red flag
    s += min(float(times_borrowed), 10) * 1.0    # tenure/trust bonus, capped at +10
    return float(max(0.0, min(100.0, s)))


def recommend_line(score, times_borrowed):
    """Map a trust score to a safe peso credit line (rounded to the nearest 50)."""
    trust = score / 100.0
    tenure_factor = min(float(times_borrowed), 20) / 20.0     # 0..1
    line = MAX_LINE * trust * (0.5 + 0.5 * tenure_factor)     # tenure can up to double the line
    return int(round(line / 50.0) * 50)


def band(score):
    """LOW / MEDIUM / HIGH risk band from the trust score."""
    return "LOW" if score >= 70 else ("MEDIUM" if score >= 40 else "HIGH")


def assess(rows):
    """Score every suki row; return dicts with score, risk band, and recommended line."""
    out = []
    for r in rows:
        s = score_suki(float(r["on_time_rate"]), float(r["avg_days_late"]),
                       float(r["defaults"]), float(r["times_borrowed"]))
        out.append(dict(
            name=r.get("name", r.get("suki_id", "?")),
            outstanding=float(r.get("outstanding", 0)),
            score=round(s, 1), risk=band(s),
            line=recommend_line(s, float(r["times_borrowed"])),
        ))
    return out


def generate_sample(path=None):
    """Write a small illustrative utang ledger (the logic is the deliverable, not the data)."""
    path = path or os.path.join(DATA_DIR, "utang_ledger.csv")
    rows = [
        # suki_id, name, on_time_rate, avg_days_late, defaults, times_borrowed, outstanding
        ("S01", "Aling Rosa",  0.98,  1, 0, 24, 150),
        ("S02", "Mang Tonio",  0.90,  3, 0, 18, 400),
        ("S03", "Neneng",      0.75,  7, 0,  9, 250),
        ("S04", "Kuya Boy",    0.60, 12, 1,  6, 600),
        ("S05", "Inday",       0.95,  2, 0, 30, 100),
        ("S06", "Mang Delfin", 0.40, 20, 2,  5, 800),
        ("S07", "Ate Cora",    0.85,  4, 0, 12, 300),
        ("S08", "Totoy",       0.30, 25, 3,  4, 500),
    ]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["suki_id", "name", "on_time_rate", "avg_days_late",
                    "defaults", "times_borrowed", "outstanding"])
        for r in rows:
            w.writerow(r)
    return path


def _load(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def summary():
    """One-line module summary for the SukiSense status board."""
    res = assess(_load(generate_sample()))
    safe = sum(r["line"] for r in res)
    high = sum(1 for r in res if r["risk"] == "HIGH")
    return f"{len(res)} suki scored · PHP {safe:,} total safe credit · {high} HIGH-risk flagged"


if __name__ == "__main__":
    res = sorted(assess(_load(generate_sample())), key=lambda x: -x["score"])
    print(f"{'suki':14}{'score':>6}{'risk':>8}{'safe line':>12}{'outstanding':>13}")
    for r in res:
        print(f"{r['name']:14}{r['score']:>6}{r['risk']:>8}"
              f"{'PHP '+str(r['line']):>12}{'PHP '+str(int(r['outstanding'])):>13}")
    # self-test: ordering sanity (a perfect payer outranks a serial defaulter)
    assert score_suki(0.98, 1, 0, 24) > score_suki(0.30, 25, 3, 4), "good payer must outrank defaulter"
    print("\n[self-test] OK — scores ordered correctly")
