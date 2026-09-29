#!/usr/bin/env python3
"""Exercise sparse local edits and source-index remapping against an oracle.

This is a prototype view over a typed snapshot and full-frame overrides. It
does not add mutation methods to the public Interactions class or serialize
the remapping/append layer.
"""

from __future__ import annotations

import json
import platform
import tempfile
import time
from collections import Counter
from pathlib import Path

from benchmark_interactions_contract import (
    UNITS,
    _record_atoms,
    _signature,
    expected,
    generate_fixture,
)
from benchmark_interactions_flat_blocks import write_flat_file
from benchmark_interactions_flat_edits import OverlayReader, append_override

import molsysmt as msm


def _replace_frame(records, frame, replacement):
    return [row for row in records if row["structure_index"] != frame] + list(
        replacement
    )


def _drop_frame(records, evaluated, frame):
    transformed = [{**row, "structure_index": row["structure_index"]
                    - (row["structure_index"] > frame)}
                   for row in records if row["structure_index"] != frame]
    coverage = [item - (item > frame) for item in evaluated if item != frame]
    return transformed, coverage


def _drop_atom(records, atom):
    transformed = []
    for row in records:
        if atom in _record_atoms(row):
            continue
        participants = [{**part, "atom_indices": [
            index - (index > atom) for index in part["atom_indices"]
        ]} for part in row["participants"]]
        transformed.append({**row, "participants": participants})
    return transformed


class RemappedView:
    """Map current indices to immutable snapshot indices and local new frames."""

    def __init__(self, reader, n_atoms, n_frames):
        self.reader = reader
        self.current_to_storage_frames = list(range(n_frames))
        self.current_to_storage_atoms = list(range(n_atoms))
        self.appended = {}
        self.invalidated = set()
        self._refresh()

    def _refresh(self):
        self.storage_to_current_frames = {
            storage: current for current, storage in enumerate(
                self.current_to_storage_frames
            ) if storage is not None
        }
        self.storage_to_current_atoms = {
            storage: current for current, storage in enumerate(
                self.current_to_storage_atoms
            )
        }

    def _covered(self, current):
        storage = self.current_to_storage_frames[current]
        if storage is None:
            return current in self.appended
        return storage in self.reader.covered and storage not in self.invalidated

    def coverage(self):
        return [current for current in range(len(self.current_to_storage_frames))
                if self._covered(current)]

    def _map_base(self, row):
        frame, kind, participants, evidence, measures, images = row
        current_frame = self.storage_to_current_frames.get(frame)
        if current_frame is None or frame in self.invalidated:
            return None
        mapped = []
        for role, atoms in participants:
            if any(atom not in self.storage_to_current_atoms for atom in atoms):
                return None
            mapped.append((role, tuple(self.storage_to_current_atoms[atom]
                                       for atom in atoms)))
        return (current_frame, kind, tuple(mapped), evidence, measures, images)

    def query_frame(self, current):
        if not self._covered(current):
            return [], Counter()
        storage = self.current_to_storage_frames[current]
        if storage is None:
            return [current], Counter(self.appended[current])
        _, found = self.reader.query_frame(storage)
        output = Counter()
        for row, count in found.items():
            mapped = self._map_base(row)
            if mapped is not None:
                output[mapped] += count
        return [current], output

    def query_frames(self, frames):
        coverage = []
        output = Counter()
        for frame in dict.fromkeys(frames):
            selected, rows = self.query_frame(frame)
            coverage.extend(selected)
            output.update(rows)
        return coverage, output

    def query_atom(self, current):
        storage = self.current_to_storage_atoms[current]
        _, found = self.reader.query_atom(storage)
        output = Counter()
        for row, count in found.items():
            mapped = self._map_base(row)
            if mapped is not None:
                output[mapped] += count
        for rows in self.appended.values():
            output.update(row for row in rows
                          if any(current in atoms for _, atoms in row[2]))
        return self.coverage(), output

    def drop_frame(self, current):
        storage = self.current_to_storage_frames.pop(current)
        if storage is not None:
            self.invalidated.add(storage)
        self.appended = {
            index - (index > current): [
                (row[0] - (row[0] > current), *row[1:]) for row in rows
            ] for index, rows in self.appended.items() if index != current
        }
        self._refresh()

    def drop_atom(self, current):
        self.current_to_storage_atoms.pop(current)
        updated = {}
        for frame, rows in self.appended.items():
            kept = []
            for row in rows:
                if any(current in atoms for _, atoms in row[2]):
                    continue
                parts = tuple((role, tuple(atom - (atom > current)
                                           for atom in atoms))
                              for role, atoms in row[2])
                kept.append((row[0], row[1], parts, *row[3:]))
            updated[frame] = kept
        self.appended = updated
        self._refresh()

    def append_frame(self, records):
        current = len(self.current_to_storage_frames)
        self.current_to_storage_frames.append(None)
        self.appended[current] = [_signature({**row, "structure_index": current})
                                  for row in records]
        self._refresh()
        return current

    def invalidate_frame(self, current):
        storage = self.current_to_storage_frames[current]
        if storage is None:
            self.appended.pop(current, None)
        else:
            self.invalidated.add(storage)

    def raw_map_bytes_lower_bound(self):
        return 8 * (len(self.current_to_storage_frames)
                    + len(self.current_to_storage_atoms))


def _check(view, records, evaluated, stage):
    frames = [10, 1, 4, 10, 0, len(view.current_to_storage_frames) - 1]
    if stage in {"after_remove", "after_add"}:
        frames.insert(0, 2)
    oracle = expected(records, evaluated, frames=frames)
    if view.query_frames(frames) != oracle:
        raise AssertionError(f"{stage}: nonconsecutive frame query differs")
    for atom in (0, 41, 42, len(view.current_to_storage_atoms) - 1):
        if atom >= len(view.current_to_storage_atoms):
            continue
        if view.query_atom(atom) != expected(records, evaluated, atoms=[atom]):
            raise AssertionError(f"{stage}: atom {atom} query differs")
    for frame in (0, 1, 2, 10, len(view.current_to_storage_frames) - 1):
        if view.query_frame(frame) != expected(records, evaluated, frames=[frame]):
            raise AssertionError(f"{stage}: frame {frame} query differs")


def main():
    n_frames, n_atoms = 1000, 500
    records, evaluated = generate_fixture(n_frames, n_atoms, 8, "mixed", 251)
    frame = 2
    original_rows = [row for row in records if row["structure_index"] == frame]
    if (len(original_rows) < 2
            or original_rows[0]["interaction_type"]
            != original_rows[1]["interaction_type"]
            or original_rows[0]["participants"]
            != original_rows[1]["participants"]
            or original_rows[0]["measurements"]
            == original_rows[1]["measurements"]):
        raise AssertionError("expected distinguishable parallel observations")
    after_remove = _replace_frame(records, frame, original_rows[1:])
    added = {
        "structure_index": frame, "interaction_type": "hbond",
        "participants": [
            {"role": "donor", "atom_indices": [400]},
            {"role": "hydrogen", "atom_indices": [401]},
            {"role": "acceptor", "atom_indices": [402]},
        ],
        "evidence": "observed_geometry",
        "measurements": {"distance": 0.23, "angle": 0.31},
        "images": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    }
    after_add = _replace_frame(after_remove, frame, [*original_rows[1:], added])
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "base.h5i"
        write_flat_file(path, records, evaluated, n_frames, n_atoms, 100)
        append_override(path, frame, original_rows[1:])
        reader = OverlayReader(path)
        view = RemappedView(reader, n_atoms, n_frames)
        _check(view, after_remove, evaluated, "after_remove")
        reader.close()
        append_override(path, frame, [*original_rows[1:], added])
        reader = OverlayReader(path)
        view = RemappedView(reader, n_atoms, n_frames)
        _check(view, after_add, evaluated, "after_add")

        start = time.perf_counter_ns()
        view.drop_frame(frame)
        drop_frame_ms = (time.perf_counter_ns() - start) / 1e6
        current_records, current_evaluated = _drop_frame(
            after_add, evaluated, frame
        )
        _check(view, current_records, current_evaluated, "after_drop_frame")

        start = time.perf_counter_ns()
        view.drop_atom(41)
        drop_atom_ms = (time.perf_counter_ns() - start) / 1e6
        current_records = _drop_atom(current_records, 41)
        _check(view, current_records, current_evaluated, "after_drop_atom")

        new_frame = len(view.current_to_storage_frames)
        appended_record = {
            **added, "structure_index": new_frame,
            "interaction_type": "new_type_after_snapshot",
        }
        assert view.append_frame([appended_record]) == new_frame
        current_records.append(appended_record)
        current_evaluated.append(new_frame)
        _check(view, current_records, current_evaluated, "after_append_frame")

        view.invalidate_frame(10)
        current_records = [row for row in current_records
                           if row["structure_index"] != 10]
        current_evaluated.remove(10)
        _check(view, current_records, current_evaluated, "after_invalidate")
        rebuilt = msm.Interactions.from_records(
            current_records, n_atoms=n_atoms - 1, n_structures=n_frames,
            evaluated_structure_indices=current_evaluated,
            method="synthetic_full_contract", measure_units=UNITS,
        )
        if rebuilt.query(structure_indices=[new_frame]).n_interactions != 1:
            raise AssertionError("rebuilt append frame lost its interaction")
        reader.close()
        print(json.dumps({
            "platform": platform.platform(), "initial_occurrences": len(records),
            "removed_parallel_observation": True,
            "after_remove_occurrences": len(after_remove),
            "after_add_occurrences": len(after_add),
            "final_occurrences": len(current_records),
            "final_evaluated_frames": len(current_evaluated),
            "drop_frame_map_ms": round(drop_frame_ms, 3),
            "drop_atom_map_ms": round(drop_atom_ms, 3),
            "raw_int64_map_bytes_lower_bound": view.raw_map_bytes_lower_bound(),
            "checked_stages": ["remove_observation", "add_relation",
                               "drop_structure", "drop_atom", "append_structure",
                               "invalidate_evaluation"],
            "public_mutation_api": False,
            "remapping_serialized": False,
        }, indent=2, default=str))


if __name__ == "__main__":
    main()
