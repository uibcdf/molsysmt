#!/usr/bin/env python3
"""Probe bounded block writing with a disk-backed atom-posting builder.

Input records and evaluated indices must be sorted. The writer keeps one
analysis block, small label dictionaries and offset tables in memory; SQLite
is a temporary external sorter for atom postings, not the result format.
"""

from __future__ import annotations

import argparse
import json
import platform
import resource
import sqlite3
import tempfile
import time
from pathlib import Path

import h5py
import numpy as np
from benchmark_interactions_adaptive_blocks import _common_arrays, _descriptor_arrays
from benchmark_interactions_contract import (
    METHOD,
    UNITS,
    expected,
    generate_fixture,
    iter_fixture,
)
from benchmark_interactions_flat_blocks import FlatReader, write_flat_file
from benchmark_interactions_indexed_files import _smallest_unsigned

import molsysmt as msm


def _next(iterator):
    return next(iterator, None)


def _append(dataset, array):
    old = dataset.shape[0]
    new = old + len(array)
    if new != old:
        dataset.resize(new, axis=0)
        dataset[old:new] = array


def _extendible(group, name, sample):
    tail = sample.shape[1:]
    first_chunk = min(4096, max(128, len(sample)))
    return group.create_dataset(
        name, shape=(0, *tail), maxshape=(None, *tail),
        chunks=(first_chunk, *tail), dtype=sample.dtype, compression="gzip",
    )


def write_streaming_flat_file(path, records, evaluated, n_frames, n_atoms,
                              block_size, scratch):
    """Write the flat-block probe from sorted one-pass input iterators."""
    records = iter(records)
    evaluated = iter(evaluated)
    next_record = _next(records)
    next_evaluated = _next(evaluated)
    last_record_frame = -1
    last_evaluated_frame = -1
    labels = {"types": [], "roles": [], "evidence": []}
    seen = {name: set() for name in labels}
    offsets = {}
    columns = None
    scopes = []
    block_event_offsets = [0]
    posting_count = 0
    with sqlite3.connect(scratch) as db, h5py.File(path, "w") as file:
        db.execute("PRAGMA journal_mode=OFF")
        db.execute("PRAGMA synchronous=OFF")
        db.execute("PRAGMA temp_store=FILE")
        db.execute("PRAGMA cache_size=-4096")
        db.execute("CREATE TABLE postings(atom INTEGER, event INTEGER)")
        file.attrs["format"] = "molsysmt.interactions.flat_block_probe"
        file.attrs["schema_version"] = 1
        data = file.create_group("data")
        coverage_data = file.create_dataset(
            "evaluated_structure_indices", shape=(0,), maxshape=(None,),
            chunks=(4096,), dtype=np.int64, compression="gzip",
        )
        for start in range(0, n_frames, block_size):
            stop = min(start + block_size, n_frames)
            rows = []
            while next_record is not None and next_record["structure_index"] < stop:
                frame = int(next_record["structure_index"])
                if frame < start or frame < last_record_frame:
                    raise ValueError("records must be ordered by structure index")
                rows.append(next_record)
                last_record_frame = frame
                next_record = _next(records)
            coverage = []
            while next_evaluated is not None and next_evaluated < stop:
                if next_evaluated < start or next_evaluated <= last_evaluated_frame:
                    raise ValueError("coverage must be sorted and unique")
                coverage.append(next_evaluated)
                last_evaluated_frame = next_evaluated
                next_evaluated = _next(evaluated)
            _append(coverage_data, np.asarray(coverage, dtype=np.int64))
            for row in rows:
                for name, values in (
                    ("types", (row["interaction_type"],)),
                    ("roles", (part["role"] for part in row["participants"])),
                    ("evidence", (row["evidence"],)),
                ):
                    for value in values:
                        if value not in seen[name]:
                            seen[name].add(value)
                            labels[name].append(value)
            result = msm.Interactions.from_records(
                rows, n_atoms=n_atoms, n_structures=n_frames,
                evaluated_structure_indices=coverage, method=METHOD,
                measure_units=UNITS, parameters={"seed": 251},
                source_id="synthetic_contract",
            )
            descriptors = {
                mode: _descriptor_arrays(result, labels, mode)
                for mode in ("global", "event")
            }
            mode = min(descriptors, key=lambda item: sum(
                array.nbytes for array in descriptors[item].values()
            ))
            scopes.append(0 if mode == "global" else 1)
            arrays = {
                **_common_arrays(result, labels, start, stop),
                **descriptors[mode],
            }
            if columns is None:
                columns = sorted(set(arrays) | set(descriptors["global"])
                                 | set(descriptors["event"]))
                samples = {
                    **arrays, **descriptors["global"], **descriptors["event"],
                }
                offsets = {name: [0] for name in columns}
                for name in columns:
                    _extendible(data, name, samples[name])
            for name in columns:
                array = arrays.get(name)
                if array is not None:
                    _append(data[name], array)
                    offsets[name].append(offsets[name][-1] + len(array))
                else:
                    offsets[name].append(offsets[name][-1])
            base = block_event_offsets[-1]
            sparse_postings = (
                (int(atom), base + position)
                for position, relation in enumerate(result.occurrence_relations)
                for atom in np.unique(result._relation_atoms(relation))
            )
            n_postings_before = db.total_changes
            db.executemany(
                "INSERT INTO postings VALUES (?, ?)",
                sparse_postings,
            )
            posting_count += db.total_changes - n_postings_before
            block_event_offsets.append(base + result.n_interactions)
        if next_record is not None or next_evaluated is not None:
            raise ValueError("record or coverage index exceeds n_frames")
        file.attrs["metadata"] = json.dumps({
            "n_atoms": n_atoms, "n_structures": n_frames,
            "block_size": block_size, "method": METHOD,
            "parameters": {"seed": 251}, "source_id": "synthetic_contract",
            "measure_units": UNITS, "columns": columns,
        })
        label_group = file.create_group("labels")
        string_dtype = h5py.string_dtype(encoding="utf-8")
        for name, values in labels.items():
            label_group.create_dataset(name,
                                       data=np.asarray(values, dtype=string_dtype))
        file.create_dataset("block_scope", data=np.asarray(scopes, dtype=np.uint8))
        file.create_dataset("column_offsets", data=np.asarray(
            [offsets[name] for name in columns], dtype=np.int64
        ), compression="gzip")
        index = file.create_group("index")
        index.create_dataset("block_event_offsets", data=_smallest_unsigned(
            block_event_offsets
        ), compression="gzip")
        db.commit()
        db.execute("CREATE INDEX postings_by_atom ON postings(atom, event)")
        atom_offset_data = np.zeros(n_atoms + 1, dtype=np.int64)
        occurrence_dtype = _smallest_unsigned([block_event_offsets[-1]]).dtype
        posting_data = index.create_dataset(
            "atom_occurrences", shape=(0,), maxshape=(None,),
            chunks=(8192,), dtype=occurrence_dtype, compression="gzip",
        )
        current_atom = 0
        batch = []
        for atom, event in db.execute(
            "SELECT atom, event FROM postings ORDER BY atom, event"
        ):
            while current_atom < atom:
                atom_offset_data[current_atom + 1] = posting_data.shape[0] + len(batch)
                current_atom += 1
            batch.append(event)
            if len(batch) == 8192:
                _append(posting_data, np.asarray(batch, dtype=occurrence_dtype))
                batch.clear()
        if batch:
            _append(posting_data, np.asarray(batch, dtype=occurrence_dtype))
        while current_atom < n_atoms:
            atom_offset_data[current_atom + 1] = posting_data.shape[0]
            current_atom += 1
        if posting_data.shape[0] != posting_count:
            raise AssertionError("posting index lost an atom occurrence")
        index.create_dataset("atom_offsets", data=_smallest_unsigned(
            atom_offset_data
        ), compression="gzip")
    return {"file_bytes": path.stat().st_size,
            "postings": posting_count, "choices": scopes,
            "scratch_bytes": scratch.stat().st_size}


def _verify(path, n_frames, n_atoms, distribution, per_frame):
    records, evaluated = generate_fixture(
        n_frames, n_atoms, per_frame, distribution, 251
    )
    reader = FlatReader(path)
    try:
        for frame in (0, 1, 2, 10, n_frames // 2, n_frames - 1):
            actual = reader.query_frame(frame)
            oracle = expected(records, evaluated, frames=[frame])
            if actual != oracle:
                raise AssertionError(f"streaming frame {frame} differs from oracle")
        for atom in (0, 42, n_atoms - 1):
            actual = reader.query_atom(atom)
            oracle = expected(records, evaluated, atoms=[atom])
            if actual != oracle:
                raise AssertionError(f"streaming atom {atom} differs from oracle")
    finally:
        reader.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("streaming", "eager"),
                        default="streaming")
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--atoms", type=int, default=500)
    parser.add_argument("--per-frame", type=int, default=8)
    parser.add_argument("--block-size", type=int, default=100)
    parser.add_argument("--distribution", choices=("stable", "churn", "mixed"),
                        default="mixed")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if (args.frames < 30 or args.atoms < 30 or args.block_size < 30
            or args.per_frame < 1):
        parser.error("frames, atoms and block size must be at least 30; per-frame positive")
    initial_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "interactions.h5i"
        scratch = Path(directory) / "postings.sqlite"
        start = time.perf_counter()
        if args.mode == "streaming":
            coverage = (frame for frame in range(args.frames) if frame % 29 != 0)
            info = write_streaming_flat_file(
                path, iter_fixture(args.frames, args.atoms, args.per_frame,
                                   args.distribution, 251),
                coverage, args.frames, args.atoms, args.block_size, scratch,
            )
        else:
            records, coverage = generate_fixture(
                args.frames, args.atoms, args.per_frame, args.distribution, 251
            )
            info = write_flat_file(
                path, records, coverage, args.frames, args.atoms,
                args.block_size,
            )
        build_s = time.perf_counter() - start
        peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if args.verify:
            _verify(path, args.frames, args.atoms, args.distribution,
                    args.per_frame)
        choices = info.pop("choices")
        normalized = ["global" if mode == 0 else "event" if mode == 1 else mode
                      for mode in choices]
        counts = {mode: normalized.count(mode) for mode in ("global", "event")}
        transitions = [block for block in range(1, len(normalized))
                       if normalized[block] != normalized[block - 1]]
        print(json.dumps({
            "platform": platform.platform(), "mode": args.mode,
            "frames": args.frames, "atoms": args.atoms,
            "per_frame": args.per_frame,
            "distribution": args.distribution, "block_size": args.block_size,
            "build_s": round(build_s, 3),
            "initial_peak_rss_kib": initial_rss,
            "post_write_peak_rss_kib": peak_rss,
            "peak_rss_delta_kib": peak_rss - initial_rss,
            **info,
            "mode_counts": counts, "mode_transitions": transitions,
            "verified": args.verify,
        }, indent=2))


if __name__ == "__main__":
    main()
