"""Measure explicit H5MSM 0.6 storage and public query costs for #256.

Run as a module under managed resource limits. Workers are sequential and fresh
per operation. Synthetic stored reports are evidence payloads, not scientifically
valid charge/type assignments. No timing threshold is a correctness gate.
"""

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import h5py
import numpy as np
import pandas as pd

import molsysmt as msm
from devtools.scripts.benchmark_native_copy import (
    _THREADS,
    _check_system,
    _expected,
    _fixture,
    _rss,
)
from devtools.scripts.study_h5msm_structure_chunks import _measure
from molsysmt import pyunitwizard as puw

_OPERATIONS = (
    "write",
    "read",
    "mechanics_layer",
    "forcefield",
    "charges",
    "coordinates",
)


def _atom_table(atoms):
    index = np.arange(atoms)
    result = pd.DataFrame(
        {
            "partial_charge": pd.array((index % 17 - 8) / 16, dtype="Float64"),
            "formal_charge": pd.array(index % 3 - 1, dtype="Int8"),
            "atom_ff_type": pd.array(np.where(index % 2, "OA", "C"), dtype="string"),
        }
    )
    result.iloc[-1] = pd.NA
    return result


def _mechanical_fixture(atoms, structures):
    system = _fixture(atoms, structures)
    mechanics = system.molecular_mechanics
    mechanics.atoms_ff = _atom_table(atoms)
    mechanics.forcefield = "synthetic_unresolved_request"
    mechanics.cutoff_distance = puw.quantity(12.0, "angstrom")
    mechanics.rigid_water = False
    for name in ("partial_charge_assignment", "atom_type_assignment"):
        setattr(
            mechanics,
            name,
            {
                "schema": "molsysmt.synthetic_storage_benchmark@1",
                "status": "synthetic_unvalidated",
                "software": {"fixture": "1"},
                "atom_indices": np.arange(atoms, dtype=np.int64),
                "values": np.arange(atoms, dtype=np.float64) / 16,
                "history": ("synthetic storage only",),
            },
        )
    return system


def _check_mechanics(mechanics, atoms):
    pd.testing.assert_frame_equal(mechanics.atoms_ff, _atom_table(atoms))
    assert mechanics.forcefield == "synthetic_unresolved_request"
    assert mechanics.rigid_water is False
    assert str(puw.get_unit(mechanics.cutoff_distance)) == "angstrom"
    np.testing.assert_allclose(
        puw.get_value(mechanics.cutoff_distance, to_unit="nm"), 1.2, rtol=1e-15, atol=0
    )
    for name in ("partial_charge_assignment", "atom_type_assignment"):
        report = getattr(mechanics, name)
        assert report["schema"] == "molsysmt.synthetic_storage_benchmark@1"
        assert report["status"] == "synthetic_unvalidated"
        assert report["software"] == {"fixture": "1"}
        assert report["history"] == ("synthetic storage only",)
        assert report["atom_indices"].dtype == np.dtype("int64")
        np.testing.assert_array_equal(report["atom_indices"], np.arange(atoms))
        np.testing.assert_array_equal(report["values"], np.arange(atoms) / 16)


def _file_storage(path):
    """Count actual allocated dataset bytes without loading any payload."""
    datasets = {}
    with h5py.File(path, "r") as file:
        assert file.attrs["version"] == "0.6"

        def visit(name, item):
            if isinstance(item, h5py.Dataset):
                datasets[name] = {
                    "shape": item.shape,
                    "dtype": str(item.dtype),
                    "storage_bytes": item.id.get_storage_size(),
                    "compression": item.compression,
                    "chunks": item.chunks,
                }

        file.visititems(visit)
    return {"file_bytes": path.stat().st_size, "datasets": datasets}


def _worker(atoms, structures, operation, repeats, path):
    chosen_atoms = [atoms - 2, 0, atoms - 2]
    chosen_structures = [structures - 1, 0, structures - 1]
    if operation == "write":
        source = _mechanical_fixture(atoms, structures)

        def prepare():
            path.unlink(missing_ok=True)
            return source

        def run(system):
            return msm.h5msm.write(system, path, format_version="0.6")

        def validate(output):
            assert Path(output) == path
            assert (
                msm.h5msm.read_axis_sizes(path)[("molecular_mechanics", None, "atom")]
                == atoms
            )

    else:

        def prepare():
            return path

        def run(filename):
            if operation == "read":
                return msm.h5msm.read(filename)
            if operation == "mechanics_layer":
                return msm.h5msm.read_layers(filename, layers="molecular_mechanics")[
                    "molecular_mechanics"
                ]
            if operation == "forcefield":
                return msm.get(filename, forcefield=True)
            if operation == "charges":
                return msm.get(
                    filename,
                    element="atom",
                    selection=chosen_atoms,
                    partial_charge=True,
                )
            return msm.get(
                filename,
                element="atom",
                selection=chosen_atoms,
                structure_indices=chosen_structures,
                coordinates=True,
            )

        def validate(output):
            if operation == "read":
                _check_system(output, atoms, structures, persisted=True)
                _check_mechanics(output.molecular_mechanics, atoms)
            elif operation == "mechanics_layer":
                _check_mechanics(output, atoms)
            elif operation == "forcefield":
                assert output == "synthetic_unresolved_request"
            elif operation == "charges":
                np.testing.assert_array_equal(
                    output, (np.asarray(chosen_atoms) % 17 - 8) / 16
                )
            else:
                assert puw.has_unit(output, "nm")
                np.testing.assert_allclose(
                    puw.get_value(output, to_unit="nm"),
                    _expected(atoms, chosen_structures, chosen_atoms),
                    rtol=1e-6,
                    atol=1e-6,
                )

    measurement = _measure(prepare, run, validate, repeats)
    return {
        "operation": operation,
        **measurement,
        "process_peak_rss_bytes": _rss("VmHWM"),
        **_file_storage(path),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case", action="append", help="Atoms x structures; repeatable."
    )
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument(
        "--max-coordinate-mib",
        type=int,
        default=64,
        help="Admission bound for float64 fixture coordinates; not a RAM reservation.",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", choices=_OPERATIONS, help=argparse.SUPPRESS)
    parser.add_argument("--file", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        cases = [
            tuple(map(int, item.split("x")))
            for item in (args.case or ["62x512", "10000x32"])
        ]
        if not 1 <= args.repeats <= 16 or not 1 <= args.max_coordinate_mib <= 1024:
            raise ValueError
        if any(
            len(case) != 2
            or min(case) < 3
            or case[0] * case[1] * 24 > args.max_coordinate_mib * 1024**2
            for case in cases
        ):
            raise ValueError
    except ValueError:
        parser.error(
            "Use at least three atoms/structures, 1–16 repeats and a 1–1024 MiB coordinate bound respected by every case."
        )
    if args.worker:
        if len(cases) != 1 or args.file is None:
            parser.error("A worker requires one case and --file.")
        print(json.dumps(_worker(*cases[0], args.worker, args.repeats, args.file)))
        return
    if args.output is None or args.output.exists():
        parser.error("An unused --output path is required.")
    root = Path(__file__).resolve().parents[2]
    result = {
        "schema_version": "molsysmt.h5msm_mechanics_benchmark@1",
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "source": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        "worktree_dirty": bool(
            subprocess.check_output(
                ["git", "-c", "core.fsmonitor=false", "status", "--porcelain"],
                cwd=root,
                text=True,
            ).strip()
        ),
        "implementation_sha256": {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in (
                "devtools/scripts/benchmark_h5msm_mechanics.py",
                "devtools/scripts/benchmark_native_copy.py",
                "devtools/scripts/study_h5msm_structure_chunks.py",
            )
        },
        "platform": platform.platform(),
        "cpu": next(
            (
                line.split(":", 1)[1].strip()
                for line in Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")
            ),
            platform.machine(),
        )
        if Path("/proc/cpuinfo").exists()
        else platform.processor() or platform.machine(),
        "python": platform.python_version(),
        "packages": {
            name: importlib.metadata.version(name)
            for name in ("numpy", "pandas", "pint", "h5py", "pyunitwizard")
        },
        "thread_environment": dict.fromkeys(_THREADS, "1"),
        "repeats": args.repeats,
        "measurement": "Sequential fresh worker per case/operation; one untimed warm-up, repeated untraced timing and a separate tracemalloc pass. Validation outside timing. File handles reopen per call. Warm/uncontrolled OS cache, no flush/fsync. Process high-water includes import, setup and validation; traced operation bytes exclude fixture setup and validation. Temporary files removed.",
        "scope": "Synthetic nullable mechanical tables and two typed evidence reports, plus stable inventory, chemistry, geometry and sparse parallel observations. Scientific assignments, arbitrary engine checkpoints, large-scale extrapolation and installed-client qualification are excluded. Mechanical queries decode the whole static mechanical domain, even for one scalar or a few atoms.",
        "units": {
            "coordinates": "nm",
            "time": "ps",
            "partial_charge": "elementary_charge",
            "stored_cutoff_distance": "angstrom",
        },
        "cases": [],
    }
    for atoms, structures in cases:
        case = {"n_atoms": atoms, "n_structures": structures, "operations": []}
        with tempfile.TemporaryDirectory(prefix="molsysmt256-storage-") as directory:
            for operation in _OPERATIONS:
                command = [
                    sys.executable,
                    "-m",
                    "devtools.scripts.benchmark_h5msm_mechanics",
                    "--worker",
                    operation,
                    "--case",
                    f"{atoms}x{structures}",
                    "--repeats",
                    str(args.repeats),
                    "--max-coordinate-mib",
                    str(args.max_coordinate_mib),
                    "--file",
                    str(Path(directory) / "system.h5msm"),
                ]
                process = subprocess.run(
                    command,
                    cwd=root,
                    env={**os.environ, **result["thread_environment"]},
                    text=True,
                    capture_output=True,
                )
                if process.stderr:
                    print(process.stderr, file=sys.stderr, end="")
                process.check_returncode()
                case["operations"].append(json.loads(process.stdout))
                print(f"Measured {atoms}x{structures}: {operation}", flush=True)
        result["cases"].append(case)
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
