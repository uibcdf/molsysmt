"""Compare frozen pre-690 and current CSR kernels without rebuilding either.

This is an advisory, bounded native-kernel study, not a public-pipeline ranking.
Run under an OS resource limit. The historical extension is executable input:
only the explicitly reviewed binary digest is admitted.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.util
import itertools
import json
import subprocess
from functools import partial
from pathlib import Path
from statistics import median
from time import perf_counter_ns

import numpy as np

import molsysmt as msm
from benchmarks.harness import _get_git_metadata
from benchmarks.telemetry import (
    array_identity,
    comparison_context,
    file_digest,
    resource_observation,
    workload,
)

ROOT = Path(__file__).resolve().parents[1]
BASELINE_SHA256 = "2f1f69f6e0539bd31ee419ec3b7a4deaab20f09045ce3e6504369c9130438525"
NATIVE_SOURCE = "rust/src/neighbors.rs"
NUMERICAL_BUDGET = 512 * 1024**2


def _load_baseline(path):
    if file_digest(path) != BASELINE_SHA256:
        raise ValueError("The baseline extension does not match the reviewed digest.")
    spec = importlib.util.spec_from_file_location("_molsysmt_pre690._rust", path)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load the reviewed baseline extension.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _cases():
    for name, structures, atoms, side, cutoff, periodic in (
        ("compact", 4, 1000, 3.0, 0.35, False),
        ("compact_pbc", 4, 1000, 3.0, 0.35, True),
        ("dilute", 4, 1000, 10.0, 0.3, False),
        ("small", 1, 64, 3.0, 0.35, False),
        ("many_small_structures", 32, 64, 3.0, 0.35, False),
        ("dense", 2, 512, 1.0, 0.35, False),
        ("one_cell_pbc", 1, 128, 1.0, 0.8, True),
    ):
        xyz = np.random.default_rng(690).uniform(0, side, size=(structures, atoms, 3))
        boxes = np.repeat((np.eye(3) * side)[None], structures, axis=0)
        yield name, xyz, boxes if periodic else None, cutoff
    box = np.array([[2.0, 0, 0], [0.4, 1.8, 0], [0.2, 0.3, 1.5]])
    xyz = np.random.default_rng(692).uniform(size=(2, 128, 3)) @ box
    yield "skew_pbc", xyz, np.repeat(box[None], 2, axis=0), 0.35


def _oracle(xyz, boxes, cutoff):
    """Enumerate all pairs; use explicit nearby lattice images for skew cells."""
    offsets, indices, distances = [0], [], []
    for s, positions in enumerate(xyz):
        shifts = None
        if boxes is not None and not np.array_equal(
            boxes[s], np.diag(np.diag(boxes[s]))
        ):
            shifts = (
                np.array(list(itertools.product(range(-2, 3), repeat=3))) @ boxes[s]
            )
        for i, point in enumerate(positions):
            delta = positions - point
            if boxes is not None:
                if shifts is None:
                    lengths = np.diag(boxes[s])
                    delta -= np.rint(delta / lengths) * lengths
                else:
                    images = delta[:, None, :] + shifts[None, :, :]
                    squared = np.einsum("ijk,ijk->ij", images, images)
                    delta = images[
                        np.arange(len(positions)), np.argmin(squared, axis=1)
                    ]
            squared = np.einsum("ij,ij->i", delta, delta)
            selected = np.flatnonzero(
                (squared <= cutoff * cutoff) & (np.arange(len(positions)) != i)
            )
            selected = selected[np.lexsort((selected, squared[selected]))]
            indices.extend(selected.tolist())
            distances.extend(np.sqrt(squared[selected]).tolist())
            offsets.append(len(indices))
    return (
        np.asarray(offsets, dtype=np.int64),
        np.asarray(indices, dtype=np.int64),
        np.asarray(distances, dtype=np.float64),
    )


def _check(actual, expected):
    np.testing.assert_array_equal(actual[0], expected[0])
    np.testing.assert_array_equal(actual[1], expected[1])
    np.testing.assert_allclose(actual[2], expected[2], rtol=0, atol=1e-13)


def _bounded_dims(dims, population):
    limit = max(1, 4 * population)
    dims = np.minimum(np.maximum(dims, 1), limit).astype(np.int64)
    while int(np.prod(dims)) > limit:
        # Rust Iterator::max_by_key selects the last equal maximum.
        axis = max(range(3), key=lambda i: (dims[i], i))
        dims[axis] = max(1, dims[axis] // 2)
    return dims


def _grid_diagnostics(xyz, boxes, cutoff):
    """Model head counts and candidate visits; these are not instrumented counters."""
    if boxes is not None and any(
        not np.array_equal(b, np.diag(np.diag(b))) for b in boxes
    ):
        return {"state": "not_modeled_for_reduced_skew_basis"}
    rows = []
    for s, positions in enumerate(xyz):
        origin = positions.min(axis=0) if boxes is None else np.zeros(3)
        lengths = (
            np.maximum(cutoff, positions.max(axis=0) - origin + 1e-5)
            if boxes is None
            else np.diag(boxes[s])
        )
        original = np.maximum(1, np.floor(lengths / cutoff)).astype(np.int64)
        coarsened = _bounded_dims(original, len(positions))
        variants = {}
        for name, dims in (("baseline", original), ("current", coarsened)):
            bins = np.floor((positions - origin) / lengths * dims).astype(np.int64)
            bins = np.clip(bins, 0, dims - 1)
            visits = 0
            for i, cell in enumerate(bins):
                difference = np.abs(bins - cell)
                if boxes is not None:
                    difference = np.minimum(difference, dims - difference)
                admitted = np.all(difference <= 1, axis=1)
                admitted[i] = False
                visits += int(np.count_nonzero(admitted))
            variants[name] = {
                "dimensions": dims.tolist(),
                "heads": int(np.prod(dims)),
                "head_bytes": int(np.prod(dims)) * 8,
                "predicted_candidate_visits": visits,
            }
        rows.append(variants)
    return {
        "state": "source_model_not_native_instrumentation",
        "excludes": "validation, scheduling, scratch growth, atomic admission, sorting and flattening costs",
        "structures": rows,
    }


def _measure(operations, expected, repeats, iterations, first):
    names = [first, "current" if first == "baseline" else "baseline"]
    for name in names:
        for _ in range(3):
            result = operations[name]()
            _check(result, expected)
            del result
    samples = {name: [] for name in names}
    for repeat in range(repeats):
        for name in names if repeat % 2 == 0 else names[::-1]:
            gc.collect()
            timings = []
            for _ in range(iterations):
                start = perf_counter_ns()
                result = operations[name]()
                timings.append(perf_counter_ns() - start)
                _check(result, expected)
                del result
            samples[name].append(sum(timings) / iterations)
    return {
        name: {"block_means_ns": values, "median_ns": median(values)}
        for name, values in samples.items()
    }


def profile(baseline_path, repeats, iterations, first):
    from molsysmt import _rust

    baseline = _load_baseline(baseline_path)
    native_digest = file_digest(_rust.__file__)
    producer_digest = file_digest(__file__)
    source_digest = file_digest(ROOT / NATIVE_SOURCE)
    for path, expected in (
        (Path(__file__).relative_to(ROOT), producer_digest),
        (NATIVE_SOURCE, source_digest),
    ):
        committed = subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT)
        if hashlib.sha256(committed).hexdigest() != expected:
            raise RuntimeError("Commit the measured producer and native source first.")
    git = _get_git_metadata()
    changes = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=ROOT, text=True
    )
    observations = {"before": resource_observation()}
    with msm.configure.context(
        use_gpu=False,
        parallel_mode=False,
        num_threads=1,
        precision="double",
        heavy_mode="off",
    ):
        context = comparison_context()
        cases = []
        for name, xyz, boxes, cutoff in _cases():
            expected = _oracle(xyz, boxes, cutoff)
            operations = {
                label: partial(
                    module.neighbor_list_csr_multi,
                    xyz,
                    xyz,
                    boxes,
                    cutoff,
                    True,
                    True,
                    1,
                    **(
                        {"memory_budget": NUMERICAL_BUDGET}
                        if label == "current"
                        else {}
                    ),
                )
                for label, module in (("baseline", baseline), ("current", _rust))
            }
            for operation in operations.values():
                _check(operation(), expected)
            timing = _measure(operations, expected, repeats, iterations, first)
            cases.append(
                {
                    "case": name,
                    "workload": workload(
                        "neighbor_list_csr_multi",
                        inputs={
                            "coordinates": array_identity(xyz),
                            **(
                                {"box": array_identity(boxes)}
                                if boxes is not None
                                else {}
                            ),
                        },
                        semantics={
                            "coordinate_unit": "nm",
                            "cutoff_nm": cutoff,
                            "exclude_self": True,
                            "sort_by_distance": True,
                            "num_threads": 1,
                            "current_memory_budget_bytes": NUMERICAL_BUDGET,
                            "baseline_budget_contract": "absent",
                        },
                        route="compiled CSR kernels; public preparation and Python projection excluded",
                        producer=__file__,
                    ),
                    "occurrences": len(expected[1]),
                    "oracle": "all pairs; orthogonal minimum images or explicit [-2,2]^3 images for the bounded skew fixture; indices exact, distances within 1e-13 nm",
                    "grid_model": _grid_diagnostics(xyz, boxes, cutoff),
                    "timing": timing,
                    "current_over_baseline_median_ratio": timing["current"]["median_ns"]
                    / timing["baseline"]["median_ns"],
                }
            )
            print(f"Measured {name}", flush=True)
        if (
            comparison_context() != context
            or _get_git_metadata() != git
            or subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=ROOT, text=True
            )
            != changes
            or file_digest(_rust.__file__) != native_digest
            or file_digest(baseline_path) != BASELINE_SHA256
            or file_digest(ROOT / NATIVE_SOURCE) != source_digest
            or file_digest(__file__) != producer_digest
        ):
            raise RuntimeError(
                "Source, binaries or execution context changed during measurement."
            )
        observations["after"] = resource_observation()
    return {
        "schema": "molsysmt.neighbor-kernel-profile@1",
        "complete": True,
        "comparison_context": context,
        "source": git,
        "worktree_changes": changes.splitlines(),
        "producer_sha256": producer_digest,
        "native_source_sha256": source_digest,
        "baseline_extension_sha256": BASELINE_SHA256,
        "current_extension_sha256": native_digest,
        "resource_observations": observations,
        "measurement": {
            "warmups_per_route": 3,
            "repeats": repeats,
            "iterations_per_block": iterations,
            "first_route": first,
            "order": "reversed on alternating repetitions",
            "timer": "time.perf_counter_ns around each call; block mean",
            "gc": "enabled, collected before each route block",
            "excluded": "imports, input/oracle preparation, equality checks, retirement and grid modeling",
            "process": "one fresh serial process, separate pinned native libraries; no fork",
            "scope": "Advisory kernel-only comparison. Grid models do not establish causal timing attribution. No RSS or public pipeline speed guarantee.",
        },
        "cases": cases,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-extension", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=15)
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--first", choices=("baseline", "current"), default="baseline")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.repeats < 3 or args.iterations < 1:
        parser.error("Require at least three repeats and one iteration.")
    if args.output.exists():
        parser.error("Choose a new output; existing evidence must not be overwritten.")
    result = profile(args.baseline_extension, args.repeats, args.iterations, args.first)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(f"Recorded {len(result['cases'])} interleaved native cases.")
