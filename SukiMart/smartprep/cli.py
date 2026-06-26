"""
SukiMart Smart-Prep — command-line entry point.
  forecast : tomorrow's prep list + backtest + writes Morning Prep Dashboard  (= run.main)
  backtest : print ONLY the rolling backtest metrics (accuracy/spoilage/profit uplift)
  data     : (re)generate the illustrative sample data and print where it landed
Run from repo root, e.g.:  ./.venv/bin/python SukiMart/smartprep/cli.py forecast
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # let siblings import by bare name
import argparse


def cmd_forecast(_args):
    """Full end-to-end run: prep list + backtest + report file (delegates to run.main)."""
    import run
    run.main()


def cmd_backtest(_args):
    """Load data like run.py, then print just the backtest KPIs (no report written)."""
    import backtest, run
    items, series, dows, _tdow = run.load()
    s = backtest.run(items, series, dows)
    print("BACKTEST (rolling one-step-ahead, gut-feel vs forecast+newsvendor):")
    print(f"  forecast accuracy  : WAPE {s['wape']*100:.0f}%   |   service level {s['service_level']*100:.0f}%")
    print(f"  spoilage           : {s['spoil_gut']*100:.0f}% (gut-feel)  ->  {s['spoil_sys']*100:.0f}% (Smart-Prep)")
    print(f"  PROFIT UPLIFT      : PHP {s['uplift_month']:,.0f}/mo  =  PHP {s['uplift_year_staged']:,.0f}/yr (staged)")
    print(f"                       PHP {s['uplift_year_full']:,.0f}/yr at full SukiMart")


def cmd_data(_args):
    """Regenerate items.csv / calendar.csv / sample_sales.csv into the data dir."""
    import datagen
    where = datagen.generate()
    print(f"Wrote sample data to {where}")


def build_parser():
    p = argparse.ArgumentParser(
        prog="cli.py", description="SukiMart Smart-Prep — perishable demand forecast + newsvendor prep.")
    sub = p.add_subparsers(dest="command", metavar="{forecast,backtest,data}")
    sub.add_parser("forecast", help="tomorrow's prep list + backtest + write report").set_defaults(func=cmd_forecast)
    sub.add_parser("backtest", help="print only the backtest metrics").set_defaults(func=cmd_backtest)
    sub.add_parser("data", help="(re)generate sample data and print path").set_defaults(func=cmd_data)
    return p


def main(argv=None):
    p = build_parser()
    args = p.parse_args(argv)
    if not getattr(args, "func", None):  # no subcommand -> show usage (like -h)
        p.print_help(); return 1
    args.func(args)
    return 0


if __name__ == "__main__":
    # ---- self-test: exercise the parser + 'data' command on synthetic data, no external state needed ----
    if len(sys.argv) > 1:
        sys.exit(main())
    print("[self-test] building parser..."); build_parser()  # parser constructs without error
    rc = main(["data"])                                       # data cmd: regenerates sample data
    assert rc == 0, "data command should return 0"
    rc = main([])                                             # no args -> usage + nonzero
    assert rc == 1, "no-command should return 1"
    print("[self-test] OK")
