"""Compare experimental coordinate ownership layouts for issue #121.

This is a study tool, not a native form or a public copy implementation. It
isolates contiguous versus structure-block storage. Non-coordinate fields are
copied eagerly using the existing native implementation. This tool does not
claim chemical copy-on-write, arbitrary table tracking, or subclass support.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import tempfile
import tracemalloc
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from time import perf_counter

import numpy as np

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest.argument.coordinates import digest_coordinates
from molsysmt.native import MolSys, Structures


def _freeze(array):
    """Own immutable numeric bytes; never freeze the caller's writable alias."""
    return np.frombuffer(array.tobytes(), dtype=array.dtype).reshape(array.shape)


def _axis(indices, size):
    if indices is None:
        return np.arange(size, dtype=np.int64)
    array = np.asarray(indices)
    if array.size == 0:
        array = np.asarray(indices, dtype=np.int64)
    if array.ndim == 0:
        array = array.reshape(1)
    if array.ndim != 1 or array.dtype.kind not in "iu":
        raise ValueError("Selections must contain integer indices.")
    if np.any(array < 0) or np.any(array >= size):
        raise ValueError("Selection contains an out-of-range index.")
    return array.astype(np.int64, copy=False)


class _Coordinates:
    """Experimental immutable coordinate blocks; raw values always use nm."""

    def __init__(self, values, block_size, shared_base=False):
        values = np.asarray(values, dtype=np.float64)
        if values.ndim != 3 or values.shape[2] != 3 or block_size <= 0:
            raise ValueError(
                "Expected (n_structures, n_atoms, 3) and a positive block size."
            )
        self.shape = values.shape
        self.block_size = block_size
        self._base = _freeze(values) if shared_base else None
        self.blocks = tuple(
            self._base[start : start + block_size].view()
            if shared_base
            else _freeze(values[start : start + block_size])
            for start in range(0, values.shape[0], block_size)
        )

    def _byte_owners(self):
        owners = {}
        for block in self.blocks:
            owner = block
            while isinstance(owner, np.ndarray) and owner.base is not None:
                owner = owner.base
            if not isinstance(owner, bytes):
                raise AssertionError("Study storage must have immutable bytes owners.")
            owners[id(owner)] = len(owner)
        return owners

    def _fork(self):
        clone = object.__new__(type(self))
        clone.__dict__ = self.__dict__.copy()
        return clone

    def _read(self, structure_indices=None, atom_indices=None):
        # An unfragmented full read reuses bytes with its own ndarray header.
        if structure_indices is None and atom_indices is None:
            if self._base is not None:
                return self._base.view()
            if not self.blocks:
                return np.empty(self.shape, dtype=np.float64)
            if len(self.blocks) == 1:
                return self.blocks[0].view()
            return np.concatenate(self.blocks, axis=0)
        structures = _axis(structure_indices, self.shape[0])
        atoms = _axis(atom_indices, self.shape[1])
        output = np.empty((structures.size, atoms.size, 3), dtype=np.float64)
        for target, index in enumerate(structures):
            block, local = divmod(int(index), self.block_size)
            output[target] = self.blocks[block][local, atoms]
        return output

    def _owned_read(self):
        values = self._read()
        return values if values.flags.owndata else values.copy()

    def _replace(self, values, structure_indices, atom_indices):
        structures = _axis(structure_indices, self.shape[0])
        atoms = _axis(atom_indices, self.shape[1])
        values = np.asarray(values, dtype=np.float64)
        if values.shape != (structures.size, atoms.size, 3):
            raise ValueError("Replacement shape must match both selected axes.")
        if not structures.size or not atoms.size:
            return self, 0
        blocks = list(self.blocks)
        block_ids = structures // self.block_size
        replacement_bytes = 0
        for block_id in np.unique(block_ids):
            scratch = blocks[block_id].copy()
            # Preserve order and last assignment for repeated structure indices.
            for offset in np.flatnonzero(block_ids == block_id):
                local = int(structures[offset]) % self.block_size
                scratch[local, atoms] = values[offset]
            blocks[block_id] = _freeze(scratch)
            replacement_bytes += blocks[block_id].nbytes
            del scratch
        clone = self._fork()
        clone.blocks = tuple(blocks)
        clone._base = None
        return clone, replacement_bytes


class _Branch:
    """A restricted study branch, deliberately not exposed as a native form."""

    def __init__(self, source, block_size, shared_base=False):
        if source.topology is None or source.structures is None:
            raise ValueError("The study requires a complete coordinate-bearing MolSys.")
        values = puw.get_value(source.structures.coordinates, to_unit="nm")
        self._coordinates = _Coordinates(values, block_size, shared_base)
        self._topology = source.topology.copy()
        self._mechanics = source.molecular_mechanics.copy()
        self._association = deepcopy(source._structure_chemical_state_indices)
        self._structure_state = deepcopy(
            {
                key: value
                for key, value in vars(source.structures).items()
                if key != "_coordinates"
            }
        )
        # Existing invalidation snapshots already detach scientific metadata.
        # This is NOT a complete implementation of Interactions.__copy__.
        self._analyses = {
            name: result.invalidate_structures([])
            for name, result in source.interactions.items()
        }

    def _fork(self):
        clone = object.__new__(type(self))
        clone._coordinates = self._coordinates._fork()
        clone._topology = self._topology.copy()
        clone._mechanics = self._mechanics.copy()
        clone._association = deepcopy(self._association)
        clone._structure_state = deepcopy(self._structure_state)
        clone._analyses = {
            name: result.invalidate_structures([])
            for name, result in self._analyses.items()
        }
        return clone

    def _get_coordinates(self, structure_indices=None, atom_indices=None):
        return puw.standardize(
            puw.quantity(self._coordinates._read(structure_indices, atom_indices), "nm")
        )

    def _get_owned_coordinates(self):
        return puw.standardize(puw.quantity(self._coordinates._owned_read(), "nm"))

    def _set_coordinates(self, value, structure_indices, atom_indices):
        # Reuse the real coordinate value contract, then extract explicit nm.
        normalized = digest_coordinates(value)
        values = puw.get_value(normalized, to_unit="nm")
        coordinates, replacement_bytes = self._coordinates._replace(
            values, structure_indices, atom_indices
        )
        if coordinates is self._coordinates:
            return 0
        structures = _axis(structure_indices, coordinates.shape[0])
        analyses = {
            name: result.invalidate_structures(structures)
            for name, result in self._analyses.items()
        }
        self._coordinates, self._analyses = coordinates, analyses
        return replacement_bytes

    def _set_formal_charge(self, atom_indices, values):
        atoms = _axis(atom_indices, self._coordinates.shape[1])
        if not atoms.size:
            return
        candidate = self._topology.copy()
        candidate._set_chemical_state_atom_attribute(
            "formal_charge", values, atom_indices=atoms
        )
        structures = np.arange(self._coordinates.shape[0], dtype=np.int64)
        analyses = {
            name: result.invalidate_structures(structures)
            for name, result in self._analyses.items()
        }
        self._topology, self._analyses = candidate, analyses

    def _to_native(self):
        # This path explicitly materializes coordinates before public H5MSM I/O.
        topology = self._topology.copy()
        structures = object.__new__(Structures)
        structures.__dict__ = deepcopy(self._structure_state)
        values = self._coordinates._owned_read()
        # Existing native setters enable writes; they cannot edit bytes-backed
        # immutable views. This bridge pays for owned mutable native storage.
        structures.coordinates = puw.quantity(values, "nm")
        result = MolSys._from_partial_domains(
            topology=topology,
            chemical_states=topology._chemical_states_domain,
            structures=structures,
        )
        result.molecular_mechanics = self._mechanics.copy()
        result._structure_chemical_state_indices = deepcopy(self._association)
        result.interactions = {
            name: analysis.invalidate_structures([])
            for name, analysis in self._analyses.items()
        }
        return result


def _fixture(n_atoms, n_structures):
    source = MolSys(n_atoms=n_atoms)
    values = (
        np.arange(n_structures * n_atoms * 3, dtype=np.float64).reshape(
            n_structures, n_atoms, 3
        )
        * 1e-5
    )
    source.structures.coordinates = puw.quantity(values, "nm")
    source.structures.time = puw.quantity(np.arange(n_structures), "ps")
    source.topology._set_chemical_state_atom_attribute("formal_charge", [0] * n_atoms)
    source.interactions = {
        "pairs": msm.Interactions.from_records(
            [
                {
                    "structure_index": index,
                    "interaction_type": "synthetic_pair",
                    "participants": [
                        {"role": "a", "atom_indices": [0]},
                        {"role": "b", "atom_indices": [n_atoms - 1]},
                    ],
                }
                for index in range(0, n_structures - 1, 3)
            ],
            n_atoms=n_atoms,
            n_structures=n_structures,
            evaluated_structure_indices=list(range(n_structures - 1)),
            method="copy_study",
            parameters={"nested": {"cutoff": 0.5}},
            software={"fixture": "1"},
        )
    }
    return source, values


def _measure(prepare, operation, repeats):
    subject = prepare()
    operation(subject)  # One untimed warm-up, with a fresh subject below.
    del subject
    samples = []
    for _ in range(repeats):
        subject = prepare()
        start = perf_counter()
        output = operation(subject)
        samples.append(perf_counter() - start)
        del output, subject
    subject = prepare()
    tracemalloc.start()
    try:
        output = operation(subject)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    del output, subject
    return {
        "median_seconds": median(samples),
        "samples_seconds": samples,
        "traced_peak_bytes": peak,
    }


def _case(
    n_atoms, n_structures, block_size, repeats, io, shared_base=False, reads_only=False
):
    source, truth = _fixture(n_atoms, n_structures)
    base = _Branch(source, block_size, shared_base)
    selected = [n_structures - 1, 0, n_structures // 2, 0]
    atoms = [n_atoms - 1, 0]
    np.testing.assert_array_equal(
        puw.get_value(base._get_coordinates(selected, atoms), to_unit="nm"),
        truth[selected][:, atoms],
    )
    edit_structures = [n_structures // 2]
    edit_atoms = [0]
    edit_values = puw.quantity([[[1.0, 2.0, 3.0]]], "nm")
    batch_structures = list(range(min(8, n_structures)))
    batch_values = puw.quantity(
        np.repeat([[[1.0, 2.0, 3.0]]], len(batch_structures), axis=0), "nm"
    )

    def fork_then_edit(branch):
        clone = branch._fork()
        clone._set_coordinates(edit_values, edit_structures, edit_atoms)
        return clone

    def scan(branch):
        return sum(float(block.sum()) for block in branch._coordinates.blocks)

    def repeat_edits(branch):
        for index in batch_structures:
            branch._set_coordinates(edit_values, [index], edit_atoms)
        return branch

    operations = {
        "capture_and_freeze": (
            lambda: source,
            lambda item: _Branch(item, block_size, shared_base),
        ),
        "coordinate_handle_fork": (
            lambda: base._coordinates,
            lambda coordinates: coordinates._fork(),
        ),
        "fork": (lambda: base, lambda branch: branch._fork()),
        "edit_one_atom": (
            base._fork,
            lambda branch: branch._set_coordinates(
                edit_values, edit_structures, edit_atoms
            ),
        ),
        "fork_then_edit": (lambda: base, fork_then_edit),
        "batched_eight_edits": (
            base._fork,
            lambda branch: branch._set_coordinates(
                batch_values, batch_structures, edit_atoms
            ),
        ),
        "repeated_eight_edits": (base._fork, repeat_edits),
        "dense_edit": (
            base._fork,
            lambda branch: branch._set_coordinates(
                puw.quantity(np.zeros_like(truth), "nm"), None, None
            ),
        ),
        "selected_read": (
            lambda: base,
            lambda branch: branch._get_coordinates(selected, atoms),
        ),
        "full_read": (lambda: base, lambda branch: branch._get_coordinates()),
        "owned_full_read": (
            lambda: base,
            lambda branch: branch._get_owned_coordinates(),
        ),
        "one_structure_read": (
            lambda: base,
            lambda branch: branch._get_coordinates(edit_structures),
        ),
        "nonconsecutive_structures_read": (
            lambda: base,
            lambda branch: branch._get_coordinates(selected),
        ),
        "full_read_after_edit": (
            lambda: fork_then_edit(base),
            lambda branch: branch._get_coordinates(),
        ),
        "block_scan": (lambda: base, scan),
    }
    if reads_only:
        operations = {
            name: operations[name]
            for name in (
                "selected_read",
                "full_read",
                "owned_full_read",
                "one_structure_read",
                "nonconsecutive_structures_read",
                "full_read_after_edit",
                "block_scan",
            )
        }
    results = {
        name: _measure(*functions, repeats) for name, functions in operations.items()
    }
    clone = base._fork()
    replacement_bytes = clone._set_coordinates(edit_values, edit_structures, edit_atoms)
    referenced_bytes = sum(clone._coordinates._byte_owners().values())
    pair_owners = base._coordinates._byte_owners() | clone._coordinates._byte_owners()
    # Account for retained backing bytes, not only the active slice lengths.
    retired, _ = base._coordinates._replace(
        np.zeros((n_structures - 1, n_atoms, 3)),
        np.arange(n_structures - 1),
        np.arange(n_atoms),
    )
    retirement_bytes = sum(retired._byte_owners().values())
    del retired
    expected = truth.copy()
    expected[edit_structures[0], 0] = [1.0, 2.0, 3.0]
    np.testing.assert_array_equal(
        puw.get_value(clone._get_coordinates(), to_unit="nm"), expected
    )
    np.testing.assert_array_equal(
        puw.get_value(base._get_coordinates(), to_unit="nm"), truth
    )
    file_bytes = None
    if io:
        with tempfile.TemporaryDirectory(prefix="molsysmt121-") as directory:
            path = Path(directory) / "branch.h5msm"

            def persist(branch):
                msm.convert(
                    branch._to_native(), to_form="file:h5msm", output_filename=str(path)
                )
                return path.stat().st_size

            def prepare_write():
                path.unlink(missing_ok=True)
                return clone

            results["materialize_and_public_h5msm_write"] = _measure(
                prepare_write, persist, repeats
            )
            file_bytes = path.stat().st_size
            restored = msm.convert(str(path), to_form="molsysmt.MolSys")
            np.testing.assert_allclose(
                puw.get_value(restored.structures.coordinates, to_unit="nm"),
                expected,
                rtol=1e-6,
                atol=1e-6,
            )
            np.testing.assert_array_equal(
                restored.interactions["pairs"].evaluated_structure_indices,
                clone._analyses["pairs"].evaluated_structure_indices,
            )
    return {
        "n_atoms": n_atoms,
        "n_structures": n_structures,
        "block_structures": block_size,
        "layout": (
            "contiguous"
            if block_size >= n_structures
            else "shared_base_blocks"
            if shared_base
            else "separate_blocks"
        ),
        "source_coordinate_bytes": truth.nbytes,
        "replacement_coordinate_bytes": replacement_bytes,
        "edited_branch_referenced_coordinate_bytes": referenced_bytes,
        "parent_and_edited_branch_unique_coordinate_bytes": sum(pair_owners.values()),
        "referenced_bytes_after_replacing_all_but_last_structure": retirement_bytes,
        "file_bytes": file_bytes,
        "operations": results,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case", action="append", help="Atoms x structures, repeatable."
    )
    parser.add_argument("--blocks", default="1,8,32")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--io", action="store_true")
    parser.add_argument("--reads-only", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.io and args.reads_only:
        parser.error("The read-only campaign does not repeat H5MSM writes.")
    cases = [
        tuple(map(int, value.split("x")))
        for value in (args.case or ["62x5000", "10000x128", "100000x64"])
    ]
    if args.repeats < 1 or any(len(case) != 2 or min(case) < 2 for case in cases):
        parser.error(
            "Use positive repeats and cases with at least two atoms/structures."
        )
    root = Path(__file__).resolve().parents[2]
    result = {
        "scope": "experimental layouts, not native API qualification",
        "campaign": "reads_only" if args.reads_only else "complete",
        "units": {"coordinates": "nm", "time": "ps"},
        "python": platform.python_version(),
        "numpy": np.__version__,
        "packages": {
            name: importlib.metadata.version(name)
            for name in ("pandas", "pyunitwizard", "h5py", "argdigest")
        },
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "cpu": platform.processor() or platform.machine(),
        "logical_cpus": os.cpu_count(),
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        "study_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_worktree_dirty": bool(
            subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=root, text=True
            ).strip()
        ),
        "measurement": "one warm-up; fresh edit subjects; median; separate tracemalloc pass, not RSS",
        "chemistry_policy": "eager native topology/chemistry copy in all contenders",
        "io_policy": "public H5MSM write after complete coordinate materialization",
        "cases": [],
    }
    for n_atoms, n_structures in cases:
        for block in dict.fromkeys([n_structures, *map(int, args.blocks.split(","))]):
            for shared_base in [False, True] if block < n_structures else [False]:
                result["cases"].append(
                    _case(
                        n_atoms,
                        n_structures,
                        block,
                        args.repeats,
                        args.io,
                        shared_base,
                        args.reads_only,
                    )
                )
                print(
                    f"Measured {n_atoms}x{n_structures}, block={block}, "
                    f"shared_base={shared_base}",
                    flush=True,
                )
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Wrote {len(result['cases'])} study cases to {args.output}")


if __name__ == "__main__":
    main()
