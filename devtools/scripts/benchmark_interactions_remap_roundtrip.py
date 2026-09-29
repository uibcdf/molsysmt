#!/usr/bin/env python3
"""Probe repeated source-index edits, typed map persistence, and compaction."""

from __future__ import annotations

import json
import platform
import tempfile
from collections import Counter
from pathlib import Path

import h5py
import numpy as np
from benchmark_interactions_contract import (
    METHOD,
    UNITS,
    _record_atoms,
    expected,
    generate_fixture,
    materialize,
)
from benchmark_interactions_flat_blocks import write_flat_file
from benchmark_interactions_flat_edits import OverlayReader
from benchmark_interactions_structural_edits import (
    RemappedView,
    _check,
    _drop_atom,
    _drop_frame,
)

import molsysmt as msm


def _reorder_frames(records, evaluated, order):
    inverse = {old: new for new, old in enumerate(order)}
    transformed = [{**row, "structure_index": inverse[row["structure_index"]]}
                   for row in records]
    coverage = sorted(inverse[frame] for frame in evaluated)
    return transformed, coverage


def _reorder_atoms(records, order):
    inverse = {old: new for new, old in enumerate(order)}
    return [{**row, "participants": [
        {**part, "atom_indices": [inverse[atom]
                                    for atom in part["atom_indices"]]}
        for part in row["participants"]
    ]} for row in records]


def _insert_frame(records, evaluated, position, evaluated_new):
    transformed = [{**row, "structure_index": row["structure_index"]
                    + (row["structure_index"] >= position)} for row in records]
    coverage = [frame + (frame >= position) for frame in evaluated]
    if evaluated_new:
        coverage.append(position)
    return transformed, sorted(coverage)


def _save_maps(path, view):
    with h5py.File(path, "r+") as file:
        group = file.create_group("remap_probe")
        group.attrs["schema_version"] = 1
        group.create_dataset("current_to_storage_frames", data=np.asarray([
            -1 if value is None else value
            for value in view.current_to_storage_frames
        ], dtype=np.int64))
        group.create_dataset("current_to_storage_atoms",
                             data=np.asarray(view.current_to_storage_atoms,
                                             dtype=np.int64))
        group.create_dataset("appended_empty_frames",
                             data=np.asarray(sorted(view.appended), dtype=np.int64))
        group.create_dataset("invalidated_storage_frames",
                             data=np.asarray(sorted(view.invalidated), dtype=np.int64))


def _load_maps(reader):
    group = reader.file["remap_probe"]
    if group.attrs["schema_version"] != 1:
        raise AssertionError("unsupported prototype remap schema")
    frames = [None if value == -1 else int(value)
              for value in group["current_to_storage_frames"][:]]
    atoms = group["current_to_storage_atoms"][:].tolist()
    view = RemappedView(reader, len(atoms), len(frames))
    view.current_to_storage_frames = frames
    view.current_to_storage_atoms = atoms
    view.appended = {int(frame): []
                     for frame in group["appended_empty_frames"][:]}
    view.invalidated = set(int(frame)
                           for frame in group["invalidated_storage_frames"][:])
    view._refresh()
    return view


def main():
    n_frames, n_atoms = 1000, 500
    records, evaluated = generate_fixture(n_frames, n_atoms, 8, "mixed", 251)
    parallel = [row for row in records if row["structure_index"] == 2][:2]
    if len(parallel) != 2 or parallel[0]["participants"] != parallel[1]["participants"]:
        raise AssertionError("fixture has no parallel observation pair")
    protected = _record_atoms(parallel[0])
    atoms_to_drop = [atom for atom in (41, 0, 100, 200, 300)
                     if atom not in protected][:2]
    if len(atoms_to_drop) != 2:
        raise AssertionError("cannot select atoms outside parallel relation")
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "base.h5i"
        write_flat_file(path, records, evaluated, n_frames, n_atoms, 100)
        base_file_bytes = path.stat().st_size
        reader = OverlayReader(path)
        view = RemappedView(reader, n_atoms, n_frames)
        try:
            _check(view, records, evaluated, "start")
            for original_atom in atoms_to_drop:
                current_atom = view.current_to_storage_atoms.index(original_atom)
                view.drop_atom(current_atom)
                records = _drop_atom(records, current_atom)
                n_atoms -= 1
                _check(view, records, evaluated, "drop_atom")
            for frame in (17, 200):
                view.drop_frame(frame)
                records, evaluated = _drop_frame(records, evaluated, frame)
                n_frames -= 1
                _check(view, records, evaluated, "drop_frame")
            frame_order = list(range(n_frames))
            frame_order[0], frame_order[-1] = frame_order[-1], frame_order[0]
            view.current_to_storage_frames = [
                view.current_to_storage_frames[index] for index in frame_order
            ]
            view._refresh()
            records, evaluated = _reorder_frames(records, evaluated, frame_order)
            _check(view, records, evaluated, "reorder_frames")
            atom_order = list(range(n_atoms))
            atom_order[0], atom_order[-1] = atom_order[-1], atom_order[0]
            view.current_to_storage_atoms = [
                view.current_to_storage_atoms[index] for index in atom_order
            ]
            view._refresh()
            records = _reorder_atoms(records, atom_order)
            _check(view, records, evaluated, "reorder_atoms")
            for position, evaluated_new in ((5, True), (6, False)):
                view.current_to_storage_frames.insert(position, None)
                view.appended = {frame + (frame >= position): rows
                                 for frame, rows in view.appended.items()}
                if evaluated_new:
                    view.appended[position] = []
                view._refresh()
                records, evaluated = _insert_frame(
                    records, evaluated, position, evaluated_new
                )
                n_frames += 1
                _check(view, records, evaluated, "insert_frame")
            if view.query_frame(5) != ([5], Counter()):
                raise AssertionError("inserted evaluated-empty frame changed")
            if view.query_frame(6) != ([], Counter()):
                raise AssertionError("inserted unevaluated frame changed")
        finally:
            reader.close()
        _save_maps(path, view)
        reader = OverlayReader(path)
        try:
            loaded = _load_maps(reader)
            _check(loaded, records, evaluated, "loaded_maps")
            for frame in (2, 5, 6, 17, 200, n_frames - 1):
                if loaded.query_frame(frame) != expected(
                    records, evaluated, frames=[frame]
                ):
                    raise AssertionError(f"loaded frame {frame} differs")
        finally:
            reader.close()
        compacted = msm.Interactions.from_records(
            records, n_atoms=n_atoms, n_structures=n_frames,
            evaluated_structure_indices=evaluated,
            method=METHOD, measure_units=UNITS,
            parameters={"seed": 251}, source_id="synthetic_contract",
        )
        compacted_path = Path(directory) / "compacted.h5i"
        compacted.save(compacted_path)
        reopened = msm.Interactions.load(compacted_path)
        for frames in ([2, 5, 6, 17, n_frames - 1], [1, 2, 1]):
            if materialize(reopened.query(structure_indices=frames)) != expected(
                records, evaluated, frames=frames
            ):
                raise AssertionError("compacted frame query differs")
        for atom in (0, 41, n_atoms - 1):
            if materialize(reopened.query(atom_indices=[atom])) != expected(
                records, evaluated, atoms=[atom]
            ):
                raise AssertionError("compacted atom query differs")
        mapped_parallel = [{
            "role": part["role"],
            "atom_indices": [view.storage_to_current_atoms[atom]
                             for atom in part["atom_indices"]],
        } for part in parallel[0]["participants"]]
        parallel_after = [row for row in records if row["structure_index"] == 2
                          and row["interaction_type"] == parallel[0]["interaction_type"]
                          and row["participants"] == mapped_parallel]
        if len(parallel_after) != 2:
            raise AssertionError("parallel observations were lost")
        print(json.dumps({
            "platform": platform.platform(), "atoms": n_atoms,
            "structures": n_frames, "evaluated": len(evaluated),
            "occurrences": len(records), "removed_original_atoms": atoms_to_drop,
            "base_file_bytes": base_file_bytes,
            "typed_map_file_bytes": path.stat().st_size,
            "compacted_file_bytes": compacted_path.stat().st_size,
            "parallel_observations_retained": len(parallel_after),
            "operations": ["drop_atom_twice", "drop_frame_twice",
                           "reorder_frames", "reorder_atoms",
                           "insert_evaluated_empty", "insert_unevaluated",
                           "save_load_maps", "compact_save_load"],
        }, indent=2))


if __name__ == "__main__":
    main()
