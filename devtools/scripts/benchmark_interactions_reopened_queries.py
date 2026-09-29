#!/usr/bin/env python3
"""Probe complete queries after independent-process HDF5 and SQLite opens.

Each child process starts without a Python relation cache. The operating-system
page cache may still be warm. The HDF5 reader is a simple projected prototype,
not the public Interactions loader or a tuned production reader.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sqlite3
import statistics
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

import h5py
import numpy as np
from benchmark_interactions_contract import (
    METHOD,
    UNITS,
    _rss,
    _signature,
    expected,
    generate_fixture,
)
from benchmark_interactions_event_native import query_event_native, write_event_native
from benchmark_interactions_indexed_files import _write_probe_index
from benchmark_interactions_sqlite import SQLiteProbe

import molsysmt as msm


def _digest(counter):
    return hashlib.sha256(repr(sorted(counter.items())).encode()).hexdigest()


def _hdf_relation(file, relation_id, labels, cache):
    if relation_id in cache:
        return cache[relation_id]
    first, last = (int(value) for value in
                   file["relation_participant_offsets"][relation_id:relation_id + 2])
    roles = file["participant_roles_codes"][first:last]
    atom_offsets = file["participant_atom_offsets"][first:last + 1]
    atoms = file["participant_atoms"][int(atom_offsets[0]):int(atom_offsets[-1])]
    participants = [
        {"role": labels["roles"][int(role)],
         "atom_indices": atoms[
             int(atom_offsets[index] - atom_offsets[0]):
             int(atom_offsets[index + 1] - atom_offsets[0])
         ].tolist()}
        for index, role in enumerate(roles)
    ]
    relation = (
        labels["types"][int(file["relation_types_codes"][relation_id])],
        participants,
    )
    cache[relation_id] = relation
    return relation


def _batched_take(dataset, ids, block_size=256):
    """Read only fixed-size pages containing the requested sorted indices."""
    output = np.empty((len(ids), *dataset.shape[1:]), dtype=dataset.dtype)
    pages = ids // block_size
    for page in np.unique(pages):
        positions = np.flatnonzero(pages == page)
        first = int(page) * block_size
        last = min(first + block_size, len(dataset))
        block = dataset[first:last]
        output[positions] = block[ids[positions] - first]
    return output


def _hdf_relations_batched(file, relation_ids, labels, page_size=128):
    """Decode requested relation descriptors by contiguous relation pages."""
    decoded = {}
    pages = relation_ids // page_size
    n_relations = len(file["relation_types_codes"])
    for page in np.unique(pages):
        selected = relation_ids[pages == page]
        first = int(page) * page_size
        last = min(first + page_size, n_relations)
        types = file["relation_types_codes"][first:last]
        part_offsets = file["relation_participant_offsets"][first:last + 1]
        part_first, part_last = int(part_offsets[0]), int(part_offsets[-1])
        roles = file["participant_roles_codes"][part_first:part_last]
        atom_offsets = file["participant_atom_offsets"][part_first:part_last + 1]
        atom_first, atom_last = int(atom_offsets[0]), int(atom_offsets[-1])
        atoms = file["participant_atoms"][atom_first:atom_last]
        for relation_id in selected:
            local = int(relation_id) - first
            participants = []
            for part in range(int(part_offsets[local]), int(part_offsets[local + 1])):
                part_local = part - part_first
                participants.append({
                    "role": labels["roles"][int(roles[part_local])],
                    "atom_indices": atoms[
                        int(atom_offsets[part_local]) - atom_first:
                        int(atom_offsets[part_local + 1]) - atom_first
                    ].tolist(),
                })
            decoded[int(relation_id)] = (
                labels["types"][int(types[local])], participants
            )
    return decoded


def _hdf_images_batched(file, ids, page_size=256):
    """Decode image spans with one contiguous read per touched event page."""
    decoded = {}
    pages = ids // page_size
    n_events = len(file["occurrence_relations"])
    for page in np.unique(pages):
        selected = ids[pages == page]
        first = int(page) * page_size
        last = min(first + page_size, n_events)
        offsets = file["occurrence_image_offsets"][first:last + 1]
        vector_first, vector_last = int(offsets[0]), int(offsets[-1])
        vectors = file["image_vectors"][vector_first:vector_last]
        for occurrence_id in selected:
            local = int(occurrence_id) - first
            decoded[int(occurrence_id)] = vectors[
                int(offsets[local]) - vector_first:
                int(offsets[local + 1]) - vector_first
            ].copy()
    return decoded


def _hdf_query(path, kind, index, *, batched=False):
    with h5py.File(path, "r") as file:
        evaluated = file["evaluated_structure_indices"][:].tolist()
        indexes = file["probe_indexes"]
        if kind == "frame":
            coverage = [index] if index in set(evaluated) else []
            first, last = indexes["frame_offsets"][index:index + 2]
            ids = np.arange(int(first), int(last), dtype=np.int64)
        else:
            coverage = evaluated
            first, last = indexes["atom_offsets"][index:index + 2]
            ids = indexes["atom_occurrences"][int(first):int(last)].astype(np.int64)
        if not len(ids):
            return coverage, Counter()
        labels = {
            "types": file["labels/relation_types"].asstr()[:],
            "roles": file["labels/participant_roles"].asstr()[:],
            "evidence": file["labels/evidence"].asstr()[:],
        }
        read = _batched_take if batched else lambda dataset, indices: dataset[indices]
        columns = {name: read(file[name], ids) for name in (
            "occurrence_structures", "occurrence_relations", "occurrence_evidence"
        )}
        measurements = {name: read(file[f"measurements/{name}"], ids)
                        for name in UNITS}
        if batched:
            relations = _hdf_relations_batched(
                file, np.unique(columns["occurrence_relations"]), labels
            )
            images_by_id = _hdf_images_batched(file, ids)
        else:
            image_starts = file["occurrence_image_offsets"][ids]
            image_ends = file["occurrence_image_offsets"][ids + 1]
            relations = {}
        output = []
        for position, occurrence_id in enumerate(ids):
            relation_id = int(columns["occurrence_relations"][position])
            if batched:
                interaction_type, participants = relations[relation_id]
                images = images_by_id[int(occurrence_id)]
            else:
                interaction_type, participants = _hdf_relation(
                    file, relation_id, labels, relations
                )
                images = file["image_vectors"][
                    int(image_starts[position]):int(image_ends[position])
                ]
            output.append(_signature({
                "structure_index": columns["occurrence_structures"][position],
                "interaction_type": interaction_type,
                "participants": participants,
                "evidence": labels["evidence"][int(
                    columns["occurrence_evidence"][position]
                )],
                "measurements": {name: value[position]
                                 for name, value in measurements.items()},
                "images": images,
            }))
        return coverage, Counter(output)


def _read_child(args):
    start = time.perf_counter_ns()
    if args.backend in ("hdf", "hdf_batch"):
        coverage, rows = _hdf_query(
            args.path, args.request, args.index,
            batched=args.backend == "hdf_batch",
        )
    elif args.backend == "hdf_event":
        coverage, rows = query_event_native(
            args.path, args.request, args.index,
            page_size=args.event_page_size,
        )
    else:
        sqlite = SQLiteProbe(args.path)
        spec = ({"frames": [args.index]} if args.request == "frame"
                else {"atoms": [args.index]})
        coverage, rows = sqlite.materialize(sqlite.select(spec))
        sqlite.close()
    query_ms = (time.perf_counter_ns() - start) / 1e6
    print(json.dumps({
        "query_ms": query_ms, "coverage": coverage,
        "rows": sum(rows.values()), "digest": _digest(rows),
        "rss_after_bytes": _rss().get("VmRSS"),
    }))


def _run_child(backend, path, request, index, event_page_size):
    command = [
        sys.executable, str(Path(__file__).resolve()), "_read",
        "--backend", backend, "--path", str(path),
        "--request", request, "--index", str(index),
        "--event-page-size", str(event_page_size),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", nargs="?", choices=("_read",))
    backend_choices = ("hdf", "hdf_batch", "hdf_event", "sqlite")
    parser.add_argument("--backend", choices=backend_choices)
    parser.add_argument("--path", type=Path)
    parser.add_argument("--request", choices=("frame", "atom"))
    parser.add_argument("--index", type=int)
    parser.add_argument("--distribution", choices=("stable", "churn"),
                        default="stable")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--backends", default="hdf,hdf_batch,sqlite")
    parser.add_argument("--event-page-size", type=int, default=128)
    args = parser.parse_args()
    if args.mode == "_read":
        if None in (args.backend, args.path, args.request, args.index):
            parser.error("_read requires backend, path, request, and index")
        _read_child(args)
        return
    if args.repeats < 1:
        parser.error("repeats must be positive")
    if args.event_page_size < 1:
        parser.error("event page size must be positive")
    backends = tuple(args.backends.split(","))
    if not backends or len(set(backends)) != len(backends) or any(
        backend not in backend_choices for backend in backends
    ):
        parser.error("backends must be a comma-separated set of known reader names")

    n_frames, n_atoms, per_frame = 1000, 500, 8
    records, evaluated = generate_fixture(
        n_frames, n_atoms, per_frame, args.distribution, 251
    )
    result = msm.Interactions.from_records(
        records, n_atoms=n_atoms, n_structures=n_frames,
        evaluated_structure_indices=evaluated, method=METHOD,
        measure_units=UNITS, parameters={"seed": 251},
        source_id="synthetic_contract",
    )
    requests = (("frame", 2), ("frame", 1), ("atom", 0), ("atom", 42))
    with tempfile.TemporaryDirectory() as directory:
        hdf_path = Path(directory) / "interactions.h5i"
        event_path = Path(directory) / "interactions_event.h5i"
        sqlite_path = Path(directory) / "interactions.sqlite"
        result.save(hdf_path)
        _write_probe_index(hdf_path, result)
        if "hdf_event" in backends:
            write_event_native(event_path, result)
        sqlite = SQLiteProbe.create(
            sqlite_path, records, evaluated, n_atoms, n_frames
        )
        sqlite.close()
        results = {}
        for request, index in requests:
            spec = ({"frames": [index]} if request == "frame"
                    else {"atoms": [index]})
            coverage, oracle = expected(records, evaluated, **spec)
            key = f"{request}:{index}"
            results[key] = {"rows": sum(oracle.values())}
            for backend in backends:
                path = (event_path if backend == "hdf_event" else sqlite_path
                        if backend == "sqlite" else hdf_path)
                measurements = [
                    _run_child(backend, path, request, index, args.event_page_size)
                    for _ in range(args.repeats)
                ]
                if any(measurement["coverage"] != coverage
                       or measurement["digest"] != _digest(oracle)
                       for measurement in measurements):
                    raise AssertionError(f"{backend} {key} differs from oracle")
                results[key][backend] = {
                    "median_open_and_query_ms": statistics.median(
                        measurement["query_ms"] for measurement in measurements
                    ),
                    "max_rss_after_bytes": max(
                        measurement["rss_after_bytes"] for measurement in measurements
                    ),
                }
        print(json.dumps({
            "platform": platform.platform(), "h5py": h5py.__version__,
            "sqlite": sqlite3.sqlite_version,
            "distribution": args.distribution, "repeats": args.repeats,
            "backends": backends, "event_page_size": args.event_page_size,
            "hdf_indexed_file_bytes": hdf_path.stat().st_size,
            "hdf_event_file_bytes": (event_path.stat().st_size
                                     if "hdf_event" in backends else None),
            "sqlite_indexed_file_bytes": sqlite_path.stat().st_size,
            "results": results,
        }, indent=2))


if __name__ == "__main__":
    main()
