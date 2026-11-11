"""Compare bounded pair packing against a reviewed, immutable Git implementation.

This measures Python representation work on small Boolean maps, not neighbor
search or molecular geometry. Run under an OS resource limit on shared hosts.
The baseline option executes this repository's helper from the selected commit.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import re
import subprocess
import tracemalloc
from functools import partial
from pathlib import Path
from statistics import median
from time import perf_counter

import numpy as np

import molsysmt as msm
from benchmarks.harness import _get_git_metadata
from benchmarks.telemetry import (
    comparison_context,
    file_digest,
    resource_observation,
    workload,
)
from molsysmt.structure._compatibility_output import contact_pairs

ROOT = Path(__file__).resolve().parents[1]
HELPER = "molsysmt/structure/_compatibility_output.py"
BASELINE = "54c9b79a0751bfc74ec204dbc4c46d6b120338fd"


def _baseline(revision):
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("The reviewed baseline must be a full Git commit hash.")
    source = subprocess.check_output(["git", "show", f"{revision}:{HELPER}"], cwd=ROOT)
    namespace = {"__name__": "_reviewed_contact_projection_baseline"}
    exec(compile(source, f"{revision}:{HELPER}", "exec"), namespace)
    return namespace["contact_pairs"], hashlib.sha256(source).hexdigest()


def _cases():
    for name, rows, columns, sparse, layout, mapped, strict_upper in (
        ("dense_16", 16, 16, False, "C", False, True),
        ("dense_128", 128, 128, False, "C", False, True),
        ("dense_512", 512, 512, False, "C", False, True),
        ("dense_mapped_512", 512, 512, False, "C", True, True),
        ("sparse_512", 512, 512, True, "C", False, True),
        ("rectangular_mapped", 128, 257, False, "C", True, False),
        ("fortran_512", 512, 512, False, "F", False, True),
        ("reversed_sparse_512", 512, 512, True, "reversed", True, True),
    ):
        i, j = np.indices((rows, columns))
        matrix = (
            (17 * i + 13 * j) % 97 == 0 if sparse else np.ones((rows, columns), bool)
        )
        del i, j
        if layout == "F":
            matrix = np.asfortranarray(matrix)
        elif layout == "reversed":
            matrix = matrix[::-1, ::-1]
        query = np.arange(rows - 1, -1, -1, dtype=np.int64) * 3 + 1000
        target = (
            query if strict_upper else np.arange(columns, dtype=np.int64) * 5 + 2000
        )
        expected = [
            [int(query[i]), int(target[j])] if mapped else [i, j]
            for i in range(rows)
            for j in range(columns)
            if matrix[i, j] and (not strict_upper or i < j)
        ]
        yield name, matrix, query, target, [expected], mapped, strict_upper


def _measure(operations, expected, repeats):
    for operation in operations.values():
        for _ in range(3):
            output = operation()
            assert output == expected
            del output
    timings = {name: [] for name in operations}
    for repetition in range(repeats):
        order = list(operations)
        if repetition % 2:
            order.reverse()
        for name in order:
            gc.collect()
            start = perf_counter()
            output = operations[name]()
            elapsed = perf_counter() - start
            assert output == expected
            timings[name].append(elapsed)
            del output
    observations = {}
    for name, operation in operations.items():
        gc.collect()
        tracemalloc.start()
        try:
            output = operation()
            current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        assert output == expected
        del output
        observations[name] = {
            "seconds": timings[name],
            "median_seconds": median(timings[name]),
            "additional_traced_current_bytes": current,
            "additional_traced_peak_bytes": peak,
        }
    return observations


def profile(baseline, repeats):
    previous, previous_digest = _baseline(baseline)
    with msm.configure.context(
        use_gpu=False,
        parallel_mode=False,
        num_threads=1,
        precision="double",
        heavy_mode="off",
    ):
        context = comparison_context()
        source = _get_git_metadata()
        source["worktree_changes"] = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True
        ).splitlines()
        current_digest = file_digest(ROOT / HELPER)
        producer_digest = file_digest(__file__)
        committed = subprocess.check_output(["git", "show", f"HEAD:{HELPER}"], cwd=ROOT)
        if hashlib.sha256(committed).hexdigest() != current_digest:
            raise RuntimeError(
                "Commit the measured implementation before recording evidence."
            )
        observations = {"before": resource_observation()}
        samples = []
        for name, matrix, query, target, expected, mapped, strict_upper in _cases():
            parameters = dict(
                paired=False,
                strict_upper=strict_upper,
                atom_indices=query,
                atom_indices_2=None if strict_upper else target,
                output_indices="atom" if mapped else "selection",
                sorted_pairs=False,
                budget=128 * 1024**2,
                caller="bounded contact projection profile",
            )
            data = matrix[np.newaxis]
            timing = _measure(
                {
                    "baseline": partial(previous, data, **parameters),
                    "current": partial(contact_pairs, data, **parameters),
                },
                expected,
                repeats,
            )
            samples.append(
                {
                    "case": name,
                    "workload": workload(
                        "Boolean contact-map to Python pair-list projection",
                        inputs={
                            "shape": list(data.shape),
                            "dtype": str(data.dtype),
                            "strides": list(data.strides),
                            "logical_map_sha256": hashlib.sha256(
                                data.tobytes()
                            ).hexdigest(),
                            "query_sha256": hashlib.sha256(query.tobytes()).hexdigest(),
                            "target_sha256": hashlib.sha256(
                                target.tobytes()
                            ).hexdigest(),
                        },
                        semantics={
                            "pairs": len(expected[0]),
                            "strict_upper": strict_upper,
                            "output_indices": parameters["output_indices"],
                            "units": "selection positions or atom indices; no physical quantity",
                            "geometry": "not computed; the exact Boolean map is supplied",
                        },
                        route="same-process alternating baseline/current private projection",
                        producer=__file__,
                    ),
                    "observations": timing,
                    "current_over_baseline_median_ratio": timing["current"][
                        "median_seconds"
                    ]
                    / timing["baseline"]["median_seconds"],
                }
            )
            print(f"Measured {name}", flush=True)
        observations["after"] = resource_observation()
        final_source = _get_git_metadata()
        final_source["worktree_changes"] = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True
        ).splitlines()
        if (
            comparison_context() != context
            or final_source != source
            or file_digest(ROOT / HELPER) != current_digest
            or file_digest(__file__) != producer_digest
        ):
            raise RuntimeError(
                "Source or execution context changed during measurement."
            )
    return {
        "schema": "molsysmt.contact-projection-study@1",
        "complete": True,
        "comparison_context": context,
        "source": source,
        "source_sha256": {HELPER: current_digest},
        "baseline": {"commit": baseline, "helper_sha256": previous_digest},
        "native_sha256": file_digest(ROOT / "molsysmt/_rust.abi3.so"),
        "resource_observations": observations,
        "measurement": {
            "producer_sha256": producer_digest,
            "warmups": 3,
            "iterations": 1,
            "repeats": repeats,
            "order": "baseline/current reversed on alternating repetitions",
            "timer": "time.perf_counter",
            "garbage_collection": "enabled; collected before each sample",
            "excluded": "imports, preparation, equality checking and result retirement",
            "memory": "additional tracemalloc allocation with supplied map/expected output prepared before tracing; not RSS",
            "process": "one fresh serial process; no fork or process worker",
        },
        "samples": samples,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default=BASELINE)
    parser.add_argument("--repeats", type=int, default=15)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    if arguments.repeats < 3:
        parser.error("At least three repetitions are required.")
    if arguments.output.exists():
        parser.error("Choose a new output; existing evidence must not be overwritten.")
    result = profile(arguments.baseline, arguments.repeats)
    with arguments.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(f"Recorded {len(result['samples'])} interleaved projection cases.")
