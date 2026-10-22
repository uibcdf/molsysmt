"""Measure resident native copying and its consumers for issue #121.

Each operation runs in a fresh subprocess. This exercises the production
MolSys/Structures implementation, independently of study_native_copy.py's
experimental layouts. No timing threshold is a correctness gate.
"""

import argparse
import gc
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import tempfile
import tracemalloc
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from time import perf_counter

import numpy as np

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSys

_OPERATIONS = (
    "deferred_copy",
    "eager_copy",
    "edit_one_atom",
    "edit_eight_structures",
    "selected_read",
    "full_read",
    "iterate_coordinates",
    "rust_distances",
    "h5msm_write",
    "h5msm_read",
)
_THREADS = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "RAYON_NUM_THREADS",
)


def _rss(field="VmRSS"):
    """Read Linux address-space counters; unavailable is not zero."""
    path = Path("/proc/self/status")
    if path.exists():
        for line in path.read_text().splitlines():
            if line.startswith(f"{field}:"):
                return int(line.split()[1]) * 1024
    return None


def _expected(n_atoms, structures, atoms):
    return (
        np.asarray(structures)[:, None, None] * n_atoms * 3
        + np.asarray(atoms)[None, :, None] * 3
        + np.arange(3)[None, None, :]
    ) * 1e-5


def _fixture(n_atoms, n_structures):
    result = MolSys(n_atoms=n_atoms)
    values = np.arange(n_structures * n_atoms * 3, dtype=np.float64)
    values *= 1e-5
    result.structures.coordinates = puw.quantity(
        values.reshape(n_structures, n_atoms, 3), "nm"
    )
    result.structures.box = puw.quantity(
        np.repeat((np.eye(3) * 10)[None], n_structures, axis=0), "nm"
    )
    result.structures.time = puw.quantity(np.arange(n_structures), "ps")
    result.topology._set_chemical_state_atom_attribute("formal_charge", [0] * n_atoms)
    records = [
        {
            "structure_index": structure,
            "interaction_type": "synthetic_pair",
            "participants": [
                {"role": "first", "atom_indices": [0]},
                {"role": "second", "atom_indices": [n_atoms - 1]},
            ],
            "measurements": {"distance": distance},
        }
        for structure in range(0, n_structures - 1, 3)
        for distance in (0.2, 0.3)
    ]
    result.interactions = {
        "pairs": msm.Interactions.from_records(
            records,
            n_atoms=n_atoms,
            n_structures=n_structures,
            evaluated_structure_indices=list(range(n_structures - 1)),
            method="synthetic_copy_benchmark",
            measure_units={"distance": "nm"},
            software={"fixture": "1"},
        )
    }
    return result


def _owners(*systems):
    """Count unique immutable geometry backing bytes, excluding object overhead."""
    owners = {}
    for system in systems:
        for name in ("_coordinates", "_box"):
            storage = getattr(system.structures, name)
            if storage is None:
                continue
            for block in storage._blocks:
                owner = block
                while isinstance(owner, np.ndarray) and owner.base is not None:
                    owner = owner.base
                if not isinstance(owner, bytes):
                    raise AssertionError("Geometry backing is not immutable bytes")
                owners[id(owner)] = len(owner)
    return owners


def _check_system(system, n_atoms, n_structures, edited=(), *, persisted=False):
    assert system.topology._molsys_owner_ref() is system
    assert system.chemical_states is system.topology._chemical_states_domain
    assert system.structures.n_atoms == n_atoms
    assert system.structures.n_structures == n_structures
    structures = list(dict.fromkeys([n_structures - 1, 0, n_structures // 2, *edited]))
    atoms = [n_atoms - 1, 0]
    expected = _expected(n_atoms, structures, atoms)
    for index, structure in enumerate(structures):
        if structure in edited:
            expected[index, 1] = [1, 2, 3]
    actual = system.structures.get_coordinates(
        indices=atoms, structure_indices=structures
    )
    assert puw.has_unit(actual, "nm")
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="nm"),
        expected,
        rtol=1e-6 if persisted else 0,
        atol=1e-6 if persisted else 0,
    )
    np.testing.assert_array_equal(
        system.interactions["pairs"].evaluated_structure_indices,
        [index for index in range(n_structures - 1) if index not in edited],
    )
    # Both parallel observations remain distinguishable through persistence.
    queried = system.interactions["pairs"].query(structure_indices=[0]).to_dict()
    expected_count = 0 if 0 in edited else 2
    assert len(queried["occurrence_indices"]) == expected_count
    if expected_count:
        np.testing.assert_array_equal(queried["occurrence_indices"], [0, 1])
    assert system.interactions["pairs"].software == {"fixture": "1"}


def _operation(name, source, path, chunk):
    n_atoms, n_structures = source.structures.n_atoms, source.structures.n_structures
    selected = [n_structures - 1, 0, n_structures // 2, 0]
    atoms = [n_atoms - 1, 0]
    edited = (
        [n_structures // 2]
        if name == "edit_one_atom"
        else list(range(min(8, n_structures)))
    )

    def prepare():
        if name.startswith("edit_"):
            return source.copy(deep=False)
        if name == "h5msm_write":
            path.unlink(missing_ok=True)
        return source

    def run(subject):
        if name in ("deferred_copy", "eager_copy"):
            return subject.copy(deep=name == "eager_copy")
        if name.startswith("edit_"):
            msm.set(
                subject,
                selection=[0],
                structure_indices=edited,
                coordinates=puw.quantity(
                    np.repeat([[[1.0, 2.0, 3.0]]], len(edited), axis=0), "nm"
                ),
            )
            return subject
        if name == "selected_read":
            return subject.structures.get(
                selection=atoms, structure_indices=selected, coordinates=True
            )
        if name == "full_read":
            return subject.structures.coordinates
        if name == "iterate_coordinates":
            total, count = 0.0, 0
            for coordinates in msm.Iterator(subject, chunk=chunk, coordinates=True):
                values = puw.get_value(coordinates, to_unit="nm")
                total += float(values.sum())
                count += len(values)
            return total, count
        if name == "rust_distances":
            return msm.structure.get_distances(
                subject, selection=[0], selection_2=[n_atoms - 1], pbc=False
            )
        if name == "h5msm_write":
            msm.convert(subject, to_form="file:h5msm", output_filename=str(path))
            return path.stat().st_size
        return msm.convert(str(path), to_form="molsysmt.MolSys")

    def validate(output):
        _check_system(source, n_atoms, n_structures)
        if name in ("deferred_copy", "eager_copy", "h5msm_read") or name.startswith(
            "edit_"
        ):
            _check_system(
                output,
                n_atoms,
                n_structures,
                edited if name.startswith("edit_") else (),
                persisted=name == "h5msm_read",
            )
            assert output is not source
            assert output.topology is not source.topology
        elif name in ("selected_read", "full_read"):
            assert puw.has_unit(output, "nm")
            if name == "selected_read":
                np.testing.assert_array_equal(
                    puw.get_value(output, to_unit="nm"),
                    _expected(n_atoms, selected, atoms),
                )
            else:
                assert output.shape == (n_structures, n_atoms, 3)
                np.testing.assert_array_equal(
                    puw.get_value(output, to_unit="nm")[selected][:, atoms],
                    _expected(n_atoms, selected, atoms),
                )
        elif name == "iterate_coordinates":
            size = n_structures * n_atoms * 3
            np.testing.assert_allclose(
                output[0], size * (size - 1) / 2 * 1e-5, rtol=1e-12
            )
            assert output[1] == n_structures
        elif name == "rust_distances":
            assert puw.has_unit(output, "nm")
            values = puw.get_value(output, to_unit="nm")
            assert values.size == n_structures
            np.testing.assert_allclose(
                values, np.sqrt(3) * (n_atoms - 1) * 3e-5, rtol=1e-9
            )
        else:
            _check_system(
                msm.convert(str(path), to_form="molsysmt.MolSys"),
                n_atoms,
                n_structures,
                persisted=True,
            )

    return prepare, run, validate


def _worker(n_atoms, n_structures, operation, repeats, chunk):
    source = _fixture(n_atoms, n_structures)
    with tempfile.TemporaryDirectory(prefix="molsysmt121-resident-") as directory:
        path = Path(directory) / "copy.h5msm"
        if operation == "h5msm_read":
            msm.convert(source, to_form="file:h5msm", output_filename=str(path))
        prepare, run, validate = _operation(operation, source, path, chunk)
        subject = prepare()
        output = run(subject)  # One same-shape warm-up, including validation.
        validate(output)
        del subject, output
        samples = []
        geometry_bytes = None
        for _ in range(repeats):
            subject = prepare()
            gc.collect()
            rss_before = _rss()
            start = perf_counter()
            output = run(subject)
            elapsed = perf_counter() - start
            rss_after, hwm = _rss(), _rss("VmHWM")
            if isinstance(output, MolSys):
                geometry_bytes = sum(_owners(source, output).values())
            samples.append(
                {
                    "seconds": elapsed,
                    "rss_before_bytes": rss_before,
                    "rss_retained_bytes": rss_after,
                    "process_hwm_bytes": hwm,
                }
            )
            validate(output)
            del subject, output
        subject = prepare()
        gc.collect()
        tracemalloc.start()
        try:
            output = run(subject)
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        validate(output)
        del subject, output
        gc.collect()
        source_bytes = sum(_owners(source).values())
        return {
            "operation": operation,
            "median_seconds": median(sample["seconds"] for sample in samples),
            "samples": samples,
            "traced_operation_peak_bytes": peak,
            "source_geometry_bytes": source_bytes,
            "source_and_result_unique_geometry_bytes": geometry_bytes,
            "rss_after_releasing_result_bytes": _rss(),
            "file_bytes": path.stat().st_size if path.exists() else None,
            "coordinate_block_structures": source.structures._coordinates._block_size,
            "coordinate_blocks": len(source.structures._coordinates._blocks),
        }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case", action="append", help="Atoms x structures; repeatable."
    )
    parser.add_argument("--operation", action="append", choices=_OPERATIONS)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--chunk", type=int, default=32)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        cases = [
            tuple(map(int, case.split("x")))
            for case in (args.case or ["62x5000", "10000x1000", "100000x100"])
        ]
        if any(len(case) != 2 or min(case) < 3 for case in cases):
            raise ValueError
    except ValueError:
        parser.error("Cases require at least three atoms and three structures.")
    if args.repeats < 1 or args.chunk < 1:
        parser.error("Repeats and chunk size must be positive.")
    if args.worker:
        if len(cases) != 1 or not args.operation or len(args.operation) != 1:
            parser.error("A worker requires exactly one case and one operation.")
        print(
            json.dumps(_worker(*cases[0], args.operation[0], args.repeats, args.chunk))
        )
        return
    if args.output is None:
        parser.error("--output is required for a campaign.")
    root = Path(__file__).resolve().parents[2]
    files = [
        Path(__file__),
        *[
            root / "molsysmt/native" / name
            for name in (
                "_structure_array.py",
                "_copy.py",
                "structures.py",
                "molsys.py",
            )
        ],
        root / "molsysmt/interactions/result.py",
        root / "molsysmt/form/_h5msm05_structures.py",
    ]
    result = {
        "scope": "production resident native paths; synthetic data; no installed-client qualification",
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        "worktree_dirty": bool(
            subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=root, text=True
            ).strip()
        ),
        "implementation_sha256": {
            str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in files
        },
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {
            name: importlib.metadata.version(name)
            for name in (
                "numpy",
                "pandas",
                "pyunitwizard",
                "h5py",
                "argdigest",
                "smonitor",
            )
        },
        "cpu": next(
            (
                line.split(":", 1)[1].strip()
                for line in Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")
            ),
            platform.machine(),
        )
        if Path("/proc/cpuinfo").exists()
        else platform.machine(),
        "logical_cpus": os.cpu_count(),
        "thread_environment": dict.fromkeys(_THREADS, "1"),
        "repeats": args.repeats,
        "iterator_chunk": args.chunk,
        "measurement": "fresh worker per case/operation; same-shape warm-up; median; fresh deferred edit subjects outside timing; separate tracemalloc pass",
        "rss_scope": "Linux address space, including imports, fixture and warm-up; before/retained counters are not operation peak; HWM includes earlier allocations; release need not return allocator arenas to OS",
        "byte_scope": "unique immutable coordinate/box bytes; excludes tables, analyses, Python headers and allocator overhead",
        "io_scope": "public H5MSM 0.5 conversion with coordinates, box, time, topology, chemical states and named analysis; warm OS cache; no fsync durability claim",
        "fixture": "linear float64 nm coordinates; one chemical state; one sparse analysis with parallel observations, evaluated-empty structures, final unevaluated structure; no velocities or arbitrary extension metadata",
        "cases": [],
    }
    env = {**os.environ, **result["thread_environment"]}
    for n_atoms, n_structures in cases:
        case = {"n_atoms": n_atoms, "n_structures": n_structures, "operations": []}
        for operation in args.operation or _OPERATIONS:
            command = [
                sys.executable,
                str(Path(__file__).resolve()),
                "--worker",
                "--case",
                f"{n_atoms}x{n_structures}",
                "--operation",
                operation,
                "--repeats",
                str(args.repeats),
                "--chunk",
                str(args.chunk),
            ]
            completed = subprocess.run(
                command, check=False, text=True, capture_output=True, env=env
            )
            if completed.stderr:
                print(completed.stderr, file=sys.stderr, end="")
            completed.check_returncode()
            case["operations"].append(json.loads(completed.stdout))
            print(f"Measured {n_atoms}x{n_structures}: {operation}", flush=True)
        result["cases"].append(case)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
