"""
PopCart PH — Decision Model v2 (LAMBO 2026 Qualifying Case)
Rebuilt after review to be Q&A-bulletproof. Key changes vs v1:
  * Stockout recovery valued at CONTRIBUTION margin, not gross margin
    (recovered sales still pay platform fees + shipping). Sensitivity shown.
  * Year-1 CASH impact shown separately from steady-state RECURRING benefit.
  * CALENDAR payback (incl. 3-month build ramp) shown next to financial payback.
  * Cebu decision GATE expressed as per-order unit economics, not growth %.
  * Hub growth GP kept GENEROUSLY at 50% (handicap in favour of the option we
    are rejecting) -- ops-fix still wins, so the result is not "engineered."

Run: python3 popcart_model.py
"""

def php(x): return f"PHP {x:,.0f}"
def pct(x): return f"{x*100:.1f}%"

# ----------------------------------------------------------------------
# BASELINE (Exhibit A, FY2025)
# ----------------------------------------------------------------------
REVENUE      = 120_000_000
GROSS_MARGIN = 0.50
NET_PROFIT   = 10_800_000
NET_MARGIN   = NET_PROFIT / REVENUE        # 9.0%

# Cost stack as % of revenue (Exhibit A) -> what a RECOVERED sale still incurs
PLATFORM_AND_MKTG = 0.10                    # most is marketing (fixed); see note
SHIPPING_SUBSIDY  = 0.20                    # variable per order
# Incremental cost on a recovered sale ~ platform commission (small) + shipping.
# Recovered demand needs ~no extra marketing (the customer already wants it).
# => contribution margin lands ~30% conservative ... 35-40% realistic.

# ----------------------------------------------------------------------
# 1) STOCKOUT OPPORTUNITY (Exhibit C) -- the gross size of the leak
# ----------------------------------------------------------------------
SKUS = [
    ("Freeze-Dried Candy Mix",   300, 11, 180),
    ("Spicy Korean Ramen",       240,  5, 320),
    ("Assorted Chocolate Crunch",160,  7, 150),
    ("Giant Bubble Gum Tubs",    180,  2, 220),
    ("Sour Belts & Bulk Packs",  120,  0, 120),
]
print("="*72)
print("1) STOCKOUT LEAK (Exhibit C)")
print("="*72)
total_lost_rev = 0
for name, upd, outdays, price in SKUS:
    lost_units = upd * outdays * 12
    lost_rev = lost_units * price
    total_lost_rev += lost_rev
    print(f"  {name:30s} {lost_units:7,} u/yr   lost revenue {php(lost_rev):>15}")
total_lost_gp = total_lost_rev * GROSS_MARGIN
print(f"  {'TOTAL lost revenue':30s} {php(total_lost_rev):>34}")
print(f"  Lost GROSS profit (at 50%): {php(total_lost_gp)}  = {pct(total_lost_gp/NET_PROFIT)} of net profit")
print("  NOTE: this is the GROSS leak. Net recoverable value uses CONTRIBUTION")
print("        margin below, because recovered sales still pay fees + shipping.")

# ----------------------------------------------------------------------
# 2) OPTION D -- FIX OPERATIONS FIRST  (contribution-margin sensitivity)
# ----------------------------------------------------------------------
SETUP   = 1_400_000          # base setup (one-time)
OPEX    = 900_000            # base annual operating (cheap MSME tools)
RECOVERY= 0.425              # base: midpoint of Assumption D (25-60%)
BUILD_MONTHS = 3             # roadmap: data cleanup + build + pilot before benefit

recovered_rev = total_lost_rev * RECOVERY
print("\n" + "="*72)
print(f"2) OPTION D -- FIX OPS FIRST   (recovery {pct(RECOVERY)}, setup {php(SETUP)}, opex {php(OPEX)}/yr)")
print("="*72)
print(f"   Recovered revenue/yr: {php(recovered_rev)}")
print(f"\n   {'Contribution':>12} | {'Recurring net/yr':>17} | {'Fin. payback':>12} | {'Calendar payback':>16}")
print("   " + "-"*64)
for cm in (0.20, 0.30, 0.40, 0.50):
    recurring = recovered_rev * cm - OPEX
    if recurring > 0:
        fin_pb = SETUP / recurring * 12
        cal_pb = fin_pb + BUILD_MONTHS
        fin_s, cal_s = f"{fin_pb:.1f} mo", f"{cal_pb:.1f} mo"
    else:
        fin_s = cal_s = "no payback"
    tag = "  <- base" if abs(cm-0.30) < 1e-9 else ""
    print(f"   {pct(cm):>12} | {php(recurring):>17} | {fin_s:>12} | {cal_s:>16}{tag}")

# Year-1 cash at base contribution (30%): benefit only flows for (12 - build) months
BASE_CM = 0.30
recurring_base = recovered_rev * BASE_CM - OPEX
yr1_benefit = recurring_base * (12 - BUILD_MONTHS) / 12
yr1_cash = yr1_benefit - SETUP
print(f"\n   Base case (30% contribution):")
print(f"     Recurring steady-state net : {php(recurring_base)}/yr  (POSITIVE)")
print(f"     Year-1 cash (9 mo benefit - setup): {php(yr1_cash)}  (negative in Yr1, normal for an investment)")
print(f"     -> Honest line: 'calendar payback is ~20 months; Year 1 is an investment year.'")

# ----------------------------------------------------------------------
# 3) OPTION A -- CEBU HUB (owned). Growth GP kept GENEROUS at 50%.
# ----------------------------------------------------------------------
CV_ORDERS, AOV = 48_100, 650
CV_REVENUE = CV_ORDERS * AOV
DMG_RATE, DMG_LOSS = 0.042, 480
print("\n" + "="*72)
print("3) OPTION A -- CEBU HUB (owned)   [growth GP credited generously at 50%]")
print("="*72)
def hub(label, ship_save, dmg_red, growth, opex):
    ship = CV_ORDERS * ship_save
    dmg  = CV_ORDERS * DMG_RATE * DMG_LOSS * dmg_red
    grow = CV_REVENUE * growth * GROSS_MARGIN     # generous 50%
    benefit = ship + dmg + grow
    net = benefit - opex
    print(f"   [{label:11s}] ship {php(ship):>12} + dmg {php(dmg):>9} + growth {php(grow):>11}"
          f" - opex {php(opex):>11} = {php(net):>12}/yr")
    return net
hub("Pessimistic", 40, 0.20, 0.00, 9_000_000)
hub("Base",        50, 0.30, 0.15, 9_000_000)
hub("Optimistic",  65, 0.40, 0.30, 7_200_000)

# Decision GATE as unit economics (review's point): what's available per order
# BEFORE assuming any growth, to cover all 3PL pick/pack/storage/transfer costs.
avail_per_order = 50 + (DMG_RATE * DMG_LOSS * 0.30)   # ship save + base damage avoided
print(f"\n   CEBU GATE (correct criterion): a 3PL must cost LESS than ~{php(avail_per_order)}")
print(f"   per order (shipping save {php(50)} + damage avoided {php(DMG_RATE*DMG_LOSS*0.30)})")
print(f"   BEFORE any growth. Gate on a real partner QUOTE, not on a growth %.")

# ----------------------------------------------------------------------
# 4) OPTION C -- MALL KIOSK (high-traffic, per kiosk)
# ----------------------------------------------------------------------
print("\n" + "="*72)
print("4) OPTION C -- MALL KIOSK (per kiosk)")
print("="*72)
def kiosk(label, rev, margin, opex_m, setup):
    net_yr = (rev*margin - opex_m) * 12
    pb = f"{setup/net_yr*12:.1f} mo" if net_yr>0 else "no payback"
    print(f"   [{label:11s}] {php(rev)}/mo x {pct(margin)} - {php(opex_m)}/mo = {php(net_yr):>12}/yr   payback {pb}")
    return net_yr
kiosk("Pessimistic", 600_000, 0.40, 450_000, 1_500_000)
kiosk("Base",        800_000, 0.45, 350_000, 1_150_000)
kiosk("Optimistic", 1_000_000,0.50, 250_000,  800_000)

# ----------------------------------------------------------------------
# 5) DOWNSIDE TEST -- recurring net/yr floor of each option
# ----------------------------------------------------------------------
print("\n" + "="*72)
print("5) DOWNSIDE TEST -- recurring (steady-state) net/yr floor")
print("="*72)
print(f"   Ops fix  (30% contrib, 25% recovery floor): { php(total_lost_rev*0.25*0.30 - OPEX) }  (still POSITIVE)")
print(f"   Cebu hub (base case)                      : PHP -3,959,216  (loses money)")
print(f"   Kiosk    (pessimistic)                    : PHP -2,520,000  (loses money)")
print("\n   The asymmetry HOLDS under honest accounting: ops-fix is the only option")
print("   with a positive recurring floor -- even when we handicap the hub generously.")
