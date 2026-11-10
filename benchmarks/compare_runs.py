"""Benchmark Regression Comparer.

This command-line script compares a current benchmarking JSON output against a reference baseline JSON.
Timing differences are advisory: a slow scientifically correct implementation
remains available. Invalid evidence retains a nonzero diagnostic exit code.
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
        Advisory relative slowdown threshold; 0.15 represents 15 percent.

    Returns
    -------
    int
        Diagnostic exit code: 0 for a numeric report, including slowdown warnings;
        1 for invalid or incomplete evidence. Neither restricts a public tool.

    Notes
    -----
    Empty/malformed data, missing reference measurements and invalid medians
    or thresholds fail before numerical comparison. This does not establish
    environment/workload comparability; that separate #567 review remains open.
    The default advisory threshold remains 15 percent for product and third-party
    timings. A numeric observation alone neither attributes a product regression
    nor validates comparability. Confirmed, comparable product slowdowns should
    be tracked in an improvement issue, without restricting a correct tool.
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
    print(f" Advisory Threshold: {threshold * 100:.1f}%")
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
        print("\nWARNING: TIMING DIFFERENCES EXCEED THE ADVISORY THRESHOLD.")
        print(
            "The following recorded timings are slower; comparability is not established:"
        )
        for reg in regressions:
            print(f"  ⚠️ {reg}")
        print("Review equivalent workloads, environment and repeated measurements.")
        print(
            "Track confirmed product inefficiency in an improvement issue; do not restrict a correct tool."
        )
        print("======================================================================")
        return 0

    print("\n======================================================================")
    print("  OBSERVATION: Matched recorded timings meet the advisory threshold.")
    print("  This does not establish workload/environment comparability.")
    print("  New paths without a reference remain unassessed.")
    print("======================================================================")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Report advisory timing differences without restricting correct tools."
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
        help="Advisory slowdown ratio threshold (e.g. 0.15)",
    )
    args = parser.parse_args()

    sys.exit(compare_baselines(args.baseline, args.current, args.threshold))
