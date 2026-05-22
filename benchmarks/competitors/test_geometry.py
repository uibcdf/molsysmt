"""Competitive Benchmark for Coordinate Geometric Kernels.

This module compares the geometric calculation speeds (RMSD, center of geometry,
and all-to-all distance matrices) of MolSysMT public APIs, MolSysMT JIT kernels,
MDTraj, and MDAnalysis.
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
from benchmarks.harness import BenchmarkHarness


def run_geometry_benchmarks(pdb_path: str, output_results: list | None = None) -> list[dict]:
    """Execute geometry benchmarks comparing MolSysMT public API, JIT kernels, MDTraj, and MDAnalysis.

    Parameters
    ----------
    pdb_path : str
        Path to the reference PDB topology file.
    output_results : list, optional
        A list to append benchmark results to.

    Returns
    -------
    list[dict]
        Benchmark timing results.
    """
    # 1. MolSysMT Prep
    system = msm.convert(pdb_path, to_form='molsysmt.MolSys')
    coords_qty = msm.get(system, element='atom', coordinates=True)
    coords_raw = msm.pyunitwizard.get_value(coords_qty, to_unit='nanometers').astype(np.float64)
    n_structures, n_atoms, _ = coords_raw.shape
    weights = np.ones(n_atoms, dtype=np.float64)

    from molsysmt.lib.structure.get_center import get_center as jit_get_center
    from molsysmt.lib.structure.get_rmsd import get_rmsd_with_single_reference_structure as jit_get_rmsd
    from molsysmt.lib.structure.get_distances import get_distances_single_system as jit_get_distances

    # 2. MDTraj Prep
    import mdtraj
    t = mdtraj.load(pdb_path)

    # 3. MDAnalysis Prep
    import MDAnalysis
    from MDAnalysis.analysis.rms import rmsd as mda_rmsd
    from MDAnalysis.analysis.distances import distance_array as mda_distance_array
    u = MDAnalysis.Universe(pdb_path)
    ref_coords = u.atoms.positions.copy()

    # Scipy for MDTraj Distances
    from scipy.spatial.distance import cdist as scipy_cdist

    # --- BENCHMARK 1: CENTER OF GEOMETRY ---
    h_msm_pub_center = BenchmarkHarness("competitor_center_molsysmt_public", iterations=20, repeats=5)
    h_msm_jit_center = BenchmarkHarness("competitor_center_molsysmt_jit", iterations=50, repeats=5)
    h_mdt_center = BenchmarkHarness("competitor_center_mdtraj", iterations=50, repeats=5)
    h_mda_center = BenchmarkHarness("competitor_center_mdanalysis", iterations=20, repeats=5)

    def run_msm_pub_center():
        return msm.structure.get_center(system, selection='all')

    def run_msm_jit_center():
        return jit_get_center(coords_raw, weights)

    def run_mdt_center():
        # MDTraj Center of geometry
        return t.xyz.mean(axis=1)

    def run_mda_center():
        # MDAnalysis Center of geometry across trajectory
        return [u.atoms.center_of_geometry() for ts in u.trajectory]

    # --- BENCHMARK 2: RMSD ---
    h_msm_pub_rmsd = BenchmarkHarness("competitor_rmsd_molsysmt_public", iterations=20, repeats=5)
    h_msm_jit_rmsd = BenchmarkHarness("competitor_rmsd_molsysmt_jit", iterations=50, repeats=5)
    h_mdt_rmsd = BenchmarkHarness("competitor_rmsd_mdtraj", iterations=50, repeats=5)
    h_mda_rmsd = BenchmarkHarness("competitor_rmsd_mdanalysis", iterations=20, repeats=5)

    def run_msm_pub_rmsd():
        return msm.structure.get_rmsd(system, reference_structure_index=0, selection='all')

    def run_msm_jit_rmsd():
        return jit_get_rmsd(coords_raw, coords_raw[0])

    def run_mdt_rmsd():
        return mdtraj.rmsd(t, t, frame=0)

    def run_mda_rmsd():
        return [mda_rmsd(u.atoms.positions, ref_coords) for ts in u.trajectory]

    # --- BENCHMARK 3: PAIRWISE DISTANCES ---
    # Filter to CA atoms (35 atoms) to keep the pairwise distance matrix timing blazingly fast
    ca_indices_msm = msm.select(system, 'atom_name == "CA"')
    ca_coords_raw = coords_raw[:, ca_indices_msm, :]
    ca_indices_mdt = t.topology.select('name CA')
    ca_atoms_mda = u.select_atoms('name CA')

    h_msm_pub_dist = BenchmarkHarness("competitor_distances_molsysmt_public", iterations=20, repeats=5)
    h_msm_jit_dist = BenchmarkHarness("competitor_distances_molsysmt_jit", iterations=50, repeats=5)
    h_mdt_dist = BenchmarkHarness("competitor_distances_mdtraj", iterations=50, repeats=5)
    h_mda_dist = BenchmarkHarness("competitor_distances_mdanalysis", iterations=50, repeats=5)

    def run_msm_pub_dist():
        return msm.structure.get_distances(system, selection='atom_name == "CA"')

    def run_msm_jit_dist():
        return jit_get_distances(ca_coords_raw)

    def run_mdt_dist():
        return [scipy_cdist(frame[ca_indices_mdt], frame[ca_indices_mdt]) for frame in t.xyz]

    def run_mda_dist():
        return [mda_distance_array(ca_atoms_mda.positions, ca_atoms_mda.positions) for ts in u.trajectory]

    results = []

    print("Running Center calculation benchmarks...")
    results.append(h_msm_pub_center.run(warmup_func=run_msm_pub_center, timed_func=run_msm_pub_center))
    results.append(h_msm_jit_center.run(warmup_func=run_msm_jit_center, timed_func=run_msm_jit_center))
    results.append(h_mdt_center.run(warmup_func=run_mdt_center, timed_func=run_mdt_center))
    results.append(h_mda_center.run(warmup_func=run_mda_center, timed_func=run_mda_center))

    print("Running RMSD calculation benchmarks...")
    results.append(h_msm_pub_rmsd.run(warmup_func=run_msm_pub_rmsd, timed_func=run_msm_pub_rmsd))
    results.append(h_msm_jit_rmsd.run(warmup_func=run_msm_jit_rmsd, timed_func=run_msm_jit_rmsd))
    results.append(h_mdt_rmsd.run(warmup_func=run_mdt_rmsd, timed_func=run_mdt_rmsd))
    results.append(h_mda_rmsd.run(warmup_func=run_mda_rmsd, timed_func=run_mda_rmsd))

    print("Running Pairwise Distances benchmarks...")
    results.append(h_msm_pub_dist.run(warmup_func=run_msm_pub_dist, timed_func=run_msm_pub_dist))
    results.append(h_msm_jit_dist.run(warmup_func=run_msm_jit_dist, timed_func=run_msm_jit_dist))
    results.append(h_mdt_dist.run(warmup_func=run_mdt_dist, timed_func=run_mdt_dist))
    results.append(h_mda_dist.run(warmup_func=run_mda_dist, timed_func=run_mda_dist))

    if output_results is not None:
        output_results.extend(results)

    return results


if __name__ == "__main__":
    pdb_file = os.path.join(repo_root, "solvated_villin.pdb")
    if not os.path.exists(pdb_file):
        print(f"Generating temporary PDB file: {pdb_file}")
        h5 = msm.systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5']
        msm.convert(h5, to_form='file:pdb', output_filename=pdb_file)

    run_geometry_benchmarks(pdb_file)
