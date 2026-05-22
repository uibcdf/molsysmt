"""Micro-benchmark for MolSysMT PyUnitWizard Operations.

This script profiles the performance of stripping, checking, and converting physical units.
It compares fast-track pathways against standard parser validation and unit checking.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Add repository root to python path to ensure robust imports
repo_root = str(Path(__file__).resolve().parents[2])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from benchmarks.harness import BenchmarkHarness, save_session_results


def run_unit_benchmarks(output_path: str | None = None) -> list[dict]:
    """Execute the PyUnitWizard physical units micro-benchmarks.

    Parameters
    ----------
    output_path : str, optional
        Absolute path to write the JSON results to.

    Returns
    -------
    list[dict]
        Timing results.
    """
    # 1. Warmup and quantity preparation
    meter_unit = puw.unit("meters")
    q_meters = 1.25 * meter_unit
    q_nanometers = 1250.0 * puw.unit("nm")

    # Benchmarks to execute:
    # A. Fast-track vs Standard Unit parsing
    harness_ft_parse = BenchmarkHarness(
        name="unit_fast_track_parse",
        iterations=1000,
        repeats=5,
    )
    harness_std_parse = BenchmarkHarness(
        name="unit_standard_parse",
        iterations=1000,
        repeats=5,
    )

    # B. Unit stripping (get_value)
    harness_get_value = BenchmarkHarness(
        name="unit_get_value_no_conversion",
        iterations=1000,
        repeats=5,
    )
    harness_get_value_convert = BenchmarkHarness(
        name="unit_get_value_with_conversion",
        iterations=1000,
        repeats=5,
    )

    # C. Dimensionality checking (check)
    harness_check_dim = BenchmarkHarness(
        name="unit_dimensionality_check",
        iterations=1000,
        repeats=5,
    )

    # 2. Run timing suites
    results = []

    # Fast-track parse to nanometers
    res_ft_parse = harness_ft_parse.run(
        warmup_func=lambda: puw.fast_track.to_nanometers(q_nanometers),
        timed_func=lambda: puw.fast_track.to_nanometers(q_nanometers),
    )
    results.append(res_ft_parse)

    # Standard unit parser validation
    res_std_parse = harness_std_parse.run(
        warmup_func=lambda: puw.unit("nanometers"),
        timed_func=lambda: puw.unit("nanometers"),
    )
    results.append(res_std_parse)

    # Get value (raw strip, no unit conversion)
    res_get_value = harness_get_value.run(
        warmup_func=lambda: puw.get_value(q_nanometers),
        timed_func=lambda: puw.get_value(q_nanometers),
    )
    results.append(res_get_value)

    # Get value (with internal conversion: meters -> nm)
    res_get_value_convert = harness_get_value_convert.run(
        warmup_func=lambda: puw.get_value(q_meters, to_unit="nm"),
        timed_func=lambda: puw.get_value(q_meters, to_unit="nm"),
    )
    results.append(res_get_value_convert)

    # Dimensionality check
    res_check_dim = harness_check_dim.run(
        warmup_func=lambda: puw.check(q_nanometers, dimensionality={"[L]": 1}),
        timed_func=lambda: puw.check(q_nanometers, dimensionality={"[L]": 1}),
    )
    results.append(res_check_dim)

    # 3. Report findings
    print("======================================================================")
    print(" MOLSYSMT PYUNITWIZARD MICRO-BENCHMARK PROFILE")
    print("======================================================================")
    print(f" Fast-track to nanometers:     {res_ft_parse['median_seconds'] * 1e6:.2f} μs")
    print(f" Standard nanometer parsing:   {res_std_parse['median_seconds'] * 1e6:.2f} μs")
    print(f" Strip value (no conversion):  {res_get_value['median_seconds'] * 1e6:.2f} μs")
    print(f" Convert & Strip value (m->nm): {res_get_value_convert['median_seconds'] * 1e6:.2f} μs")
    print(f" Dimensionality check [L]^1:  {res_check_dim['median_seconds'] * 1e6:.2f} μs")
    print("======================================================================")

    # Export if path is supplied
    if output_path:
        save_session_results(
            session_name="micro-units-performance",
            results=results,
            output_path=output_path,
        )

    return results


if __name__ == "__main__":
    out_dir = os.path.join(repo_root, "benchmarks", "baselines")
    out_file = os.path.join(out_dir, "micro_units_session.json")
    run_unit_benchmarks(output_path=out_file)
