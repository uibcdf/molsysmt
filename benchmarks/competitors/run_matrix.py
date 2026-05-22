"""Orchestration Matrix Runner for Competitive Benchmarks.

This script runs all micro and macro competitive benchmarks, structures results
into an interactive summary, and exports the baselines session JSON.
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
from benchmarks.harness import save_session_results
from benchmarks.competitors.test_loading import run_loading_benchmarks
from benchmarks.competitors.test_selections import run_selection_benchmarks
from benchmarks.competitors.test_geometry import run_geometry_benchmarks


def main():
    print("======================================================================")
    print(" STARTING MOLSYSMT COMPETITIVE PERFORMANCE BENCHMARK MATRIX")
    print("======================================================================")

    # 1. Setup temporary PDB file for the topology reference
    pdb_path = os.path.join(repo_root, "solvated_villin.pdb")
    if not os.path.exists(pdb_path):
        print(f"Generating temporary reference PDB: {pdb_path}")
        h5 = msm.systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5']
        msm.convert(h5, to_form='file:pdb', output_filename=pdb_path)

    # 2. Run all benchmark suites
    results = []

    print("\n--- PHASE 1: Trajectory Loading Suite ---")
    run_loading_benchmarks(pdb_path, results)

    print("\n--- PHASE 2: Selection Language Suite ---")
    run_selection_benchmarks(pdb_path, results)

    print("\n--- PHASE 3: Coordinate Geometric Calculations Suite ---")
    run_geometry_benchmarks(pdb_path, results)

    # 3. Save JSON Session results
    out_dir = os.path.join(repo_root, "benchmarks", "baselines")
    out_file = os.path.join(out_dir, "competitor_matrix_session.json")
    print(f"\nExporting telemetry session to {out_file}...")
    save_session_results(
        session_name="competitive-performance-matrix",
        results=results,
        output_path=out_file
    )

    # 4. Generate & Display Gorgeous ASCII Comparison Table
    # Parse results for easy matrix reporting
    res_dict = {r["name"]: r["median_seconds"] * 1000 for r in results}

    print("\n" + "=" * 86)
    print(f" {'MOLSYSMT COMPETITIVE BENCHMARK MATRIX SUMMARY (MEDIAN TIMINGS IN MS)':^84}")
    print("=" * 86)
    print(f" {'Operation Area':<28} | {'MolSysMT Public':<15} | {'MolSysMT JIT':<12} | {'MDTraj':<10} | {'MDAnalysis':<10}")
    print("-" * 86)

    # Helper function to print a matrix line safely
    def print_line(label: str, msm_pub_key: str, msm_jit_key: str | None, mdt_key: str, mda_key: str):
        val_msm_pub = f"{res_dict[msm_pub_key]:11.3f} ms" if msm_pub_key in res_dict else "N/A"
        val_msm_jit = f"{res_dict[msm_jit_key]:9.3f} ms" if msm_jit_key and msm_jit_key in res_dict else "N/A"
        val_mdt = f"{res_dict[mdt_key]:7.3f} ms" if mdt_key in res_dict else "N/A"
        val_mda = f"{res_dict[mda_key]:7.3f} ms" if mda_key in res_dict else "N/A"
        print(f" {label:<28} | {val_msm_pub:<15} | {val_msm_jit:<12} | {val_mdt:<10} | {val_mda:<10}")

    # Section: File Loading
    print_line("Trajectory Load (DCD)", "competitor_loading_molsysmt", None, "competitor_loading_mdtraj", "competitor_loading_mdanalysis")
    print("-" * 86)

    # Section: Atom Selections
    print_line("Selection Simple (CA)", "competitor_selection_molsysmt_simple", None, "competitor_selection_mdtraj_simple", "competitor_selection_mdanalysis_simple")
    print_line("Selection Complex", "competitor_selection_molsysmt_complex", None, "competitor_selection_mdtraj_complex", "competitor_selection_mdanalysis_complex")
    print("-" * 86)

    # Section: Geometric calculations
    print_line("Center of Geometry", "competitor_center_molsysmt_public", "competitor_center_molsysmt_jit", "competitor_center_mdtraj", "competitor_center_mdanalysis")
    print_line("RMSD Calculation", "competitor_rmsd_molsysmt_public", "competitor_rmsd_molsysmt_jit", "competitor_rmsd_mdtraj", "competitor_rmsd_mdanalysis")
    print_line("Pairwise Distances", "competitor_distances_molsysmt_public", "competitor_distances_molsysmt_jit", "competitor_distances_mdtraj", "competitor_distances_mdanalysis")

    print("=" * 86 + "\n")

    # Clean up temporary PDB file to keep repo clean
    if os.path.exists(pdb_path):
        print(f"Cleaning up temporary reference PDB: {pdb_path}")
        os.remove(pdb_path)


if __name__ == "__main__":
    main()
