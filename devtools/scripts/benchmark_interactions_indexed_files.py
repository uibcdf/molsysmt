#!/usr/bin/env python3
"""Compare full-field HDF5 and SQLite files with persisted atom indexes.

The HDF5 index group is an experimental sidecar ignored by the public loader.
This probe measures file bytes and index correctness, not cold query latency.
"""

from __future__ import annotations

import argparse
import json
import platform
import sqlite3
import tempfile
import time
from pathlib import Path

import h5py
import numpy as np
from benchmark_interactions_contract import (
    METHOD,
    UNITS,
    _direct_postings,
    _record_atoms,
    expected,
    generate_fixture,
    materialize,
)
from benchmark_interactions_sqlite import SQLiteProbe

import molsysmt as msm


def _smallest_unsigned(values):
    largest = int(np.max(values)) if len(values) else 0
    dtype = np.min_scalar_type(largest)
    if not np.issubdtype(dtype, np.unsignedinteger):
        dtype = np.dtype("u1")
    return np.asarray(values, dtype=dtype)


def _write_probe_index(path, result):
    atom_offsets, atom_occurrences, atom_count = _direct_postings(result)
    frame_offsets = np.searchsorted(
        result.occurrence_structures,
        np.arange(result.n_structures + 1),
        side="left",
    )
    arrays = {
        "frame_offsets": _smallest_unsigned(frame_offsets),
        "atom_offsets": _smallest_unsigned(atom_offsets),
        "atom_occurrences": _smallest_unsigned(atom_occurrences),
        "occurrence_atom_count": _smallest_unsigned(atom_count),
    }
    with h5py.File(path, "a") as file:
        group = file.create_group("probe_indexes")
        group.attrs["schema_version"] = 1
        for name, array in arrays.items():
            group.create_dataset(
                name, data=array, compression="gzip" if array.size else None
            )
        stored = {name: group[name].id.get_storage_size() for name in arrays}
    return arrays, stored


def _check_index(path, result, records, evaluated):
    loaded = msm.Interactions.load(path)
    if materialize(loaded) != expected(records, evaluated):
        raise AssertionError("indexed HDF5 payload changed during round trip")
    with h5py.File(path, "r") as file:
        group = file["probe_indexes"]
        frame_offsets = group["frame_offsets"][:]
        atom_offsets = group["atom_offsets"][:]
        atom_occurrences = group["atom_occurrences"][:]
        atom_count = group["occurrence_atom_count"][:]
        if not np.array_equal(
            frame_offsets,
            np.searchsorted(
                loaded.occurrence_structures,
                np.arange(loaded.n_structures + 1),
                side="left",
            ),
        ):
            raise AssertionError("HDF5 frame offsets changed")
        for atom in range(loaded.n_atoms):
            positions = atom_occurrences[atom_offsets[atom] : atom_offsets[atom + 1]]
            if np.any(np.diff(positions) <= 0):
                raise AssertionError("atom postings are not sorted and unique")
            if any(
                atom
                not in loaded._relation_atoms(loaded.occurrence_relations[position])
                for position in positions
            ):
                raise AssertionError("atom posting points to an unrelated occurrence")
        if not np.array_equal(
            atom_count,
            [
                len(
                    _record_atoms(
                        {"participants": loaded.relation(relation)["participants"]}
                    )
                )
                for relation in loaded.occurrence_relations
            ],
        ):
            raise AssertionError("distinct atom counts changed")
        if len(atom_occurrences) != int(np.sum(atom_count)):
            raise AssertionError("atom postings do not cover all participants")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--atoms", type=int, default=500)
    parser.add_argument("--per-frame", type=int, default=8)
    parser.add_argument(
        "--distribution",
        choices=("stable", "churn", "mixed", "persistent"),
        default="stable",
    )
    parser.add_argument("--seed", type=int, default=251)
    args = parser.parse_args()
    if args.frames < 30 or args.atoms < 30 or not 1 <= args.per_frame <= 119:
        parser.error("frames and atoms must be >=30; per-frame 1..119")
    if args.seed != 251:
        parser.error("the SQLite probe currently fixes its metadata seed at 251")

    records, evaluated = generate_fixture(
        args.frames, args.atoms, args.per_frame, args.distribution, args.seed
    )
    result = msm.Interactions.from_records(
        records,
        n_atoms=args.atoms,
        n_structures=args.frames,
        evaluated_structure_indices=evaluated,
        method=METHOD,
        measure_units=UNITS,
        parameters={"seed": args.seed},
        source_id="synthetic_contract",
    )
    with tempfile.TemporaryDirectory() as directory:
        hdf_path = Path(directory) / "interactions.h5i"
        sqlite_path = Path(directory) / "interactions.sqlite"
        result.save(hdf_path)
        hdf_without_index = hdf_path.stat().st_size
        start = time.perf_counter()
        arrays, stored = _write_probe_index(hdf_path, result)
        index_write_s = time.perf_counter() - start
        hdf_with_index = hdf_path.stat().st_size
        _check_index(hdf_path, result, records, evaluated)

        sqlite = SQLiteProbe.create(
            sqlite_path, records, evaluated, args.atoms, args.frames
        )
        if (
            sqlite.metadata["n_atoms"] != args.atoms
            or sqlite.metadata["n_structures"] != args.frames
            or sqlite.metadata["method"] != METHOD
        ):
            raise AssertionError("SQLite analysis metadata changed")
        if sqlite.materialize(sqlite.select({})) != expected(records, evaluated):
            raise AssertionError("SQLite full result differs from record oracle")
        sqlite.close()
        sqlite_bytes = sqlite_path.stat().st_size
        print(
            json.dumps(
                {
                    "platform": platform.platform(),
                    "h5py": h5py.__version__,
                    "sqlite": sqlite3.sqlite_version,
                    "frames": args.frames,
                    "atoms": args.atoms,
                    "distribution": args.distribution,
                    "evaluated_frames": len(evaluated),
                    "occurrences": len(records),
                    "hdf_without_index_bytes": hdf_without_index,
                    "hdf_with_index_bytes": hdf_with_index,
                    "hdf_index_file_delta_bytes": hdf_with_index - hdf_without_index,
                    "hdf_index_numeric_bytes": sum(
                        array.nbytes for array in arrays.values()
                    ),
                    "hdf_index_dataset_storage_bytes": sum(stored.values()),
                    "hdf_index_dataset_storage_by_column": stored,
                    "hdf_index_write_s": index_write_s,
                    "sqlite_indexed_file_bytes": sqlite_bytes,
                    "sqlite_to_hdf_indexed_file_ratio": sqlite_bytes / hdf_with_index,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
