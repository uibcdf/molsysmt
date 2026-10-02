#!/usr/bin/env python3
"""Benchmark synthetic sparse interaction storage and indexed queries."""

from __future__ import annotations

import argparse
import gc
import json
import platform
import statistics
import sys
import tempfile
import time
from importlib.metadata import version
from pathlib import Path

import numpy as np

import molsysmt as msm


def _deep_size(value, seen=None):
    if seen is None:
        seen = set()
    if id(value) in seen:
        return 0
    seen.add(id(value))
    size = sys.getsizeof(value)
    if isinstance(value, dict):
        size += sum(
            _deep_size(key, seen) + _deep_size(item, seen)
            for key, item in value.items()
        )
    elif isinstance(value, (tuple, list)):
        size += sum(_deep_size(item, seen) for item in value)
    elif hasattr(value, "__dict__"):
        size += _deep_size(vars(value), seen)
    return size


def _timed_queries(call, requests):
    samples = []
    for request in requests:
        start = time.perf_counter()
        call(request)
        samples.append((time.perf_counter() - start) * 1000)
    return {
        "median_ms": statistics.median(samples),
        "p95_ms": sorted(samples)[int(0.95 * (len(samples) - 1))],
    }


def _linux_memory_bytes():
    status = Path("/proc/self/status")
    if not status.exists():
        return {}
    return {
        key: int(value.split()[0]) * 1024
        for line in status.read_text().splitlines()
        if (parts := line.split(":", 1)) and len(parts) == 2
        for key, value in [parts]
        if key in {"VmRSS", "VmHWM"}
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--atoms", type=int, default=1000)
    parser.add_argument("--per-frame", type=int, default=10)
    parser.add_argument(
        "--distinct-relations",
        action="store_true",
        help="Generate fresh participant sets on every frame",
    )
    args = parser.parse_args()
    if args.frames < 1 or args.atoms < 30 or args.per_frame < 1:
        parser.error("frames and per-frame must be positive; atoms must be at least 30")

    rng = np.random.default_rng(251)
    relation_pool = []
    for index in range(200):
        atoms = rng.choice(args.atoms, size=3, replace=False).tolist()
        relation_pool.append(
            (
                "hbond",
                [
                    ("donor", [atoms[0]]),
                    ("hydrogen", [atoms[1]]),
                    ("acceptor", [atoms[2]]),
                ],
            )
        )
    for index in range(100):
        atoms = rng.choice(args.atoms, size=6, replace=False).tolist()
        relation_pool.append(("pi_pi", [("ring", atoms[:3]), ("ring", atoms[3:])]))
    for index in range(100):
        atoms = rng.choice(args.atoms, size=2, replace=False).tolist()
        relation_pool.append(
            ("disulfide_candidate", [("sulfur", [atoms[0]]), ("sulfur", [atoms[1]])])
        )

    rss_before_records = _linux_memory_bytes().get("VmRSS")
    records = []
    for frame in range(args.frames):
        for relation in rng.choice(
            len(relation_pool),
            size=args.per_frame,
            replace=False if args.per_frame <= len(relation_pool) else True,
        ):
            kind, participants = relation_pool[int(relation)]
            if args.distinct_relations:
                sizes = [len(atoms) for _, atoms in participants]
                sampled = rng.choice(args.atoms, size=sum(sizes), replace=False)
                cursor = 0
                fresh = []
                for (role, _), size in zip(participants, sizes):
                    fresh.append((role, sampled[cursor : cursor + size].tolist()))
                    cursor += size
                participants = fresh
            records.append(
                {
                    "structure_index": frame,
                    "interaction_type": kind,
                    "participants": [
                        {"role": role, "atom_indices": atoms}
                        for role, atoms in participants
                    ],
                    "measurements": {"distance": float(rng.uniform(0.1, 0.5))},
                }
            )
    start = time.perf_counter()
    result = msm.Interactions.from_records(
        records,
        n_atoms=args.atoms,
        n_structures=args.frames,
        evaluated_structure_indices=np.arange(args.frames),
        method="synthetic_benchmark",
        measure_units={"distance": "nm"},
    )
    build_s = time.perf_counter() - start
    rss_after_build = _linux_memory_bytes().get("VmRSS")
    del records
    gc.collect()
    memory_after_input_release = _linux_memory_bytes()
    bytes_before_index = _deep_size(result)
    start = time.perf_counter()
    result.query(atom_indices=[0])
    index_s = time.perf_counter() - start
    bytes_after_index = _deep_size(result)

    frames = rng.integers(0, args.frames, size=200)
    atoms = rng.integers(0, args.atoms, size=200)
    frame_times = _timed_queries(
        lambda frame: result.query(structure_indices=[int(frame)]), frames
    )
    atom_times = _timed_queries(
        lambda atom: result.query(atom_indices=[int(atom)]), atoms
    )
    structure_groups = rng.integers(0, args.frames, size=(200, 4))
    combined_times = _timed_queries(
        lambda request: result.query(
            structure_indices=request[0], atom_indices=[int(request[1])]
        ),
        zip(structure_groups, atoms),
    )
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "interactions.h5i"
        start = time.perf_counter()
        result.save(path)
        save_s = time.perf_counter() - start
        file_bytes = path.stat().st_size
        import h5py

        with h5py.File(path, "r") as file:
            metadata_attr_bytes = len(file.attrs["metadata"].encode("utf-8"))
        start = time.perf_counter()
        loaded = msm.Interactions.load(path)
        load_s = time.perf_counter() - start
        assert loaded.n_interactions == result.n_interactions

    cpu_info = Path("/proc/cpuinfo")
    cpu_model = (
        next(
            (
                line.split(":", 1)[1].strip()
                for line in cpu_info.read_text().splitlines()
                if line.startswith("model name")
            ),
            None,
        )
        if cpu_info.exists()
        else None
    )
    print(
        json.dumps(
            {
                "platform": platform.platform(),
                "python": platform.python_version(),
                "cpu_model": cpu_model,
                "numpy": np.__version__,
                "h5py": version("h5py"),
                "frames": args.frames,
                "atoms": args.atoms,
                "distinct_relations": args.distinct_relations,
                "occurrences": result.n_interactions,
                "relations": len(result.relation_types),
                "build_s": build_s,
                "cold_atom_index_s": index_s,
                "result_bytes_before_index": bytes_before_index,
                "result_bytes_after_index": bytes_after_index,
                "numeric_bytes_after_index": result.numeric_nbytes,
                "rss_before_records_bytes": rss_before_records,
                "rss_after_build_bytes": rss_after_build,
                "rss_after_input_release_bytes": memory_after_input_release.get(
                    "VmRSS"
                ),
                "peak_rss_bytes": memory_after_input_release.get("VmHWM"),
                "frame_query": frame_times,
                "atom_query": atom_times,
                "combined_query": combined_times,
                "serialized_bytes": file_bytes,
                "metadata_attr_bytes": metadata_attr_bytes,
                "save_s": save_s,
                "load_s": load_s,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
