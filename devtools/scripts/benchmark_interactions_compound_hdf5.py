#!/usr/bin/env python3
"""Probe compact HDF5 records as a lower-call flat interaction layout.

The repacker materializes blocks while converting an experimental flat file.
It compares complete results and file-backed query costs, not bounded writes.
"""

from __future__ import annotations

import argparse
import json
import platform
import sqlite3
import statistics
import tempfile
import time
from collections import Counter
from pathlib import Path

import h5py
import numpy as np
from benchmark_interactions_contract import (
    UNITS,
    _signature,
    expected,
    generate_fixture,
)
from benchmark_interactions_flat_blocks import FlatReader, write_flat_file
from benchmark_interactions_projected_reader import ProjectedReader
from benchmark_interactions_sqlite import SQLiteProbe

EVENT_DTYPE = np.dtype([
    ("structure", "u4"), ("relation", "u4"), ("evidence", "u2"),
    ("distance", "f8"), ("angle", "f8"), ("image_start", "u4"),
    ("image_stop", "u4"), ("atom_count", "u2"),
], align=False)
RELATION_DTYPE = np.dtype([
    ("kind", "u2"), ("part_start", "u4"), ("part_stop", "u4"),
], align=False)
PARTICIPANT_DTYPE = np.dtype([
    ("role", "u2"), ("atom_start", "u4"), ("atom_stop", "u4"),
], align=False)
TABLES = ("events", "relations", "participants", "atoms", "images", "frames")


def write_compound_file(source, target):
    """Repack all fields into three record tables and three numeric arrays."""
    reader = FlatReader(source)
    try:
        size = reader.metadata["block_size"]
        n_blocks = (reader.metadata["n_structures"] + size - 1) // size
        buffers = {name: [] for name in TABLES}
        offsets = {name: [0] for name in TABLES}
        for block in range(n_blocks):
            common, descriptors, scope = reader._block(block)
            event_count = len(common["occurrence_structures"])
            events = np.empty(event_count, dtype=EVENT_DTYPE)
            events["structure"] = common["occurrence_structures"]
            events["relation"] = (
                descriptors["occurrence_relations"] if scope == "global"
                else np.arange(event_count)
            )
            events["evidence"] = common["occurrence_evidence"]
            events["distance"] = common["measure_distance"]
            events["angle"] = common["measure_angle"]
            events["image_start"] = common["occurrence_image_offsets"][:-1]
            events["image_stop"] = common["occurrence_image_offsets"][1:]
            events["atom_count"] = common["occurrence_atom_count"]

            if scope == "global":
                kinds = descriptors["relation_type_codes"]
                part_offsets = descriptors["relation_participant_offsets"]
            else:
                kinds = descriptors["occurrence_type_codes"]
                part_offsets = descriptors["occurrence_participant_offsets"]
            relations = np.empty(len(kinds), dtype=RELATION_DTYPE)
            relations["kind"] = kinds
            relations["part_start"] = part_offsets[:-1]
            relations["part_stop"] = part_offsets[1:]

            roles = descriptors["participant_role_codes"]
            atom_offsets = descriptors["participant_atom_offsets"]
            participants = np.empty(len(roles), dtype=PARTICIPANT_DTYPE)
            participants["role"] = roles
            participants["atom_start"] = atom_offsets[:-1]
            participants["atom_stop"] = atom_offsets[1:]
            arrays = {
                "events": events, "relations": relations,
                "participants": participants,
                "atoms": descriptors["participant_atoms"].astype(np.uint32),
                "images": common["image_vectors"],
                "frames": common["frame_offsets"].astype(np.uint32),
            }
            for name, array in arrays.items():
                buffers[name].append(array)
                offsets[name].append(offsets[name][-1] + len(array))
    finally:
        reader.close()

    with h5py.File(source, "r") as old, h5py.File(target, "w") as file:
        file.attrs["format"] = "molsysmt.interactions.compound_block_probe"
        file.attrs["schema_version"] = 1
        file.attrs["metadata"] = old.attrs["metadata"]
        for name in ("labels", "index", "evaluated_structure_indices", "block_scope"):
            old.copy(name, file)
        file.create_dataset("block_offsets", data=np.asarray(
            [offsets[name] for name in TABLES], dtype=np.int64
        ))
        data = file.create_group("data")
        for name in TABLES:
            array = np.concatenate(buffers[name])
            data.create_dataset(
                name, data=array, compression="gzip" if array.size else None
            )
    return {"file_bytes": target.stat().st_size,
            "event_dtype_bytes": EVENT_DTYPE.itemsize,
            "relation_dtype_bytes": RELATION_DTYPE.itemsize,
            "participant_dtype_bytes": PARTICIPANT_DTYPE.itemsize}


class CompoundReader:
    """Read only touched records from packed HDF5 tables."""

    def __init__(self, path, strategy="adaptive"):
        self.file = h5py.File(path, "r")
        if self.file.attrs.get("format") != "molsysmt.interactions.compound_block_probe":
            raise ValueError("unsupported compound-block probe format")
        self.metadata = json.loads(self.file.attrs["metadata"])
        if self.metadata["measure_units"] != UNITS:
            raise ValueError("unexpected measure units")
        self.coverage = self.file["evaluated_structure_indices"][:].tolist()
        self.covered = set(self.coverage)
        self.offsets = self.file["block_offsets"][:]
        self.block_event_offsets = self.file["index/block_event_offsets"][:]
        self.labels = {name: self.file[f"labels/{name}"].asstr()[:]
                       for name in ("types", "roles", "evidence")}
        self.datasets = {}
        self.strategy = strategy
        self.read_calls = 0
        self.logical_rows_read = 0

    def close(self):
        self.file.close()

    def _take(self, name, block, indices):
        indices = sorted({int(index) for index in indices})
        if not indices:
            return {}
        dataset = self.datasets.get(name)
        if dataset is None:
            dataset = self.file[f"data/{name}"]
            self.datasets[name] = dataset
        start = int(self.offsets[TABLES.index(name), block])
        first, last = indices[0], indices[-1]
        span = last - first + 1
        use_span = (
            span == len(indices) or self.strategy == "span"
            or (self.strategy == "adaptive" and span <= 4 * len(indices))
        )
        if use_span:
            values = dataset[start + first:start + last + 1]
            selected = (values[index - first] for index in indices)
            self.logical_rows_read += span
        else:
            values = dataset[np.asarray(indices, dtype=np.int64) + start]
            selected = iter(values)
            self.logical_rows_read += len(indices)
        self.read_calls += 1
        return dict(zip(indices, selected))

    def _rows(self, block, positions):
        positions = sorted({int(position) for position in positions})
        if not positions:
            return []
        events = self._take("events", block, positions)
        relations = self._take("relations", block,
                               (event["relation"] for event in events.values()))
        part_indices = sorted({part for relation in relations.values()
                               for part in range(int(relation["part_start"]),
                                                 int(relation["part_stop"]))})
        participants = self._take("participants", block, part_indices)
        atom_indices = sorted({atom for part in participants.values()
                               for atom in range(int(part["atom_start"]),
                                                 int(part["atom_stop"]))})
        atoms = self._take("atoms", block, atom_indices)
        image_indices = sorted({image for event in events.values()
                                for image in range(int(event["image_start"]),
                                                   int(event["image_stop"]))})
        images = self._take("images", block, image_indices)

        output = []
        for position in positions:
            event = events[position]
            relation = relations[int(event["relation"])]
            parts = []
            for index in range(int(relation["part_start"]),
                               int(relation["part_stop"])):
                part = participants[index]
                parts.append({
                    "role": self.labels["roles"][int(part["role"])],
                    "atom_indices": [int(atoms[atom])
                                     for atom in range(int(part["atom_start"]),
                                                       int(part["atom_stop"]))],
                })
            output.append(_signature({
                "structure_index": event["structure"],
                "interaction_type": self.labels["types"][int(relation["kind"])],
                "participants": parts,
                "evidence": self.labels["evidence"][int(event["evidence"])],
                "measurements": {"distance": event["distance"],
                                 "angle": event["angle"]},
                "images": [images[image]
                           for image in range(int(event["image_start"]),
                                              int(event["image_stop"]))],
            }))
        return output

    def query_frame(self, frame):
        if frame not in self.covered:
            return [], Counter()
        block = frame // self.metadata["block_size"]
        local = frame - block * self.metadata["block_size"]
        bounds = self._take("frames", block, [local, local + 1])
        return [frame], Counter(self._rows(
            block, range(int(bounds[local]), int(bounds[local + 1]))
        ))

    def query_atom(self, atom):
        offsets = self.file["index/atom_offsets"][atom:atom + 2]
        ids = self.file["index/atom_occurrences"][int(offsets[0]):int(offsets[1])]
        blocks = np.searchsorted(self.block_event_offsets, ids, side="right") - 1
        output = []
        for block in np.unique(blocks):
            positions = ids[blocks == block] - self.block_event_offsets[block]
            output.extend(self._rows(int(block), positions))
        return self.coverage, Counter(output)


def _measure(path, backend, kind, index, repeats):
    times = []
    calls = []
    spec = ({"frames": [index]} if kind == "frame" else {"atoms": [index]})
    for _ in range(repeats):
        start = time.perf_counter_ns()
        if backend == "compound":
            reader = CompoundReader(path)
            actual = (reader.query_frame(index) if kind == "frame"
                      else reader.query_atom(index))
            calls.append(reader.read_calls)
        elif backend == "flat":
            reader = FlatReader(path)
            actual = (reader.query_frame(index) if kind == "frame"
                      else reader.query_atom(index))
        else:
            reader = SQLiteProbe(path)
            actual = reader.materialize(reader.select(spec))
        reader.close()
        times.append((time.perf_counter_ns() - start) / 1e6)
    return actual, round(statistics.median(times), 3), calls[0] if calls else None


def _session_probe(paths, records, evaluated):
    """Time checked requests against one open reader per backend."""
    rng = np.random.default_rng(251)
    frames = rng.choice(1000, size=200, replace=False).tolist()
    atoms = [0, 42, *rng.choice(np.arange(1, 500), size=18,
                                replace=False).tolist()]
    requests = [("frame", frame) for frame in frames]
    requests.extend(("atom", atom) for atom in atoms)
    oracles = [expected(
        records, evaluated,
        **({"frames": [index]} if kind == "frame" else {"atoms": [index]})
    ) for kind, index in requests]
    output = {}
    for backend, path in paths.items():
        if backend == "compound":
            reader = CompoundReader(path)
        elif backend == "projected":
            reader = ProjectedReader(path)
        elif backend == "flat":
            reader = FlatReader(path)
        else:
            reader = SQLiteProbe(path)
        samples = {"frame": [], "atom": []}
        named = {}
        try:
            for (kind, index), oracle in zip(requests, oracles):
                start = time.perf_counter_ns()
                if backend == "sqlite":
                    spec = ({"frames": [index]} if kind == "frame"
                            else {"atoms": [index]})
                    actual = reader.materialize(reader.select(spec))
                else:
                    actual = (reader.query_frame(index) if kind == "frame"
                              else reader.query_atom(index))
                elapsed = (time.perf_counter_ns() - start) / 1e6
                if actual != oracle:
                    raise AssertionError(
                        f"{backend} session {kind}:{index} differs from oracle"
                    )
                samples[kind].append(elapsed)
                if kind == "atom" and index in (0, 42):
                    named[str(index)] = round(elapsed, 3)
        finally:
            reader.close()
        output[backend] = {
            kind: {
                "median_ms": round(statistics.median(times), 3),
                "p95_ms": round(float(np.percentile(times, 95)), 3),
            } for kind, times in samples.items()
        }
        output[backend]["named_atom_ms"] = named
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--block-size", type=int, default=100)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--distribution", choices=("stable", "churn", "mixed"),
                        default="mixed")
    parser.add_argument("--session-probe", action="store_true")
    args = parser.parse_args()
    if args.block_size < 1 or args.repeats < 1:
        parser.error("block size and repeats must be positive")
    n_frames, n_atoms = 1000, 500
    records, evaluated = generate_fixture(
        n_frames, n_atoms, 8, args.distribution, 251
    )
    requests = (("frame", 2), ("frame", 1), ("frame", 750),
                ("atom", 0), ("atom", 42))
    with tempfile.TemporaryDirectory() as directory:
        flat_path = Path(directory) / "flat.h5i"
        compound_path = Path(directory) / "compound.h5i"
        sql_path = Path(directory) / "rows.sqlite"
        flat_info = write_flat_file(
            flat_path, records, evaluated, n_frames, n_atoms, args.block_size
        )
        compound_info = write_compound_file(flat_path, compound_path)
        sql = SQLiteProbe.create(sql_path, records, evaluated, n_atoms, n_frames)
        sql.close()
        measures = {}
        for kind, index in requests:
            spec = ({"frames": [index]} if kind == "frame"
                    else {"atoms": [index]})
            oracle = expected(records, evaluated, **spec)
            key = f"{kind}:{index}"
            measures[key] = {"rows": sum(oracle[1].values())}
            for backend, path in (("flat", flat_path),
                                  ("compound", compound_path),
                                  ("sqlite", sql_path)):
                actual, ms, calls = _measure(
                    path, backend, kind, index, args.repeats
                )
                if actual != oracle:
                    raise AssertionError(f"{backend} {key} differs from oracle")
                measures[key][backend] = ms
                if calls is not None:
                    measures[key]["compound_data_reads"] = calls
        sessions = (_session_probe({
            "flat": flat_path, "projected": flat_path,
            "compound": compound_path, "sqlite": sql_path,
        }, records, evaluated) if args.session_probe else None)
        print(json.dumps({
            "platform": platform.platform(), "h5py": h5py.__version__,
            "sqlite": sqlite3.sqlite_version, "distribution": args.distribution,
            "block_size": args.block_size, "repeats": args.repeats,
            "occurrences": len(records), "flat": flat_info,
            "compound": compound_info, "sqlite_file_bytes": sql_path.stat().st_size,
            "median_open_query_ms": measures,
            "persistent_session": sessions,
        }, indent=2))


if __name__ == "__main__":
    main()
