#!/usr/bin/env python3
"""Verify streamed interaction files with bounded-sample fresh-process reads.

The writer receives one-pass records. The parent replays the deterministic
fixture and retains only requested query signatures for its independent oracle.
Each query opens the file in a new process. The operating-system page cache may
still be warm, so these are fresh-process reads rather than cold-disk reads.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

from benchmark_interactions_contract import (
    _record_atoms,
    _rss,
    _signature,
    iter_fixture,
)
from benchmark_interactions_flat_blocks import FlatReader
from benchmark_interactions_packed_reader import (
    PackedReader,
    column_bytes,
    decoded_counter,
)
from benchmark_interactions_streaming_writer import write_streaming_flat_file


def _digest(value):
    return hashlib.sha256(repr(value).encode()).hexdigest()


def _read(path, kind, index, backend):
    initial_memory = _rss()
    start = time.perf_counter()
    reader = FlatReader(path) if backend == "flat" else PackedReader(path)
    try:
        if kind == "frame":
            coverage, result = (reader.query_frame(index) if backend == "flat"
                                else reader.query_frame_columns(index))
        else:
            coverage, result = (reader.query_atom(index) if backend == "flat"
                                else reader.query_atom_columns(index))
    finally:
        reader.close()
    query_ms = round((time.perf_counter() - start) * 1000, 3)
    final_memory = _rss()
    payload_bytes = None if backend == "flat" else column_bytes(result)
    rows = result if backend == "flat" else decoded_counter(
        result, reader.labels
    )
    return {
        "query_ms": query_ms,
        "coverage_count": len(coverage),
        "coverage_digest": _digest(coverage),
        "rows": sum(rows.values()),
        "rows_digest": _digest(sorted(rows.items())),
        "payload_bytes": payload_bytes,
        "initial_rss_bytes": initial_memory.get("VmRSS"),
        "final_rss_bytes": final_memory.get("VmRSS"),
        "initial_hwm_bytes": initial_memory.get("VmHWM"),
        "final_hwm_bytes": final_memory.get("VmHWM"),
    }


def _oracle(n_frames, n_atoms, per_frame, distribution, frame_indices,
            atom_indices):
    expected = {(kind, index): Counter()
                for kind, indices in (("frame", frame_indices),
                                      ("atom", atom_indices))
                for index in indices}
    frame_set = set(frame_indices)
    atom_set = set(atom_indices)
    records_seen = 0
    for record in iter_fixture(n_frames, n_atoms, per_frame, distribution, 251):
        records_seen += 1
        frame = record["structure_index"]
        matching_atoms = _record_atoms(record) & atom_set
        if frame not in frame_set and not matching_atoms:
            continue
        signature = _signature(record)
        if frame in frame_set:
            expected["frame", frame][signature] += 1
        for atom in matching_atoms:
            expected["atom", atom][signature] += 1
    evaluated = [frame for frame in range(n_frames) if frame % 29 != 0]
    return expected, evaluated, records_seen


def _child(path, kind, index, backend):
    command = [sys.executable, str(Path(__file__).resolve()), "--child",
               "--path", str(path), "--kind", kind, "--index", str(index),
               "--backend", backend]
    start = time.perf_counter()
    process = subprocess.run(command, check=True, capture_output=True, text=True)
    result = json.loads(process.stdout)
    result["process_wall_ms"] = round((time.perf_counter() - start) * 1000, 3)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--child", action="store_true")
    parser.add_argument("--path", type=Path)
    parser.add_argument("--kind", choices=("frame", "atom"))
    parser.add_argument("--index", type=int)
    parser.add_argument("--backend", choices=("flat", "packed"))
    parser.add_argument("--backends", default="flat,packed")
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--atoms", type=int, default=500)
    parser.add_argument("--per-frame", type=int, default=8)
    parser.add_argument("--distribution", choices=("stable", "churn", "mixed"),
                        default="mixed")
    parser.add_argument("--block-size", type=int, default=100)
    args = parser.parse_args()
    if args.child:
        if (args.path is None or args.kind is None or args.index is None
                or args.backend is None):
            parser.error("child reads require path, kind, index, and backend")
        print(json.dumps(_read(args.path, args.kind, args.index, args.backend)))
        return
    backends = tuple(args.backends.split(","))
    if not backends or len(set(backends)) != len(backends) or any(
        backend not in {"flat", "packed"} for backend in backends
    ):
        parser.error("backends must be a unique comma-separated subset of flat,packed")
    if args.frames < 30 or args.per_frame < 1:
        parser.error("frames must be at least 30 and per-frame must be positive")
    if args.atoms < 43 or args.block_size < 30:
        parser.error("atoms must be at least 43 and block size at least 30")
    frame_indices = tuple(dict.fromkeys(
        (0, 1, 2, 10, args.frames // 2, args.frames - 1)
    ))
    atom_indices = tuple(dict.fromkeys((0, 42, args.atoms - 1)))
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "interactions.h5i"
        scratch = Path(directory) / "postings.sqlite"
        start = time.perf_counter()
        write_info = write_streaming_flat_file(
            path,
            iter_fixture(args.frames, args.atoms, args.per_frame,
                         args.distribution, 251),
            (frame for frame in range(args.frames) if frame % 29 != 0),
            args.frames, args.atoms, args.block_size, scratch,
        )
        write_ms = round((time.perf_counter() - start) * 1000, 3)
        expected, evaluated, records_seen = _oracle(
            args.frames, args.atoms, args.per_frame, args.distribution,
            frame_indices, atom_indices,
        )
        queries = []
        for kind, indices in (("frame", frame_indices), ("atom", atom_indices)):
            for index in indices:
                coverage = (
                    [index] if index in evaluated else []
                ) if kind == "frame" else evaluated
                oracle = expected[kind, index]
                for backend in backends:
                    actual = _child(path, kind, index, backend)
                    if (actual["coverage_count"] != len(coverage)
                            or actual["coverage_digest"] != _digest(coverage)
                            or actual["rows"] != sum(oracle.values())
                            or actual["rows_digest"] != _digest(sorted(oracle.items()))):
                        raise AssertionError(
                            f"{backend} {kind} {index} differs from oracle"
                        )
                    queries.append({"backend": backend, "kind": kind,
                                    "index": index, "rows": actual["rows"],
                                    "query_ms": actual["query_ms"],
                                    "process_wall_ms": actual["process_wall_ms"],
                                    "payload_bytes": actual["payload_bytes"],
                                    "initial_rss_bytes": actual["initial_rss_bytes"],
                                    "final_rss_bytes": actual["final_rss_bytes"],
                                    "initial_hwm_bytes": actual["initial_hwm_bytes"],
                                    "final_hwm_bytes": actual["final_hwm_bytes"]})
        print(json.dumps({
            "platform": platform.platform(),
            "frames": args.frames, "atoms": args.atoms,
            "per_frame": args.per_frame, "distribution": args.distribution,
            "block_size": args.block_size, "records_seen": records_seen,
            "write_ms": write_ms,
            "file_bytes": write_info["file_bytes"],
            "scratch_bytes": write_info["scratch_bytes"],
            "mode_counts": {
                "global": write_info["choices"].count(0),
                "event": write_info["choices"].count(1),
            },
            "sampled_requests_verified": len(frame_indices) + len(atom_indices),
            "reader_checks_verified": len(queries),
            "queries": queries,
        }, indent=2))


if __name__ == "__main__":
    main()
