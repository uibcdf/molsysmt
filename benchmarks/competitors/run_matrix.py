"""Orchestration Matrix Runner for Competitive Benchmarks.

This script runs all micro and macro competitive benchmarks, structures results
into an interactive summary, and exports the baselines session JSON.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

# Add repository root to python path to ensure robust imports
repo_root = str(Path(__file__).resolve().parents[2])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import molsysmt as msm  # noqa: E402
from benchmarks.competitors.test_geometry import run_geometry_benchmarks  # noqa: E402
from benchmarks.competitors.test_loading import run_loading_benchmarks  # noqa: E402
from benchmarks.competitors.test_selections import (  # noqa: E402
    run_selection_benchmarks,
)
from benchmarks.harness import _get_git_metadata, save_session_results  # noqa: E402
from benchmarks.telemetry import (  # noqa: E402
    comparison_context,
    file_digest,
    resource_observation,
)


def _canonicalize_owned_reference(path):
    """Replace only the two known volatile records in our newly generated PDB."""
    import hashlib

    destination = Path(path)
    raw = destination.read_bytes()
    lines = raw.splitlines(keepends=True)
    headers = [
        i
        for i, line in enumerate(lines)
        if line.startswith(b"HEADER    MOLECULAR SYSTEM")
    ]
    timestamps = [
        i
        for i, line in enumerate(lines)
        if line.startswith(b"REMARK   1 Created by MolSysMT version ")
    ]
    if len(headers) != 1 or len(timestamps) != 1:
        raise RuntimeError(
            "The owned reference's generated provenance records require review."
        )
    originals = {
        str(index): lines[index].decode("ascii") for index in [*headers, *timestamps]
    }
    lines[headers[0]] = b"HEADER    MOLSYSMT BENCHMARK REFERENCE\n"
    lines[timestamps[0]] = b"REMARK   1 BENCHMARK REFERENCE; SEE SESSION PROVENANCE\n"
    prepared = b"".join(lines)
    destination.write_bytes(prepared)
    return {
        "normalization": "owned-generated-pdb-provenance@1",
        "original_records": originals,
        "raw_pdb_sha256": hashlib.sha256(raw).hexdigest(),
        "prepared_pdb_sha256": hashlib.sha256(prepared).hexdigest(),
    }


from molsysmt._pyunitwizard import STANDARD_UNITS  # noqa: E402


def _prepare_reference(pdb_path):
    """Diagnose the active source runtime and prepare the unchanged H5 reference."""
    from molsysmt._private.molecular_system_validation import assess_molecular_system

    h5 = msm.systems["chicken villin HP35"]["traj_chicken_villin_HP35_solvated.h5"]
    source = Path(h5)
    rust = importlib.util.find_spec("molsysmt._rust")
    providers = {}
    for name in ("numpy", "pandas", "mdtraj", "h5py"):
        try:
            providers[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            providers[name] = None
    evidence = {
        "python": sys.executable,
        "python_version": sys.version,
        "molsysmt": msm.__file__,
        "molsysmt_version": msm.__version__,
        "rust": None if rust is None else rust.origin,
        "providers": providers,
        "input": str(source),
        "input_exists": source.is_file(),
        "input_bytes": source.stat().st_size if source.is_file() else None,
    }
    print("BENCHMARK_RUNTIME " + json.dumps(evidence, sort_keys=True), flush=True)
    if rust is None:
        raise RuntimeError(
            "The benchmark source runtime cannot find molsysmt._rust. "
            "Install the compiled checkout with python -m pip install --editable . --no-deps."
        )
    assessment = assess_molecular_system(h5)
    print(
        "BENCHMARK_REFERENCE "
        + json.dumps(
            {
                "forms": assessment.forms,
                "valid": assessment.is_valid_single_system,
                "reason": assessment.reason,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    if not assessment.is_valid_single_system:
        raise RuntimeError(f"Benchmark H5 reference is invalid: {assessment.reason}")
    if not os.path.exists(pdb_path):
        print(f"Generating temporary reference PDB: {pdb_path}", flush=True)
        msm.convert(h5, to_form="file:pdb", output_filename=pdb_path)
        provenance = _canonicalize_owned_reference(pdb_path)
        provenance["source_h5_sha256"] = file_digest(h5)
        provenance["producer_version"] = msm.__version__
        return provenance
    return {
        "normalization": "existing-input-unchanged",
        "prepared_pdb_sha256": file_digest(pdb_path),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(repo_root) / "benchmarks/baselines/competitor_matrix_session.json",
        help="Session JSON destination; CI uses a separate evidence file rather than renewing the baseline.",
    )
    args = parser.parse_args(argv)
    args.output = args.output.expanduser().resolve()
    if args.output.is_dir():
        parser.error("--output must name a JSON file, not a directory")
    print("======================================================================")
    print(" STARTING MOLSYSMT COMPETITIVE PERFORMANCE BENCHMARK MATRIX")
    print("======================================================================")

    # Give each campaign its own reference; never reuse or remove a caller file.
    results = []
    with (
        tempfile.TemporaryDirectory(prefix="molsysmt-benchmark-") as directory,
        msm.configure.context(
            use_gpu=False,
            parallel_mode=False,
            num_threads=1,
            precision="double",
            heavy_mode="off",
        ),
        msm.pyunitwizard.context(
            default_form="pint", default_parser="pint", standard_units=STANDARD_UNITS
        ),
    ):
        pdb_path = str(Path(directory) / "reference.pdb")
        reference_preparation = _prepare_reference(pdb_path)
        observations = {"before": resource_observation()}
        starting_context = comparison_context()
        starting_source = _get_git_metadata()
        print("\n--- PHASE 1: Trajectory Loading Suite ---")
        run_loading_benchmarks(pdb_path, results)
        print("\n--- PHASE 2: Selection Language Suite ---")
        run_selection_benchmarks(pdb_path, results)
        print("\n--- PHASE 3: Coordinate Geometric Calculations Suite ---")
        run_geometry_benchmarks(pdb_path, results)
        context = comparison_context()
        observations["after"] = resource_observation()
        if context != starting_context or _get_git_metadata() != starting_source:
            raise RuntimeError(
                "Benchmark source/execution context changed during measurement."
            )

    # 3. Save JSON Session results
    out_file = args.output
    print(f"\nExporting telemetry session to {out_file}...")
    save_session_results(
        session_name="competitive-performance-matrix",
        results=results,
        output_path=out_file,
        comparison_context=context,
        resource_observations=observations,
        reference_preparation=reference_preparation,
    )

    # 4. Generate & Display Gorgeous ASCII Comparison Table
    # Parse results for easy matrix reporting
    res_dict = {r["name"]: r["median_seconds"] * 1000 for r in results}
    res_ram = {r["name"]: r["peak_rss_mb"] for r in results}

    print("\n" + "=" * 86)
    print(
        f" {'MOLSYSMT COMPETITIVE BENCHMARK TIMING MATRIX SUMMARY (MEDIAN TIMINGS IN MS)':^84}"
    )
    print("=" * 86)
    print(
        f" {'Operation Area':<28} | {'MolSysMT Public':<15} | {'MolSysMT Rust':<12} | {'MDTraj':<10} | {'MDAnalysis':<10}"
    )
    print("-" * 86)

    # Helper function to print a matrix line safely
    def print_line(
        label: str,
        msm_pub_key: str,
        msm_jit_key: str | None,
        mdt_key: str,
        mda_key: str,
    ):
        val_msm_pub = (
            f"{res_dict[msm_pub_key]:11.3f} ms" if msm_pub_key in res_dict else "N/A"
        )
        val_msm_jit = (
            f"{res_dict[msm_jit_key]:9.3f} ms"
            if msm_jit_key and msm_jit_key in res_dict
            else "N/A"
        )
        val_mdt = f"{res_dict[mdt_key]:7.3f} ms" if mdt_key in res_dict else "N/A"
        val_mda = f"{res_dict[mda_key]:7.3f} ms" if mda_key in res_dict else "N/A"
        print(
            f" {label:<28} | {val_msm_pub:<15} | {val_msm_jit:<12} | {val_mdt:<10} | {val_mda:<10}"
        )

    # Section: File Loading
    print_line(
        "Trajectory Load (DCD)",
        "competitor_loading_molsysmt",
        None,
        "competitor_loading_mdtraj",
        "competitor_loading_mdanalysis",
    )
    print("-" * 86)

    # Section: Atom Selections
    print_line(
        "Selection Simple (CA)",
        "competitor_selection_molsysmt_simple",
        None,
        "competitor_selection_mdtraj_simple",
        "competitor_selection_mdanalysis_simple",
    )
    print_line(
        "Selection Complex",
        "competitor_selection_molsysmt_complex",
        None,
        "competitor_selection_mdtraj_complex",
        "competitor_selection_mdanalysis_complex",
    )
    print("-" * 86)

    # Section: Geometric calculations
    print_line(
        "Center of Geometry",
        "competitor_center_molsysmt_public",
        "competitor_center_molsysmt_jit",
        "competitor_center_mdtraj",
        "competitor_center_mdanalysis",
    )
    print_line(
        "RMSD Calculation",
        "competitor_rmsd_molsysmt_public",
        "competitor_rmsd_molsysmt_jit",
        "competitor_rmsd_mdtraj",
        "competitor_rmsd_mdanalysis",
    )
    print_line(
        "Pairwise Distances",
        "competitor_distances_molsysmt_public",
        "competitor_distances_molsysmt_jit",
        "competitor_distances_mdtraj",
        "competitor_distances_mdanalysis",
    )

    print("=" * 86 + "\n")

    print("=" * 86)
    print(
        f" {'MOLSYSMT COMPETITIVE BENCHMARK MEMORY MATRIX SUMMARY (PEAK RAM IN MB)':^84}"
    )
    print("=" * 86)
    print(
        f" {'Operation Area':<28} | {'MolSysMT Public':<15} | {'MolSysMT Rust':<12} | {'MDTraj':<10} | {'MDAnalysis':<10}"
    )
    print("-" * 86)

    # Helper function to print a memory line safely
    def print_mem_line(
        label: str,
        msm_pub_key: str,
        msm_jit_key: str | None,
        mdt_key: str,
        mda_key: str,
    ):
        val_msm_pub = (
            f"{res_ram[msm_pub_key]:11.2f} MB" if msm_pub_key in res_ram else "N/A"
        )
        val_msm_jit = (
            f"{res_ram[msm_jit_key]:9.2f} MB"
            if msm_jit_key and msm_jit_key in res_ram
            else "N/A"
        )
        val_mdt = f"{res_ram[mdt_key]:7.2f} MB" if mdt_key in res_ram else "N/A"
        val_mda = f"{res_ram[mda_key]:7.2f} MB" if mda_key in res_ram else "N/A"
        print(
            f" {label:<28} | {val_msm_pub:<15} | {val_msm_jit:<12} | {val_mdt:<10} | {val_mda:<10}"
        )

    # Section: File Loading
    print_mem_line(
        "Trajectory Load (DCD)",
        "competitor_loading_molsysmt",
        None,
        "competitor_loading_mdtraj",
        "competitor_loading_mdanalysis",
    )
    print("-" * 86)

    # Section: Atom Selections
    print_mem_line(
        "Selection Simple (CA)",
        "competitor_selection_molsysmt_simple",
        None,
        "competitor_selection_mdtraj_simple",
        "competitor_selection_mdanalysis_simple",
    )
    print_mem_line(
        "Selection Complex",
        "competitor_selection_molsysmt_complex",
        None,
        "competitor_selection_mdtraj_complex",
        "competitor_selection_mdanalysis_complex",
    )
    print("-" * 86)

    # Section: Geometric calculations
    print_mem_line(
        "Center of Geometry",
        "competitor_center_molsysmt_public",
        "competitor_center_molsysmt_jit",
        "competitor_center_mdtraj",
        "competitor_center_mdanalysis",
    )
    print_mem_line(
        "RMSD Calculation",
        "competitor_rmsd_molsysmt_public",
        "competitor_rmsd_molsysmt_jit",
        "competitor_rmsd_mdtraj",
        "competitor_rmsd_mdanalysis",
    )
    print_mem_line(
        "Pairwise Distances",
        "competitor_distances_molsysmt_public",
        "competitor_distances_molsysmt_jit",
        "competitor_distances_mdtraj",
        "competitor_distances_mdanalysis",
    )

    print("=" * 86 + "\n")


if __name__ == "__main__":
    main()
