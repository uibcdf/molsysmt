from __future__ import annotations
import argparse
from coverage_utils import load_json, file_rows, aggregate_by_package, sort_packages, bar, grade

parser = argparse.ArgumentParser(description="Print a hierarchical coverage map.")
parser.add_argument("--root", default="molsysmt")
parser.add_argument("--max-depth", type=int, default=2)
parser.add_argument("--sort", choices=["coverage", "name"], default="coverage")
parser.add_argument("--subpackage", default=None)
args = parser.parse_args()

data = load_json("coverage.json")
rows = file_rows(data, package_root=args.root, subpackage=args.subpackage)

print("\nCoverage map\n")
for depth in range(1, args.max_depth + 1):
    packages = aggregate_by_package(rows, root=args.root, depth=depth)
    packages = sort_packages(packages, mode=args.sort)
    if not packages:
        continue
    print(f"Depth {depth}")
    print("-" * 96)
    for row in packages:
        indent = "  " * max(0, row["package"].count(".") - 1)
        print(f"{indent}{row['package']:<46}  {bar(row['percent'], 18)}  {row['percent']:6.1f}%  [{grade(row['percent'])}]")
    print()
