#!/usr/bin/env python3
"""Compare frame-major and temporal-run incidence indexes.

This probe measures only structure/relation incidence indexes. It excludes
the common relation descriptors and per-occurrence measurements. A run maps
each structure to a measurement row, so geometry is not discarded. Parallel
observations and changing relation membership are not encoded here.

The Rust probe runs in a child process. Its parent owns the compiled library
directory until the child exits; native call timings exclude compilation and
process startup. This does not measure total process memory or startup latency.
"""

from __future__ import annotations

import argparse
import ctypes
import json
import os
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import h5py
import numpy as np


def generate(n_frames, n_relations, active_count, survival):
    """Generate correlated relation presence with explicit empty endpoints."""
    rng = np.random.default_rng(251)
    active = set(int(x) for x in rng.choice(n_relations, active_count, replace=False))
    by_frame = [[]]
    for frame in range(1, n_frames - 1):
        if frame > 1:
            active = {relation for relation in active if rng.random() < survival}
            needed = active_count - len(active)
            if needed:
                candidates = np.fromiter(
                    (
                        relation
                        for relation in range(n_relations)
                        if relation not in active
                    ),
                    dtype=np.int32,
                )
                active.update(
                    int(x) for x in rng.choice(candidates, needed, replace=False)
                )
        by_frame.append(sorted(active))
    by_frame.append([])
    return by_frame


def frame_major(by_frame):
    counts = np.asarray([len(relations) for relations in by_frame], dtype=np.int32)
    offsets = np.empty(len(by_frame) + 1, dtype=np.int32)
    offsets[0] = 0
    offsets[1:] = np.cumsum(counts)
    relations = np.asarray(
        [relation for members in by_frame for relation in members], dtype=np.int32
    )
    return offsets, relations


def temporal_runs(by_frame, n_relations, block_size):
    """Encode relation-major runs and block-level candidate bitmaps."""
    runs = [[] for _ in range(n_relations)]
    for frame, relations in enumerate(by_frame):
        for relation in relations:
            if runs[relation] and runs[relation][-1][1] == frame:
                runs[relation][-1][1] += 1
            else:
                runs[relation].append([frame, frame + 1])
    relation_offsets = np.empty(n_relations + 1, dtype=np.int32)
    relation_offsets[0] = 0
    relation_offsets[1:] = np.cumsum([len(group) for group in runs])
    starts = np.asarray([start for group in runs for start, _ in group], dtype=np.int32)
    ends = np.asarray([end for group in runs for _, end in group], dtype=np.int32)
    lengths = ends - starts
    measure_starts = np.empty(len(starts), dtype=np.int32)
    if len(starts):
        measure_starts[0] = 0
        measure_starts[1:] = np.cumsum(lengths[:-1])
    n_blocks = (len(by_frame) + block_size - 1) // block_size
    candidates = np.zeros((n_blocks, n_relations), dtype=np.bool_)
    for relation, group in enumerate(runs):
        for start, end in group:
            candidates[start // block_size : (end - 1) // block_size + 1, relation] = (
                True
            )
    packed_candidates = np.packbits(candidates, axis=1, bitorder="little")
    return relation_offsets, starts, ends, measure_starts, packed_candidates


def frame_query(offsets, relations, frame):
    return relations[offsets[frame] : offsets[frame + 1]]


def run_query(index, frame, block_size, n_relations):
    offsets, starts, ends, measure_starts, packed_candidates = index
    bits = np.unpackbits(packed_candidates[frame // block_size], bitorder="little")[
        :n_relations
    ]
    present = []
    measure_rows = []
    for relation in np.flatnonzero(bits):
        first, last = int(offsets[relation]), int(offsets[relation + 1])
        run = first + int(np.searchsorted(starts[first:last], frame, side="right")) - 1
        if run >= first and frame < ends[run]:
            present.append(int(relation))
            measure_rows.append(int(measure_starts[run] + frame - starts[run]))
    return np.asarray(present, dtype=np.int32), np.asarray(measure_rows, dtype=np.int32)


def run_query_vectorized(index, frame, block_size, n_relations):
    """Search candidate relation runs in batched NumPy operations."""
    offsets, starts, ends, measure_starts, packed_candidates = index
    bits = np.unpackbits(packed_candidates[frame // block_size], bitorder="little")[
        :n_relations
    ]
    candidates = np.flatnonzero(bits).astype(np.int32)
    if not len(candidates):
        empty = np.empty(0, dtype=np.int32)
        return empty, empty
    low = offsets[candidates].copy()
    high = offsets[candidates + 1].copy()
    while np.any(low < high):
        active = np.flatnonzero(low < high)
        middle = (low[active] + high[active]) // 2
        later = starts[middle] <= frame
        low[active[later]] = middle[later] + 1
        high[active[~later]] = middle[~later]
    runs = low - 1
    safe_runs = np.maximum(runs, 0)
    present = (runs >= offsets[candidates]) & (frame < ends[safe_runs])
    selected = runs[present]
    measure_rows = measure_starts[selected] + frame - starts[selected]
    return candidates[present], measure_rows.astype(np.int32, copy=False)


def time_queries(query, requests):
    samples = []
    for frame in requests:
        before = time.perf_counter_ns()
        query(int(frame))
        samples.append((time.perf_counter_ns() - before) / 1e6)
    return {
        "median_ms": round(statistics.median(samples), 5),
        "p95_ms": round(sorted(samples)[int(0.95 * (len(samples) - 1))], 5),
    }


def _compile_rust_probe(library_path):
    """Compiling into the directory owned by the native-process caller."""
    source = Path(__file__).with_name("interactions_temporal_kernel.rs")
    try:
        subprocess.run(
            [
                "rustc",
                "--edition=2021",
                "-O",
                "--crate-type=cdylib",
                str(source),
                "-o",
                str(library_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        if error.stderr:
            sys.stderr.write(error.stderr)
        raise


def _load_rust_query(index, block_size, n_relations, library_path):
    """Loading native calls and retaining their buffers for the child lifetime."""
    library = ctypes.CDLL(str(library_path))
    function = library.query_temporal_runs
    u32_pointer = ctypes.POINTER(ctypes.c_uint32)
    function.argtypes = [
        ctypes.c_uint32,
        ctypes.c_uint32,
        ctypes.c_size_t,
        u32_pointer,
        u32_pointer,
        u32_pointer,
        u32_pointer,
        ctypes.POINTER(ctypes.c_uint8),
        ctypes.c_size_t,
        u32_pointer,
        u32_pointer,
        ctypes.c_size_t,
    ]
    function.restype = ctypes.c_size_t
    batch_function = library.query_temporal_runs_batch
    batch_function.argtypes = [
        u32_pointer,
        ctypes.c_size_t,
        ctypes.c_uint32,
        ctypes.c_size_t,
        u32_pointer,
        u32_pointer,
        u32_pointer,
        u32_pointer,
        ctypes.POINTER(ctypes.c_uint8),
        ctypes.c_size_t,
        u32_pointer,
        u32_pointer,
        u32_pointer,
        ctypes.c_size_t,
    ]
    batch_function.restype = ctypes.c_size_t
    offset, starts, ends, measure_starts, candidates = index
    native_arrays = [
        np.ascontiguousarray(array, dtype=np.uint32)
        for array in (offset, starts, ends, measure_starts)
    ]
    packed = np.ascontiguousarray(candidates, dtype=np.uint8)
    pointers = [array.ctypes.data_as(u32_pointer) for array in native_arrays]
    candidate_pointer = packed.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
    output_relations = np.empty(n_relations, dtype=np.uint32)
    output_measure_rows = np.empty(n_relations, dtype=np.uint32)
    output_relation_pointer = output_relations.ctypes.data_as(u32_pointer)
    output_measure_pointer = output_measure_rows.ctypes.data_as(u32_pointer)

    def query(frame):
        count = function(
            int(frame),
            block_size,
            n_relations,
            *pointers,
            candidate_pointer,
            packed.shape[1],
            output_relation_pointer,
            output_measure_pointer,
            n_relations,
        )
        if count > n_relations:
            raise RuntimeError("native temporal query rejected the supplied arrays")
        return output_relations[:count].copy(), output_measure_rows[:count].copy()

    def batch_query(frames):
        selected = np.asarray(
            list(dict.fromkeys(int(x) for x in frames)), dtype=np.uint32
        )
        capacity = len(selected) * n_relations
        batch_offsets = np.empty(len(selected) + 1, dtype=np.uint32)
        batch_relations = np.empty(capacity, dtype=np.uint32)
        batch_rows = np.empty(capacity, dtype=np.uint32)
        count = batch_function(
            selected.ctypes.data_as(u32_pointer),
            len(selected),
            block_size,
            n_relations,
            *pointers,
            candidate_pointer,
            packed.shape[1],
            batch_offsets.ctypes.data_as(u32_pointer),
            batch_relations.ctypes.data_as(u32_pointer),
            batch_rows.ctypes.data_as(u32_pointer),
            capacity,
        )
        if count > capacity:
            raise RuntimeError(
                "native batch temporal query rejected the supplied arrays"
            )
        return selected, batch_offsets, batch_relations[:count], batch_rows[:count]

    return library, native_arrays, packed, query, batch_query


def _run_native_process(args):
    """Waiting for native process exit before retiring its compiled library."""
    suffix = (
        ".dll"
        if sys.platform == "win32"
        else (".dylib" if sys.platform == "darwin" else ".so")
    )
    with tempfile.TemporaryDirectory(prefix="molsysmt-temporal-") as scratch:
        library_path = Path(scratch) / f"interactions_temporal{suffix}"
        _compile_rust_probe(library_path)
        child_environment = os.environ.copy()
        for variable in ("TMPDIR", "TMP", "TEMP"):
            child_environment[variable] = scratch
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "--frames",
            str(args.frames),
            "--relations",
            str(args.relations),
            "--active",
            str(args.active),
            "--survival",
            str(args.survival),
            "--block-size",
            str(args.block_size),
            "--rust",
            "--_native-library",
            str(library_path),
        ]
        if args.hdf:
            command.append("--hdf")
        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=child_environment,
        ) as child:
            try:
                stdout, stderr = child.communicate()
            except BaseException:
                if child.poll() is None:
                    child.kill()
                child.wait()
                raise
            if stderr:
                sys.stderr.write(stderr)
            if child.returncode:
                raise subprocess.CalledProcessError(
                    child.returncode, command, output=stdout, stderr=stderr
                )
    print(stdout, end="")


def hdf_round_trip(
    path, representation, arrays, distances, evidence, n_frames, n_relations, block_size
):
    """Write and verify a typed, index-only HDF5 probe with common measures."""
    with h5py.File(path, "w") as file:
        file.attrs["schema_probe_version"] = 1
        file.attrs["representation"] = representation
        file.attrs["structure_axis"] = "evaluated_structure_ordinal"
        file.attrs["n_relations"] = n_relations
        file.attrs["block_size"] = block_size
        file.attrs["distance_unit"] = "nm"
        payload = {
            "evaluated_structure_indices": np.arange(n_frames, dtype=np.int32),
            **arrays,
        }
        if distances is not None:
            payload["distance_nm"] = distances
            payload["evidence_code"] = evidence
        for name, array in payload.items():
            file.create_dataset(
                name,
                data=array,
                compression="gzip" if array.size else None,
                shuffle=bool(array.size),
            )
    with h5py.File(path, "r") as file:
        assert file.attrs["schema_probe_version"] == 1
        assert file.attrs["representation"] == representation
        for name, array in payload.items():
            np.testing.assert_array_equal(file[name][:], array)
    return path.stat().st_size


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=10000)
    parser.add_argument("--relations", type=int, default=400)
    parser.add_argument("--active", type=int, default=10)
    parser.add_argument("--survival", type=float, default=0.95)
    parser.add_argument("--block-size", type=int, default=100)
    parser.add_argument(
        "--rust",
        action="store_true",
        help="Compile a standalone Rust query probe with rustc",
    )
    parser.add_argument(
        "--hdf",
        action="store_true",
        help="Compare typed HDF5 round trips for the two indexes",
    )
    parser.add_argument("--_native-library", help=argparse.SUPPRESS)
    args = parser.parse_args()
    library_path = args._native_library
    del args._native_library
    if (
        args.frames < 3
        or args.relations < 1
        or not 0 < args.active <= args.relations
        or not 0 <= args.survival <= 1
        or args.block_size < 1
    ):
        parser.error(
            "invalid positive dimensions, active count, survival, or block size"
        )
    if library_path is not None and not args.rust:
        parser.error("the internal native-library option requires --rust")
    if args.rust and library_path is None:
        _run_native_process(args)
        return
    _benchmark(args, library_path)


def _benchmark(args, library_path=None):
    """Measuring unchanged incidence queries within a single process."""
    by_frame = generate(args.frames, args.relations, args.active, args.survival)
    start = time.perf_counter()
    offsets, relations = frame_major(by_frame)
    frame_build_s = time.perf_counter() - start
    start = time.perf_counter()
    runs = temporal_runs(by_frame, args.relations, args.block_size)
    run_build_s = time.perf_counter() - start
    rng = np.random.default_rng(29)
    requests = [0, 1, args.frames - 1]
    requests.extend(int(x) for x in rng.integers(0, args.frames, size=200))
    for frame in range(args.frames):
        np.testing.assert_array_equal(
            run_query(runs, frame, args.block_size, args.relations)[0],
            frame_query(offsets, relations, frame),
        )
        for actual, expected in zip(
            run_query_vectorized(runs, frame, args.block_size, args.relations),
            run_query(runs, frame, args.block_size, args.relations),
        ):
            np.testing.assert_array_equal(actual, expected)
    all_measure_rows = np.concatenate(
        [
            run_query(runs, frame, args.block_size, args.relations)[1]
            for frame in range(args.frames)
        ]
    )
    np.testing.assert_array_equal(
        np.sort(all_measure_rows), np.arange(len(relations), dtype=np.int32)
    )
    result = {
        "config": vars(args),
        "occurrences": len(relations),
        "runs": len(runs[1]),
        "evaluated_empty_structures": sum(not members for members in by_frame),
        "frame_major_index_bytes": offsets.nbytes + relations.nbytes,
        "run_index_bytes": sum(array.nbytes for array in runs),
        "block_bitmap_bytes": runs[4].nbytes,
        "frame_major_build_s": round(frame_build_s, 3),
        "run_build_s": round(run_build_s, 3),
        "frame_major_query": time_queries(
            lambda frame: frame_query(offsets, relations, frame), requests
        ),
        "run_query": time_queries(
            lambda frame: run_query(runs, frame, args.block_size, args.relations),
            requests,
        ),
        "run_query_vectorized": time_queries(
            lambda frame: run_query_vectorized(
                runs, frame, args.block_size, args.relations
            ),
            requests,
        ),
    }
    if args.rust:
        native_resources = _load_rust_query(
            runs, args.block_size, args.relations, library_path
        )
        native_query, native_batch_query = native_resources[-2:]
        for frame in range(args.frames):
            for actual, expected in zip(
                native_query(frame),
                run_query_vectorized(runs, frame, args.block_size, args.relations),
            ):
                np.testing.assert_array_equal(actual, expected)
        result["rust_ctypes_query"] = time_queries(native_query, requests)
        batches = [
            rng.integers(0, args.frames, size=100, dtype=np.int32) for _ in range(30)
        ]
        for request in batches[:3]:
            selected, batch_offsets, batch_relations, batch_rows = native_batch_query(
                request
            )
            for position, frame in enumerate(selected):
                first, last = batch_offsets[position : position + 2]
                expected_relations, expected_rows = run_query_vectorized(
                    runs, int(frame), args.block_size, args.relations
                )
                np.testing.assert_array_equal(
                    batch_relations[first:last], expected_relations
                )
                np.testing.assert_array_equal(batch_rows[first:last], expected_rows)

        def time_batches(query):
            samples = []
            for request in batches:
                before = time.perf_counter_ns()
                query(request)
                samples.append((time.perf_counter_ns() - before) / 1e6)
            return round(statistics.median(samples), 4)

        result["hundred_structure_query_ms"] = {
            "frame_major_python": time_batches(
                lambda request: [
                    frame_query(offsets, relations, int(frame))
                    for frame in dict.fromkeys(request)
                ]
            ),
            "rust_single_calls": time_batches(
                lambda request: [
                    native_query(frame) for frame in dict.fromkeys(request)
                ]
            ),
            "rust_one_batch_call": time_batches(native_batch_query),
        }
    if args.hdf:
        rng_measure = np.random.default_rng(18)
        distances = rng_measure.uniform(0.1, 0.5, size=len(relations)).astype(
            np.float64
        )
        evidence = rng_measure.integers(0, 2, size=len(relations), dtype=np.uint8)
        run_distances = np.empty_like(distances)
        run_distances[all_measure_rows] = distances
        run_evidence = np.empty_like(evidence)
        run_evidence[all_measure_rows] = evidence
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            result["hdf_index_and_common_measures_bytes"] = {
                "frame_major": hdf_round_trip(
                    base / "frame_major.h5",
                    "frame_major",
                    {"frame_offsets": offsets, "occurrence_relations": relations},
                    distances,
                    evidence,
                    args.frames,
                    args.relations,
                    args.block_size,
                ),
                "temporal_runs": hdf_round_trip(
                    base / "temporal_runs.h5",
                    "temporal_runs",
                    dict(
                        zip(
                            (
                                "relation_offsets",
                                "run_starts",
                                "run_ends",
                                "run_measure_starts",
                                "block_candidates",
                            ),
                            runs,
                        )
                    ),
                    run_distances,
                    run_evidence,
                    args.frames,
                    args.relations,
                    args.block_size,
                ),
            }
            result["hdf_index_only_bytes"] = {
                "frame_major": hdf_round_trip(
                    base / "frame_major_index.h5",
                    "frame_major",
                    {"frame_offsets": offsets, "occurrence_relations": relations},
                    None,
                    None,
                    args.frames,
                    args.relations,
                    args.block_size,
                ),
                "temporal_runs": hdf_round_trip(
                    base / "temporal_runs_index.h5",
                    "temporal_runs",
                    dict(
                        zip(
                            (
                                "relation_offsets",
                                "run_starts",
                                "run_ends",
                                "run_measure_starts",
                                "block_candidates",
                            ),
                            runs,
                        )
                    ),
                    None,
                    None,
                    args.frames,
                    args.relations,
                    args.block_size,
                ),
            }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
