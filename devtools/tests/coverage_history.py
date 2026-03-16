from __future__ import annotations
import argparse, os
from datetime import datetime, timezone
from coverage_utils import load_json, dump_json

def append_record(summary_json: str, history_path: str):
    summary = load_json(summary_json)
    history = {"records": []}
    if os.path.exists(history_path):
        history = load_json(history_path)

    record = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "generated_at_utc": summary.get("generated_at_utc"),
        "package_root": summary.get("package_root"),
        "subpackage_filter": summary.get("subpackage_filter"),
        "overall_percent": summary["overall"]["percent"],
        "files": summary["overall"]["files"],
        "statements": summary["overall"]["statements"],
        "missing": summary["overall"]["missing"],
        "top_level_packages": [{"package": r["package"], "percent": r["percent"]} for r in summary.get("top_level_packages", [])],
        "packages": [{"package": r["package"], "percent": r["percent"]} for r in summary.get("packages", [])],
    }
    history.setdefault("records", []).append(record)
    dump_json(history_path, history)
    print(f"Appended record to {history_path}")

def report(history_path: str, last: int = 10):
    if not os.path.exists(history_path):
        raise SystemExit(f"History file not found: {history_path}")
    history = load_json(history_path)
    records = history.get("records", [])
    if not records:
        print("History file exists but has no records.")
        return
    records = records[-last:]
    print("\nCoverage history\n")
    print(f"{'Recorded at':<28}  {'Overall':>8}  {'Files':>7}  {'Statements':>10}  {'Missing':>8}")
    print("-" * 88)
    for rec in records:
        print(f"{rec['recorded_at_utc']:<28}  {rec['overall_percent']:7.1f}%  {rec['files']:7d}  {rec['statements']:10d}  {rec['missing']:8d}")

parser = argparse.ArgumentParser(description="Maintain coverage history.")
sub = parser.add_subparsers(dest="command", required=True)
p1 = sub.add_parser("append")
p1.add_argument("--summary-json", required=True)
p1.add_argument("--history", required=True)
p2 = sub.add_parser("report")
p2.add_argument("--history", required=True)
p2.add_argument("--last", type=int, default=10)
args = parser.parse_args()

if args.command == "append":
    append_record(args.summary_json, args.history)
else:
    report(args.history, args.last)
