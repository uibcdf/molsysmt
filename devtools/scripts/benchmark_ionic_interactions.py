#!/usr/bin/env python3
"""Measure ionic calculation, query, and H5MSM costs in isolated worker processes.

Synthetic separated Na/Cl pairs vary by frame, including evaluated-empty frames.
Optional protein fixtures use fixed coordinates and declared chemical states.
Repeating an ensemble is a scale control, not additional independent structures.
"""

import argparse
import gc
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import numpy as np


def _fixture(atoms, frames, charged_atoms=None):
    import molsysmt as msm
    from molsysmt.native import MolSys, Topology

    charged_atoms = atoms if charged_atoms is None else charged_atoms
    system = MolSys()
    system.topology = Topology(n_atoms=atoms)
    system.topology.atoms["atom_type"] = ["Na", "Cl"] * (charged_atoms // 2) + ["He"] * (atoms - charged_atoms)
    msm.set(system, element="atom", formal_charge=[1, -1] * (charged_atoms // 2) + [0] * (atoms - charged_atoms))
    system.topology._reference_chemical_state.connectivity_completeness = "complete"
    xyz = np.zeros((frames, atoms, 3))
    xyz[:, :, 0] = np.repeat(np.arange(atoms // 2) * 3., 2)[None]
    for frame in range(frames):
        shifts = np.full(charged_atoms // 2, .25)
        if frame % 5 == 1:
            shifts[:] = 1.
        elif frame % 5 == 2:
            shifts[np.arange(charged_atoms // 2) % 3 == 0] = .6
        xyz[frame, 1:charged_atoms:2, 0] += shifts
    system.structures.append(coordinates=msm.pyunitwizard.quantity(xyz, "nm"))
    return system


def _rss_bytes(field="VmRSS"):
    status = Path("/proc/self/status")
    if status.exists():
        for line in status.read_text().splitlines():
            if line.startswith(f"{field}:"):
                return int(line.split()[1]) * 1024
    return None


def _worker(args):
    import molsysmt as msm
    from molsysmt.form import _h5msm05_modular
    from molsysmt.interactions.ionic import _reducer
    from molsysmt.interactions.ionic.get_ionic_interactions import (
        get_ionic_interactions,
    )
    from molsysmt.physchem import get_charge_centers as charge_function
    from molsysmt.structure import _group_minimum_contacts

    # Warm compiled geometry using a tiny independent fixture before loading input.
    get_ionic_interactions(_fixture(2, 1), ".4 nm", pbc=False, heavy_mode="off")
    start = time.perf_counter()
    source = msm.convert(args.input, to_form="molsysmt.MolSys") if args.source == "native" else args.input
    source_load_s = time.perf_counter() - start
    stages = {}
    candidates = [0]

    def wrap(owner, name, label):
        original = getattr(owner, name)

        def measured(*positional, **keyword):
            before = time.perf_counter()
            result = original(*positional, **keyword)
            stages[label] = stages.get(label, 0.) + time.perf_counter() - before
            if label == "neighbors_s":
                candidates[0] += len(result[1])
            return result

        setattr(owner, name, measured)

    import importlib

    charge_module = importlib.import_module("molsysmt.physchem.get_charge_centers")
    # The public detector imports this function from its defining module per call.
    charge_module.get_charge_centers = charge_function
    wrap(charge_module, "get_charge_centers", "recognition_s")
    wrap(_h5msm05_modular, "_read_calculation_chemistry", "chemistry_read_s")
    wrap(_group_minimum_contacts, "neighbor_list_csr_multi", "neighbors_s")
    wrap(_reducer, "bounded_group_minimum_contacts", "group_geometry_s")
    wrap(_reducer._IonicReducer, "consume", "consume_s")
    wrap(_reducer._IonicReducer, "finalize", "packing_s")
    durations, observations, rss_before = [], [], []
    result = None
    with msm.configure.context(
        chunk_size=args.chunk, max_ram_usage=args.budget,
        emit_heavy_telemetry=False,
    ):
        for _ in range(args.repeats):
            result = None
            gc.collect()
            stages.clear()
            candidates[0] = 0
            rss_before.append(_rss_bytes())
            start = time.perf_counter()
            result = get_ionic_interactions(source, f"{args.threshold} nm", pbc=False, heavy_mode=args.mode)
            durations.append(time.perf_counter() - start)
            observations.append({**stages, "candidate_pairs": candidates[0]})
    bytes_before_index = result.numeric_nbytes
    start = time.perf_counter()
    result.query(atom_indices=[0])
    first_atom_query_s = time.perf_counter() - start
    bytes_after_index = result.numeric_nbytes

    def query_time(function):
        samples = []
        for _ in range(50):
            start = time.perf_counter()
            function()
            samples.append(time.perf_counter() - start)
        return float(np.median(samples))

    frame_query_s = query_time(lambda: result.query(structure_indices=[0]))
    atom_query_s = query_time(lambda: result.query(atom_indices=[0]))
    with tempfile.TemporaryDirectory() as directory:
        output = str(Path(directory) / "ionic.h5msm")
        start = time.perf_counter()
        msm.h5msm.write_layers(output, interactions={"ionic": result})
        write_s = time.perf_counter() - start
        file_bytes = Path(output).stat().st_size
        start = time.perf_counter()
        restored = msm.h5msm.read_layers(output, layers="interactions")["interactions"]["ionic"]
        read_s = time.perf_counter() - start
        np.testing.assert_array_equal(restored.occurrence_structures, result.occurrence_structures)
        np.testing.assert_allclose(restored.measurements["distance"], result.measurements["distance"])
    if args.dataset:
        from ionic_validation_systems import (
            cartesian_reference,
            observation_columns,
            prepare_system,
        )

        _, reference, xyz, _ = prepare_system(args.dataset)
        expected = cartesian_reference(reference, np.tile(xyz, (args.cycles, 1, 1)), args.threshold)
        actual = observation_columns(result, reference)
        assert actual.keys() == expected.keys() and result.n_interactions == len(expected)
        for key, value in expected.items():
            np.testing.assert_allclose(actual[key], value, atol=1e-12, rtol=0)
    grouped = {}
    for label in {key for row in observations for key in row}:
        grouped[label] = float(np.median([row.get(label, 0.) for row in observations]))
    grouped["group_reduction_s"] = grouped.get("group_geometry_s", 0.) - grouped.get("neighbors_s", 0.)
    grouped["validation_acceptance_accumulation_s"] = grouped.get("consume_s", 0.) - grouped.get("group_geometry_s", 0.)
    return {
        "source": args.source, "mode": args.mode, "source_load_s": source_load_s,
        "calculation_samples_s": durations, "calculation_median_s": float(np.median(durations)),
        "stage_medians": grouped, "occurrences": result.n_interactions,
        "relations": len(result.relation_types), "chunks": result.parameters["execution_chunks"],
        "numeric_bytes_before_index": bytes_before_index, "numeric_bytes_after_index": bytes_after_index,
        "rss_before_calculation_bytes": rss_before,
        # Linux VmHWM belongs to this address space. ru_maxrss can also include
        # the parent's pre-exec high-water mark when subprocess uses fork.
        "process_peak_rss_bytes": _rss_bytes("VmHWM"),
        "rusage_peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
        "frame_query_median_s": frame_query_s, "first_atom_query_s": first_atom_query_s,
        "atom_query_median_s": atom_query_s, "h5msm_write_s": write_s,
        "h5msm_read_s": read_s, "h5msm_bytes": file_bytes,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atoms", type=int, default=1000)
    parser.add_argument("--frames", type=int, default=300)
    parser.add_argument("--charged-atoms", type=int)
    parser.add_argument("--dataset", choices=["trp_cage", "villin"])
    parser.add_argument("--cycles", type=int, default=1)
    parser.add_argument("--threshold", type=float, default=.4)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--chunk", type=int, default=32)
    parser.add_argument("--budget", type=int, default=1024**3)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--input")
    parser.add_argument("--source", choices=["native", "file"])
    parser.add_argument("--mode", choices=["off", "force"])
    args = parser.parse_args()
    if args.cycles < 1 or not np.isfinite(args.threshold) or args.threshold <= 0:
        parser.error("Use a positive cycle count and finite positive threshold in nm.")
    if args.atoms < 2 or args.atoms % 2 or min(args.frames, args.repeats, args.chunk, args.budget) < 1:
        parser.error("Use an even positive atom count and positive frame/repetition/chunk/budget counts.")
    if args.charged_atoms is not None and (
        args.charged_atoms < 2 or args.charged_atoms % 2 or args.charged_atoms > args.atoms
    ):
        parser.error("charged-atoms must be an even count between 2 and atoms.")
    if args.input:
        print(json.dumps(_worker(args)))
        return
    import molsysmt as msm

    root = Path(__file__).resolve().parents[2]
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True).strip())
    results = []
    dataset_metadata = {}
    if args.dataset:
        from ionic_validation_systems import MANIFEST, prepare_system

        from molsysmt.native import Structures

        fixture, reference, xyz, _ = prepare_system(args.dataset)
        fixture.structures = Structures(coordinates=msm.pyunitwizard.quantity(
            np.tile(xyz, (args.cycles, 1, 1)), "nm"))
        args.atoms, args.frames = reference["atoms"], reference["structures"] * args.cycles
        args.charged_atoms = len(reference["charge_atoms"])
        dataset_metadata = {
            "dataset": args.dataset, "source_artifact": reference["path"],
            "source_sha256": reference["sha256"], "cycles": args.cycles,
            "independent_structures": reference["structures"],
            "chemical_state": json.loads(MANIFEST.read_text())["state_definition"],
            "rdkit": version("rdkit"),
            "oracle": "Fixed participant manifest and exhaustive Cartesian displacement calculation; verified outside timed calculation.",
        }
    else:
        fixture = _fixture(args.atoms, args.frames, args.charged_atoms)
    with tempfile.TemporaryDirectory() as directory:
        source = str(Path(directory) / "source.h5msm")
        msm.convert(fixture, to_form=source)
        for form in ("native", "file"):
            for mode in ("off", "force"):
                command = [
                    sys.executable, str(Path(__file__).resolve()), "--input", source,
                    "--source", form, "--mode", mode, "--atoms", str(args.atoms),
                    "--frames", str(args.frames), "--repeats", str(args.repeats),
                    "--chunk", str(args.chunk), "--budget", str(args.budget),
                    "--threshold", str(args.threshold),
                ]
                if args.dataset:
                    command.extend(["--dataset", args.dataset, "--cycles", str(args.cycles)])
                completed = subprocess.run(command, check=True, capture_output=True, text=True)
                results.append(json.loads(completed.stdout))
                print(f"Completed {form}/{mode}", file=sys.stderr, flush=True)
    report = {
        "date_utc": datetime.now(timezone.utc).isoformat(), "base_commit": commit,
        "worktree_dirty": dirty, "platform": platform.platform(),
        "python": platform.python_version(), "numpy": np.__version__, "h5py": version("h5py"),
        "molsysmt": msm.__version__, "atoms": args.atoms, "frames": args.frames,
        "charged_atoms": args.atoms if args.charged_atoms is None else args.charged_atoms,
        "cpu": next((line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines()
                     if line.startswith("model name")), "unknown"),
        "thread_environment": {name: os.environ.get(name) for name in (
            "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMBA_NUM_THREADS")},
        "implementation_sha256": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in (Path(__file__).resolve(),
                                               root / "molsysmt/interactions/ionic/get_ionic_interactions.py",
                                               root / "molsysmt/interactions/ionic/_reducer.py")},
        "coordinate_bytes": args.atoms * args.frames * 24, "repeats": args.repeats,
        "distance_threshold_nm": args.threshold,
        "chunk_size_limit": args.chunk, "ram_budget_bytes": args.budget,
        "warmup": "one tiny independent ionic calculation per worker; OS page cache uncontrolled",
        "rss_scope": "Linux VmHWM since worker exec through calculation, indexing, serialization and reload; includes source loading",
        "fixture": "protein coordinates with a declared chemical state; no PBC" if args.dataset else "synthetic independent Na/Cl pairs; empty and variable frames; no PBC",
        **dataset_metadata,
        "results": results,
    }
    if args.dataset:
        for path in (root / "devtools/scripts/ionic_validation_systems.py", MANIFEST):
            report["implementation_sha256"][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded)


if __name__ == "__main__":
    main()
