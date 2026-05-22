"""Benchmark Regression Comparer.

This command-line script compares a current benchmarking JSON output against a reference baseline JSON.
It enforces the 15% performance regression threshold, exiting with a non-zero code if the threshold is violated.
"""

from __future__ import annotations

import argparse
import json
import sys


def compare_baselines(baseline_path: str, current_path: str, threshold: float = 0.15) -> int:
    """Compare a current run against a reference baseline and audit for regressions.

    Parameters
    ----------
    baseline_path : str
        Path to the reference baseline JSON.
    current_path : str
        Path to the current run JSON.
    threshold : float, default=0.15
        Timing regression limit (0.15 represents a 15% slow-down limit).

    Returns
    -------
    int
        Exit code (0 if passes validation, 1 if regressions are detected).
    """
    try:
        with open(baseline_path, "r", encoding="utf-8") as f:
            baseline_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading baseline JSON from {baseline_path}: {e}")
        return 1

    try:
        with open(current_path, "r", encoding="utf-8") as f:
            current_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading current JSON from {current_path}: {e}")
        return 1

    base_results = baseline_data.get("results", {})
    curr_results = current_data.get("results", {})

    if not base_results:
        print(f"⚠️ Warning: Reference baseline has no results key: {baseline_path}")
    if not curr_results:
        print(f"⚠️ Warning: Current run has no results key: {current_path}")

    regressions: list[str] = []
    improvements: list[str] = []
    conforming: list[str] = []

    print("======================================================================")
    print(" MOLSYSMT PERFORMANCE REGRESSION AUDIT")
    print(f" Reference Baseline: {baseline_path}")
    print(f" Current Run:        {current_path}")
    print(f" Allowed Threshold:  {threshold * 100:.1f}%")
    print("======================================================================")

    for name, curr_entry in curr_results.items():
        if name not in base_results:
            print(f"ℹ️ New benchmark '{name}': median = {curr_entry['median_seconds'] * 1e6:.2f} μs (No baseline reference)")
            continue

        base_entry = base_results[name]
        base_median = base_entry["median_seconds"]
        curr_median = curr_entry["median_seconds"]

        if base_median <= 0.0:
            print(f"⚠️ Skipped '{name}': baseline median is 0 or negative.")
            continue

        pct_change = (curr_median - base_median) / base_median
        diff_us = (curr_median - base_median) * 1e6

        status_str = f"{name}: Base {base_median * 1e6:.2f} μs | Curr {curr_median * 1e6:.2f} μs | Change {pct_change * 100:+.2f}% ({diff_us:+.2f} μs)"

        if pct_change > threshold:
            regressions.append(status_str)
        elif pct_change < -threshold:
            improvements.append(status_str)
        else:
            conforming.append(status_str)

    print("\n--- Conforming Paths ---")
    if conforming:
        for c in conforming:
            print(f"  ✅ {c}")
    else:
        print("  (None)")

    print("\n--- Improved Paths ---")
    if improvements:
        for imp in improvements:
            print(f"  🚀 {imp}")
    else:
        print("  (None)")

    if regressions:
        print("\n❌ PERFORMANCE REGRESSION VIOLATIONS DETECTED!")
        print("The following hot paths degraded beyond the permitted threshold:")
        for reg in regressions:
            print(f"  🔴 {reg}")
        print("======================================================================")
        return 1

    print("\n======================================================================")
    print("  🎉 PASS: All benchmarks conform to the performance target.")
    print("======================================================================")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enforce benchmarking regression limits.")
    parser.add_argument("--baseline", required=True, help="Path to reference baseline JSON")
    parser.add_argument("--current", required=True, help="Path to current benchmark session JSON")
    parser.add_argument("--threshold", type=float, default=0.15, help="Regression ratio threshold (e.g. 0.15)")
    args = parser.parse_args()

    sys.exit(compare_baselines(args.baseline, args.current, args.threshold))
