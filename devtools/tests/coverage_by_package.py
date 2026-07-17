from __future__ import annotations

import argparse

from coverage_utils import load_json, file_rows, aggregate_by_package, sort_packages


def main(argv=None):
    """Print package-level coverage aggregated from coverage.json."""
    parser = argparse.ArgumentParser(description="Aggregate coverage by package.")
    parser.add_argument("--root", default="molsysmt")
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--subpackage", default=None)
    args = parser.parse_args(argv)

    data = load_json("coverage.json")
    rows = file_rows(data, package_root=args.root, subpackage=args.subpackage)
    packages = sort_packages(
        aggregate_by_package(rows, root=args.root, depth=args.depth),
        mode="coverage",
    )

    print("\nCoverage by package\n")
    print(f"{'Cover':>7}  {'Stmts':>7}  {'Miss':>7}  {'Files':>7}  Package")
    print("-" * 110)
    for row in packages:
        print(
            f"{row['percent']:6.1f}%  {row['statements']:7d}  "
            f"{row['missing']:7d}  {row['files']:7d}  {row['package']}"
        )


if __name__ == "__main__":
    main()
