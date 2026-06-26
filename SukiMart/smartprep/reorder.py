"""
Classic reorder points for the ~900 NON-perishable grocery SKUs.
These don't spoil, so the newsvendor (over-prep cost = spoilage) doesn't apply.
Instead we use the textbook (s, S) continuous-review model:
  reorder point s = avg_daily*lead_time + safety_stock     (cover demand during lead time)
  safety_stock    = service_z * std_daily * sqrt(lead_time) (buffer against demand variability)
  order-up-to  S  = s + avg_daily*review_period            (top up for the next review cycle)
service_z 1.65 -> ~95% in-stock during lead time. review_period=7 (weekly buy run).
"""
import os, csv
import numpy as np

REVIEW_PERIOD = 7   # days between order reviews (weekly resupply run)


def reorder_point(avg_daily, lead_time_days, std_daily, service_z=1.65):
    """When on-hand drops to this level, reorder: cover lead-time demand + safety stock."""
    s = avg_daily * lead_time_days + service_z * std_daily * np.sqrt(lead_time_days)
    return max(0, int(round(float(s))))


def suggest_orders(items, on_hand, service_z=1.65, review_period=REVIEW_PERIOD):
    """
    Flag SKUs at/below their reorder point and size the order.
    items   : iterable of dicts with sku_id, name, avg_daily, std_daily, lead_time
    on_hand : dict {sku_id: units currently in stock}
    Returns one row per SKU NEEDING reorder, with order_qty = order_up_to - on_hand.
    """
    out = []
    for it in items:
        sku = it["sku_id"]
        avg, std, lt = float(it["avg_daily"]), float(it["std_daily"]), float(it["lead_time"])
        have = float(on_hand.get(sku, 0))
        rop = reorder_point(avg, lt, std, service_z)
        if have <= rop:                                   # at/below trigger -> reorder
            order_up_to = rop + avg * review_period        # cover lead time + next review cycle
            qty = max(0, int(round(order_up_to - have)))
            out.append(dict(sku_id=sku, name=it.get("name", sku), on_hand=int(have),
                            reorder_point=rop, order_up_to=int(round(order_up_to)),
                            order_qty=qty))
    return out


def generate_sample(path="SukiMart/smartprep/data/grocery_items.csv"):
    """Write a small illustrative grocery_items.csv (non-perishable staples)."""
    rows = [
        # sku_id, name, avg_daily, std_daily, lead_time, on_hand
        ("RCE-5K", "Rice 5kg sack",     6, 2.0, 3, 30),   # comfortably above ROP -> no order
        ("OIL-1L", "Cooking oil 1L",   10, 3.5, 4,  8),   # below ROP -> reorder
        ("SUG-1K", "Sugar 1kg",         8, 2.5, 2, 25),   # above ROP -> no order
        ("SOY-1L", "Soy sauce 1L",      5, 2.0, 5,  6),   # at/below ROP -> reorder
        ("CAN-SAR","Sardines (can)",   14, 4.0, 3, 12),   # below ROP -> reorder
        ("DET-1K", "Detergent 1kg",     4, 1.5, 7, 40),   # high lead time but well-stocked
    ]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sku_id", "name", "avg_daily", "std_daily", "lead_time", "on_hand"])
        for r in rows:
            w.writerow(r)
    return path


if __name__ == "__main__":
    import csv as _csv
    p = generate_sample()
    print("Wrote sample to", p)
    with open(p) as f:
        items = list(_csv.DictReader(f))
    on_hand = {it["sku_id"]: int(it["on_hand"]) for it in items}

    print(f"\n{'SKU':9}{'name':18}{'on_hand':>8}{'ROP':>6}{'up_to':>7}")
    for it in items:
        rop = reorder_point(float(it["avg_daily"]), float(it["lead_time"]), float(it["std_daily"]))
        up_to = rop + float(it["avg_daily"]) * REVIEW_PERIOD
        print(f"{it['sku_id']:9}{it['name']:18}{int(it['on_hand']):>8}{rop:>6}{round(up_to):>7}")

    print("\nREORDER NOW:")
    for r in suggest_orders(items, on_hand):
        print(f"  {r['sku_id']:9} {r['name']:18} on_hand={r['on_hand']:<4} "
              f"ROP={r['reorder_point']:<4} -> order {r['order_qty']} (up to {r['order_up_to']})")
