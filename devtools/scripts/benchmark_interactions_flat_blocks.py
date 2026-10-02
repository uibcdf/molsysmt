#!/usr/bin/env python3
"""Probe flat HDF5 interaction blocks, lazy queries, and indexed file size.

The writer retains input records and an atom-index accumulator in memory. The
reader loads only touched blocks; it is an experimental codec, not H5MSM.
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import tempfile
import time
from collections import Counter, OrderedDict
from pathlib import Path

import h5py
import numpy as np
from benchmark_interactions_adaptive_blocks import (
    _common_arrays,
    _descriptor_arrays,
    _labels,
)
from benchmark_interactions_adaptive_blocks import (
    _write_file as write_group_file,
)
from benchmark_interactions_contract import (
    METHOD,
    UNITS,
    _direct_postings,
    _signature,
    expected,
    generate_fixture,
)
from benchmark_interactions_indexed_files import _smallest_unsigned
from benchmark_interactions_sqlite import SQLiteProbe

import molsysmt as msm


def _make_blocks(records, evaluated, n_frames, n_atoms, block_size):
    labels = _labels(records)
    blocks = []
    for start in range(0, n_frames, block_size):
        stop = min(start + block_size, n_frames)
        rows = [row for row in records if start <= row["structure_index"] < stop]
        coverage = [frame for frame in evaluated if start <= frame < stop]
        result = msm.Interactions.from_records(
            rows,
            n_atoms=n_atoms,
            n_structures=n_frames,
            evaluated_structure_indices=coverage,
            method=METHOD,
            measure_units=UNITS,
            parameters={"seed": 251},
            source_id="synthetic_contract",
        )
        descriptors = {
            mode: _descriptor_arrays(result, labels, mode)
            for mode in ("global", "event")
        }
        projected = {
            mode: sum(array.nbytes for array in fields.values())
            for mode, fields in descriptors.items()
        }
        blocks.append((start, stop, result, descriptors, projected))
    return labels, blocks


def write_flat_file(
    path, records, evaluated, n_frames, n_atoms, block_size, policy="adaptive"
):
    """Write one flat dataset per field and one shared block-offset matrix."""
    labels, blocks = _make_blocks(records, evaluated, n_frames, n_atoms, block_size)
    column_names = sorted(
        set(_common_arrays(blocks[0][2], labels, blocks[0][0], blocks[0][1]))
        | set(blocks[0][3]["global"])
        | set(blocks[0][3]["event"])
    )
    sample = {
        **_common_arrays(blocks[0][2], labels, blocks[0][0], blocks[0][1]),
        **blocks[0][3]["global"],
        **blocks[0][3]["event"],
    }
    buffers = {name: [] for name in column_names}
    offsets = {name: [0] for name in column_names}
    postings = [[] for _ in range(n_atoms)]
    block_event_offsets = [0]
    choices = []
    for start, stop, result, descriptors, projected in blocks:
        mode = min(projected, key=projected.get) if policy == "adaptive" else policy
        choices.append(mode)
        arrays = {
            **_common_arrays(result, labels, start, stop),
            **descriptors[mode],
        }
        for name in column_names:
            value = arrays.get(name)
            if value is None:
                value = np.empty((0, *sample[name].shape[1:]), dtype=sample[name].dtype)
            buffers[name].append(value)
            offsets[name].append(offsets[name][-1] + len(value))
        atom_offsets, atom_occurrences, _ = _direct_postings(result)
        for atom in range(n_atoms):
            postings[atom].extend(
                block_event_offsets[-1] + int(event)
                for event in atom_occurrences[
                    atom_offsets[atom] : atom_offsets[atom + 1]
                ]
            )
        block_event_offsets.append(block_event_offsets[-1] + result.n_interactions)
    with h5py.File(path, "w") as file:
        file.attrs["format"] = "molsysmt.interactions.flat_block_probe"
        file.attrs["schema_version"] = 1
        file.attrs["metadata"] = json.dumps(
            {
                "n_atoms": n_atoms,
                "n_structures": n_frames,
                "block_size": block_size,
                "method": METHOD,
                "parameters": {"seed": 251},
                "source_id": "synthetic_contract",
                "measure_units": UNITS,
                "columns": column_names,
            }
        )
        string_dtype = h5py.string_dtype(encoding="utf-8")
        label_group = file.create_group("labels")
        for name, values in labels.items():
            label_group.create_dataset(
                name, data=np.asarray(values, dtype=string_dtype)
            )
        file.create_dataset(
            "evaluated_structure_indices",
            data=np.asarray(evaluated, dtype=np.int64),
            compression="gzip",
        )
        file.create_dataset(
            "block_scope",
            data=np.asarray(
                [0 if mode == "global" else 1 for mode in choices], dtype=np.uint8
            ),
        )
        file.create_dataset(
            "column_offsets",
            data=np.asarray([offsets[name] for name in column_names], dtype=np.int64),
            compression="gzip",
        )
        data = file.create_group("data")
        for name in column_names:
            array = np.concatenate(buffers[name], axis=0)
            data.create_dataset(
                name, data=array, compression="gzip" if array.size else None
            )
        index = file.create_group("index")
        atom_offsets = np.r_[0, np.cumsum([len(group) for group in postings])]
        for name, array in {
            "atom_offsets": _smallest_unsigned(atom_offsets),
            "atom_occurrences": _smallest_unsigned(
                [event for group in postings for event in group]
            ),
            "block_event_offsets": _smallest_unsigned(block_event_offsets),
        }.items():
            index.create_dataset(
                name, data=array, compression="gzip" if array.size else None
            )
    return {
        "choices": choices,
        "file_bytes": path.stat().st_size,
        "postings": sum(map(len, postings)),
    }


def _decode_positions(common, descriptors, scope, labels, positions):
    """Decode selected local event positions after loading one touched block."""
    output = []
    for event in positions:
        relation = (
            int(descriptors["occurrence_relations"][event])
            if scope == "global"
            else int(event)
        )
        if scope == "global":
            type_code = descriptors["relation_type_codes"][relation]
            part_offsets = descriptors["relation_participant_offsets"]
        else:
            type_code = descriptors["occurrence_type_codes"][relation]
            part_offsets = descriptors["occurrence_participant_offsets"]
        participants = []
        for part in range(int(part_offsets[relation]), int(part_offsets[relation + 1])):
            first = int(descriptors["participant_atom_offsets"][part])
            last = int(descriptors["participant_atom_offsets"][part + 1])
            participants.append(
                {
                    "role": labels["roles"][
                        int(descriptors["participant_role_codes"][part])
                    ],
                    "atom_indices": descriptors["participant_atoms"][
                        first:last
                    ].tolist(),
                }
            )
        first = int(common["occurrence_image_offsets"][event])
        last = int(common["occurrence_image_offsets"][event + 1])
        output.append(
            _signature(
                {
                    "structure_index": common["occurrence_structures"][event],
                    "interaction_type": labels["types"][int(type_code)],
                    "participants": participants,
                    "evidence": labels["evidence"][
                        int(common["occurrence_evidence"][event])
                    ],
                    "measurements": {
                        name: common[f"measure_{name}"][event] for name in UNITS
                    },
                    "images": common["image_vectors"][first:last],
                }
            )
        )
    return output


class FlatReader:
    """Read only selected blocks from one flat file in one open session."""

    def __init__(self, path):
        self.file = h5py.File(path, "r")
        if self.file.attrs.get("format") != "molsysmt.interactions.flat_block_probe":
            raise ValueError("unsupported flat-block probe format")
        self.metadata = json.loads(self.file.attrs["metadata"])
        if self.metadata["measure_units"] != UNITS:
            raise ValueError("unexpected measure units")
        self.coverage = self.file["evaluated_structure_indices"][:].tolist()
        self.covered = set(self.coverage)
        self.columns = self.metadata["columns"]
        self.offsets = self.file["column_offsets"][:]
        self.column_index = {name: index for index, name in enumerate(self.columns)}
        self.scopes = self.file["block_scope"][:]
        self.block_event_offsets = self.file["index/block_event_offsets"][:]
        self.labels = {
            name: self.file[f"labels/{name}"].asstr()[:]
            for name in ("types", "roles", "evidence")
        }
        self.cache = OrderedDict()

    def close(self):
        self.file.close()

    def _block(self, block):
        if block in self.cache:
            self.cache.move_to_end(block)
            return self.cache[block]
        common = {}
        descriptors = {}
        for name in self.columns:
            position = self.column_index[name]
            first, last = self.offsets[position, block : block + 2]
            if first == last:
                continue
            array = self.file[f"data/{name}"][int(first) : int(last)]
            if name in {
                "occurrence_structures",
                "occurrence_evidence",
                "occurrence_image_offsets",
                "image_vectors",
                "frame_offsets",
                "occurrence_atom_count",
                "measure_distance",
                "measure_angle",
            }:
                common[name] = array
            else:
                descriptors[name] = array
        scope = "global" if self.scopes[block] == 0 else "event"
        self.cache[block] = (common, descriptors, scope)
        if len(self.cache) > 4:
            self.cache.popitem(last=False)
        return self.cache[block]

    def query_frame(self, frame):
        if frame not in self.covered:
            return [], Counter()
        block = frame // self.metadata["block_size"]
        local = frame - block * self.metadata["block_size"]
        if block not in self.cache:
            position = self.column_index["frame_offsets"]
            column_start = int(self.offsets[position, block])
            first, last = self.file["data/frame_offsets"][
                column_start + local : column_start + local + 2
            ]
            if first == last:
                return [frame], Counter()
        common, descriptors, scope = self._block(block)
        first, last = common["frame_offsets"][local : local + 2]
        rows = _decode_positions(
            common, descriptors, scope, self.labels, range(int(first), int(last))
        )
        return [frame], Counter(rows)

    def query_atom(self, atom):
        offsets = self.file["index/atom_offsets"][atom : atom + 2]
        ids = self.file["index/atom_occurrences"][int(offsets[0]) : int(offsets[1])]
        blocks = np.searchsorted(self.block_event_offsets, ids, side="right") - 1
        output = []
        for block in np.unique(blocks):
            common, descriptors, scope = self._block(int(block))
            positions = ids[blocks == block] - self.block_event_offsets[block]
            output.extend(
                _decode_positions(common, descriptors, scope, self.labels, positions)
            )
        return self.coverage, Counter(output)


def _group_query(path, kind, index, block_size):
    with h5py.File(path, "r") as file:
        evaluated = file["evaluated_structure_indices"][:].tolist()
        labels = {
            name: file[f"labels/{name}"].asstr()[:]
            for name in ("types", "roles", "evidence")
        }

        def read_selected(block, positions):
            group = file["blocks"][str(block)]
            common = {name: dataset[:] for name, dataset in group["common"].items()}
            descriptors = {
                name: dataset[:] for name, dataset in group["descriptors"].items()
            }
            return _decode_positions(
                common, descriptors, group.attrs["scope"], labels, positions
            )

        if kind == "frame":
            if index not in set(evaluated):
                return [], Counter()
            block = index // block_size
            group = file["blocks"][str(block)]
            local = index - block * block_size
            first, last = group["common/frame_offsets"][local : local + 2]
            if first == last:
                return [index], Counter()
            return [index], Counter(read_selected(block, range(int(first), int(last))))
        index_group = file["index"]
        first, last = index_group["atom_offsets"][index : index + 2]
        ids = index_group["atom_occurrences"][int(first) : int(last)]
        block_offsets = index_group["block_event_offsets"][:]
        blocks = np.searchsorted(block_offsets, ids, side="right") - 1
        output = []
        for block in np.unique(blocks):
            positions = ids[blocks == block] - block_offsets[block]
            output.extend(read_selected(int(block), positions))
        return evaluated, Counter(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--block-size", type=int, default=100)
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    if args.block_size < 1 or args.repeats < 1:
        parser.error("block size and repeats must be positive")
    n_frames, n_atoms = 1000, 500
    records, evaluated = generate_fixture(n_frames, n_atoms, 8, "mixed", 251)
    requests = (("frame", 2), ("frame", 1), ("frame", 750), ("atom", 0), ("atom", 42))
    with tempfile.TemporaryDirectory() as directory:
        group_path = Path(directory) / "group.h5i"
        flat_path = Path(directory) / "flat.h5i"
        sqlite_path = Path(directory) / "rows.sqlite"
        group_info = write_group_file(
            group_path,
            records,
            evaluated,
            n_frames,
            n_atoms,
            args.block_size,
            "adaptive",
        )
        flat_info = write_flat_file(
            flat_path,
            records,
            evaluated,
            n_frames,
            n_atoms,
            args.block_size,
        )
        sqlite = SQLiteProbe.create(sqlite_path, records, evaluated, n_atoms, n_frames)
        sqlite.close()
        measurements = {}
        for kind, index in requests:
            spec = {"frames": [index]} if kind == "frame" else {"atoms": [index]}
            oracle = expected(records, evaluated, **spec)
            key = f"{kind}:{index}"
            measurements[key] = {"rows": sum(oracle[1].values())}
            for backend in ("group", "flat", "sqlite"):
                times = []
                for _ in range(args.repeats):
                    start = time.perf_counter_ns()
                    if backend == "group":
                        actual = _group_query(group_path, kind, index, args.block_size)
                    elif backend == "flat":
                        reader = FlatReader(flat_path)
                        actual = (
                            reader.query_frame(index)
                            if kind == "frame"
                            else reader.query_atom(index)
                        )
                        reader.close()
                    else:
                        probe = SQLiteProbe(sqlite_path)
                        actual = probe.materialize(probe.select(spec))
                        probe.close()
                    times.append((time.perf_counter_ns() - start) / 1e6)
                    if actual != oracle:
                        raise AssertionError(f"{backend} {key} differs from oracle")
                measurements[key][backend] = round(statistics.median(times), 3)
        print(
            json.dumps(
                {
                    "platform": platform.platform(),
                    "h5py": h5py.__version__,
                    "block_size": args.block_size,
                    "repeats": args.repeats,
                    "occurrences": len(records),
                    "group": group_info,
                    "flat": flat_info,
                    "sqlite_file_bytes": sqlite_path.stat().st_size,
                    "median_open_query_ms": measurements,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
