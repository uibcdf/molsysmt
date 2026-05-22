"""Macro-benchmark for MolSysMT Trajectory Reading & Out-of-Core Streaming.

This script profiles the performance and out-of-core capabilities of MolSysMT when loading
and processing structural trajectories. It benchmarks three methods on the solvated chicken villin
HP35 trajectory (20 frames, 4369 atoms):
1. Eager trajectory loading (reading all coordinates in one call).
2. Frame-by-frame out-of-core streaming via `msm.Iterator`.
3. Out-of-core chunked processing via `ChunkedExecutor` in `heavy_mode='force'`.
"""

from __future__ import annotations

import os
import sys
import numpy as np
from pathlib import Path

# Add repository root to python path to ensure robust imports
repo_root = str(Path(__file__).resolve().parents[2])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.execution import ChunkedExecutor, Reducer
from benchmarks.harness import BenchmarkHarness, save_session_results


class CoordinatesCollector(Reducer):
    """Simple Reducer that collects coordinates across chunks to verify correctness."""

    def initialize(self, metadata):
        self.all_coords = []

    def consume(self, chunk):
        # We make a copy of coordinates to keep them safe
        self.all_coords.append(chunk['coordinates'].copy())

    def finalize(self):
        return np.concatenate(self.all_coords, axis=0)


def run_trajectory_benchmarks(output_path: str | None = None) -> list[dict]:
    """Execute the trajectory loading and chunked execution macro-benchmarks.

    Parameters
    ----------
    output_path : str, optional
        Absolute path to write the JSON results to.

    Returns
    -------
    list[dict]
        List of results dictionaries.
    """
    print("Locating chicken villin HP35 solvated trajectory (DCD)...")
    dcd_path = msm.systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd']
    print(f"Path: {dcd_path}")

    # 1. Instantiate Benchmark Harnesses
    harness_eager = BenchmarkHarness("macro_trajectory_eager_load", iterations=10, repeats=5)
    harness_iterator = BenchmarkHarness("macro_trajectory_iterator", iterations=10, repeats=5)
    harness_executor = BenchmarkHarness("macro_trajectory_chunked_executor", iterations=10, repeats=5)

    # 2. Run Functions definition
    def run_eager():
        coords = msm.get(dcd_path, element='atom', coordinates=True)
        return puw.get_value(coords, to_unit='nm')

    def run_iterator():
        iterator = msm.Iterator(dcd_path, coordinates=True)
        all_coords = []
        for chunk in iterator:
            all_coords.append(puw.get_value(chunk[0], to_unit='nm'))
        return np.concatenate(all_coords, axis=0)

    def run_executor():
        reducer = CoordinatesCollector()
        executor = ChunkedExecutor(
            molecular_system=dcd_path,
            form='file:dcd',
            operation='benchmark_collect_coordinates',
            reducer=reducer,
            chunk_size=5,
            heavy_mode='force',
            attributes=['coordinates'],
        )
        return executor.execute()

    # 3. Run Benchmarks
    results = []

    print("Benchmarking eager trajectory load...")
    res_eager = harness_eager.run(
        warmup_func=run_eager,
        timed_func=run_eager
    )
    results.append(res_eager)

    print("Benchmarking out-of-core frame iterator...")
    res_iterator = harness_iterator.run(
        warmup_func=run_iterator,
        timed_func=run_iterator
    )
    results.append(res_iterator)

    print("Benchmarking heavy chunked executor...")
    res_executor = harness_executor.run(
        warmup_func=run_executor,
        timed_func=run_executor
    )
    results.append(res_executor)

    # Validate that shapes match across eager and heavy paths
    eager_shape = run_eager().shape
    executor_shape = run_executor().shape
    print(f"\nEager shape: {eager_shape}, Executor shape: {executor_shape}")
    assert eager_shape == executor_shape, "Mismatch between eager and chunked coordinates shapes!"
    print("Verification passed: eager and chunked coordinates shapes match exactly.")

    # 4. Display Summary Table
    print("\n" + "=" * 78)
    print(f" {'MOLSYSMT TRAJECTORY STREAMING MACRO-BENCHMARK RESULTS':^76}")
    print("=" * 78)
    print(f" {'Benchmark Name':<42} | {'Median Time':<15} | {'Min Time':<12}")
    print("-" * 78)
    for r in results:
        print(f" {r['name']:<42} | {r['median_seconds'] * 1000:11.3f} ms | {r['min_seconds'] * 1000:8.3f} ms")
    print("=" * 78 + "\n")

    # Export if requested
    if output_path:
        save_session_results(
            session_name="macro-trajectory-streaming",
            results=results,
            output_path=output_path,
        )

    return results


if __name__ == "__main__":
    out_dir = os.path.join(repo_root, "benchmarks", "baselines")
    out_file = os.path.join(out_dir, "macro_trajectories_session.json")
    run_trajectory_benchmarks(output_path=out_file)
