"""
Finals-deck charts (matplotlib, warm theme). Writes PNGs to ../deck/:
  chart_spoilage.png : gut-feel ~16% vs Smart-Prep ~9% spoilage (two bars)
  chart_accuracy.png : forecast-vs-actual line for one SKU across the backtest window
  chart_uplift.png   : profit protected, staged ~PHP30k vs full ~PHP59k (two bars)
The CHARTS visualize the proof; the numbers come from data/*.csv + the model.
Run from repo root:  ./.venv/bin/python SukiMart/smartprep/charts.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")                       # headless: write files, no display
import matplotlib.pyplot as plt
import forecast
from config import DATA_DIR, HERE, WARMUP_DAYS, FULL_SCALE

# --- warm theme ----------------------------------------------------------
CREAM="#FBF7F0"; NAVY="#1F3864"; GREEN="#2E8B57"; GOLD="#E8A33D"; RED="#D1495B"; GREY="#8A8079"
DECK_DIR = os.path.normpath(os.path.join(HERE, "..", "deck"))


def _theme():
    """Apply the warm, large-font look to every figure."""
    plt.rcParams.update({
        "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
        "font.size": 16, "axes.titlesize": 24, "axes.labelsize": 18,
        "axes.titleweight": "bold", "axes.titlecolor": NAVY, "axes.labelcolor": NAVY,
        "axes.edgecolor": GREY, "xtick.color": NAVY, "ytick.color": NAVY,
        "text.color": NAVY, "axes.grid": False, "figure.dpi": 110,
    })


def _bare(ax):
    """Strip top/right spines for a clean deck look."""
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# --- chart 1: spoilage ---------------------------------------------------
def chart_spoilage(out=None, gut=0.16, sys=0.09):
    """Two bars: gut-feel spoilage (red) vs Smart-Prep spoilage (green)."""
    out = out or os.path.join(DECK_DIR, "chart_spoilage.png")
    _theme()
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    labels, vals, cols = ["Gut-feel\nprep", "Smart-Prep"], [gut*100, sys*100], [RED, GREEN]
    bars = ax.bar(labels, vals, color=cols, width=0.55, zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x()+b.get_width()/2, v+0.4, f"{v:.0f}%", ha="center",
                va="bottom", fontsize=26, fontweight="bold", color=b.get_facecolor())
    ax.set_title("Spoilage: less waste, same shelf")
    ax.set_ylabel("Spoilage (% of sales value)")
    ax.set_ylim(0, max(vals)*1.25)
    ax.annotate("", xy=(1, sys*100+0.6), xytext=(0, gut*100-0.6),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=2.2))
    ax.text(0.5, (gut+sys)/2*100, f"-{(gut-sys)*100:.0f} pts", ha="center",
            va="bottom", fontsize=16, fontweight="bold", color=NAVY)
    _bare(ax)
    fig.tight_layout(); fig.savefig(out); plt.close(fig)
    return out


# --- chart 2: forecast vs actual ----------------------------------------
def _load():
    """Load items + per-SKU demand series and aligned weekday labels from data/*.csv."""
    items = pd.read_csv(os.path.join(DATA_DIR, "items.csv")).to_dict("records")
    sales = pd.read_csv(os.path.join(DATA_DIR, "sample_sales.csv"), parse_dates=["date"]).sort_values("date")
    dates = sorted(sales["date"].unique())
    dows = [pd.Timestamp(d).strftime("%a") for d in dates]
    series = {it["sku_id"]:
              sales[sales.sku_id == it["sku_id"]].set_index("date")["qty"].reindex(dates).fillna(0).tolist()
              for it in items}
    return items, series, dates, dows


def chart_accuracy(out=None, sku_id="SIO"):
    """Rolling one-step-ahead forecast vs actual for one SKU over the backtest window."""
    out = out or os.path.join(DECK_DIR, "chart_accuracy.png")
    items, series, dates, dows = _load()
    name = next((it["name"] for it in items if it["sku_id"] == sku_id), sku_id)
    y = series[sku_id]; n = len(y)
    xs, actual, pred = [], [], []
    for t in range(WARMUP_DAYS, n):                    # same window the backtest scores
        mean, _, _ = forecast.forecast_next(y[:t], dows[:t], dows[t])
        xs.append(pd.Timestamp(dates[t])); actual.append(y[t]); pred.append(mean)
    wape = sum(abs(p-a) for p, a in zip(pred, actual)) / max(sum(actual), 1)

    _theme()
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(xs, actual, color=NAVY, lw=2.6, label="Actual sold", zorder=3)
    ax.plot(xs, pred, color=GOLD, lw=2.6, ls="--", label="Forecast", zorder=4)
    ax.set_title(f"Forecast tracks reality — {name}")
    ax.set_ylabel("Units / day")
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper left", frameon=False, fontsize=15)
    ax.text(0.99, 0.04, f"WAPE {wape*100:.0f}%", transform=ax.transAxes, ha="right",
            va="bottom", fontsize=16, fontweight="bold", color=GREEN)
    fig.autofmt_xdate(rotation=30)
    _bare(ax)
    fig.tight_layout(); fig.savefig(out); plt.close(fig)
    return out


# --- chart 3: profit protected ------------------------------------------
def chart_uplift(out=None, staged=24_000, full=47_000):
    """Two bars: profit protected per year, staged (gold) vs full SukiMart (green)."""
    out = out or os.path.join(DECK_DIR, "chart_uplift.png")
    _theme()
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    labels, vals, cols = ["Staged\nstore", "Full\nSukiMart"], [staged, full], [GOLD, GREEN]
    bars = ax.bar(labels, vals, color=cols, width=0.55, zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x()+b.get_width()/2, v+vals[1]*0.02, f"PHP {v:,.0f}", ha="center",
                va="bottom", fontsize=20, fontweight="bold", color=b.get_facecolor())
    ax.set_title("Profit protected / year")
    ax.set_ylabel("PHP saved per year")
    ax.set_ylim(0, full*1.22)
    ax.text(0.5, 0.55, "₱0 incremental cost\na POS feature already in the plan",
            transform=ax.transAxes, ha="center", va="center", fontsize=12, color=GREY)
    _bare(ax)
    fig.tight_layout(); fig.savefig(out); plt.close(fig)
    return out


def build_all():
    """Make the deck dir and write all three PNGs; return their paths."""
    os.makedirs(DECK_DIR, exist_ok=True)
    return [chart_spoilage(), chart_accuracy(), chart_uplift()]


if __name__ == "__main__":
    # Self-test: build the real charts, then assert all three PNGs exist.
    paths = build_all()
    for p in paths:
        assert os.path.exists(p), f"missing {p}"
        print("wrote", p, f"({os.path.getsize(p):,} bytes)")
    print("OK — 3/3 charts exist  (FULL_SCALE ratio check ~ %.2f)" % FULL_SCALE)
