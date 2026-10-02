#!/usr/bin/env python3
"""Probe local full-frame overrides on a flat interaction snapshot.

The append marker tests logical pending/committed visibility, not atomic HDF5
crash recovery. Each edit group is typed but repeated edits need compaction.
"""

from __future__ import annotations

import json
import platform
import statistics
import tempfile
import time
from collections import Counter
from pathlib import Path

import h5py
from benchmark_interactions_adaptive_blocks import (
    _common_arrays,
    _descriptor_arrays,
)
from benchmark_interactions_contract import (
    METHOD,
    UNITS,
    _record_atoms,
    expected,
    generate_fixture,
)
from benchmark_interactions_flat_blocks import (
    FlatReader,
    _decode_positions,
    write_flat_file,
)
from benchmark_interactions_sqlite import SQLiteProbe

import molsysmt as msm


def append_override(path, frame, rows, *, commit=True):
    """Append one typed full-frame replacement with a visibility marker."""
    with h5py.File(path, "r+") as file:
        metadata = json.loads(file.attrs["metadata"])
        labels = {
            name: file[f"labels/{name}"].asstr()[:]
            for name in ("types", "roles", "evidence")
        }
        result = msm.Interactions.from_records(
            rows,
            n_atoms=metadata["n_atoms"],
            n_structures=metadata["n_structures"],
            evaluated_structure_indices=[frame],
            method=METHOD,
            measure_units=UNITS,
            parameters={"seed": 251},
            source_id="synthetic_contract",
        )
        common = _common_arrays(result, labels, frame, frame + 1)
        descriptors = _descriptor_arrays(result, labels, "event")
        journal = file.require_group("journal")
        name = f"{len(journal):06d}"
        group = journal.create_group(name)
        group.attrs["structure_index"] = frame
        group.attrs["committed"] = False
        for section, arrays in (("common", common), ("descriptors", descriptors)):
            target = group.create_group(section)
            for column, array in arrays.items():
                target.create_dataset(
                    column,
                    data=array,
                    compression="gzip" if array.size else None,
                )
        file.flush()
        if commit:
            group.attrs["committed"] = True
            file.flush()
    return name


def commit_override(path, name):
    with h5py.File(path, "r+") as file:
        file[f"journal/{name}"].attrs["committed"] = True
        file.flush()


class OverlayReader(FlatReader):
    """Merge latest committed full-frame replacements with the base snapshot."""

    def __init__(self, path):
        super().__init__(path)
        self.overrides = {}
        if "journal" in self.file:
            for name, group in sorted(self.file["journal"].items()):
                if bool(group.attrs.get("committed", False)):
                    self.overrides[int(group.attrs["structure_index"])] = name

    def _override_rows(self, frame):
        group = self.file[f"journal/{self.overrides[frame]}"]
        common = {name: dataset[:] for name, dataset in group["common"].items()}
        descriptors = {
            name: dataset[:] for name, dataset in group["descriptors"].items()
        }
        return _decode_positions(
            common,
            descriptors,
            "event",
            self.labels,
            range(len(common["occurrence_structures"])),
        )

    def query_frame(self, frame):
        if frame in self.overrides:
            return [frame], Counter(self._override_rows(frame))
        return super().query_frame(frame)

    def query_atom(self, atom):
        coverage, base = super().query_atom(atom)
        if not self.overrides:
            return coverage, base
        selected = Counter(
            {row: count for row, count in base.items() if row[0] not in self.overrides}
        )
        for frame in self.overrides:
            selected.update(
                row
                for row in self._override_rows(frame)
                if any(atom in atoms for _, atoms in row[2])
            )
        return coverage, selected


def _check(path, records, evaluated, frame, atoms):
    reader = OverlayReader(path)
    try:
        specs = [
            ({"frames": [candidate]}, reader.query_frame(candidate))
            for candidate in (frame, frame + 1, 1, 0)
        ]
        specs.extend(({"atoms": [atom]}, reader.query_atom(atom)) for atom in atoms)
        for spec, actual in specs:
            if actual != expected(records, evaluated, **spec):
                raise AssertionError(f"overlay differs from oracle for {spec}")
    finally:
        reader.close()


def _check_sqlite(probe, records, evaluated, frame, atoms):
    specs = [{"frames": [candidate]} for candidate in (frame, frame + 1, 1, 0)]
    specs.extend({"atoms": [atom]} for atom in atoms)
    for spec in specs:
        if probe.materialize(probe.select(spec)) != expected(
            records, evaluated, **spec
        ):
            raise AssertionError(f"SQLite edit differs from oracle for {spec}")


def _frame_atoms(rows):
    return sorted({atom for row in rows for atom in _record_atoms(row)})


def _timed_reopened_queries(
    hdf_path, sqlite_path, records, evaluated, frame, atoms, repeats=5
):
    output = {}
    requests = [("frame", frame), *(("atom", atom) for atom in atoms)]
    for kind, index in requests:
        spec = {"frames": [index]} if kind == "frame" else {"atoms": [index]}
        oracle = expected(records, evaluated, **spec)
        output[f"{kind}:{index}"] = {}
        for backend, path in (("hdf_overlay", hdf_path), ("sqlite", sqlite_path)):
            samples = []
            for _ in range(repeats):
                start = time.perf_counter_ns()
                reader = (
                    OverlayReader(path)
                    if backend == "hdf_overlay"
                    else (SQLiteProbe(path))
                )
                if backend == "hdf_overlay":
                    actual = (
                        reader.query_frame(index)
                        if kind == "frame"
                        else reader.query_atom(index)
                    )
                else:
                    actual = reader.materialize(reader.select(spec))
                reader.close()
                samples.append((time.perf_counter_ns() - start) / 1e6)
                if actual != oracle:
                    raise AssertionError(
                        f"{backend} reopened query differs from oracle"
                    )
            output[f"{kind}:{index}"][backend] = statistics.median(samples)
    return output


def main():
    n_frames, n_atoms, frame = 1000, 500, 10
    records, evaluated = generate_fixture(n_frames, n_atoms, 8, "mixed", 251)
    original = [row for row in records if row["structure_index"] == frame]
    moved_atom = original[0]["participants"][0]["atom_indices"][0]
    retained = [row for row in original if moved_atom not in _record_atoms(row)]
    new_record = {
        "structure_index": frame,
        "interaction_type": "hbond",
        "participants": [
            {"role": "donor", "atom_indices": [moved_atom]},
            {"role": "hydrogen", "atom_indices": [(moved_atom + 1) % n_atoms]},
            {"role": "acceptor", "atom_indices": [(moved_atom + 2) % n_atoms]},
        ],
        "evidence": "observed_geometry",
        "measurements": {"distance": 0.211, "angle": 0.22},
        "images": [[0, 0, 0], [0, 0, 0], [1, 0, 0]],
    }
    replacement = [*retained, new_record]
    edited = [row for row in records if row["structure_index"] != frame]
    edited.extend(replacement)
    empty = [row for row in records if row["structure_index"] != frame]
    atoms_to_check = {moved_atom, (moved_atom + 2) % n_atoms, 0, 42}
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "base.h5i"
        write_flat_file(path, records, evaluated, n_frames, n_atoms, 100)
        base_bytes = path.stat().st_size
        _check(path, records, evaluated, frame, atoms_to_check)
        start = time.perf_counter()
        pending = append_override(path, frame, replacement, commit=False)
        pending_s = time.perf_counter() - start
        _check(path, records, evaluated, frame, atoms_to_check)
        pending_bytes = path.stat().st_size
        commit_override(path, pending)
        _check(path, edited, evaluated, frame, atoms_to_check)
        committed_bytes = path.stat().st_size
        start = time.perf_counter()
        append_override(path, frame, [], commit=True)
        empty_s = time.perf_counter() - start
        _check(path, empty, evaluated, frame, atoms_to_check)
        empty_bytes = path.stat().st_size
        repeated_times = []
        final_records = empty
        for iteration in range(20):
            version = [
                *retained,
                {
                    **new_record,
                    "measurements": {
                        "distance": 0.211 + iteration * 1e-6,
                        "angle": 0.22,
                    },
                },
            ]
            start = time.perf_counter()
            append_override(path, frame, version, commit=True)
            repeated_times.append((time.perf_counter() - start) * 1000)
            final_records = [*empty, *version]
            _check(path, final_records, evaluated, frame, atoms_to_check)
        repeated_bytes = path.stat().st_size
        compacted = Path(directory) / "compacted.h5i"
        start = time.perf_counter()
        write_flat_file(compacted, final_records, evaluated, n_frames, n_atoms, 100)
        compact_s = time.perf_counter() - start
        _check(compacted, final_records, evaluated, frame, atoms_to_check)
        sqlite_path = Path(directory) / "rows.sqlite"
        probe = SQLiteProbe.create(sqlite_path, records, evaluated, n_atoms, n_frames)
        sqlite_base_bytes = sqlite_path.stat().st_size
        _check_sqlite(probe, records, evaluated, frame, atoms_to_check)
        start = time.perf_counter()
        probe.replace_incident(frame, _frame_atoms(original), replacement)
        sqlite_first_ms = (time.perf_counter() - start) * 1000
        _check_sqlite(probe, edited, evaluated, frame, atoms_to_check)
        start = time.perf_counter()
        probe.replace_incident(frame, _frame_atoms(replacement), [])
        sqlite_empty_ms = (time.perf_counter() - start) * 1000
        _check_sqlite(probe, empty, evaluated, frame, atoms_to_check)
        sqlite_repeated = []
        current_frame_rows = []
        for iteration in range(20):
            version = [
                *retained,
                {
                    **new_record,
                    "measurements": {
                        "distance": 0.211 + iteration * 1e-6,
                        "angle": 0.22,
                    },
                },
            ]
            start = time.perf_counter()
            probe.replace_incident(frame, _frame_atoms(current_frame_rows), version)
            sqlite_repeated.append((time.perf_counter() - start) * 1000)
            current_frame_rows = version
            _check_sqlite(probe, [*empty, *version], evaluated, frame, atoms_to_check)
        sqlite_after_edits_bytes = sqlite_path.stat().st_size
        post_edit_queries = _timed_reopened_queries(
            path,
            sqlite_path,
            final_records,
            evaluated,
            frame,
            [moved_atom, 0],
        )
        start = time.perf_counter()
        with probe.connection:
            probe.connection.execute(
                "DELETE FROM relations WHERE relation_id NOT IN "
                "(SELECT DISTINCT relation_id FROM occurrences)"
            )
        probe.connection.execute("VACUUM")
        sqlite_compaction_s = time.perf_counter() - start
        sqlite_compacted_bytes = sqlite_path.stat().st_size
        probe.close()
        reopened = SQLiteProbe(sqlite_path)
        _check_sqlite(reopened, final_records, evaluated, frame, atoms_to_check)
        reopened.close()
        post_compaction_queries = _timed_reopened_queries(
            compacted,
            sqlite_path,
            final_records,
            evaluated,
            frame,
            [moved_atom, 0],
        )
        print(
            json.dumps(
                {
                    "platform": platform.platform(),
                    "h5py": h5py.__version__,
                    "frame": frame,
                    "moved_atom": moved_atom,
                    "removed_incident": len(original) - len(retained),
                    "replacement_rows": len(replacement),
                    "base_file_bytes": base_bytes,
                    "pending_file_bytes": pending_bytes,
                    "committed_file_bytes": committed_bytes,
                    "empty_file_bytes": empty_bytes,
                    "after_20_more_edits_bytes": repeated_bytes,
                    "compacted_file_bytes": compacted.stat().st_size,
                    "append_pending_ms": pending_s * 1000,
                    "append_empty_ms": empty_s * 1000,
                    "median_repeated_append_ms": statistics.median(repeated_times),
                    "compaction_s": compact_s,
                    "sqlite_base_file_bytes": sqlite_base_bytes,
                    "sqlite_after_20_more_edits_bytes": sqlite_after_edits_bytes,
                    "sqlite_compacted_file_bytes": sqlite_compacted_bytes,
                    "sqlite_first_edit_ms": sqlite_first_ms,
                    "sqlite_empty_edit_ms": sqlite_empty_ms,
                    "sqlite_median_repeated_edit_ms": statistics.median(
                        sqlite_repeated
                    ),
                    "sqlite_compaction_s": sqlite_compaction_s,
                    "post_edit_median_reopened_query_ms": post_edit_queries,
                    "post_compaction_median_reopened_query_ms": post_compaction_queries,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
