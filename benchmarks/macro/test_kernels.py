"""Macro-benchmark for MolSysMT Mathematical Coordinate Kernels.

This script benchmarks RMSD, center of mass, and pairwise distances calculations on a realistic
38-frame, 304-atom Trp-Cage mini-protein (1l2y). It evaluates both the high-level public API wrappers
and the raw JIT-compiled library kernels under GC isolation and JIT pre-warming.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
import numpy as np

# Add repository root to python path to ensure robust imports
repo_root = str(Path(__file__).resolve().parents[2])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import molsysmt as msm
from benchmarks.harness import BenchmarkHarness, save_session_results


def run_coordinate_benchmarks(output_path: str | None = None) -> list[dict]:
    """Execute the coordinate and mathematical JIT kernel macro-benchmarks.

    Parameters
    ----------
    output_path : str, optional
        Absolute path to write the JSON results to.

    Returns
    -------
    list[dict]
        List of results dictionaries.
    """
    # 1. Load the Trp-Cage protein system and prepare inputs
    print("Loading Trp-Cage (1l2y.pdb) system...")
    pdb_path = msm.systems['Trp-Cage']['1l2y.pdb']
    system = msm.convert(pdb_path, to_form='molsysmt.MolSys')

    # Fetch pint Quantity coordinates and strip units to get raw float64 numpy array
    coords_qty = msm.get(system, element='atom', coordinates=True)
    coords_raw = msm.pyunitwizard.get_value(coords_qty, to_unit='nanometers').astype(np.float64)

    n_structures, n_atoms, _ = coords_raw.shape
    print(f"Loaded {n_structures} frames, each with {n_atoms} atoms.")

    # Prepare weights for center of mass (equal weights for simple geometric center)
    weights = np.ones(n_atoms, dtype=np.float64)

    # 2. Instantiate Benchmark Harnesses
    # Public APIs
    harness_center_public = BenchmarkHarness("macro_get_center_public_api", iterations=50, repeats=5)
    harness_rmsd_public = BenchmarkHarness("macro_get_rmsd_public_api", iterations=50, repeats=5)
    harness_distances_public = BenchmarkHarness("macro_get_distances_public_api", iterations=10, repeats=5)

    # Raw JIT Kernels
    harness_center_jit = BenchmarkHarness("macro_get_center_jit_kernel", iterations=100, repeats=5)
    harness_rmsd_jit = BenchmarkHarness("macro_get_rmsd_jit_kernel", iterations=100, repeats=5)
    harness_distances_jit = BenchmarkHarness("macro_get_distances_jit_kernel", iterations=20, repeats=5)

    # 3. Run Benchmarks
    results = []

    # Import the raw JIT functions
    from molsysmt.lib.structure.get_center import get_center as jit_get_center
    from molsysmt.lib.structure.get_rmsd import get_rmsd_with_single_reference_structure as jit_get_rmsd
    from molsysmt.lib.structure.get_distances import get_distances_single_system as jit_get_distances

    # --- CENTER OF MASS / GEOMETRIC CENTER ---
    print("Benchmarking Center calculations...")
    res_center_pub = harness_center_public.run(
        warmup_func=lambda: msm.structure.get_center(system, selection='all'),
        timed_func=lambda: msm.structure.get_center(system, selection='all')
    )
    res_center_jit = harness_center_jit.run(
        warmup_func=lambda: jit_get_center(coords_raw, weights),
        timed_func=lambda: jit_get_center(coords_raw, weights)
    )
    results.extend([res_center_pub, res_center_jit])

    # --- RMSD ---
    print("Benchmarking RMSD calculations...")
    res_rmsd_pub = harness_rmsd_public.run(
        warmup_func=lambda: msm.structure.get_rmsd(system, reference_structure_index=0, selection='all'),
        timed_func=lambda: msm.structure.get_rmsd(system, reference_structure_index=0, selection='all')
    )
    res_rmsd_jit = harness_rmsd_jit.run(
        warmup_func=lambda: jit_get_rmsd(coords_raw, coords_raw[0]),
        timed_func=lambda: jit_get_rmsd(coords_raw, coords_raw[0])
    )
    results.extend([res_rmsd_pub, res_rmsd_jit])

    # --- DISTANCES ---
    print("Benchmarking Distances calculations...")
    res_dist_pub = harness_distances_public.run(
        warmup_func=lambda: msm.structure.get_distances(system, selection='all'),
        timed_func=lambda: msm.structure.get_distances(system, selection='all')
    )
    res_dist_jit = harness_distances_jit.run(
        warmup_func=lambda: jit_get_distances(coords_raw),
        timed_func=lambda: jit_get_distances(coords_raw)
    )
    results.extend([res_dist_pub, res_dist_jit])

    # 4. Display Summary Table
    print("\n" + "=" * 78)
    print(f" {'MOLSYSMT COORDINATE MATH MACRO-BENCHMARK RESULTS':^76}")
    print("=" * 78)
    print(f" {'Benchmark Name':<42} | {'Median Time':<15} | {'Min Time':<12}")
    print("-" * 78)
    for r in results:
        print(f" {r['name']:<42} | {r['median_seconds'] * 1000:11.3f} ms | {r['min_seconds'] * 1000:8.3f} ms")
    print("=" * 78 + "\n")

    # Export if requested
    if output_path:
        save_session_results(
            session_name="macro-coordinate-kernels",
            results=results,
            output_path=output_path,
        )

    return results


if __name__ == "__main__":
    out_dir = os.path.join(repo_root, "benchmarks", "baselines")
    out_file = os.path.join(out_dir, "macro_kernels_session.json")
    run_coordinate_benchmarks(output_path=out_file)
