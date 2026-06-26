"""
SukiMart (LAMBO 2026 Finals) — break-even & three-path model.
All inputs from the case exhibits. Run: ../.venv/bin/python sukimart_model.py
"""
def php(x): return f"PHP {x:,.0f}"

# ---- TODAY: Tindahan ni Tina (Exhibit A) ----
SALES=180_000; GM=0.175; GP=SALES*GM            # 31,500
CASH_OPEX=5_700; CASH_TO_TINA=GP-CASH_OPEX      # 25,800 (what Tina THINKS she earns)
FAIR_WAGE=16_000; TRUE_PROFIT=CASH_TO_TINA-FAIR_WAGE  # 9,800 economic profit
print("="*64,"\nTODAY — Tindahan ni Tina (Exhibit A)")
print(f"  Gross profit (17.5%): {php(GP)}   cash to Tina: {php(CASH_TO_TINA)}")
print(f"  Fair wage (Exhibit A memo): {php(FAIR_WAGE)}")
print(f"  TRUE economic profit: {php(TRUE_PROFIT)}/mo  <- the real baseline")

# ---- SUKIMART fixed costs (Exhibit D) ----
FIXED_CASH=147_000   # incl owner salary 18,000 + full loan amort 22,000
# loan 750k @18%/48mo -> payment ~22,028; year-1 interest ~10k/mo (rest is principal)
INT_ONLY=10_000
FIXED_PL=FIXED_CASH-22_000+INT_ONLY             # P&L view ~135,000
print("\n"+"="*64,"\nSUKIMART fixed costs (Exhibit D)")
print(f"  CASH/survival view: {php(FIXED_CASH)}/mo (all loan cash leaves drawer)")
print(f"  P&L view (interest-only ~{php(INT_ONLY)}): ~{php(FIXED_PL)}/mo")

# ---- BREAK-EVEN: gross profit must cover fixed cost ----
print("\n"+"="*64,"\nBREAK-EVEN — required monthly SALES (cash view, GP must = 147,000)")
for m in (0.175,0.20,0.22,0.24,0.25,0.28):
    req=FIXED_CASH/m
    print(f"  at {m*100:4.1f}% blended margin -> {php(req)}/mo  = {php(req/30)}/day")

# ---- Translate to transactions/day vs location capacity (Exhibit E/F/G) ----
print("\n"+"="*64,"\nCAN THE LOCATION DELIVER?  (Exhibit E/F)")
print("  Passersby 1,800/day · current 96 txns/day · convenience benchmark 150-450 txns, basket 90-140")
for m,basket in [(0.24,120),(0.24,100)]:
    req_day=FIXED_CASH/m/30
    txns=req_day/basket
    print(f"  break-even at {m*100:.0f}% margin, basket {php(basket)}: need {txns:.0f} txns/day "
          f"= {txns/1800*100:.1f}% of passersby")

# ---- THREE SCENARIOS for SukiMart monthly profit (after ALL costs incl salary) ----
print("\n"+"="*64,"\nSUKIMART SCENARIOS — net cash after all fixed costs (salary already inside)")
def scn(label,txns,basket,margin):
    sales=txns*basket*30; gp=sales*margin; net=gp-FIXED_CASH
    print(f"  [{label:11}] {txns} txns x {php(basket)} x30 = {php(sales)}/mo | GP@{margin*100:.0f}% {php(gp)} "
          f"| net {php(net)}/mo")
    return net
scn("Pessimistic",150,100,0.22)   # location underperforms
scn("Base",       200,120,0.24)   # plausible mid
scn("Optimistic", 280,130,0.25)   # strong capture + good mix

# ---- AI WHERE IT EARNS ITS PLACE: perishable spoilage forecasting ----
print("\n"+"="*64,"\nAI PAYBACK — perishable spoilage forecasting (the defensible use)")
PERISH_SHARE=0.20      # ready-to-eat + chilled ~20% of a convenience store's sales
for store_sales in (600_000,720_000):
    perish=store_sales*PERISH_SHARE
    loss_now=perish*0.16      # backtested gut-feel baseline: 16% spoilage
    loss_fixed=perish*0.09    # Smart-Prep profit-optimal: 9%
    saved=loss_now-loss_fixed
    print(f"  store {php(store_sales)}/mo -> perishable {php(perish)} | spoilage 16%->9% saves "
          f"{php(saved)}/mo = {php(saved*12)}/yr")
print("  Cost: built into POS software (~PHP 4,000/mo, already in Exhibit D). Specific, costed, payback-positive.")
