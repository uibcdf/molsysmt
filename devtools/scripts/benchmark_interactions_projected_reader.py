#!/usr/bin/env python3
"""Compare selective HDF5 reads with whole-block and indexed-row queries.

This is an experimental reader for the flat-block probe, not a public codec.
It gathers only requested event, relation, participant, and image positions.
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
from benchmark_interactions_sqlite import SQLiteProbe


class ProjectedReader(FlatReader):
    """Fetch selected positions of every required field from the flat file."""

    def __init__(self, path, strategy="adaptive"):
        super().__init__(path)
        if strategy not in {"adaptive", "gather", "span"}:
            raise ValueError("unknown projected read strategy")
        self.strategy = strategy
        self.datasets = {}
        self.read_calls = 0
        self.logical_rows_read = 0

    def _take(self, name, block, indices):
        indices = sorted({int(index) for index in indices})
        if not indices:
            return {}
        dataset = self.datasets.get(name)
        if dataset is None:
            dataset = self.file[f"data/{name}"]
            self.datasets[name] = dataset
        start = int(self.offsets[self.column_index[name], block])
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

    def _pairs(self, name, block, indices):
        indices = sorted({int(index) for index in indices})
        values = self._take(name, block, (*indices, *(index + 1 for index in indices)))
        return {index: (int(values[index]), int(values[index + 1]))
                for index in indices}

    def _rows(self, block, positions):
        positions = sorted({int(position) for position in positions})
        if not positions:
            return []
        structures = self._take("occurrence_structures", block, positions)
        evidence = self._take("occurrence_evidence", block, positions)
        measures = {name: self._take(f"measure_{name}", block, positions)
                    for name in UNITS}
        image_bounds = self._pairs("occurrence_image_offsets", block, positions)
        image_indices = sorted({image for first, last in image_bounds.values()
                                for image in range(first, last)})
        images = self._take("image_vectors", block, image_indices)

        if self.scopes[block] == 0:
            relation_by_event = self._take("occurrence_relations", block, positions)
            relations = sorted({int(relation) for relation in relation_by_event.values()})
            types = self._take("relation_type_codes", block, relations)
            part_bounds = self._pairs("relation_participant_offsets", block, relations)
        else:
            relation_by_event = {position: position for position in positions}
            relations = positions
            types = self._take("occurrence_type_codes", block, relations)
            part_bounds = self._pairs("occurrence_participant_offsets", block, relations)

        part_indices = sorted({part for first, last in part_bounds.values()
                               for part in range(first, last)})
        roles = self._take("participant_role_codes", block, part_indices)
        atom_bounds = self._pairs("participant_atom_offsets", block, part_indices)
        atom_indices = sorted({atom for first, last in atom_bounds.values()
                               for atom in range(first, last)})
        atoms = self._take("participant_atoms", block, atom_indices)

        output = []
        for event in positions:
            relation = int(relation_by_event[event])
            participants = []
            for part in range(*part_bounds[relation]):
                participants.append({
                    "role": self.labels["roles"][int(roles[part])],
                    "atom_indices": [int(atoms[atom])
                                     for atom in range(*atom_bounds[part])],
                })
            output.append(_signature({
                "structure_index": structures[event],
                "interaction_type": self.labels["types"][int(types[relation])],
                "participants": participants,
                "evidence": self.labels["evidence"][int(evidence[event])],
                "measurements": {name: values[event]
                                 for name, values in measures.items()},
                "images": [images[image] for image in range(*image_bounds[event])],
            }))
        return output

    def query_frame(self, frame):
        if frame not in self.covered:
            return [], Counter()
        block = frame // self.metadata["block_size"]
        local = frame - block * self.metadata["block_size"]
        bounds = self._pairs("frame_offsets", block, [local])[local]
        return [frame], Counter(self._rows(block, range(*bounds)))

    def query_atom(self, atom):
        offsets = self.file["index/atom_offsets"][atom:atom + 2]
        ids = self.file["index/atom_occurrences"][int(offsets[0]):int(offsets[1])]
        blocks = np.searchsorted(self.block_event_offsets, ids, side="right") - 1
        output = []
        for block in np.unique(blocks):
            positions = ids[blocks == block] - self.block_event_offsets[block]
            output.extend(self._rows(int(block), positions))
        return self.coverage, Counter(output)


def _measure(path, kind, index, backend, repeats, strategy):
    samples = []
    calls = []
    rows_read = []
    for _ in range(repeats):
        start = time.perf_counter_ns()
        if backend == "sqlite":
            reader = SQLiteProbe(path)
            spec = ({"frames": [index]} if kind == "frame"
                    else {"atoms": [index]})
            result = reader.materialize(reader.select(spec))
            reader.close()
        else:
            reader = (ProjectedReader(path, strategy) if backend == "projected"
                      else FlatReader(path))
            result = (reader.query_frame(index) if kind == "frame"
                      else reader.query_atom(index))
            if backend == "projected":
                calls.append(reader.read_calls)
                rows_read.append(reader.logical_rows_read)
            reader.close()
        samples.append((time.perf_counter_ns() - start) / 1e6)
    return result, round(statistics.median(samples), 3), {
        "projected_column_reads": calls[0] if calls else None,
        "projected_logical_rows_read": rows_read[0] if rows_read else None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--block-size", type=int, default=100)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--distribution", choices=("stable", "churn", "mixed"),
                        default="mixed")
    parser.add_argument("--strategy", choices=("adaptive", "gather", "span"),
                        default="adaptive")
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
        sqlite_path = Path(directory) / "rows.sqlite"
        file_info = write_flat_file(
            flat_path, records, evaluated, n_frames, n_atoms, args.block_size
        )
        sql = SQLiteProbe.create(sqlite_path, records, evaluated, n_atoms, n_frames)
        sql.close()
        output = {}
        for kind, index in requests:
            spec = ({"frames": [index]} if kind == "frame"
                    else {"atoms": [index]})
            oracle = expected(records, evaluated, **spec)
            key = f"{kind}:{index}"
            output[key] = {"rows": sum(oracle[1].values())}
            for backend in ("whole_block", "projected", "sqlite"):
                path = sqlite_path if backend == "sqlite" else flat_path
                actual, elapsed, diagnostics = _measure(
                    path, kind, index, backend, args.repeats, args.strategy
                )
                if actual != oracle:
                    raise AssertionError(f"{backend} {key} differs from oracle")
                output[key][backend] = elapsed
                if backend == "projected":
                    output[key].update(diagnostics)
        print(json.dumps({
            "platform": platform.platform(), "h5py": h5py.__version__,
            "sqlite": sqlite3.sqlite_version,
            "block_size": args.block_size, "repeats": args.repeats,
            "distribution": args.distribution, "strategy": args.strategy,
            "occurrences": len(records),
            "flat": file_info, "sqlite_file_bytes": sqlite_path.stat().st_size,
            "median_open_query_ms": output,
        }, indent=2))


if __name__ == "__main__":
    main()
