"""MolSysMT Benchmarking Harness.

This module provides the core orchestration engine to execute high-precision performance benchmarks
with Numba JIT pre-warming, garbage collection isolation, and structured JSON telemetry exports.
"""

from __future__ import annotations

import gc
import json
import os
import platform
import sys
from datetime import datetime, timezone
from statistics import median, stdev
from time import perf_counter
from typing import Callable, Any


class BenchmarkHarness:
    """Central runner for high-precision performance measurements in MolSysMT."""

    def __init__(self, name: str, iterations: int = 25, repeats: int = 5):
        """Initializing the benchmark harness parameters.

        Parameters
        ----------
        name : str
            Name of the benchmark case.
        iterations : int, default=25
            Number of iterations per timing block.
        repeats : int, default=5
            Number of independent repeat blocks.
        """
        self.name = name
        self.iterations = iterations
        self.repeats = repeats

    def run(self, warmup_func: Callable[[], Any], timed_func: Callable[[], Any]) -> dict[str, Any]:
        """Execute the benchmark with JIT pre-warming and GC isolation.

        Parameters
        ----------
        warmup_func : Callable[[], Any]
            Function executed once to pre-compile JIT kernels or pre-warm caches.
        timed_func : Callable[[], Any]
            Function targeted for timing blocks.

        Returns
        -------
        dict[str, Any]
            Timing statistics and execution metadata.
        """
        # 1. Warm-up invocation (essential for JIT compilation / lazy cache lookups)
        warmup_func()

        # 2. Timing loops under GC isolation
        samples: list[float] = []
        gc.disable()
        try:
            for _ in range(self.repeats):
                t0 = perf_counter()
                for _ in range(self.iterations):
                    timed_func()
                t1 = perf_counter()
                samples.append((t1 - t0) / self.iterations)
        finally:
            gc.enable()

        # 3. Calculate statistics
        med_val = median(samples)
        min_val = min(samples)
        max_val = max(samples)
        std_val = stdev(samples) if len(samples) > 1 else 0.0

        # Lazy import of molsysmt to fetch package version safely
        import molsysmt as msm

        return {
            "name": self.name,
            "median_seconds": med_val,
            "min_seconds": min_val,
            "max_seconds": max_val,
            "stddev_seconds": std_val,
            "repeats": self.repeats,
            "iterations": self.iterations,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "environment": {
                "python_version": platform.python_version(),
                "system": platform.system(),
                "machine": platform.machine(),
                "molsysmt_version": msm.__version__,
            },
        }


def save_session_results(session_name: str, results: list[dict[str, Any]], output_path: str) -> None:
    """Save a list of benchmark results to a structured JSON file.

    Parameters
    ----------
    session_name : str
        Name of the benchmark run session.
    results : list[dict[str, Any]]
        List of result dictionaries returned by BenchmarkHarness.
    output_path : str
        Absolute path where the JSON file will be written.
    """
    import molsysmt as msm

    output = {
        "session_name": session_name,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "os": platform.system(),
            "os_release": platform.release(),
            "python": platform.python_version(),
            "machine": platform.machine(),
            "molsysmt_version": msm.__version__,
        },
        "results": {r["name"]: r for r in results},
    }

    # Ensure parent directories exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, sort_keys=True)
