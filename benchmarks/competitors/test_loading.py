"""Competitive Benchmark for Trajectory Loading.

This module compares the trajectory loading performance of MolSysMT, MDTraj,
and MDAnalysis on the solvated chicken villin HP35 system (20 frames, 4369 atoms).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Add repository root to python path to ensure robust imports
repo_root = str(Path(__file__).resolve().parents[2])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import molsysmt as msm  # noqa: E402
from benchmarks.harness import BenchmarkHarness  # noqa: E402
from benchmarks.telemetry import array_identity, file_digest, workload  # noqa: E402


def run_loading_benchmarks(
    pdb_path: str,
    output_results: list | None = None,
    *,
    _prepare_only=False,
    _input_paths=None,
) -> list[dict]:
    """Execute trajectory loading benchmarks comparing MolSysMT, MDTraj, and MDAnalysis.

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
    dcd_path = str(
        msm.systems["chicken villin HP35"]["traj_chicken_villin_HP35_solvated.dcd"]
    )
    h5_path = str(
        msm.systems["chicken villin HP35"]["traj_chicken_villin_HP35_solvated.h5"]
    )

    if _input_paths is not None:
        dcd_path, h5_path = _input_paths

    # 1. MolSysMT Eager Trajectory Loading
    harness_msm = BenchmarkHarness(
        "competitor_loading_molsysmt", iterations=10, repeats=5
    )

    def load_msm():
        coords = msm.get(dcd_path, element="atom", coordinates=True)
        return coords

    # 2. MDTraj Loading
    import mdtraj

    harness_mdtraj = BenchmarkHarness(
        "competitor_loading_mdtraj", iterations=10, repeats=5
    )

    def load_mdtraj():
        t = mdtraj.load(dcd_path, top=h5_path)
        return t

    # 3. MDAnalysis Loading
    import MDAnalysis

    harness_mda = BenchmarkHarness(
        "competitor_loading_mdanalysis", iterations=10, repeats=5
    )

    def load_mda():
        # Eager load coordinates in MDAnalysis by iterating or accessing coordinates to trigger disk load
        u = MDAnalysis.Universe(pdb_path, dcd_path)
        coords = u.trajectory.timeseries(order="fac")
        return coords

    import numpy as np

    reference = mdtraj.load_hdf5(h5_path).xyz.astype(np.float64)
    paths = {"dcd": dcd_path, "h5": h5_path, "pdb": pdb_path}
    for harness, function, provider, call, output in [
        (
            harness_msm,
            load_msm,
            "molsysmt",
            "get(file:dcd,coordinates=True)",
            "quantity",
        ),
        (
            harness_mdtraj,
            load_mdtraj,
            "mdtraj",
            "load(dcd,top=h5)",
            "Trajectory including topology",
        ),
        (
            harness_mda,
            load_mda,
            "MDAnalysis",
            "Universe(pdb,dcd).trajectory.timeseries(order=fac)",
            "ndarray",
        ),
    ]:
        value = function()
        if provider == "molsysmt":
            value = msm.pyunitwizard.get_value(value, to_unit="nm")
        elif provider == "mdtraj":
            value = value.xyz
        else:
            value = value / 10
        assert value.shape == reference.shape
        np.testing.assert_allclose(value, reference, rtol=1e-6, atol=1e-6)
        harness.workload = workload(
            "read_all_coordinate_structures",
            inputs={
                "files": {key: file_digest(path) for key, path in paths.items()},
                "n_atoms": reference.shape[1],
                "n_structures": reference.shape[0],
                "coordinates": array_identity(reference),
            },
            semantics={
                "unit": "nm",
                "pbc": False,
                "structure_order": "all source structures",
                "validation": "all coordinates equal independent H5 reference before timing",
                "absolute_tolerance_nm": 1e-6,
                "relative_tolerance": 1e-6,
            },
            route={
                "provider": provider,
                "call": call,
                "input_dtype": str(value.dtype),
                "output": output,
            },
            producer=__file__,
        )

    prepared = {}
    for harness, function in [
        (harness_msm, load_msm),
        (harness_mdtraj, load_mdtraj),
        (harness_mda, load_mda),
    ]:
        prepared[harness.name] = (function, harness.workload)
        harness.factory = {
            "module": __name__,
            "function": "run_loading_benchmarks",
            "args": [pdb_path],
            "kwargs": {"_prepare_only": True, "_input_paths": [dcd_path, h5_path]},
            "case": harness.name,
        }
    if _prepare_only:
        return prepared

    results = []

    print("Running loading benchmark: MolSysMT...")
    res_msm = harness_msm.run(warmup_func=load_msm, timed_func=load_msm)
    results.append(res_msm)

    print("Running loading benchmark: MDTraj...")
    res_mdtraj = harness_mdtraj.run(warmup_func=load_mdtraj, timed_func=load_mdtraj)
    results.append(res_mdtraj)

    print("Running loading benchmark: MDAnalysis...")
    res_mda = harness_mda.run(warmup_func=load_mda, timed_func=load_mda)
    results.append(res_mda)

    if output_results is not None:
        output_results.extend(results)

    return results


if __name__ == "__main__":
    # Generate the solvated pdb file if it doesn't exist
    pdb_file = os.path.join(repo_root, "solvated_villin.pdb")
    if not os.path.exists(pdb_file):
        print(f"Generating temporary PDB file: {pdb_file}")
        h5 = msm.systems["chicken villin HP35"]["traj_chicken_villin_HP35_solvated.h5"]
        msm.convert(h5, to_form="file:pdb", output_filename=pdb_file)

    run_loading_benchmarks(pdb_file)
