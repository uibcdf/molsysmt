"""Benchmark Regression Comparer.

This command-line script compares a current benchmarking JSON output against a reference baseline JSON.
It enforces the 15% performance regression threshold, exiting with a non-zero code if the threshold is violated.
"""

from __future__ import annotations

import argparse
import json
import math
import sys


def _validated_results(data, label):
    """Require actual finite positive timing records before comparing ratios."""
    if not isinstance(data, dict):
        raise ValueError(f"{label} must be a JSON object.")
    results = data.get("results")
    if not isinstance(results, dict) or not results:
        raise ValueError(f"{label} must contain nonempty results.")
    for name, entry in results.items():
        if not isinstance(name, str) or not name.strip() or not isinstance(entry, dict):
            raise ValueError(f"{label} contains an invalid benchmark record.")
        value = entry.get("median_seconds")
        try:
            valid = (
                not isinstance(value, bool)
                and isinstance(value, (int, float))
                and math.isfinite(value)
                and value > 0
            )
        except OverflowError:
            valid = False
        if not valid:
            raise ValueError(
                f"{label} benchmark {name!r} requires finite positive median_seconds."
            )
    return results


def compare_baselines(
    baseline_path: str, current_path: str, threshold: float = 0.15
) -> int:
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

    Notes
    -----
    Empty/malformed data, missing reference measurements and invalid medians
    or thresholds fail before numerical comparison. This does not establish
    environment/workload comparability; that separate #567 review remains open.
    Existing matched third-party measurements retain their blocking role and
    the default threshold remains 15 percent.
    """
    try:
        with open(baseline_path, "r", encoding="utf-8") as f:
            baseline_data = json.load(f)
    except (OSError, ValueError, TypeError) as e:
        print(f"❌ Error loading baseline JSON from {baseline_path}: {e}")
        return 1

    try:
        with open(current_path, "r", encoding="utf-8") as f:
            current_data = json.load(f)
    except (OSError, ValueError, TypeError) as e:
        print(f"❌ Error loading current JSON from {current_path}: {e}")
        return 1

    try:
        if (
            isinstance(threshold, bool)
            or not isinstance(threshold, (int, float))
            or not math.isfinite(threshold)
            or threshold < 0
        ):
            raise ValueError("The threshold must be finite and nonnegative.")
        base_results = _validated_results(baseline_data, "Reference baseline")
        curr_results = _validated_results(current_data, "Current run")
        missing = sorted(set(base_results) - set(curr_results))
        if missing:
            raise ValueError(
                f"Current run is missing reference measurements: {missing}"
            )
    except (ValueError, OverflowError) as e:
        print(f"Invalid benchmark comparison: {e}")
        return 1

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
            print(
                f"ℹ️ New benchmark '{name}': median = {curr_entry['median_seconds'] * 1e6:.2f} μs (No baseline reference)"
            )
            continue

        base_entry = base_results[name]
        base_median = base_entry["median_seconds"]
        curr_median = curr_entry["median_seconds"]

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
    print("  PASS: Matched recorded timings meet the numeric threshold.")
    print("  New paths without a reference remain unassessed.")
    print("======================================================================")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Enforce benchmarking regression limits."
    )
    parser.add_argument(
        "--baseline", required=True, help="Path to reference baseline JSON"
    )
    parser.add_argument(
        "--current", required=True, help="Path to current benchmark session JSON"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.15,
        help="Regression ratio threshold (e.g. 0.15)",
    )
    args = parser.parse_args()

    sys.exit(compare_baselines(args.baseline, args.current, args.threshold))
