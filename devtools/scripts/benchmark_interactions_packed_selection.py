#!/usr/bin/env python3
"""Check typed file queries against source-index and atom-set record semantics.

The streamed file is read through the experimental packed reader. The oracle
selects full records independently of file indexes and descriptor encodings.
"""

from __future__ import annotations

import argparse
import json
import platform
import tempfile
import time
from pathlib import Path

from benchmark_interactions_contract import (
    _record_atoms,
    expected,
    generate_fixture,
)
from benchmark_interactions_packed_reader import PackedReader, decoded_counter
from benchmark_interactions_streaming_writer import write_streaming_flat_file


def _requests(records, n_frames):
    ring = next(row for row in records if row["interaction_type"] == "pi_pi")
    first_ring = ring["participants"][0]["atom_indices"]
    second_ring = ring["participants"][1]["atom_indices"]
    whole_relation = sorted(_record_atoms(ring))
    frames = [
        n_frames - 1,
        ring["structure_index"],
        1,
        ring["structure_index"],
        0,
        n_frames // 2,
    ]
    return (
        {"frames": frames},
        {"frames": [0, 1]},
        {"frames": [ring["structure_index"]]},
        {"atoms": [0]},
        {"atoms": [first_ring[0], first_ring[0]]},
        {"atoms": first_ring, "mode": "incident", "frames": frames},
        {"atoms": first_ring, "mode": "internal", "frames": frames},
        {"atoms": first_ring, "mode": "cross", "frames": frames},
        {"atoms": whole_relation, "mode": "internal", "frames": frames},
        {"atoms": whole_relation, "mode": "cross"},
        {"atoms": [], "mode": "incident", "frames": frames},
        {"between": (first_ring, second_ring), "frames": frames},
        {"between": (first_ring, second_ring), "exclusive": True, "frames": frames},
        {"between": (whole_relation, second_ring), "exclusive": True, "frames": frames},
        {},
    )


def _check(reader, records, evaluated, spec, planner):
    if "between" in spec:
        a, b = spec["between"]
        actual_coverage, columns = reader.between_columns(
            a,
            b,
            structure_indices=spec.get("frames"),
            exclusive=spec.get("exclusive", False),
            planner=planner,
        )
    else:
        actual_coverage, columns = reader.query_columns(
            structure_indices=spec.get("frames"),
            atom_indices=spec.get("atoms"),
            mode=spec.get("mode", "incident"),
            planner=planner,
        )
    oracle_coverage, oracle_rows = expected(records, evaluated, **spec)
    if actual_coverage != oracle_coverage:
        raise AssertionError(f"coverage differs for {spec} with {planner}")
    if decoded_counter(columns, reader.labels) != oracle_rows:
        raise AssertionError(f"complete rows differ for {spec} with {planner}")
    if any(value.dtype.hasobject for value in columns.values()):
        raise AssertionError("typed projection contains an object array")
    count = len(columns["structure_indices"])
    if count == 0 and (
        columns["participant_offsets"].tolist() != [0]
        or columns["atom_offsets"].tolist() != [0]
        or columns["image_vectors"].shape != (0, 3)
    ):
        raise AssertionError("empty selection has unstable typed shape")
    found_frames = list(dict.fromkeys(columns["structure_indices"].tolist()))
    expected_frames = [
        frame
        for frame in oracle_coverage
        if any(signature[0] == frame for signature in oracle_rows)
    ]
    if found_frames != expected_frames:
        raise AssertionError(
            f"structure request order differs for {spec} with {planner}"
        )
    return count


def _edge_cases(directory):
    """Exercise repeated atoms, compound overlap, and parallel observations."""
    records = [
        {
            "structure_index": 2,
            "interaction_type": "three_body",
            "participants": [
                {"role": "left", "atom_indices": [0, 1]},
                {"role": "right", "atom_indices": [0, 2]},
            ],
            "evidence": "observed_geometry",
            "measurements": {"distance": 0.25, "angle": 0.4},
            "images": [[0, 0, 0], [1, 0, 0]],
        },
        {
            "structure_index": 3,
            "interaction_type": "pair",
            "participants": [
                {"role": "first", "atom_indices": [3]},
                {"role": "second", "atom_indices": [4]},
            ],
            "evidence": "source_annotation",
            "measurements": {"distance": 0.30, "angle": -1.0},
            "images": [[0, 0, 0], [0, 0, 0]],
        },
        {
            "structure_index": 3,
            "interaction_type": "pair",
            "participants": [
                {"role": "first", "atom_indices": [3]},
                {"role": "second", "atom_indices": [4]},
            ],
            "evidence": "source_annotation",
            "measurements": {"distance": 0.32, "angle": -1.0},
            "images": [[0, 1, 0], [0, 0, 0]],
        },
        {
            "structure_index": 6,
            "interaction_type": "pi_pi",
            "participants": [
                {"role": "ring", "atom_indices": [5, 6, 7]},
                {"role": "ring", "atom_indices": [7, 8, 9]},
            ],
            "evidence": "observed_geometry",
            "measurements": {"distance": 0.35, "angle": 0.1},
            "images": [[0, 0, 0], [0, 0, 0]],
        },
    ]
    evaluated = [2, 3, 4, 5, 6]
    specs = (
        {"frames": [6, 5, 2, 2, 0], "atoms": [0], "mode": "cross"},
        {"frames": [2], "atoms": [0, 1, 2], "mode": "internal"},
        {"frames": [2], "atoms": [0, 1], "mode": "cross"},
        {"frames": [3], "atoms": [3, 4], "mode": "internal"},
        {"frames": [6], "atoms": [7], "mode": "cross"},
        {"between": ([0], [1]), "frames": [2]},
        {"between": ([0, 1], [0, 2]), "frames": [2], "exclusive": True},
        {"frames": [5]},
    )
    path = directory / "edge_interactions.h5i"
    scratch = directory / "edge_postings.sqlite"
    write_streaming_flat_file(path, iter(records), iter(evaluated), 40, 43, 30, scratch)
    reader = PackedReader(path)
    checks = 0
    try:
        for spec in specs:
            planners = (
                ("auto", "frame", "atom")
                if "atoms" in spec or "between" in spec
                else ("auto",)
            )
            for planner in planners:
                _check(reader, records, evaluated, spec, planner)
                checks += 1
    finally:
        reader.close()
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--atoms", type=int, default=500)
    parser.add_argument("--per-frame", type=int, default=8)
    parser.add_argument("--block-size", type=int, default=100)
    parser.add_argument(
        "--distribution", choices=("stable", "mixed", "churn"), default="mixed"
    )
    args = parser.parse_args()
    if args.frames < 30 or args.atoms < 30 or args.per_frame < 1:
        parser.error("frames and atoms must be at least 30; per-frame positive")
    if args.block_size < 30:
        parser.error("block size must be at least 30")
    records, evaluated = generate_fixture(
        args.frames, args.atoms, args.per_frame, args.distribution, 251
    )
    requests = _requests(records, args.frames)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "interactions.h5i"
        scratch = Path(directory) / "postings.sqlite"
        write_info = write_streaming_flat_file(
            path,
            iter(records),
            iter(evaluated),
            args.frames,
            args.atoms,
            args.block_size,
            scratch,
        )
        reader = PackedReader(path)
        try:
            start = time.perf_counter()
            counts = []
            checks = 0
            for spec in requests:
                planners = (
                    ("auto", "frame", "atom")
                    if spec.get("frames") is not None
                    and ("atoms" in spec or "between" in spec)
                    else ("auto",)
                )
                for planner in planners:
                    count = _check(reader, records, evaluated, spec, planner)
                    checks += 1
                    if planner == "auto":
                        counts.append(count)
            query_s = time.perf_counter() - start
        finally:
            reader.close()
        edge_checks = _edge_cases(Path(directory))
        print(
            json.dumps(
                {
                    "platform": platform.platform(),
                    "frames": args.frames,
                    "atoms": args.atoms,
                    "distribution": args.distribution,
                    "occurrences": len(records),
                    "file_bytes": write_info["file_bytes"],
                    "mode_counts": {
                        "global": write_info["choices"].count(0),
                        "event": write_info["choices"].count(1),
                    },
                    "semantic_cases_verified": len(counts),
                    "planner_checks_verified": checks,
                    "edge_case_checks_verified": edge_checks,
                    "selected_counts": counts,
                    "query_and_oracle_s": round(query_s, 3),
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
