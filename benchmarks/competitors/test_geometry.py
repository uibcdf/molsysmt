"""Competitive Benchmark for Coordinate Geometric Kernels.

This module compares the geometric calculation speeds (RMSD, center of geometry,
and all-to-all distance matrices) of MolSysMT public APIs, MolSysMT JIT kernels,
MDTraj, and MDAnalysis. Every route uses unaligned RMSD and nonperiodic
full pair grids; the legacy ``jit`` result keys now identify Rust kernels.
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

import molsysmt as msm  # noqa: E402
from benchmarks.harness import BenchmarkHarness  # noqa: E402
from benchmarks.telemetry import array_identity, file_digest, workload  # noqa: E402


def run_geometry_benchmarks(
    pdb_path: str, output_results: list | None = None, *, _prepare_only=False
) -> list[dict]:
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
    system = msm.convert(pdb_path, to_form="molsysmt.MolSys")
    coords_qty = msm.get(system, element="atom", coordinates=True)
    coords_raw = msm.pyunitwizard.get_value(coords_qty, to_unit="nanometers").astype(
        np.float64
    )
    n_structures, n_atoms, _ = coords_raw.shape
    weights = np.ones(n_atoms, dtype=np.float64)

    # 2. MDTraj Prep
    import mdtraj

    from molsysmt.lib.structure.get_center import get_center as jit_get_center
    from molsysmt.lib.structure.get_distances import (
        get_distances_single_system as jit_get_distances,
    )
    from molsysmt.lib.structure.get_rmsd import (
        get_rmsd_with_single_reference_structure as jit_get_rmsd,
    )

    t = mdtraj.load(pdb_path)

    # 3. MDAnalysis Prep
    import MDAnalysis
    from MDAnalysis.analysis.distances import distance_array as mda_distance_array
    from MDAnalysis.analysis.rms import rmsd as mda_rmsd

    u = MDAnalysis.Universe(pdb_path)
    ref_coords = u.atoms.positions.copy()

    # --- BENCHMARK 1: CENTER OF GEOMETRY ---
    h_msm_pub_center = BenchmarkHarness(
        "competitor_center_molsysmt_public", iterations=20, repeats=5
    )
    h_msm_jit_center = BenchmarkHarness(
        "competitor_center_molsysmt_jit", iterations=50, repeats=5
    )
    h_mdt_center = BenchmarkHarness(
        "competitor_center_mdtraj", iterations=50, repeats=5
    )
    h_mda_center = BenchmarkHarness(
        "competitor_center_mdanalysis", iterations=20, repeats=5
    )

    def run_msm_pub_center():
        return msm.structure.get_center(system, selection="all")

    def run_msm_jit_center():
        return jit_get_center(coords_raw, weights)

    def run_mdt_center():
        # MDTraj Center of geometry
        return t.xyz.mean(axis=1)

    def run_mda_center():
        # MDAnalysis Center of geometry across trajectory
        return [u.atoms.center_of_geometry() for ts in u.trajectory]

    # --- BENCHMARK 2: RMSD ---
    h_msm_pub_rmsd = BenchmarkHarness(
        "competitor_rmsd_molsysmt_public", iterations=20, repeats=5
    )
    h_msm_jit_rmsd = BenchmarkHarness(
        "competitor_rmsd_molsysmt_jit", iterations=50, repeats=5
    )
    h_mdt_rmsd = BenchmarkHarness("competitor_rmsd_mdtraj", iterations=50, repeats=5)
    h_mda_rmsd = BenchmarkHarness(
        "competitor_rmsd_mdanalysis", iterations=20, repeats=5
    )

    def run_msm_pub_rmsd():
        return msm.structure.get_rmsd(
            system, reference_structure_index=0, selection="all"
        )

    def run_msm_jit_rmsd():
        return jit_get_rmsd(coords_raw, coords_raw[0])

    def run_mdt_rmsd():
        return mdtraj.rmsd(t, t, frame=0, superpose=False, parallel=False)

    def run_mda_rmsd():
        return [mda_rmsd(u.atoms.positions, ref_coords) for ts in u.trajectory]

    # --- BENCHMARK 3: PAIRWISE DISTANCES ---
    # Filter to CA atoms (35 atoms) to keep the pairwise distance matrix timing blazingly fast
    ca_indices_msm = msm.select(system, 'atom_name == "CA"')
    ca_coords_raw = coords_raw[:, ca_indices_msm, :]
    ca_indices_mdt = t.topology.select("name CA")
    ca_atoms_mda = u.select_atoms("name CA")

    h_msm_pub_dist = BenchmarkHarness(
        "competitor_distances_molsysmt_public", iterations=20, repeats=5
    )
    h_msm_jit_dist = BenchmarkHarness(
        "competitor_distances_molsysmt_jit", iterations=50, repeats=5
    )
    h_mdt_dist = BenchmarkHarness(
        "competitor_distances_mdtraj", iterations=50, repeats=5
    )
    h_mda_dist = BenchmarkHarness(
        "competitor_distances_mdanalysis", iterations=50, repeats=5
    )

    def run_msm_pub_dist():
        return msm.structure.get_distances(
            system, selection='atom_name == "CA"', pbc=False
        )

    def run_msm_jit_dist():
        return jit_get_distances(ca_coords_raw)

    def run_mdt_dist():
        return mdtraj.compute_distances(t, ca_pairs_mdt, periodic=False).reshape(
            n_structures, len(ca_indices_mdt), len(ca_indices_mdt)
        )

    def run_mda_dist():
        return [
            mda_distance_array(ca_atoms_mda.positions, ca_atoms_mda.positions)
            for ts in u.trajectory
        ]

    np.testing.assert_array_equal(ca_indices_mdt, ca_indices_msm)
    np.testing.assert_array_equal(ca_atoms_mda.indices, ca_indices_msm)
    ca_pairs_mdt = np.array(
        [(int(i), int(j)) for i in ca_indices_mdt for j in ca_indices_mdt],
        dtype=np.int32,
    ).reshape(-1, 2)

    # Scientific equality is checked on the actual prepared data before timing.
    expected_center = coords_raw.mean(axis=1)
    expected_rmsd = np.sqrt(
        np.mean(np.sum((coords_raw - coords_raw[0]) ** 2, axis=-1), axis=-1)
    )
    expected_distances = np.linalg.norm(
        ca_coords_raw[:, :, None] - ca_coords_raw[:, None, :], axis=-1
    )
    families = [
        (
            "centroid",
            expected_center,
            [
                (
                    h_msm_pub_center,
                    run_msm_pub_center,
                    "molsysmt",
                    "structure.get_center",
                    "float64",
                    "quantity",
                ),
                (
                    h_msm_jit_center,
                    run_msm_jit_center,
                    "molsysmt",
                    "lib.structure.get_center",
                    "float64",
                    "ndarray",
                ),
                (
                    h_mdt_center,
                    run_mdt_center,
                    "mdtraj",
                    "Trajectory.xyz.mean",
                    str(t.xyz.dtype),
                    "ndarray",
                ),
                (
                    h_mda_center,
                    run_mda_center,
                    "MDAnalysis",
                    "AtomGroup.center_of_geometry",
                    str(u.atoms.positions.dtype),
                    "list of arrays",
                ),
            ],
        ),
        (
            "unaligned_rmsd",
            expected_rmsd,
            [
                (
                    h_msm_pub_rmsd,
                    run_msm_pub_rmsd,
                    "molsysmt",
                    "structure.get_rmsd",
                    "float64",
                    "quantity",
                ),
                (
                    h_msm_jit_rmsd,
                    run_msm_jit_rmsd,
                    "molsysmt",
                    "lib.structure.get_rmsd",
                    "float64",
                    "ndarray",
                ),
                (
                    h_mdt_rmsd,
                    run_mdt_rmsd,
                    "mdtraj",
                    "rmsd(superpose=False,parallel=False)",
                    str(t.xyz.dtype),
                    "ndarray",
                ),
                (
                    h_mda_rmsd,
                    run_mda_rmsd,
                    "MDAnalysis",
                    "analysis.rms.rmsd(center=False,superposition=False)",
                    str(u.atoms.positions.dtype),
                    "list",
                ),
            ],
        ),
        (
            "full_pairwise_distances",
            expected_distances,
            [
                (
                    h_msm_pub_dist,
                    run_msm_pub_dist,
                    "molsysmt",
                    "structure.get_distances(pbc=False)",
                    "float64",
                    "quantity",
                ),
                (
                    h_msm_jit_dist,
                    run_msm_jit_dist,
                    "molsysmt",
                    "lib.structure.get_distances",
                    "float64",
                    "ndarray",
                ),
                (
                    h_mdt_dist,
                    run_mdt_dist,
                    "mdtraj",
                    "compute_distances(periodic=False)",
                    str(t.xyz.dtype),
                    "ndarray",
                ),
                (
                    h_mda_dist,
                    run_mda_dist,
                    "MDAnalysis",
                    "analysis.distances.distance_array(box=None)",
                    str(u.atoms.positions.dtype),
                    "list of arrays",
                ),
            ],
        ),
    ]
    for operation, expected, routes in families:
        for harness, function, provider, call, dtype, output in routes:
            observed = function()
            if msm.pyunitwizard.is_quantity(observed):
                observed = msm.pyunitwizard.get_value(observed, to_unit="nm")
            else:
                observed = np.asarray(observed) / (
                    10 if provider == "MDAnalysis" else 1
                )
            observed = np.asarray(observed)
            if operation == "centroid":
                assert observed.shape in {(n_structures, 3), (n_structures, 1, 3)}
                observed = observed.reshape(n_structures, 3)
            else:
                assert observed.shape == expected.shape
            np.testing.assert_allclose(
                observed,
                expected,
                rtol=1e-6,
                atol=1e-5,
                err_msg=harness.name,
            )
            harness.workload = workload(
                operation,
                inputs={
                    "files": {"pdb": file_digest(pdb_path)},
                    "n_atoms": n_atoms,
                    "n_structures": n_structures,
                    "coordinates": array_identity(coords_raw),
                    "selected_indices": list(map(int, ca_indices_msm))
                    if operation == "full_pairwise_distances"
                    else "all",
                },
                semantics={
                    "unit": "nm",
                    "pbc": False,
                    "superposition": False,
                    "reference_structure_index": 0
                    if operation == "unaligned_rmsd"
                    else None,
                    "validation": "independent NumPy coordinate equality before timing",
                    "absolute_tolerance_nm": 1e-5,
                    "relative_tolerance": 1e-6,
                },
                route={
                    "provider": provider,
                    "call": call,
                    "input_dtype": dtype,
                    "output": output,
                },
                producer=__file__,
            )

    prepared = {
        harness.name: (function, harness.workload)
        for _, _, routes in families
        for harness, function, *_ in routes
    }
    if _prepare_only:
        return prepared
    for _, _, routes in families:
        for harness, *_ in routes:
            harness.factory = {
                "module": __name__,
                "function": "run_geometry_benchmarks",
                "args": [pdb_path],
                "kwargs": {"_prepare_only": True},
                "case": harness.name,
            }

    results = []

    print("Running Center calculation benchmarks...")
    results.append(
        h_msm_pub_center.run(
            warmup_func=run_msm_pub_center, timed_func=run_msm_pub_center
        )
    )
    results.append(
        h_msm_jit_center.run(
            warmup_func=run_msm_jit_center, timed_func=run_msm_jit_center
        )
    )
    results.append(
        h_mdt_center.run(warmup_func=run_mdt_center, timed_func=run_mdt_center)
    )
    results.append(
        h_mda_center.run(warmup_func=run_mda_center, timed_func=run_mda_center)
    )

    print("Running RMSD calculation benchmarks...")
    results.append(
        h_msm_pub_rmsd.run(warmup_func=run_msm_pub_rmsd, timed_func=run_msm_pub_rmsd)
    )
    results.append(
        h_msm_jit_rmsd.run(warmup_func=run_msm_jit_rmsd, timed_func=run_msm_jit_rmsd)
    )
    results.append(h_mdt_rmsd.run(warmup_func=run_mdt_rmsd, timed_func=run_mdt_rmsd))
    results.append(h_mda_rmsd.run(warmup_func=run_mda_rmsd, timed_func=run_mda_rmsd))

    print("Running Pairwise Distances benchmarks...")
    results.append(
        h_msm_pub_dist.run(warmup_func=run_msm_pub_dist, timed_func=run_msm_pub_dist)
    )
    results.append(
        h_msm_jit_dist.run(warmup_func=run_msm_jit_dist, timed_func=run_msm_jit_dist)
    )
    results.append(h_mdt_dist.run(warmup_func=run_mdt_dist, timed_func=run_mdt_dist))
    results.append(h_mda_dist.run(warmup_func=run_mda_dist, timed_func=run_mda_dist))

    if output_results is not None:
        output_results.extend(results)

    return results


if __name__ == "__main__":
    pdb_file = os.path.join(repo_root, "solvated_villin.pdb")
    if not os.path.exists(pdb_file):
        print(f"Generating temporary PDB file: {pdb_file}")
        h5 = msm.systems["chicken villin HP35"]["traj_chicken_villin_HP35_solvated.h5"]
        msm.convert(h5, to_form="file:pdb", output_filename=pdb_file)

    run_geometry_benchmarks(pdb_file)
