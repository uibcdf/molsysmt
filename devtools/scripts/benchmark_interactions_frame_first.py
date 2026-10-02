#!/usr/bin/env python3
"""Compare frame-first and atom-posting plans for narrow trajectory queries.

The output is a complete typed selection with grouped participants, roles,
measurements, evidence, and images. Fresh child processes avoid sharing a
Python block cache; the operating-system page cache may still be warm.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import statistics
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
from benchmark_interactions_packed_reader import (
    PackedReader,
    column_bytes,
    decoded_counter,
)
from benchmark_interactions_streaming_writer import write_streaming_flat_file


def _digest(value):
    return hashlib.sha256(repr(value).encode()).hexdigest()


def _selection(n_frames):
    return [n_frames - 1, 2, n_frames // 2, 10, 2, 1, 0]


def _child(path, frames, planner):
    initial = _rss()
    start = time.perf_counter()
    reader = PackedReader(path)
    try:
        coverage, columns = reader.query_columns(
            structure_indices=frames, atom_indices=[0], planner=planner
        )
        query_ms = (time.perf_counter() - start) * 1000
        memory = _rss()
        rows = decoded_counter(columns, reader.labels)
    finally:
        reader.close()
    return {
        "query_ms": round(query_ms, 3),
        "rows": sum(rows.values()),
        "rows_digest": _digest(sorted(rows.items())),
        "coverage": coverage,
        "payload_bytes": column_bytes(columns),
        "hwm_growth_bytes": memory["VmHWM"] - initial["VmHWM"],
    }


def _oracle(n_frames, n_atoms, per_frame, distribution, frames):
    coverage = [frame for frame in dict.fromkeys(frames) if frame % 29 != 0]
    selected = set(coverage)
    rows = Counter()
    for record in iter_fixture(n_frames, n_atoms, per_frame, distribution, 251):
        if record["structure_index"] in selected and 0 in _record_atoms(record):
            rows[_signature(record)] += 1
    return coverage, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--child", action="store_true")
    parser.add_argument("--path", type=Path)
    parser.add_argument("--planner", choices=("frame", "atom", "auto"))
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--atoms", type=int, default=500)
    parser.add_argument("--per-frame", type=int, default=8)
    parser.add_argument(
        "--distribution", choices=("stable", "mixed", "churn"), default="churn"
    )
    parser.add_argument("--block-size", type=int, default=100)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    if args.child:
        if args.path is None or args.planner is None:
            parser.error("child requires path and planner")
        print(json.dumps(_child(args.path, _selection(args.frames), args.planner)))
        return
    if args.frames < 30 or args.atoms < 30 or args.per_frame < 1:
        parser.error("frames and atoms must be at least 30; per-frame positive")
    if args.block_size < 30 or args.repeats < 1:
        parser.error("block size must be at least 30; repeats positive")
    frames = _selection(args.frames)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "interactions.h5i"
        scratch = Path(directory) / "postings.sqlite"
        info = write_streaming_flat_file(
            path,
            iter_fixture(
                args.frames, args.atoms, args.per_frame, args.distribution, 251
            ),
            (frame for frame in range(args.frames) if frame % 29 != 0),
            args.frames,
            args.atoms,
            args.block_size,
            scratch,
        )
        coverage, oracle = _oracle(
            args.frames, args.atoms, args.per_frame, args.distribution, frames
        )
        oracle_digest = _digest(sorted(oracle.items()))
        measurements = {plan: [] for plan in ("frame", "atom", "auto")}
        for _ in range(args.repeats):
            for plan in measurements:
                command = [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    "--child",
                    "--path",
                    str(path),
                    "--planner",
                    plan,
                    "--frames",
                    str(args.frames),
                ]
                process = subprocess.run(
                    command, check=True, capture_output=True, text=True
                )
                result = json.loads(process.stdout)
                if (
                    result["coverage"] != coverage
                    or result["rows"] != sum(oracle.values())
                    or result["rows_digest"] != oracle_digest
                ):
                    raise AssertionError(f"{plan} differs from record oracle")
                measurements[plan].append(result)
        print(
            json.dumps(
                {
                    "platform": platform.platform(),
                    "frames": args.frames,
                    "atoms": args.atoms,
                    "per_frame": args.per_frame,
                    "distribution": args.distribution,
                    "selected_frames": frames,
                    "returned_rows": sum(oracle.values()),
                    "file_bytes": info["file_bytes"],
                    "repeats": args.repeats,
                    "plans": {
                        plan: {
                            "median_query_ms": round(
                                statistics.median(
                                    result["query_ms"] for result in results
                                ),
                                3,
                            ),
                            "median_hwm_growth_bytes": int(
                                statistics.median(
                                    result["hwm_growth_bytes"] for result in results
                                )
                            ),
                            "payload_bytes": results[0]["payload_bytes"],
                        }
                        for plan, results in measurements.items()
                    },
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
