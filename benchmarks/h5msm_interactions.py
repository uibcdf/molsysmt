#!/usr/bin/env python3
"""Benchmark private file queries and the public H5MSM 0.5 loaded path.

Run from the repository root. The public path uses `molsysmt.h5msm.write_layers`
and `read_layers`; the selective file reader remains private.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import subprocess
import tempfile
import time
import tracemalloc
from pathlib import Path

import h5py
import numpy as np

import molsysmt as msm
from molsysmt.interactions._h5msm05 import (
    read_interactions_file,
    write_interactions_file,
)
from molsysmt.interactions._hdf5_query import HDF5InteractionsReader


def make_result(n_atoms, n_structures, occurrences_per_structure, n_relations):
    """Build reproducible sparse data with empty and unevaluated frames."""
    evaluated = [frame for frame in range(n_structures) if frame % 13 != 0]
    records = []
    for frame in evaluated:
        if frame % 7 == 0:
            continue
        for ordinal in range(occurrences_per_structure):
            relation = (frame * 31 + ordinal * 17) % n_relations
            records.append(
                {
                    "structure_index": frame,
                    "interaction_type": "pair",
                    "participants": [
                        {"role": "first", "atom_indices": [2 * relation]},
                        {"role": "second", "atom_indices": [2 * relation + 1]},
                    ],
                    "measurements": {"distance": 0.2 + frame * 0.00001},
                }
            )
    return msm.Interactions.from_records(
        records,
        n_atoms=n_atoms,
        n_structures=n_structures,
        evaluated_structure_indices=evaluated,
        method="synthetic_benchmark",
        measure_units={"distance": "nm"},
        parameters={"occurrences_per_nonempty_frame": occurrences_per_structure},
    )


def memory_query(result, request, filters):
    """Materialize the in-memory query with descriptors like the file path."""
    payload = result.query(structure_indices=request, **filters).to_dict()
    payload["relations"] = {
        int(relation): result.relation(int(relation))
        for relation in np.unique(payload["relation_indices"])
    }
    return payload


def signature(payload):
    """Compare selected coverage, occurrences, descriptors, and measurements."""
    descriptors = tuple(
        (
            int(relation),
            descriptor["interaction_type"],
            tuple(
                (participant["role"], tuple(participant["atom_indices"].tolist()))
                for participant in descriptor["participants"]
            ),
        )
        for relation, descriptor in sorted(payload["relations"].items())
    )
    return (
        tuple(payload["evaluated_structure_indices"].tolist()),
        tuple(payload["structure_indices"].tolist()),
        tuple(payload["relation_indices"].tolist()),
        descriptors,
        tuple(payload["evidence"].tolist()),
        tuple(payload["measurements"]["distance"].tolist()),
        payload["measure_units"]["distance"],
    )


def measure(call, requests):
    samples = []
    for request in requests:
        start = time.perf_counter_ns()
        call(request)
        samples.append((time.perf_counter_ns() - start) / 1_000_000)
    return {
        "median_ms": statistics.median(samples),
        "p95_ms": float(np.percentile(samples, 95)),
        "samples_ms": samples,
    }


def git_metadata():
    """Identify the code version when running inside a Git checkout."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = bool(
            subprocess.run(
                ["git", "status", "--porcelain"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
        )
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "dirty": None}
    return {"commit": commit, "dirty": dirty}


def linux_value(filename, prefix):
    """Read one Linux hardware field when available."""
    try:
        with open(filename, encoding="utf-8") as stream:
            for line in stream:
                if line.startswith(prefix):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return None


def run(args):
    if (
        args.atoms < 4
        or args.structures < 15
        or args.occurrences < 1
        or args.queries < 1
    ):
        raise ValueError(
            "Use at least 4 atoms, 15 structures, 1 occurrence, and 1 query."
        )
    n_relations = (
        min(100, args.atoms // 2) if args.relations is None else args.relations
    )
    if n_relations < 2 or n_relations > args.atoms // 2:
        raise ValueError("relations must be between 2 and atoms // 2.")
    rng = np.random.default_rng(args.seed)
    result = make_result(args.atoms, args.structures, args.occurrences, n_relations)
    frames = [int(x) for x in rng.integers(args.structures, size=args.queries)]
    groups = [
        rng.choice(
            args.structures, size=min(8, args.structures), replace=False
        ).tolist()
        for _ in range(args.queries)
    ]
    atom = 2 * ((31 * (args.structures // 2)) % n_relations)
    cases = {
        "one_frame": [(frame,) for frame in frames],
        "eight_nonconsecutive_frames": groups,
        "atom_in_eight_frames": groups,
        "atom_in_entire_trajectory": [range(args.structures)] * 3,
    }
    with tempfile.TemporaryDirectory(prefix="molsysmt_h5msm_bench_") as directory:
        filename = Path(directory) / "interactions.h5msm"
        start = time.perf_counter()
        write_interactions_file(filename, {"benchmark": result})
        write_s = time.perf_counter() - start
        file_bytes = filename.stat().st_size

        start = time.perf_counter()
        with HDF5InteractionsReader(filename, "benchmark") as reader:
            cold_open_query = reader.query([frames[0]])
        cold_open_query_s = time.perf_counter() - start
        if signature(cold_open_query) != signature(
            memory_query(result, [frames[0]], {})
        ):
            raise AssertionError("First file query disagrees with memory.")

        start = time.perf_counter()
        loaded = read_interactions_file(filename)["benchmark"]
        full_load_s = time.perf_counter() - start
        numeric_bytes = sum(
            value.nbytes
            for value in loaded.__dict__.values()
            if isinstance(value, np.ndarray)
        )

        timings = {}
        with HDF5InteractionsReader(filename, "benchmark") as reader:
            for name, requests in cases.items():
                filters = {"atom_indices": [atom]} if name.startswith("atom_") else {}
                for request in requests:
                    file_payload = reader.query(request, **filters)
                    memory_payload = memory_query(loaded, request, filters)
                    if signature(file_payload) != signature(memory_payload):
                        raise AssertionError(
                            f"File and memory differ for {name}: {request}"
                        )
                # Warm both paths before collecting separate samples.
                reader.query(requests[0], **filters)
                memory_query(loaded, requests[0], filters)
                timings[name] = {
                    "open_file_reader": measure(
                        lambda request, filters=filters: reader.query(
                            request, **filters
                        ),
                        requests,
                    ),
                    "loaded_memory": measure(
                        lambda request, filters=filters: memory_query(
                            loaded, request, filters
                        ),
                        requests,
                    ),
                }

        tracemalloc.start()
        with HDF5InteractionsReader(filename, "benchmark") as reader:
            reader.query(groups[0], atom_indices=[atom])
            _, reader_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        tracemalloc.start()
        loaded_again = read_interactions_file(filename)["benchmark"]
        memory_query(loaded_again, groups[0], {"atom_indices": [atom]})
        _, full_load_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        public_filename = Path(directory) / "public_interactions.h5msm"
        start = time.perf_counter()
        msm.h5msm.write_layers(str(public_filename), interactions={"benchmark": result})
        public_first_write_s = time.perf_counter() - start
        public_warm_filename = Path(directory) / "public_interactions_warm.h5msm"
        start = time.perf_counter()
        msm.h5msm.write_layers(
            str(public_warm_filename), interactions={"benchmark": result}
        )
        public_warm_write_s = time.perf_counter() - start
        public_file_bytes = public_filename.stat().st_size
        start = time.perf_counter()
        public_loaded = msm.h5msm.read_layers(
            str(public_filename), layers="interactions", analysis_names="benchmark"
        )["interactions"]["benchmark"]
        public_first_load_s = time.perf_counter() - start
        start = time.perf_counter()
        public_loaded = msm.h5msm.read_layers(
            str(public_filename), layers="interactions", analysis_names="benchmark"
        )["interactions"]["benchmark"]
        public_warm_load_s = time.perf_counter() - start
        tracemalloc.start()
        public_loaded_for_memory = msm.h5msm.read_layers(
            str(public_filename), layers="interactions", analysis_names="benchmark"
        )["interactions"]["benchmark"]
        _, public_load_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        del public_loaded_for_memory
        public_numeric_bytes = sum(
            value.nbytes
            for value in public_loaded.__dict__.values()
            if isinstance(value, np.ndarray)
        )
        public_timings = {}
        for name, requests in cases.items():
            filters = {"atom_indices": [atom]} if name.startswith("atom_") else {}
            for request in requests:
                if signature(
                    memory_query(public_loaded, request, filters)
                ) != signature(memory_query(result, request, filters)):
                    raise AssertionError(
                        f"Public H5MSM result differs for {name}: {request}"
                    )
            memory_query(public_loaded, requests[0], filters)
            public_timings[name] = measure(
                lambda request, filters=filters: memory_query(
                    public_loaded, request, filters
                ),
                requests,
            )

    return {
        "schema": "molsysmt.h5msm05_interactions_benchmark.v2",
        "environment": {
            "date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "cpu_model": linux_value("/proc/cpuinfo", "model name"),
            "logical_cpus": os.cpu_count(),
            "memory_total": linux_value("/proc/meminfo", "MemTotal"),
            "gpu": "not used",
            "thread_environment": {
                key: os.environ.get(key)
                for key in (
                    "OMP_NUM_THREADS",
                    "OPENBLAS_NUM_THREADS",
                    "MKL_NUM_THREADS",
                    "NUMEXPR_NUM_THREADS",
                    "HDF5_USE_FILE_LOCKING",
                )
            },
            "python": platform.python_version(),
            "numpy": np.__version__,
            "h5py": h5py.__version__,
            "molsysmt": getattr(msm, "__version__", "unknown"),
            "pid": os.getpid(),
            "git": git_metadata(),
            "storage": "temporary directory; filesystem and cache state not controlled",
        },
        "input": {
            "n_atoms": args.atoms,
            "n_structures": args.structures,
            "occurrences_per_nonempty_frame": args.occurrences,
            "relation_catalog_size": n_relations,
            "n_occurrences": result.n_interactions,
            "n_queries_regular_cases": args.queries,
            "n_queries_entire_trajectory_case": 3,
            "seed": args.seed,
            "atom_index": atom,
        },
        "storage": {
            "write_s": write_s,
            "file_bytes": file_bytes,
            "loaded_numeric_array_bytes": numeric_bytes,
            "full_load_s": full_load_s,
            "first_open_and_query_s": cold_open_query_s,
            "python_tracemalloc_reader_peak_bytes": reader_peak,
            "python_tracemalloc_full_load_peak_bytes": full_load_peak,
        },
        "queries": timings,
        "public_h5msm": {
            "first_write_layers_s": public_first_write_s,
            "warm_write_layers_s": public_warm_write_s,
            "file_bytes": public_file_bytes,
            "first_read_layers_s": public_first_load_s,
            "warm_read_layers_s": public_warm_load_s,
            "loaded_numeric_array_bytes": public_numeric_bytes,
            "python_tracemalloc_load_peak_bytes": public_load_peak,
            "queries_after_load": public_timings,
        },
        "notes": [
            "The selective file reader is private; the public write_layers/read_layers path is measured separately.",
            "First and repeated public calls include different import and filesystem cache states; neither is a cold-disk measurement.",
            "Selected coverage, occurrences, descriptors, evidence, and distance are checked before timing.",
            "tracemalloc excludes HDF5 native allocations and filesystem cache.",
            "First open/query is not a cold filesystem-cache measurement.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atoms", type=int, default=1000)
    parser.add_argument("--structures", type=int, default=1000)
    parser.add_argument("--occurrences", type=int, default=2)
    parser.add_argument(
        "--relations",
        type=int,
        help="Distinct pair relationships (default: min(100, atoms // 2))",
    )
    parser.add_argument("--queries", type=int, default=30)
    parser.add_argument("--seed", type=int, default=20260929)
    parser.add_argument("--output", type=Path, help="Optional JSON result path")
    args = parser.parse_args()
    report = run(args)
    output = json.dumps(report, indent=2) + "\n"
    if args.output is not None:
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
