#!/usr/bin/env python3
"""Probe bounded block writing and complete HDF5 interaction queries.

This exploratory codec is not H5MSM and has no transactional update protocol.
It preserves semantic fields but identifies relations by their participant keys
across blocks; local numeric relation IDs are deliberately not global IDs.
Run from the repository root.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import tempfile
import time
from functools import lru_cache
from pathlib import Path

import h5py
import numpy as np
from benchmark_interactions_layouts import (
    EVIDENCE,
    KINDS,
    ROLES,
    build_atom_index,
    encode,
    event_relation,
    iter_event_frames,
    payload_bytes,
)
from benchmark_interactions_layouts import query_atom as query_atom_local


def memory_high_water_bytes():
    """Read the Linux process high-water mark without an optional dependency."""
    try:
        with open("/proc/self/status", encoding="utf-8") as stream:
            for line in stream:
                if line.startswith("VmHWM:"):
                    return int(line.split()[1]) * 1024
    except OSError:
        pass
    return None


def write_arrays(group, arrays):
    for name, array in arrays.items():
        group.create_dataset(name, data=array, compression="gzip" if array.size else None)


def read_arrays(group):
    return {name: dataset[:] for name, dataset in group.items()}


def event_signature(arrays, event, source_frame):
    """Return all semantic fields of one occurrence for correctness checks."""
    relation = int(event_relation(arrays, event))
    first_part = int(arrays["relation_participant_offsets"][relation])
    last_part = int(arrays["relation_participant_offsets"][relation + 1])
    participants = []
    for part in range(first_part, last_part):
        first_atom = int(arrays["participant_atom_offsets"][part])
        last_atom = int(arrays["participant_atom_offsets"][part + 1])
        participants.append((
            int(arrays["participant_roles"][part]),
            tuple(int(atom) for atom in arrays["participant_atoms"][first_atom:last_atom]),
        ))
    first_image = int(arrays["image_offsets"][event])
    last_image = int(arrays["image_offsets"][event + 1])
    return (
        source_frame,
        int(arrays["relation_types"][relation]),
        tuple(participants),
        int(arrays["occurrence_evidence"][event]),
        float(arrays["distance_nm"][event]),
        tuple(tuple(int(x) for x in vector) for vector in
              arrays["image_vectors"][first_image:last_image]),
    )


def source_signature(event):
    frame, (kind, participants), evidence, distance, images = event
    return (
        frame, kind, participants, evidence, distance,
        tuple(tuple(int(x) for x in vector) for vector in images),
    )


def choose_block(events, n_frames, n_atoms, source_start):
    local_events = [(frame - source_start, key, evidence, distance, image)
                    for frame, key, evidence, distance, image in events]
    choices = []
    for scope in ("global", "event"):
        arrays = encode(local_events, n_frames, n_atoms, scope)
        arrays["source_frame_map"] += source_start
        arrays["evaluated_frames"] += source_start
        del arrays["source_atom_map"]
        choices.append((payload_bytes(arrays), scope, arrays))
    _, scope, arrays = min(choices, key=lambda choice: choice[0])
    index = build_atom_index(arrays, n_atoms, scope)
    return scope, arrays, index


def write_blocks(path, n_frames, n_atoms, block_size, churn, duplicates, hot_atom):
    atom_blocks = [[] for _ in range(n_atoms)]
    chosen = {"global": 0, "event": 0}
    max_block_bytes = 0
    total_block_numeric_bytes = 0
    n_events = 0
    empty_frames = 0
    start = time.perf_counter()
    with h5py.File(path, "w") as file:
        file.attrs["codec_probe_version"] = 1
        file.attrs["method"] = "synthetic_file_backed_benchmark"
        file.attrs["units"] = json.dumps({"distance_nm": "nm"})
        file.attrs["type_labels"] = json.dumps(KINDS)
        file.attrs["role_labels"] = json.dumps(ROLES)
        file.attrs["evidence_labels"] = json.dumps(EVIDENCE)
        file.attrs["n_frames"] = n_frames
        file.attrs["n_atoms"] = n_atoms
        file.attrs["block_size"] = block_size
        file.create_dataset("source_atom_map", data=np.arange(n_atoms, dtype=np.int32))
        groups = file.create_group("blocks")
        batch = []
        for frame, frame_events in enumerate(iter_event_frames(
            n_frames, n_atoms, churn, duplicates, hot_atom
        )):
            empty_frames += not frame_events
            n_events += len(frame_events)
            batch.extend(frame_events)
            source_start = (frame // block_size) * block_size
            evaluated = frame - source_start + 1
            if evaluated < block_size and frame + 1 < n_frames:
                continue
            block_number = source_start // block_size
            scope, arrays, index = choose_block(batch, evaluated, n_atoms, source_start)
            chosen[scope] += 1
            block_numeric_bytes = payload_bytes(arrays) + payload_bytes(index)
            max_block_bytes = max(max_block_bytes, block_numeric_bytes)
            total_block_numeric_bytes += block_numeric_bytes
            block = groups.create_group(str(block_number))
            block.attrs["scope"] = scope
            write_arrays(block.create_group("payload"), arrays)
            write_arrays(block.create_group("index"), index)
            present = np.flatnonzero(np.diff(index["atom_offsets"]))
            for atom in present:
                atom_blocks[int(atom)].append(block_number)
            batch.clear()
        assert not batch
        offsets = np.empty(n_atoms + 1, dtype=np.int64)
        offsets[0] = 0
        offsets[1:] = np.cumsum([len(blocks) for blocks in atom_blocks])
        file.create_dataset("atom_block_offsets", data=offsets, compression="gzip")
        file.create_dataset(
            "atom_block_postings",
            data=np.asarray([block for blocks in atom_blocks for block in blocks],
                            dtype=np.int32),
            compression="gzip",
        )
    return {
        "write_s": round(time.perf_counter() - start, 3),
        "file_bytes": os.path.getsize(path),
        "events": n_events,
        "evaluated_empty_frames": empty_frames,
        "chosen_blocks": chosen,
        "max_block_numeric_bytes": max_block_bytes,
        "total_block_numeric_bytes": total_block_numeric_bytes,
        "atom_block_index_python_entries": sum(map(len, atom_blocks)),
        "process_peak_rss_bytes": memory_high_water_bytes(),
    }


def read_block(file, block_number):
    group = file["blocks"][str(block_number)]
    return group.attrs["scope"], read_arrays(group["payload"]), read_arrays(group["index"])


def query_frame(file, frame, block_reader=None):
    block_number = frame // int(file.attrs["block_size"])
    _, arrays, _ = (read_block(file, block_number) if block_reader is None
                    else block_reader(block_number))
    local_frame = frame - block_number * int(file.attrs["block_size"])
    first = int(arrays["frame_offsets"][local_frame])
    last = int(arrays["frame_offsets"][local_frame + 1])
    return [event_signature(arrays, event, frame) for event in range(first, last)]


def query_frame_projected(file, frame):
    """Read only the occurrence and descriptor columns needed by one structure."""
    block_number = frame // int(file.attrs["block_size"])
    block = file["blocks"][str(block_number)]
    payload = block["payload"]
    local_frame = frame - block_number * int(file.attrs["block_size"])
    first, last = (int(x) for x in payload["frame_offsets"][local_frame:local_frame + 2])
    if first == last:
        return []
    arrays = {
        "occurrence_evidence": payload["occurrence_evidence"][first:last],
        "distance_nm": payload["distance_nm"][first:last],
    }
    image_offsets = payload["image_offsets"][first:last + 1]
    arrays["image_vectors"] = payload["image_vectors"][
        int(image_offsets[0]):int(image_offsets[-1])
    ]
    arrays["image_offsets"] = image_offsets - image_offsets[0]
    if block.attrs["scope"] == "event":
        relation_offsets = payload["relation_participant_offsets"][first:last + 1]
        part_first, part_last = int(relation_offsets[0]), int(relation_offsets[-1])
        atom_offsets = payload["participant_atom_offsets"][part_first:part_last + 1]
        arrays.update({
            "relation_types": payload["relation_types"][first:last],
            "relation_participant_offsets": relation_offsets - part_first,
            "participant_roles": payload["participant_roles"][part_first:part_last],
            "participant_atom_offsets": atom_offsets - atom_offsets[0],
            "participant_atoms": payload["participant_atoms"][
                int(atom_offsets[0]):int(atom_offsets[-1])
            ],
        })
    else:
        arrays["occurrence_relations"] = payload["occurrence_relations"][first:last]
        for name in (
            "relation_types", "relation_participant_offsets", "participant_roles",
            "participant_atom_offsets", "participant_atoms",
        ):
            arrays[name] = payload[name][:]
    return [event_signature(arrays, event, frame) for event in range(last - first)]


def query_atom(file, atom, frames=None, block_reader=None):
    offsets = file["atom_block_offsets"]
    first, last = offsets[atom:atom + 2]
    blocks = file["atom_block_postings"][first:last]
    selected = None if frames is None else set(int(frame) for frame in frames)
    selected_blocks = None if selected is None else {
        frame // int(file.attrs["block_size"]) for frame in selected
    }
    results = []
    for block_number in blocks:
        if selected_blocks is not None and int(block_number) not in selected_blocks:
            continue
        scope, arrays, index = (read_block(file, int(block_number))
                                if block_reader is None else block_reader(int(block_number)))
        for event in query_atom_local(arrays, index, atom, scope):
            local_frame = int(np.searchsorted(arrays["frame_offsets"], event,
                                              side="right") - 1)
            source_frame = int(arrays["source_frame_map"][local_frame])
            if selected is None or source_frame in selected:
                results.append(event_signature(arrays, int(event), source_frame))
    return results


def timings(function, requests):
    values = []
    sizes = []
    for request in requests:
        start = time.perf_counter_ns()
        result = function(request)
        values.append((time.perf_counter_ns() - start) / 1e6)
        sizes.append(len(result))
    return {
        "median_ms": round(statistics.median(values), 3),
        "p95_ms": round(sorted(values)[int(0.95 * (len(values) - 1))], 3),
        "result_count_median": statistics.median(sizes),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=10000)
    parser.add_argument("--atoms", type=int, default=1000)
    parser.add_argument("--block-size", type=int, default=500)
    parser.add_argument("--churn", action="store_true")
    parser.add_argument("--duplicates", action="store_true")
    parser.add_argument("--hot-atom", action="store_true")
    parser.add_argument("--write-only", action="store_true",
                        help="Skip verification and queries for write scaling runs")
    args = parser.parse_args()
    if args.frames < 2 or args.atoms < 20 or args.block_size < 1:
        parser.error("frames >= 2, atoms >= 20, and positive block-size required")
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "interactions.h5i"
        result = write_blocks(path, args.frames, args.atoms, args.block_size,
                              args.churn, args.duplicates, args.hot_atom)
        if args.write_only:
            result["config"] = vars(args)
            print(json.dumps(result, indent=2))
            return
        rng = np.random.default_rng(29)
        frames = [0, 1, min(17, args.frames - 1), args.frames - 1]
        frames.extend(int(x) for x in rng.integers(0, args.frames, size=16))
        atoms = [0, 1, args.atoms // 2]
        atoms.extend(int(x) for x in rng.integers(0, args.atoms, size=3))
        expected_frames = {frame: [] for frame in frames}
        expected_atoms = {atom: [] for atom in atoms}
        for frame_events in iter_event_frames(
            args.frames, args.atoms, args.churn, args.duplicates, args.hot_atom
        ):
            for event in frame_events:
                frame, key = event[:2]
                signature = source_signature(event)
                if frame in expected_frames:
                    expected_frames[frame].append(signature)
                participant_atoms = {atom for _, members in key[1] for atom in members}
                for atom in participant_atoms & expected_atoms.keys():
                    expected_atoms[atom].append(signature)
        with h5py.File(path, "r") as file:
            for frame, expected in expected_frames.items():
                assert query_frame(file, frame) == expected
                assert query_frame_projected(file, frame) == expected
            for atom, expected in expected_atoms.items():
                assert query_atom(file, atom) == expected
            selected = [args.frames - 1, 1, 1, 0]
            assert query_atom(file, atoms[0], selected) == [
                event for event in expected_atoms[atoms[0]] if event[0] in set(selected)
            ]
            result["frame_query_full"] = timings(
                lambda frame: query_frame(file, frame), frames
            )
            result["frame_query_projected"] = timings(
                lambda frame: query_frame_projected(file, frame), frames
            )
            result["atom_query_full_trajectory"] = timings(
                lambda atom: query_atom(file, atom), atoms
            )
            result["atom_query_selected_frames"] = timings(
                lambda atom: query_atom(file, atom, selected), atoms
            )
            total_blocks = (args.frames + args.block_size - 1) // args.block_size
            cached_reader = lru_cache(maxsize=total_blocks)(
                lambda block_number: read_block(file, block_number)
            )
            for block_number in range(total_blocks):
                cached_reader(block_number)
            result["full_block_cache"] = {
                "capacity_blocks": total_blocks,
                "numeric_bytes": result["total_block_numeric_bytes"],
                "frame_query": timings(
                    lambda frame: query_frame(file, frame, cached_reader), frames
                ),
                "atom_query_full_trajectory": timings(
                    lambda atom: query_atom(file, atom, block_reader=cached_reader),
                    atoms,
                ),
            }
            small_capacity = min(4, total_blocks)
            small_reader = lru_cache(maxsize=small_capacity)(
                lambda block_number: read_block(file, block_number)
            )
            result["small_block_cache"] = {
                "capacity_blocks": small_capacity,
                "frame_query": timings(
                    lambda frame: query_frame(file, frame, small_reader), frames
                ),
                "atom_query_full_trajectory": timings(
                    lambda atom: query_atom(file, atom, block_reader=small_reader),
                    atoms,
                ),
                "cache_info": str(small_reader.cache_info()),
            }
        result["config"] = vars(args)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
