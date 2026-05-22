"""Micro-benchmark for MolSysMT Digestion Overhead.

This script isolates and profiles the performance safety tax introduced by the @arg_digest decorator.
It compares timing between running a public API function with digestion enabled vs skipped.
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
from benchmarks.harness import BenchmarkHarness, save_session_results


def run_digestion_benchmarks(output_path: str | None = None) -> dict[str, float]:
    """Execute the digestion validation overhead micro-benchmarks.

    Parameters
    ----------
    output_path : str, optional
        Absolute path to write the JSON results to.

    Returns
    -------
    dict[str, float]
        Timing results.
    """
    # 1. Warm-up and validation targets
    # We use simple attribute inquiries to profile pure decorator parsing time
    from molsysmt.attribute import is_mechanical_attribute, is_topological_attribute

    attribute_name = "coordinates"

    # Define harness instances
    harness_digested_mech = BenchmarkHarness(
        name="digestion_is_mechanical_attribute_enabled",
        iterations=500,
        repeats=5,
    )
    harness_skipped_mech = BenchmarkHarness(
        name="digestion_is_mechanical_attribute_skipped",
        iterations=500,
        repeats=5,
    )

    harness_digested_topo = BenchmarkHarness(
        name="digestion_is_topological_attribute_enabled",
        iterations=500,
        repeats=5,
    )
    harness_skipped_topo = BenchmarkHarness(
        name="digestion_is_topological_attribute_skipped",
        iterations=500,
        repeats=5,
    )

    # 2. Run benchmarks
    results = []

    # Mechanical Attribute enabled/skipped
    res_digested_mech = harness_digested_mech.run(
        warmup_func=lambda: is_mechanical_attribute(attribute_name, skip_digestion=False),
        timed_func=lambda: is_mechanical_attribute(attribute_name, skip_digestion=False),
    )
    res_skipped_mech = harness_skipped_mech.run(
        warmup_func=lambda: is_mechanical_attribute(attribute_name, skip_digestion=True),
        timed_func=lambda: is_mechanical_attribute(attribute_name, skip_digestion=True),
    )
    results.extend([res_digested_mech, res_skipped_mech])

    # Topological Attribute enabled/skipped
    res_digested_topo = harness_digested_topo.run(
        warmup_func=lambda: is_topological_attribute(attribute_name, skip_digestion=False),
        timed_func=lambda: is_topological_attribute(attribute_name, skip_digestion=False),
    )
    res_skipped_topo = harness_skipped_topo.run(
        warmup_func=lambda: is_topological_attribute(attribute_name, skip_digestion=True),
        timed_func=lambda: is_topological_attribute(attribute_name, skip_digestion=True),
    )
    results.extend([res_digested_topo, res_skipped_topo])

    # 3. Calculate and display calculated safety tax overhead
    mech_tax = res_digested_mech["median_seconds"] - res_skipped_mech["median_seconds"]
    topo_tax = res_digested_topo["median_seconds"] - res_skipped_topo["median_seconds"]

    print("======================================================================")
    print(" MOLSYSMT DIGESTION SAFETY TAX AUDIT")
    print("======================================================================")
    print(f" Mechanical Inquire digested: {res_digested_mech['median_seconds'] * 1e6:.2f} μs")
    print(f" Mechanical Inquire skipped:  {res_skipped_mech['median_seconds'] * 1e6:.2f} μs")
    print(f" Isolate Digestion Safety Tax: {mech_tax * 1e6:.2f} μs")
    print("----------------------------------------------------------------------")
    print(f" Topological Inquire digested: {res_digested_topo['median_seconds'] * 1e6:.2f} μs")
    print(f" Topological Inquire skipped:  {res_skipped_topo['median_seconds'] * 1e6:.2f} μs")
    print(f" Isolate Digestion Safety Tax: {topo_tax * 1e6:.2f} μs")
    print("======================================================================")

    # Export if requested
    if output_path:
        save_session_results(
            session_name="micro-digestion-overhead",
            results=results,
            output_path=output_path,
        )

    return {
        "is_mechanical_attribute_tax_seconds": mech_tax,
        "is_topological_attribute_tax_seconds": topo_tax,
    }


if __name__ == "__main__":
    out_dir = os.path.join(repo_root, "benchmarks", "baselines")
    out_file = os.path.join(out_dir, "micro_digestion_session.json")
    run_digestion_benchmarks(output_path=out_file)
