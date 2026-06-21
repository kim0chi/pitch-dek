"""
PopCart PH — DARK-THEME visual pack (cohesion with the dark deck).
Transparent backgrounds so visuals sit on the slide. Run: .venv/bin/python generate_visuals.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, FancyArrowPatch, Rectangle, Ellipse

os.makedirs("assets", exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans"})

TITLE="#FFFFFF"; LIME="#C3F53C"; INK="#E6E6E6"; MUTE="#9AA0A6"
SLATE="#16212E"; SLATE2="#24303F"; GREEN="#2ECC71"; RED="#E74C3C"
ORANGE="#F39C12"; SKY="#5B9BD5"; GOLD="#F1C40F"

def newfig(w=10,h=5.6):
    fig,ax=plt.subplots(figsize=(w,h)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    fig.patch.set_alpha(0); ax.patch.set_alpha(0); return fig,ax
def axfig(w=10,h=5.2):
    fig,ax=plt.subplots(figsize=(w,h)); fig.patch.set_alpha(0); ax.patch.set_alpha(0); return fig,ax
def card(ax,x,y,w,h,fc=SLATE,ec=None,lw=2,rad=0.03):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={rad}",fc=fc,ec=ec or fc,lw=lw))
def title(ax,t,sub=None,accent=LIME):
    ax.text(0.5,0.95,t,ha="center",va="top",fontsize=20,fontweight="bold",color=TITLE)
    if sub: ax.text(0.5,0.85,sub,ha="center",va="top",fontsize=12,color=MUTE,style="italic")
def arrow(ax,p1,p2,color=LIME,lw=2.5,mut=22):
    ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",mutation_scale=mut,color=color,lw=lw,shrinkA=0,shrinkB=0))
def save(fig,name):
    fig.savefig(f"assets/{name}",dpi=200,bbox_inches="tight",pad_inches=0.18,transparent=True)
    plt.close(fig); print("  "+name)

print("Generating DARK visuals...")

# 1) LEAK BUCKET ----------------------------------------------------------
fig,ax=newfig(10,5.8)
title(ax,"The leak you can't see")
ax.add_patch(Polygon([(0.28,0.66),(0.60,0.66),(0.535,0.30),(0.345,0.30)],closed=True,fc=SLATE2,ec=SKY,lw=3))
ax.add_patch(Polygon([(0.29,0.62),(0.59,0.62),(0.535,0.31),(0.345,0.31)],closed=True,fc=SKY,ec="none",alpha=0.55))
ax.add_patch(Ellipse((0.44,0.66),0.32,0.05,fc=SLATE2,ec=SKY,lw=3))
ax.text(0.44,0.49,"PROFIT\n₱10.8M kept",ha="center",va="center",fontsize=12,fontweight="bold",color=TITLE)
ax.add_patch(Circle((0.535,0.40),0.013,fc="#0A0A0A",ec=RED,lw=1.5))
for dx,dy in [(0.575,0.36),(0.62,0.31),(0.665,0.26),(0.71,0.22)]:
    ax.add_patch(Ellipse((dx,dy),0.018,0.030,fc=RED,ec="none",alpha=0.9))
ax.add_patch(Ellipse((0.79,0.18),0.24,0.055,fc=RED,ec="none",alpha=0.35))
ax.text(0.79,0.18,"₱7.35M/yr lost",ha="center",va="center",fontsize=13,fontweight="bold",color=RED)
card(ax,0.63,0.55,0.33,0.16,SLATE,ec=LIME,lw=2,rad=0.04)
ax.text(0.795,0.63,"= 68% of net profit\nleaking every year",ha="center",va="center",fontsize=12.5,fontweight="bold",color=TITLE)
ax.text(0.5,0.10,'"You see the empty shelf — never the pesos walking out the door."',ha="center",fontsize=12.5,style="italic",color=LIME)
save(fig,"01_leak_bucket.png")

# 2) LOST PROFIT BY SKU ---------------------------------------------------
fig,ax=axfig(10,5.2)
sk=["Freeze-Dried\nCandy","Spicy Korean\nRamen","Chocolate\nCrunch","Giant Bubble\nGum","Sour Belts"]
gp=[3.56,2.30,1.01,0.48,0.0]; cols=[RED if v==max(gp) else SKY for v in gp]
ax.barh(sk[::-1],gp[::-1],color=cols[::-1],edgecolor="none",height=0.62)
for i,v in enumerate(gp[::-1]):
    ax.text(v+0.06,i,f"₱{v:.2f}M" if v>0 else "₱0 (never out)",va="center",fontsize=11,fontweight="bold",color=RED if v==max(gp) else INK)
ax.set_xlim(0,4.2); ax.set_xlabel("Gross profit lost to stockouts per year (₱M)",fontsize=11,color=MUTE)
ax.set_title("One product is half the problem",fontsize=18,fontweight="bold",color=TITLE,loc="left",pad=12)
ax.text(0,1.04,"Total ₱7.35M/yr — freeze-dried candy alone is ₱3.56M",transform=ax.transAxes,fontsize=11,color=MUTE)
ax.tick_params(colors=INK,length=0); [s.set_visible(False) for s in ax.spines.values()]
ax.xaxis.label.set_color(MUTE); ax.set_axisbelow(True); ax.xaxis.grid(True,color="#2A2A2A")
for lab in ax.get_yticklabels(): lab.set_color(INK)
for lab in ax.get_xticklabels(): lab.set_color(MUTE)
save(fig,"02_lost_profit_by_sku.png")

# 3) ASYMMETRY ------------------------------------------------------------
fig,ax=axfig(10,5.4)
opts=["Fix Operations\nFirst","Cebu Hub\n(owned)","Mall\nKiosk"]
worst=[0.20,-6.88,-2.52]; best=[3.51,1.00,3.00]; base=[0.97,-3.96,0.12]; yp=[2,1,0]
ax.axvspan(-7.8,0,color=RED,alpha=0.10)
for y,w,bst,bs in zip(yp,worst,best,base):
    if w<0:
        ax.barh(y,-w,left=w,height=0.5,color=RED,edgecolor="none")
        ax.barh(y,bst,left=0,height=0.5,color=GREEN,edgecolor="none")
    else:
        ax.barh(y,bst-w,left=w,height=0.5,color=GREEN,edgecolor="none")
    ax.plot([bs,bs],[y-0.28,y+0.28],color=TITLE,lw=3)
    ax.text(w-0.15,y,f"{w:+.1f}",va="center",ha="right",fontsize=10.5,fontweight="bold",color=INK)
    ax.text(bst+0.15,y,f"{bst:+.1f}",va="center",ha="left",fontsize=10.5,fontweight="bold",color=INK)
ax.axvline(0,color=TITLE,lw=1.5)
ax.set_yticks(yp); ax.set_yticklabels(opts,fontsize=12,fontweight="bold")
ax.set_xlim(-7.9,4.5); ax.set_xlabel("Recurring net profit / year — worst → best case (₱M)",fontsize=11,color=MUTE)
ax.set_title("Only one option keeps a positive recurring floor",fontsize=17,fontweight="bold",color=TITLE,loc="left",pad=24)
ax.text(0,1.10,'"On a 9% margin, you don\'t bet the rent on lotto."   ▪ white tick = base case',transform=ax.transAxes,fontsize=10.5,color=MUTE,style="italic")
ax.text(-3.8,-0.64,"loses money",ha="center",fontsize=10,color=RED,fontweight="bold")
ax.text(2.1,-0.64,"makes money",ha="center",fontsize=10,color=GREEN,fontweight="bold")
[s.set_visible(False) for s in ax.spines.values()]; ax.tick_params(colors=INK,length=0)
for lab in ax.get_yticklabels(): lab.set_color(INK)
for lab in ax.get_xticklabels(): lab.set_color(MUTE)
save(fig,"03_asymmetry.png")

# 4) GRAB vs CAR ----------------------------------------------------------
fig,ax=newfig(10,5.4)
title(ax,"Buying a car vs taking Grab")
card(ax,0.05,0.16,0.42,0.58,SLATE,ec=RED,lw=2.5,rad=0.04)
ax.text(0.26,0.68,"OWNED HUB = buy a car",ha="center",fontsize=13,fontweight="bold",color=RED)
ax.add_patch(FancyBboxPatch((0.13,0.45),0.26,0.10,boxstyle="round,pad=0,rounding_size=0.03",fc=RED,ec="none"))
ax.add_patch(Polygon([(0.17,0.55),(0.22,0.62),(0.31,0.62),(0.35,0.55)],closed=True,fc=RED,ec="none"))
ax.add_patch(Circle((0.18,0.44),0.028,fc=TITLE)); ax.add_patch(Circle((0.34,0.44),0.028,fc=TITLE))
ax.text(0.26,0.33,"₱9M/year whether\nyou drive or not (fixed)",ha="center",fontsize=11.5,color=INK)
ax.text(0.26,0.225,"worst case −₱6.9M",ha="center",fontsize=11,fontweight="bold",color=RED)
card(ax,0.53,0.16,0.42,0.58,SLATE,ec=GREEN,lw=2.5,rad=0.04)
ax.text(0.74,0.68,"3PL = take Grab",ha="center",fontsize=13,fontweight="bold",color=GREEN)
ax.add_patch(FancyBboxPatch((0.66,0.43),0.16,0.18,boxstyle="round,pad=0,rounding_size=0.02",fc=SLATE2,ec=GREEN,lw=2.5))
ax.text(0.74,0.52,"₱/ride",ha="center",fontsize=12,fontweight="bold",color=GREEN)
ax.text(0.74,0.33,"pay only when\nyou ship (variable)",ha="center",fontsize=11.5,color=INK)
ax.text(0.74,0.225,"start here, scale safely",ha="center",fontsize=11,fontweight="bold",color=GREEN)
ax.text(0.5,0.07,'"Don\'t know how far you\'ll drive? Take Grab first — then buy the car."',ha="center",fontsize=12,style="italic",color=LIME)
save(fig,"04_grab_vs_car.png")

# 5) SAWTOOTH -------------------------------------------------------------
fig,ax=axfig(10,5.2)
xs=[0,6,9,9,15,18,18,22]; ys=[12,6,3,12,6,3,12,8]
ax.axhspan(0,2,color=RED,alpha=0.16)
ax.plot(xs,ys,color=SKY,lw=3,solid_capstyle="round",solid_joinstyle="round")
ax.axhline(6,color=GOLD,lw=2.5,ls="--")
ax.text(0.3,6.4,"REORDER POINT  (the low-fuel light)",fontsize=11,fontweight="bold",color=GOLD)
ax.text(0.3,0.75,"stockout danger zone",fontsize=10.5,fontweight="bold",color=RED)
ax.annotate("reorder fires —\nshelf still stocked",xy=(6,6),xytext=(2.4,9.8),fontsize=10,color=TITLE,fontweight="bold",ha="center",arrowprops=dict(arrowstyle="-|>",color=TITLE,lw=2))
ax.annotate("stock arrives with\nbuffer to spare",xy=(9,3),xytext=(12.6,2.4),fontsize=10,color=GREEN,fontweight="bold",ha="center",arrowprops=dict(arrowstyle="-|>",color=GREEN,lw=2))
ax.set_ylim(0,14); ax.set_xlim(0,22)
ax.set_title("Reorder before the shelf is empty — not after",fontsize=18,fontweight="bold",color=TITLE,loc="left",pad=12)
ax.text(0,1.04,"Old way: reorder only when it looks empty — fatal with a 14–30 day restock.",transform=ax.transAxes,fontsize=10.5,color=MUTE)
ax.set_xlabel("days",fontsize=10,color=MUTE); ax.set_yticks([])
[s.set_visible(False) for s in ax.spines.values()]; ax.tick_params(colors=MUTE,length=0)
for lab in ax.get_xticklabels(): lab.set_color(MUTE)
save(fig,"05_inventory_sawtooth.png")

# 6) CONTRIBUTION WATERFALL ----------------------------------------------
fig,ax=axfig(10,5.2)
labels=["Price\n₱180","− Cost of\ngoods ₱90","− TikTok\nfee ₱9","− Shipping\n₱27","Take-home\n₱54"]
starts=[0,90,81,54,0]; heights=[180,90,9,27,54]; cols=[SKY,RED,RED,RED,GREEN]
for i,(s,h,c) in enumerate(zip(starts,heights,cols)):
    ax.bar(i,h,bottom=s,color=c,edgecolor="none",width=0.62,alpha=0.92)
    if i in(1,2,3): ax.text(i,s+h+4,f"−₱{h}",ha="center",fontsize=10.5,color=RED,fontweight="bold")
ax.text(0,184,"₱180",ha="center",fontsize=11,fontweight="bold",color=TITLE)
ax.text(4,58,"₱54",ha="center",fontsize=12,fontweight="bold",color=GREEN)
for i in range(4):
    yc=[180,90,81,54][i]; ax.plot([i+0.31,i+1-0.31],[yc,yc],color=MUTE,lw=1,ls="--")
ax.set_xticks(range(5)); ax.set_xticklabels(labels,fontsize=10.5)
ax.set_ylim(0,200); ax.set_yticks([])
ax.set_title("Gross salary vs take-home pay",fontsize=18,fontweight="bold",color=TITLE,loc="left",pad=12)
ax.text(0,1.04,"A ₱180 candy keeps ~₱54 after fees & shipping — we size recovery on take-home (30%), not gross (50%)",transform=ax.transAxes,fontsize=10.3,color=MUTE)
[s.set_visible(False) for s in ax.spines.values()]; ax.tick_params(colors=INK,length=0)
for lab in ax.get_xticklabels(): lab.set_color(INK)
save(fig,"06_contribution_waterfall.png")

# 7) PAYBACK SENSITIVITY --------------------------------------------------
fig,ax=axfig(10,5.0)
cm=["20%\n(harsh)","30%\n(base)","40%\n(realistic)","50%\n(full gross)"]; pb=[51,20,13,11]
cols=[MUTE,LIME,GREEN,GREEN]
ax.bar(cm,pb,color=cols,edgecolor="none",width=0.6)
for i,v in enumerate(pb): ax.text(i,v+1.2,f"{v} mo",ha="center",fontsize=11.5,fontweight="bold",color=cols[i])
ax.axhline(12,color=RED,lw=2,ls="--"); ax.text(3.4,13.6,"12-mo line",color=RED,fontsize=10,ha="right")
ax.set_ylim(0,56); ax.set_ylabel("Calendar payback (months)",fontsize=11,color=MUTE)
ax.set_title("Payback changes with the money left from each recovered sale",fontsize=15,fontweight="bold",color=TITLE,loc="left",pad=12)
ax.text(0,1.04,"Recovery held at 42.5%. Year 1 is an investment year (−₱0.67M); positive thereafter.",transform=ax.transAxes,fontsize=10.5,color=MUTE)
[s.set_visible(False) for s in ["top","right"] if ax.spines[s].set_visible(False)]
for s in ["top","right"]: ax.spines[s].set_visible(False)
for s in ["left","bottom"]: ax.spines[s].set_color("#3A3A3A")
ax.tick_params(colors=MUTE,length=0); ax.set_axisbelow(True); ax.yaxis.grid(True,color="#2A2A2A")
for lab in ax.get_xticklabels(): lab.set_color(INK)
for lab in ax.get_yticklabels(): lab.set_color(MUTE)
ax.yaxis.label.set_color(MUTE)
save(fig,"07_payback_sensitivity.png")

# 8) INVESTMENT TREE ------------------------------------------------------
fig,ax=newfig(10,5.0)
title(ax,"Year 1 you plant. Year 2 you harvest.")
card(ax,0.06,0.18,0.40,0.52,SLATE,ec=GOLD,lw=2,rad=0.04)
ax.text(0.26,0.64,"YEAR 1 — plant",ha="center",fontsize=13,fontweight="bold",color=GOLD)
ax.plot([0.26,0.26],[0.30,0.40],color="#7A5C3A",lw=3)
ax.add_patch(Ellipse((0.235,0.42),0.05,0.04,fc=GREEN)); ax.add_patch(Ellipse((0.285,0.42),0.05,0.04,fc=GREEN))
ax.text(0.26,0.245,"−₱0.67M cash\n(setup + build)",ha="center",fontsize=11.5,fontweight="bold",color=INK)
arrow(ax,(0.47,0.44),(0.55,0.44),color=LIME,lw=3)
card(ax,0.56,0.18,0.40,0.52,SLATE,ec=GREEN,lw=2,rad=0.04)
ax.text(0.76,0.64,"YEAR 2+ — harvest",ha="center",fontsize=13,fontweight="bold",color=GREEN)
ax.plot([0.76,0.76],[0.30,0.45],color="#7A5C3A",lw=4)
ax.add_patch(Circle((0.76,0.50),0.07,fc=GREEN,ec="none"))
for fx,fy in[(0.73,0.50),(0.79,0.50),(0.76,0.54),(0.74,0.47),(0.78,0.47)]: ax.add_patch(Circle((fx,fy),0.012,fc=RED))
ax.text(0.76,0.245,"+₱1.0–1.6M/yr\nevery year after",ha="center",fontsize=11.5,fontweight="bold",color=INK)
save(fig,"08_investment_tree.png")

# 9) RENTED LAND ----------------------------------------------------------
fig,ax=newfig(10,5.2)
title(ax,"Don't build on land you don't own")
card(ax,0.05,0.18,0.52,0.55,SLATE,ec=RED,lw=2.5,rad=0.04)
ax.text(0.31,0.67,"TikTok Shop = rented land",ha="center",fontsize=13,fontweight="bold",color=RED)
ax.add_patch(Rectangle((0.22,0.33),0.18,0.16,fc=SLATE2,ec=RED,lw=2.5))
ax.add_patch(Polygon([(0.20,0.49),(0.31,0.59),(0.42,0.49)],closed=True,fc=RED,ec="none"))
ax.text(0.31,0.26,"landlord can change the rent,\nthe rules, or the locks — overnight",ha="center",fontsize=10.8,color=INK)
card(ax,0.62,0.18,0.33,0.55,SLATE,ec=GREEN,lw=2.5,rad=0.04)
ax.text(0.785,0.67,"Webstore = your lot",ha="center",fontsize=12.5,fontweight="bold",color=GREEN)
ax.add_patch(Rectangle((0.74,0.35),0.09,0.10,fc=SLATE2,ec=GREEN,lw=2.5))
ax.add_patch(Polygon([(0.73,0.45),(0.785,0.51),(0.84,0.45)],closed=True,fc=GREEN,ec="none"))
ax.text(0.785,0.28,"small + cheap,\nbut nobody can\nevict you",ha="center",fontsize=10.8,color=INK)
save(fig,"09_rented_land.png")

print("Done. 9 dark visuals in assets/")
