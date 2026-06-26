"""
Tests for the SukiSense prototype modules: reorder, utang, basket.
Same import convention as test_smartprep.py (siblings import by bare name).

Run from repo root:  ./.venv/bin/python -m pytest SukiMart/smartprep/tests -q
"""
import os, sys
sys.path.insert(0, os.path.join("SukiMart", "smartprep"))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import reorder
import utang
import basket


# ---------- Smart Reorder ----------
def test_reorder_point_grows_with_demand_and_leadtime():
    base = reorder.reorder_point(avg_daily=10, lead_time_days=3, std_daily=2)
    assert reorder.reorder_point(20, 3, 2) > base          # more demand -> higher trigger
    assert reorder.reorder_point(10, 6, 2) > base          # longer lead time -> higher trigger
    assert reorder.reorder_point(10, 3, 8) > base          # more variability -> bigger safety stock


def test_suggest_orders_flags_only_low_stock():
    items = [
        dict(sku_id="A", name="A", avg_daily=10, std_daily=3, lead_time=4),  # ROP high
        dict(sku_id="B", name="B", avg_daily=2,  std_daily=1, lead_time=2),  # ROP low
    ]
    rop_a = reorder.reorder_point(10, 4, 3)
    on_hand = {"A": rop_a - 1, "B": 999}                    # A below trigger, B well above
    orders = reorder.suggest_orders(items, on_hand)
    flagged = {o["sku_id"] for o in orders}
    assert "A" in flagged and "B" not in flagged
    assert all(o["order_qty"] > 0 for o in orders)         # a flagged SKU orders a positive qty


# ---------- Utang Score ----------
def test_utang_score_bounds_and_ordering():
    good = utang.score_suki(on_time_rate=0.98, avg_days_late=1, defaults=0, times_borrowed=24)
    bad = utang.score_suki(on_time_rate=0.30, avg_days_late=25, defaults=3, times_borrowed=4)
    assert 0.0 <= bad <= good <= 100.0                     # clamped to [0,100], good > bad
    assert utang.band(good) == "LOW" and utang.band(bad) == "HIGH"


def test_utang_defaults_reduce_score_and_line():
    clean = utang.score_suki(0.9, 3, 0, 10)
    with_default = utang.score_suki(0.9, 3, 1, 10)
    assert with_default < clean                            # a default must lower the score
    assert utang.recommend_line(clean, 10) >= utang.recommend_line(with_default, 10)


# ---------- Basket Lift ----------
def test_basket_lift_identifies_paired_items():
    baskets = [["coffee", "pandesal"]] * 4 + [["rice"], ["sardines"], ["softdrink"]]
    rules = basket.associations(baskets, min_support=0.1)
    assert rules, "should find at least one association"
    top = rules[0]
    assert {top["antecedent"], top["consequent"]} == {"coffee", "pandesal"}
    assert top["lift"] > 1.0                               # bought together more than chance


def test_basket_min_support_filters_flukes():
    # coffee+pandesal appear together 5x; a one-off egg+load pair must be filtered out
    baskets = [["coffee", "pandesal"]] * 5 + [["egg", "load"]]
    rules = basket.associations(baskets, min_support=0.2)  # 0.2*6 = 1.2 -> needs >=2 baskets
    pairs = {frozenset((r["antecedent"], r["consequent"])) for r in rules}
    assert frozenset(("coffee", "pandesal")) in pairs
    assert frozenset(("egg", "load")) not in pairs
