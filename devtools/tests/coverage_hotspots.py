from __future__ import annotations
import argparse
from coverage_utils import load_json, file_rows

parser = argparse.ArgumentParser(description="Show files with the lowest coverage.")
parser.add_argument("--top", type=int, default=15)
parser.add_argument("--package", default="molsysmt")
parser.add_argument("--subpackage", default=None)
args = parser.parse_args()

data = load_json("coverage.json")
rows = file_rows(data, package_root=args.package, subpackage=args.subpackage)
rows.sort(key=lambda x: (-x["missing"], x["percent"], x["path"]))

print("\nFiles with most uncovered lines\n")
print(f"{'Cover':>7}  {'Stmts':>7}  {'Miss':>7}  File")
print("-" * 110)
for row in rows[:args.top]:
    print(f"{row['percent']:6.1f}%  {row['statements']:7d}  {row['missing']:7d}  {row['path']}")
