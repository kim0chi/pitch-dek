"""
SukiMart — three-path 12-month pressure test (LAMBO 2026 Finals).  v2 (review-corrected)
Paths: 1) Full Jump  2) Staged Transition  3) Disciplined Sari-Sari.

CONSISTENCY RULES (so all three compare apples-to-apples):
  * ECONOMIC PROFIT = cash to Tina - PHP 16,000 fair wage (Exhibit A memo), for ALL paths.
  * Full-jump fixed cost 147,000 INCLUDES an 18k owner salary; we strip it out
    (129k fixed-ex-salary) so "cash to Tina" = GP - 129k, comparable to the no-salary paths.
  * Full-jump ramp tops out at 1.0 (steady = the case 'base'), no overshoot, so Mo-12 run-rate = base.
  * POS + AI software (~3k/mo) is INCLUDED in staged opex (itemised below).
Run:  ./.venv/bin/python SukiMart/sukimart_three_paths.py
"""
def php(x): return f"PHP {x:,.0f}"
WAGE=16_000

# ---------- BASELINE (Exhibit A) ----------
base_cash=180_000*0.175-5_700          # 25,800
base_econ=base_cash-WAGE               # 9,800
print("="*72)
print(f"BASELINE today: cash to Tina {php(base_cash)}/mo  |  TRUE economic profit {php(base_econ)}/mo")

# =====================================================================
# PATH 3 — DISCIPLINED SARI-SARI
# =====================================================================
d_sales=180_000*1.08; d_margin=0.19; d_opex=5_000; d_capex=30_000
d_cash=d_sales*d_margin-d_opex
d_econ=d_cash-WAGE
d_year1=d_cash*12-d_capex
print("\n"+"="*72)
print("PATH 3 — DISCIPLINED SARI-SARI")
print(f"  run-rate: cash {php(d_cash)}/mo  econ profit {php(d_econ)}/mo")
print(f"  YEAR-1 cash to Tina (after {php(d_capex)} capex): {php(d_year1)}   | no loan | savings kept ~{php(600_000-d_capex)}")

# =====================================================================
# PATH 2 — STAGED TRANSITION  (no loan in the modeled year)
#   opex itemised (Mo-12): helper 9k + chiller/RTE power 4k + RTE supplies/spoilage 5k
#                          + POS+AI software 3k + bags/misc 3k = 24k  (POS+AI INCLUDED)
# =====================================================================
s_sales =[180,195,210,230,250,270,285,295,305,312,318,320]   # k/mo
s_margin=[17.5,18,18.5,19,19.5,20,20.5,21,21,21,21,21]        # %
s_opex  =[6,8,11,14,16,18,20,22,23,24,24,24]                  # k/mo (incl POS+AI ~3k from Mo-3)
s_capex=150_000
s_year1=-s_capex
for i in range(12):
    cash=s_sales[i]*1000*s_margin[i]/100 - s_opex[i]*1000
    s_year1+=cash
m12_cash=s_sales[11]*1000*s_margin[11]/100 - s_opex[11]*1000
print("\n"+"="*72)
print("PATH 2 — STAGED TRANSITION  (self-funded, NO loan in Year 1)")
print(f"  Mo-12 run-rate: cash {php(m12_cash)}/mo  econ profit {php(m12_cash-WAGE)}/mo")
print(f"  YEAR-1 cash to Tina (after {php(s_capex)} capex): {php(s_year1)}   | no loan | savings kept ~{php(600_000-s_capex)}")
print(f"  PLUS: 12 months of real demand data to de-risk a later loan/full-build decision")

# =====================================================================
# PATH 1 — FULL JUMP  (600k savings + 750k loan; fixed 147k incl 18k salary)
#   ramp tops out at 1.0 (steady = base). cash to Tina = GP - 129k (fixed ex-salary).
# =====================================================================
FIX_EX_SAL=129_000; BUFFER=95_000
ramp=[0.55,0.65,0.75,0.85,0.95,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
print("\n"+"="*72)
print("PATH 1 — FULL JUMP   (needs PHP 1.35M: 600k savings + 750k loan)")
print(f"  {'scenario':>12} {'steady sales':>13} {'mgn':>5} {'run-rate econ/mo':>17} {'Yr-1 op cash':>14} {'downside liquidity':>19}")
def fulljump(label,ss,m):
    cum=0
    for r in ramp: cum += ss*r*m - FIX_EX_SAL
    steady_cash=ss*m-FIX_EX_SAL
    econ=steady_cash-WAGE
    liq=BUFFER+cum                         # 600k savings already spent as capital; only 95k buffer remains
    print(f"  {label:>12} {php(ss):>13} {m*100:>4.0f}% {php(econ):>17} {php(cum):>14} {php(liq):>19}")
    return econ,cum,liq
fulljump("Pessimistic",450_000,0.22)
fulljump("Base",       720_000,0.24)
fulljump("Optimistic",1_092_000,0.25)
print("  Base reconciles to the case's PHP 25,800 'surplus' (that's after an 18k salary;")
print("  econ profit is +2k higher because a FAIR wage is 16k, not 18k).")

# =====================================================================
# AI PAYBACK — perishable spoilage forecasting, AT THE RIGHT STORE SIZE
# =====================================================================
print("\n"+"="*72)
print("AI — perishable spoilage forecasting (POS-based; cost ~3k/mo already in opex)")
for label,sales,pshare in [("Staged store (~320k/mo)",320_000,0.25),
                           ("Full SukiMart (~720k/mo)",720_000,0.22)]:
    perish=sales*pshare
    saved=perish*(0.16-0.09)
    print(f"  {label:>26}: perishable {php(perish)}/mo  spoilage 16%->9% saves {php(saved)}/mo = {php(saved*12)}/yr")

# =====================================================================
# THE HONEST TRADE-OFF
# =====================================================================
print("\n"+"="*72)
print("THE TRADE-OFF (say this out loud):")
print(f"  Path 3 wins YEAR-1 CASH ({php(d_year1)}) but caps run-rate at {php(d_econ)}/mo.")
print(f"  Path 2 sacrifices ~{php(d_year1-s_year1)} of Year-1 cash to reach a {php(m12_cash-WAGE)}/mo run-rate")
print(f"        (~same as full-jump BASE {php(720_000*0.24-FIX_EX_SAL-WAGE)}/mo) WITHOUT the 750k loan, + buys data.")
print(f"  Path 1 base run-rate barely beats Path 2, but risks 1.35M and her 600k savings in the downside.")
