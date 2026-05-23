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


def _get_peak_rss_mb() -> float:
    """Retrieve peak Resident Set Size (RSS) in MB for the current process."""
    try:
        with open("/proc/self/status", "r") as f:
            for line in f:
                if line.startswith("VmHWM:"):
                    parts = line.split()
                    if len(parts) >= 2:
                        return float(parts[1]) / 1024.0
    except Exception:
        pass
    try:
        import resource
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    except Exception:
        return 0.0


def _subprocess_worker(warmup_func, timed_func, iterations, repeats, queue):
    import gc
    from time import perf_counter
    # 1. Capture base memory before warm-up
    base_rss = _get_peak_rss_mb()

    # 2. Warm-up invocation (essential for JIT compilation / lazy cache lookups)
    warmup_func()

    # 3. Timing loops under GC isolation
    samples = []
    gc.disable()
    try:
        for _ in range(repeats):
            t0 = perf_counter()
            for _ in range(iterations):
                timed_func()
            t1 = perf_counter()
            samples.append((t1 - t0) / iterations)
    finally:
        gc.enable()

    # 4. Capture peak memory after runs
    peak_rss = _get_peak_rss_mb()

    # Send results back
    queue.put((samples, base_rss, peak_rss))


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
        """Execute the benchmark inside an isolated subprocess to prevent peak RAM contamination.

        Parameters
        ----------
        warmup_func : Callable[[], Any]
            Function executed once to pre-compile JIT kernels or pre-warm caches.
        timed_func : Callable[[], Any]
            Function targeted for timing blocks.

        Returns
        -------
        dict[str, Any]
            Timing and memory statistics, and execution metadata.
        """
        import multiprocessing

        ctx = multiprocessing.get_context('fork')
        queue = ctx.Queue()

        p = ctx.Process(
            target=_subprocess_worker,
            args=(warmup_func, timed_func, self.iterations, self.repeats, queue)
        )
        p.start()
        p.join()

        if p.exitcode != 0:
            raise RuntimeError(f"Benchmark worker process for {self.name} failed with exit code {p.exitcode}")

        samples, base_rss, peak_rss = queue.get()

        # Calculate statistics
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
            "peak_rss_mb": peak_rss,
            "base_rss_mb": base_rss,
            "delta_rss_mb": max(0.0, peak_rss - base_rss),
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
