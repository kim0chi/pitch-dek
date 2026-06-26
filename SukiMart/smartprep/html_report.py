"""
Phone-friendly single-file Morning Prep report (Tina opens it on her phone).
Mobile-first HTML with inline CSS (no external assets, no JS) so it renders the
same on any phone and can be shared as a file or message attachment.
Layout: header -> 3 big tap-friendly KPI cards -> prep table (Item / PREPARE / why).
"""
import os, html, datetime as dt
from config import HERE

# Warm theme
CREAM="#FBF7F0"; NAVY="#1F3864"; GREEN="#2E8B57"; GOLD="#E8A33D"
INK="#1F2421"; GREY="#8A8079"; CARD="#FFFFFF"; LINE="#EADFCF"


def _esc(v):
    return html.escape(str(v))


def write_html(recs, summary, target_dow, out=None):
    """Write the mobile-first morning report; return the file path.
    recs: list of dict(name,prep,forecast,why,method)
    summary: dict(uplift_month,spoil_gut,spoil_sys,wape,service_level)
    """
    out = out or os.path.join(HERE, "morning_report.html")
    today = dt.date.today().strftime("%a %d %b %Y")

    # --- 3 KPI cards (big numbers, tap-friendly) ---
    cards = [
        ("Items to prep", f"{len(recs)}", "today's list", NAVY),
        ("Saved / month", f"PHP {summary['uplift_month']:,.0f}", "vs gut-feel prep", GREEN),
        ("Spoilage", f"{summary['spoil_gut']*100:.0f}% &rarr; {summary['spoil_sys']*100:.0f}%", "gut &rarr; Smart-Prep", GOLD),
    ]
    kpi_html = "\n".join(
        f'''      <div class="kpi" style="border-top:6px solid {col}">
        <div class="kpi-label">{_esc(lab)}</div>
        <div class="kpi-value" style="color:{col}">{val}</div>
        <div class="kpi-sub">{sub}</div>
      </div>''' for (lab, val, sub, col) in cards)

    # --- prep rows (big PREPARE number is the load-bearing cell) ---
    rows_html = "\n".join(
        f'''      <tr>
        <td class="item">{_esc(r["name"])}<div class="meta">forecast {_esc(r["forecast"])} &middot; {_esc(r["method"])}</div></td>
        <td class="prep">{_esc(r["prep"])}</td>
        <td class="why">{_esc(r["why"])}</td>
      </tr>''' for r in recs)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>SukiMart &middot; Morning Prep</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:{CREAM};color:{INK};font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
       -webkit-text-size-adjust:100%;line-height:1.4}}
  .wrap{{max-width:520px;margin:0 auto;padding:16px 14px 40px}}
  /* header */
  header{{background:{NAVY};color:#fff;border-radius:18px;padding:18px 18px 16px;margin-bottom:16px}}
  header .brand{{font-size:13px;letter-spacing:.14em;text-transform:uppercase;opacity:.8}}
  header h1{{font-size:24px;margin:4px 0 6px;font-weight:800}}
  header .sub{{font-size:14px;opacity:.92}}
  header .when{{font-size:12px;opacity:.7;margin-top:6px}}
  .pill{{display:inline-block;background:{GOLD};color:{NAVY};font-weight:800;border-radius:999px;
        padding:3px 12px;font-size:14px}}
  /* KPI cards: stack on phones, 3-across when wide */
  .kpis{{display:grid;grid-template-columns:1fr;gap:12px;margin-bottom:20px}}
  @media(min-width:480px){{.kpis{{grid-template-columns:1fr 1fr 1fr}}}}
  .kpi{{background:{CARD};border-radius:16px;padding:16px 16px 14px;
       box-shadow:0 1px 3px rgba(31,36,33,.10);min-height:96px}}
  .kpi-label{{font-size:13px;color:{GREY};font-weight:600;text-transform:uppercase;letter-spacing:.04em}}
  .kpi-value{{font-size:30px;font-weight:800;margin:4px 0 2px;line-height:1.1}}
  .kpi-sub{{font-size:12px;color:{GREY}}}
  /* prep table */
  .section{{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:{NAVY};
           font-weight:800;margin:4px 4px 8px}}
  table{{width:100%;border-collapse:separate;border-spacing:0;background:{CARD};
        border-radius:16px;overflow:hidden;box-shadow:0 1px 3px rgba(31,36,33,.10)}}
  thead th{{background:{NAVY};color:#fff;font-size:12px;text-align:left;
           padding:11px 12px;text-transform:uppercase;letter-spacing:.05em}}
  thead th.c{{text-align:center}}
  tbody td{{padding:14px 12px;border-top:1px solid {LINE};vertical-align:middle}}
  tbody tr:first-child td{{border-top:none}}
  .item{{font-size:16px;font-weight:700}}
  .item .meta{{font-size:12px;color:{GREY};font-weight:500;margin-top:3px}}
  .prep{{text-align:center;font-size:30px;font-weight:800;color:{GREEN};white-space:nowrap;width:78px}}
  .why{{font-size:13px;color:{INK};width:38%}}
  /* footer note */
  .note{{margin-top:18px;background:{CARD};border-left:5px solid {GREEN};border-radius:12px;
        padding:13px 15px;font-size:13px;color:{INK};box-shadow:0 1px 3px rgba(31,36,33,.08)}}
  .note b{{color:{NAVY}}}
  .foot{{text-align:center;color:{GREY};font-size:11px;margin-top:16px}}
</style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="brand">SukiMart &middot; Smart-Prep</div>
      <h1>Morning Prep</h1>
      <div class="sub">Tomorrow is <span class="pill">{_esc(target_dow)}</span> &mdash; prepare this much, and no more.</div>
      <div class="when">System recommends &middot; Tina decides &middot; {today}</div>
    </header>

    <div class="kpis">
{kpi_html}
    </div>

    <div class="section">Today's prep list</div>
    <table>
      <thead>
        <tr><th>Item</th><th class="c">Prepare</th><th>Why</th></tr>
      </thead>
      <tbody>
{rows_html}
      </tbody>
    </table>

    <div class="note">
      <b>Cook to the forecast, not to a guess.</b><br>
      Backtest: forecast accuracy {summary['wape']*100:.0f}% WAPE &middot;
      service level {summary['service_level']*100:.0f}% (rarely sold out).
    </div>
    <div class="foot">SukiMart Smart-Prep &middot; perishable demand forecasting + newsvendor prep</div>
  </div>
</body>
</html>
"""
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    return out


if __name__ == "__main__":
    # self-test: synthetic recs + summary -> write file, assert key content present
    recs = [
        dict(name="Siomai (4pc)", prep=31, forecast=27, why="prep MORE — high margin", method="holt-winters"),
        dict(name="Hot coffee",   prep=33, forecast=30, why="prep MORE — high margin", method="holt-winters"),
        dict(name="Pandesal (pc)",prep=38, forecast=41, why="prep LESS — spoils cheap", method="seasonal-baseline"),
    ]
    summary = dict(uplift_month=8420.0, spoil_gut=0.18, spoil_sys=0.06,
                   wape=0.12, service_level=0.94)
    p = write_html(recs, summary, "Sat", out=os.path.join(HERE, "morning_report.html"))
    htmltxt = open(p, encoding="utf-8").read()
    assert "<html" in htmltxt, "missing <html"
    for r in recs:
        assert r["name"] in htmltxt, f"missing SKU name {r['name']}"
    assert "PHP 8,420" in htmltxt and "Sat" in htmltxt, "missing KPI/dow content"
    print("self-test OK ->", p, "|", len(htmltxt), "bytes")
