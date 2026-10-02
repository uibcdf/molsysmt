#!/usr/bin/env python3
"""Measure local replacement against full sparse-result reconstruction.

The edit journal here is an exploratory numeric payload. It is not the public
Interactions mutation API and does not provide atomic HDF5 transactions.
"""

from __future__ import annotations

import argparse
import json
import platform
import tempfile
import time
from pathlib import Path

import h5py
import numpy as np
from benchmark_interactions_layouts import (
    build_atom_index,
    check_lossless,
    encode,
    make_events,
    payload_bytes,
    query_atom,
    save_arrays,
    time_queries,
)


def event_atoms(event):
    return {atom for _, member_atoms in event[1][1] for atom in member_atoms}


def replace_affected_events(events, frame, n_atoms):
    original = [event for event in events if event[0] == frame]
    affected_atom = original[0][1][1][0][1][0]
    retained = [event for event in original if affected_atom not in event_atoms(event)]
    new_participants = (
        (0, (affected_atom,)),
        (1, ((affected_atom + 1) % n_atoms,)),
        (2, ((affected_atom + 2) % n_atoms,)),
    )
    new_event = (
        frame,
        (0, new_participants),
        0,
        0.25,
        np.asarray([[0, 0, 0], [0, 0, 0], [1, 0, 0]], dtype=np.int8),
    )
    replacement = [*retained, new_event]
    start = next(index for index, event in enumerate(events) if event[0] == frame)
    end = start + len(original)
    edited = [*events[:start], *replacement, *events[end:]]
    return edited, replacement, affected_atom, len(original) - len(retained)


def encode_local(events, n_frames, n_atoms, first_frame, canonical_ids):
    local_events = [
        (frame - first_frame, key, evidence, distance, images)
        for frame, key, evidence, distance, images in events
    ]
    arrays = encode(local_events, n_frames, n_atoms, "global")
    local_keys = dict.fromkeys(event[1] for event in local_events)
    next_id = max(canonical_ids.values(), default=-1) + 1
    ids = []
    for key in local_keys:
        if key not in canonical_ids:
            canonical_ids[key] = next_id
            next_id += 1
        ids.append(canonical_ids[key])
    arrays["canonical_relation_ids"] = np.asarray(ids, dtype=np.int32)
    arrays["source_frame_map"] = np.arange(
        first_frame, first_frame + n_frames, dtype=np.int32
    )
    return arrays


def write_edit_group(path, name, arrays):
    with h5py.File(path, "r+") as file:
        group = file.require_group("edit_journal").create_group(name)
        group.attrs["scope"] = "replace_evaluated_frames"
        for column, values in arrays.items():
            group.create_dataset(
                column, data=values, compression="gzip" if values.size else None
            )


def atom_count_after_overlay(
    base, base_index, replacement, replacement_index, frame, atom
):
    base_events = query_atom(base, base_index, atom, "event")
    first = base["frame_offsets"][frame]
    last = base["frame_offsets"][frame + 1]
    begin = np.searchsorted(base_events, first)
    end = np.searchsorted(base_events, last)
    replacement_events = query_atom(replacement, replacement_index, atom, "event")
    return len(base_events) - (end - begin) + len(replacement_events)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--atoms", type=int, default=1000)
    parser.add_argument("--block-size", type=int, default=100)
    parser.add_argument("--repeated-edits", type=int, default=20)
    parser.add_argument("--churn", action="store_true")
    args = parser.parse_args()
    if (
        args.frames <= 11
        or args.atoms < 20
        or args.block_size < 1
        or args.repeated_edits < 1
    ):
        parser.error("frames > 11, atoms >= 20, block size and edits positive")
    frame = 10
    events = make_events(args.frames, args.atoms, args.churn)
    base = encode(events, args.frames, args.atoms, "global")
    base_index = build_atom_index(base, args.atoms, "event")
    canonical_ids = {}
    for event_index, event in enumerate(events):
        canonical_ids.setdefault(event[1], event_index)
    edited_events, frame_replacement, affected_atom, removed = replace_affected_events(
        events, frame, args.atoms
    )

    start = time.perf_counter()
    rebuilt = encode(edited_events, args.frames, args.atoms, "global")
    rebuilt_index = build_atom_index(rebuilt, args.atoms, "event")
    full_rebuild_s = time.perf_counter() - start

    start = time.perf_counter()
    frame_delta = encode_local(frame_replacement, 1, args.atoms, frame, canonical_ids)
    frame_index = build_atom_index(frame_delta, args.atoms, "event")
    frame_delta_s = time.perf_counter() - start
    check_lossless(
        frame_delta,
        [
            (0, key, evidence, distance, images)
            for _, key, evidence, distance, images in frame_replacement
        ],
        1,
    )

    block_start = frame // args.block_size * args.block_size
    block_stop = min(block_start + args.block_size, args.frames)
    block_events = [
        event for event in edited_events if block_start <= event[0] < block_stop
    ]
    start = time.perf_counter()
    block_delta = encode_local(
        block_events,
        block_stop - block_start,
        args.atoms,
        block_start,
        canonical_ids,
    )
    block_index = build_atom_index(block_delta, args.atoms, "event")
    block_delta_s = time.perf_counter() - start
    check_lossless(
        block_delta,
        [
            (structure_index - block_start, key, evidence, distance, images)
            for structure_index, key, evidence, distance, images in block_events
        ],
        block_stop - block_start,
    )

    for atom in {affected_atom, (affected_atom + 1) % args.atoms, 0, args.atoms - 1}:
        expected = len(query_atom(rebuilt, rebuilt_index, atom, "event"))
        observed = atom_count_after_overlay(
            base, base_index, frame_delta, frame_index, frame, atom
        )
        assert observed == expected
    assert (
        len(frame_replacement)
        == np.diff(rebuilt["frame_offsets"][[frame, frame + 1]])[0]
    )
    assert len(block_events) == block_delta["frame_offsets"][-1]
    assert frame_delta["source_frame_map"].tolist() == [frame]

    empty_frame = encode_local([], 1, args.atoms, frame, canonical_ids)
    assert empty_frame["evaluated_frames"].tolist() == [0]
    assert empty_frame["frame_offsets"].tolist() == [0, 0]

    requested_atoms = np.r_[
        np.random.default_rng(26).integers(0, args.atoms, size=100),
        np.full(100, affected_atom, dtype=np.int32),
    ]
    full_atom_count_query = time_queries(
        lambda atom: len(query_atom(rebuilt, rebuilt_index, int(atom), "event")),
        requested_atoms,
    )
    overlay_atom_count_query = time_queries(
        lambda atom: atom_count_after_overlay(
            base, base_index, frame_delta, frame_index, frame, int(atom)
        ),
        requested_atoms,
    )

    with tempfile.TemporaryDirectory() as directory:
        base_path = Path(directory) / "base.h5i"
        save_arrays(base_path, base, "global", args.block_size)
        base_file_bytes = base_path.stat().st_size
        start = time.perf_counter()
        write_edit_group(base_path, f"frame_{frame}", frame_delta)
        append_frame_s = time.perf_counter() - start
        frame_append_bytes = base_path.stat().st_size - base_file_bytes

        block_path = Path(directory) / "block.h5i"
        save_arrays(block_path, base, "global", args.block_size)
        base_block_bytes = block_path.stat().st_size
        start = time.perf_counter()
        write_edit_group(block_path, f"block_{block_start}", block_delta)
        append_block_s = time.perf_counter() - start
        block_append_bytes = block_path.stat().st_size - base_block_bytes

        rebuilt_path = Path(directory) / "rebuilt.h5i"
        start = time.perf_counter()
        save_arrays(rebuilt_path, rebuilt, "global", args.block_size)
        rewrite_full_s = time.perf_counter() - start
        rebuilt_file_bytes = rebuilt_path.stat().st_size

        repeated_path = Path(directory) / "repeated.h5i"
        save_arrays(repeated_path, base, "global", args.block_size)
        repeated_base_bytes = repeated_path.stat().st_size
        start = time.perf_counter()
        for version in range(args.repeated_edits):
            version_delta = frame_delta.copy()
            version_delta["distance_nm"] = frame_delta["distance_nm"].copy()
            version_delta["distance_nm"][-1] += version * 1e-6
            write_edit_group(repeated_path, f"version_{version:04d}", version_delta)
        repeated_append_s = time.perf_counter() - start
        repeated_append_bytes = repeated_path.stat().st_size - repeated_base_bytes

    print(
        json.dumps(
            {
                "platform": platform.platform(),
                "python": platform.python_version(),
                "numpy": np.__version__,
                "h5py": h5py.__version__,
                "frames": args.frames,
                "atoms": args.atoms,
                "events_before": len(events),
                "events_after": len(edited_events),
                "churn": args.churn,
                "edited_frame": frame,
                "affected_atom": affected_atom,
                "removed_observations": removed,
                "new_observations": 1,
                "full_rebuild_s": round(full_rebuild_s, 4),
                "frame_delta_build_s": round(frame_delta_s, 4),
                "block_delta_build_s": round(block_delta_s, 4),
                "base_core_bytes": payload_bytes(base),
                "full_rebuilt_core_bytes": payload_bytes(rebuilt),
                "frame_delta_core_bytes": payload_bytes(frame_delta),
                "block_delta_core_bytes": payload_bytes(block_delta),
                "base_atom_index_bytes": payload_bytes(base_index),
                "frame_delta_atom_index_bytes": payload_bytes(frame_index),
                "block_delta_atom_index_bytes": payload_bytes(block_index),
                "base_file_bytes": base_file_bytes,
                "frame_append_bytes": frame_append_bytes,
                "block_append_bytes": block_append_bytes,
                "full_rebuilt_file_bytes": rebuilt_file_bytes,
                "append_frame_s": round(append_frame_s, 4),
                "append_block_s": round(append_block_s, 4),
                "rewrite_full_s": round(rewrite_full_s, 4),
                "repeated_edits": args.repeated_edits,
                "repeated_append_bytes": repeated_append_bytes,
                "repeated_append_s": round(repeated_append_s, 4),
                "full_atom_count_query": full_atom_count_query,
                "overlay_atom_count_query": overlay_atom_count_query,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
