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
_COPY_EDIT_OPERATIONS = _OPERATIONS[:4]
_WORKLOADS = ("baseline", "mutable_observables", "many_interactions")
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


def _busy_analysis(n_atoms, n_structures, *, changing):
    """Construct variable synthetic counts with typed columns, never all pairs."""
    width = min(128, n_atoms * (n_atoms - 1))
    n_relations = (
        min(width * n_structures, n_atoms * (n_atoms - 1)) if changing else width
    )
    codes = np.arange(n_relations, dtype=np.int64)
    first = codes // (n_atoms - 1)
    second = codes % (n_atoms - 1)
    second += second >= first
    counts = np.resize([width, 0, width // 2], n_structures - 1) * 2
    structures = np.repeat(np.arange(n_structures - 1), counts)
    offsets = np.r_[0, np.cumsum(counts)]
    local = np.arange(len(structures)) - np.repeat(offsets[:-1], counts)
    relations = local // 2
    if changing:
        relations = (structures * width + relations) % n_relations
    return msm.Interactions(
        n_atoms=n_atoms,
        n_structures=n_structures,
        evaluated_structure_indices=np.arange(n_structures - 1),
        relation_types=("synthetic_busy_pair",) * n_relations,
        relation_participant_offsets=np.arange(0, 2 * n_relations + 1, 2),
        participant_roles=("first", "second") * n_relations,
        participant_atom_offsets=np.arange(2 * n_relations + 1),
        participant_atoms=np.column_stack([first, second]).ravel(),
        occurrence_structures=structures,
        occurrence_relations=relations,
        occurrence_evidence=np.zeros(len(structures), dtype=np.int64),
        evidence_labels=("synthetic geometry",),
        measurements={"distance": 0.2 + 0.1 * (local % 2)},
        measure_units={"distance": "nm"},
        method="synthetic_copy_benchmark",
        software={"fixture": "1"},
    )


def _fixture(n_atoms, n_structures, workload="baseline"):
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
    result.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [0] * n_atoms
    )
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
    if workload == "mutable_observables":
        result.structures.velocities = puw.quantity(
            np.ones((n_structures, n_atoms, 3)), "nm/ps"
        )
        result.structures.b_factor = puw.quantity(
            np.full((n_structures, n_atoms), 0.04), "nm**2"
        )
        result.structures.occupancy = np.full((n_structures, n_atoms), 0.5)
        signal = np.arange(n_structures * min(n_atoms, 128), dtype=np.float64)
        result.extension_payload = {"signal": signal, "alias": signal, "owner": result}
    elif workload == "many_interactions":
        result.interactions = {
            **result.interactions,
            "reused": _busy_analysis(n_atoms, n_structures, changing=False),
            "changing": _busy_analysis(n_atoms, n_structures, changing=True),
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


def _mutable_arrays(system):
    """List only the extra observable/extension arrays defined by this fixture."""
    return [
        value
        for value in (
            system.structures._velocities,
            system.structures._b_factor,
            system.structures._occupancy,
            getattr(system, "extension_payload", {}).get("signal"),
        )
        if value is not None
    ]


def _mutable_bytes(*systems):
    owners = {}
    for system in systems:
        for value in _mutable_arrays(system):
            while isinstance(value.base, np.ndarray):
                value = value.base
            owners[id(value)] = value.nbytes
    return sum(owners.values())


def _check_workload(system, n_atoms, n_structures, workload, edited=()):
    if workload == "mutable_observables":
        assert puw.has_unit(system.structures.velocities, "nm/ps")
        assert puw.has_unit(system.structures.b_factor, "nm**2")
        np.testing.assert_array_equal(system.structures._velocities, 1.0)
        np.testing.assert_array_equal(system.structures._b_factor, 0.04)
        np.testing.assert_array_equal(system.structures.occupancy, 0.5)
        payload = system.extension_payload
        assert payload["owner"] is system
        assert payload["signal"] is payload["alias"]
        np.testing.assert_array_equal(
            payload["signal"], np.arange(n_structures * min(n_atoms, 128))
        )
    elif workload == "many_interactions":
        width = min(128, n_atoms * (n_atoms - 1))
        selected = list(dict.fromkeys([0, 1, n_structures // 2, n_structures - 1]))
        for name in ("reused", "changing"):
            analysis = system.interactions[name]
            np.testing.assert_array_equal(
                analysis.evaluated_structure_indices,
                [i for i in range(n_structures - 1) if i not in edited],
            )
            assert analysis.software == {"fixture": "1"}
            catalog_size = (
                min(width * n_structures, n_atoms * (n_atoms - 1))
                if name == "changing"
                else width
            )
            for structure in selected:
                count = (width, 0, width // 2)[structure % 3] * 2
                if structure == n_structures - 1 or structure in edited:
                    count = 0
                observations = analysis.query(structure_indices=[structure]).to_dict()
                assert len(observations["occurrence_indices"]) == count
                local = np.arange(count)
                expected_relations = local // 2
                if name == "changing":
                    expected_relations = (
                        structure * width + expected_relations
                    ) % catalog_size
                np.testing.assert_array_equal(
                    observations["relation_indices"], expected_relations
                )
                np.testing.assert_allclose(
                    observations["measurements"]["distance"], 0.2 + 0.1 * (local % 2)
                )


def _check_system(system, n_atoms, n_structures, edited=(), *, persisted=False):
    assert system.topology._molsys_owner_ref() is system
    assert not hasattr(system.topology, "_chemical_states_domain")
    assert system.chemical_states.n_atoms == n_atoms
    assert system.chemical_states.get(n_chemical_states=True) == 1
    assert (
        system.chemical_states.get(element="atom", formal_charge=True) == [0] * n_atoms
    )
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


def _operation(name, source, path, chunk, workload="baseline"):
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
        _check_workload(source, n_atoms, n_structures, workload)
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
            _check_workload(
                output,
                n_atoms,
                n_structures,
                workload,
                edited if name.startswith("edit_") else (),
            )
            for original, duplicate in zip(
                _mutable_arrays(source), _mutable_arrays(output)
            ):
                assert not np.shares_memory(original, duplicate)
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


def _worker(
    n_atoms,
    n_structures,
    operation,
    repeats,
    chunk,
    workload="baseline",
    warm_atom_index=False,
):
    source = _fixture(n_atoms, n_structures, workload)
    if warm_atom_index:
        for analysis in source.interactions.values():
            analysis.query(atom_indices=[0])
    with tempfile.TemporaryDirectory(prefix="molsysmt121-resident-") as directory:
        path = Path(directory) / "copy.h5msm"
        if operation == "h5msm_read":
            msm.convert(source, to_form="file:h5msm", output_filename=str(path))
        prepare, run, validate = _operation(operation, source, path, chunk, workload)
        subject = prepare()
        output = run(subject)  # One same-shape warm-up, including validation.
        validate(output)
        del subject, output
        samples = []
        geometry_bytes = None
        mutable_bytes = None
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
                mutable_bytes = _mutable_bytes(source, output)
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
            "source_mutable_array_bytes": _mutable_bytes(source),
            "source_and_result_unique_mutable_array_bytes": mutable_bytes,
            "source_analyses": {
                name: {
                    "relations": len(value.relation_types),
                    "occurrences": value.n_interactions,
                    "numeric_bytes": value.numeric_nbytes,
                }
                for name, value in source.interactions.items()
            },
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
    parser.add_argument("--workload", choices=_WORKLOADS, default="baseline")
    parser.add_argument("--warm-atom-index", action="store_true")
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
    if (
        args.workload != "baseline"
        and args.operation
        and any(name not in _COPY_EDIT_OPERATIONS for name in args.operation)
    ):
        parser.error("Additional workloads measure only copying and edits.")
    if args.warm_atom_index and args.workload != "many_interactions":
        parser.error("Atom-index warming requires the many_interactions workload.")
    if args.worker:
        if len(cases) != 1 or not args.operation or len(args.operation) != 1:
            parser.error("A worker requires exactly one case and one operation.")
        print(
            json.dumps(
                _worker(
                    *cases[0],
                    args.operation[0],
                    args.repeats,
                    args.chunk,
                    args.workload,
                    args.warm_atom_index,
                )
            )
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
        root / "molsysmt/native/topology.py",
        root / "molsysmt/native/chemical_states.py",
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
        "workload": args.workload,
        "atom_indexes_warmed": args.warm_atom_index,
        "iterator_chunk": args.chunk,
        "measurement": "fresh worker per case/operation; same-shape warm-up; median; fresh deferred edit subjects outside timing; separate tracemalloc pass",
        "rss_scope": "Linux address space, including imports, fixture and warm-up; before/retained counters are not operation peak; HWM includes earlier allocations; release need not return allocator arenas to OS",
        "byte_scope": "unique immutable coordinate/box bytes; excludes tables, analyses, Python headers and allocator overhead",
        "io_scope": "public H5MSM 0.5 conversion with coordinates, box, time, topology, chemical states and named analysis; warm OS cache; no fsync durability claim",
        "fixture": {
            "baseline": "linear float64 nm coordinates; one chemical state; one sparse analysis with parallel observations, evaluated-empty structures and a final unevaluated structure",
            "mutable_observables": "baseline plus float64 velocities (nm/ps), B factors (nm**2), occupancy and a mutable extension signal with aliases and an owner cycle",
            "many_interactions": "baseline plus two typed-column synthetic analyses, each up to 256 observations per evaluated structure; reused versus changing pair catalogs; no quadratic atom-pair allocation",
        }[args.workload],
        "cases": [],
    }
    env = {**os.environ, **result["thread_environment"]}
    for n_atoms, n_structures in cases:
        case = {"n_atoms": n_atoms, "n_structures": n_structures, "operations": []}
        operations = args.operation or (
            _OPERATIONS if args.workload == "baseline" else _COPY_EDIT_OPERATIONS
        )
        for operation in operations:
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
                "--workload",
                args.workload,
            ]
            if args.warm_atom_index:
                command.append("--warm-atom-index")
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
