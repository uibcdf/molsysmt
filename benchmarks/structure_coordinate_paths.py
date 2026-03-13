from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from statistics import median
from time import perf_counter
from typing import Callable

os.environ.setdefault("NUMBA_DISABLE_CACHE", "1")

import molsysmt as msm
from molsysmt import systems
from molsysmt._private import jit as msm_jit
from molsysmt.lib.structure._kernel_inputs import (
    align_coordinates_values_and_unit,
    extract_coordinates_value_and_unit,
)

_ORIGINAL_NJIT = msm_jit.nb.njit


def _benchmark_njit(signature=None, cache=True, **kwargs):
    return _ORIGINAL_NJIT(signature, cache=False, **kwargs)


msm_jit.nb.njit = _benchmark_njit


def _time_block(func: Callable[[], None], iterations: int) -> float:
    t0 = perf_counter()
    for _ in range(iterations):
        func()
    t1 = perf_counter()
    return (t1 - t0) / iterations


def _benchmark(func: Callable[[], None], iterations: int, repeats: int) -> dict[str, float]:
    func()
    samples = [_time_block(func, iterations) for _ in range(repeats)]
    return {
        "median_seconds": median(samples),
        "min_seconds": min(samples),
        "max_seconds": max(samples),
    }


def _build_payloads() -> dict[str, object]:
    xyz = msm.convert(
        systems["particles 4"]["traj_particles_4.xyznpy"],
        to_form="XYZ",
    )

    return {
        "xyz": xyz,
    }


def run_baseline(repeats: int = 5) -> dict[str, object]:
    """Run a small deterministic performance baseline for hot coordinate paths."""

    payloads = _build_payloads()

    xyz = payloads["xyz"]

    benchmarks: dict[str, tuple[int, Callable[[], None]]] = {
        "kernel_extract_xyz_coordinates": (
            25,
            lambda: extract_coordinates_value_and_unit(xyz),
        ),
        "kernel_align_xyz_coordinates": (
            25,
            lambda: align_coordinates_values_and_unit(
                xyz[0],
                xyz[1],
            ),
        ),
        "structure_get_center_xyz": (
            10,
            lambda: msm.structure.get_center(xyz),
        ),
        "structure_get_distances_xyz": (
            10,
            lambda: msm.structure.get_distances(xyz),
        ),
        "structure_get_rmsd_xyz": (
            10,
            lambda: msm.structure.get_rmsd(
                xyz,
                structure_indices="all",
                reference_structure_index=0,
            ),
        ),
    }

    results: dict[str, dict[str, float]] = {}

    for name, (iterations, func) in benchmarks.items():
        results[name] = _benchmark(func, iterations=iterations, repeats=repeats)

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": "3.13",
        "repeats": repeats,
        "profile": "xyz-default",
        "results": results,
        "notes": {
            "dataset_primary": "particles 4 XYZ trajectory",
            "warmup_status": "per-benchmark local warmup only",
            "cache_policy": "numba disk cache disabled inside benchmark process",
            "pending_follow_up": (
                "MolSys/HDF5-heavy paths remain to be measured after the local "
                "Numba cache locator issue is resolved."
            ),
            "purpose": (
                "Compare public coordinate-heavy wrappers against the local "
                "kernel-input preparation layer used by hot structure paths."
            ),
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(run_baseline(repeats=args.repeats), indent=2, sort_keys=True))
