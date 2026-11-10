"""MolSysMT Benchmarking Harness.

This module provides the core orchestration engine for isolated repeated
measurements with structured JSON telemetry exports.
"""

from __future__ import annotations

import gc
import importlib
import importlib.util
import json
import platform
import queue as queue_module
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from statistics import median, stdev
from time import monotonic, perf_counter
from typing import Any, Callable

from benchmarks.telemetry import file_digest


def _get_git_metadata() -> dict[str, str | bool | None]:
    """Return the repository revision and dirty-state evidence."""

    repository = Path(__file__).resolve().parents[1]
    try:
        commit = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "rev-parse", "HEAD"],
            cwd=repository,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "status", "--porcelain"],
            cwd=repository,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return {"git_commit": None, "git_dirty": None}
    return {"git_commit": commit, "git_dirty": bool(status.strip())}


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


def _subprocess_worker(
    warmup_func, timed_func, iterations, repeats, queue, base_rss=None
):
    # 1. Capture base memory before workload preparation.
    if base_rss is None:
        base_rss = _get_peak_rss_mb()

    # 2. Prepare imports, data, and any lazy runtime state outside timed loops.
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


def _factory_worker(
    factory, expected_workload, policy, units, iterations, repeats, queue
):
    """Prepare native objects inside a fresh interpreter, not through a fork."""
    base_rss = _get_peak_rss_mb()
    import molsysmt as msm

    with msm.configure.context(**policy), msm.pyunitwizard.context(**units):
        module = importlib.import_module(factory["module"])
        cases = getattr(module, factory["function"])(
            *factory["args"], **factory["kwargs"]
        )
        timed_func, actual_workload = cases[factory["case"]]
        if actual_workload != expected_workload:
            raise RuntimeError(
                "Prepared worker input/observable differs from the declared workload."
            )
        _subprocess_worker(timed_func, timed_func, iterations, repeats, queue, base_rss)


class BenchmarkHarness:
    """Run isolated warm timing observations with explicit measurement evidence."""

    def __init__(
        self,
        name: str,
        iterations: int = 25,
        repeats: int = 5,
        *,
        workload=None,
        factory=None,
        worker_timeout=120.0,
    ):
        """Initializing the benchmark harness parameters.

        Parameters
        ----------
        name : str
            Name of the benchmark case.
        iterations : int, default=25
            Number of iterations per timing block.
        repeats : int, default=5
            Number of repeat blocks; these are not independent machine samples.
        workload : dict or None, default=None
            Description of actual prepared inputs, observable, units, precision
            and provider. Missing descriptions remain unassessed by comparison.
        factory : dict or None, default=None
            Importable case-preparation descriptor for a fresh spawn worker.
            Native objects are constructed there, never serialized from the parent.
            Without it, the explicitly legacy closure/fork route remains bounded
            but is unsuitable for inherited native runtimes or held locks.
        worker_timeout : float, default=120.0
            Finite wall-clock deadline in seconds for preparation and execution.
        """
        self.name = name
        if any(
            isinstance(value, bool) or not isinstance(value, int) or value <= 0
            for value in (iterations, repeats)
        ):
            raise ValueError(
                "Benchmark iterations and repeats must be positive integers."
            )
        self.iterations = iterations
        self.repeats = repeats
        self.workload = json.loads(json.dumps(workload, allow_nan=False))
        self.factory = factory
        if (
            isinstance(worker_timeout, bool)
            or not isinstance(worker_timeout, (int, float))
            or not 0 < worker_timeout < float("inf")
        ):
            raise ValueError("Benchmark worker timeout must be finite and positive.")
        self.worker_timeout = float(worker_timeout)

    def run(
        self, warmup_func: Callable[[], Any], timed_func: Callable[[], Any]
    ) -> dict[str, Any]:
        """Execute the benchmark inside an isolated subprocess to prevent peak RAM contamination.

        Parameters
        ----------
        warmup_func : Callable[[], Any]
            Function executed once to prepare imports, data, and lazy runtime state.
        timed_func : Callable[[], Any]
            Function targeted for timing blocks.

        Returns
        -------
        dict[str, Any]
            Timing and memory statistics, and execution metadata.
        """
        import multiprocessing

        import molsysmt as msm

        method = "spawn" if self.factory is not None else "fork"
        ctx = multiprocessing.get_context(method)
        queue = ctx.Queue()
        if self.factory is None:
            target = _subprocess_worker
            arguments = (warmup_func, timed_func, self.iterations, self.repeats, queue)
        else:
            target = _factory_worker
            policy = {
                name: getattr(msm.configure, name)
                for name in (
                    "parallel_mode",
                    "num_threads",
                    "gpu_mode",
                    "precision",
                    "heavy_mode",
                )
            }
            report = msm.pyunitwizard.configure.report()
            units = {
                name: report[name]
                for name in ("default_form", "default_parser", "standard_units")
            }
            arguments = (
                self.factory,
                self.workload,
                policy,
                units,
                self.iterations,
                self.repeats,
                queue,
            )
        p = ctx.Process(target=target, args=arguments)
        deadline = monotonic() + self.worker_timeout
        try:
            p.start()
            # Drain IPC before joining: a full feeder pipe must not deadlock join.
            while True:
                remaining = deadline - monotonic()
                if remaining <= 0:
                    raise RuntimeError(f"Benchmark worker {self.name} timed out.")
                try:
                    samples, base_rss, peak_rss = queue.get(
                        timeout=min(0.25, remaining)
                    )
                    break
                except queue_module.Empty:
                    if not p.is_alive():
                        raise RuntimeError(
                            f"Benchmark worker {self.name} failed with exit code {p.exitcode} before returning evidence."
                        ) from None
            p.join(timeout=max(0, deadline - monotonic()))
            if p.is_alive():
                raise RuntimeError(
                    f"Benchmark worker {self.name} timed out after returning evidence."
                )
            if p.exitcode != 0:
                raise RuntimeError(
                    f"Benchmark worker {self.name} failed with exit code {p.exitcode}."
                )
        finally:
            if p.is_alive():
                p.terminate()
                p.join(timeout=2)
                if p.is_alive():
                    p.kill()
                    p.join()
            if p.pid is not None:
                p.close()
            queue.close()

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
            "samples_seconds": samples,
            "worker_timeout_seconds": self.worker_timeout,
            "measurement": {
                "harness_sha256": file_digest(__file__),
                "statistic": "median of per-call block means",
                "timer": "time.perf_counter",
                "process": "spawn_factory" if self.factory is not None else "fork",
                "warmup_calls": 1,
                "gc_during_timing": False,
            },
            "workload": self.workload,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "environment": {
                "python_version": platform.python_version(),
                "system": platform.system(),
                "machine": platform.machine(),
                "molsysmt_version": msm.__version__,
            },
        }


def save_session_results(
    session_name: str,
    results: list[dict[str, Any]],
    output_path: str,
    *,
    comparison_context=None,
    resource_observations=None,
) -> None:
    """Save a list of benchmark results to a structured JSON file.

    Parameters
    ----------
    session_name : str
        Name of the benchmark run session.
    results : list[dict[str, Any]]
        List of result dictionaries returned by BenchmarkHarness.
    output_path : str
        Path where the JSON file will be written.
    comparison_context : dict or None, default=None
        Captured runtime, hardware, provider, resource and policy identities.
    resource_observations : dict or None, default=None
        Before/after host observations, distinct from compatibility identities.
    """
    import molsysmt as msm

    names = [entry["name"] for entry in results]
    if not names or len(names) != len(set(names)):
        raise ValueError("Benchmark sessions require nonempty, unique case names.")
    backend = importlib.util.find_spec("molsysmt._rust")
    output = {
        "session_name": session_name,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "os": platform.system(),
            "os_release": platform.release(),
            "python": platform.python_version(),
            "machine": platform.machine(),
            "molsysmt_version": msm.__version__,
            "native_backend_sha256": None
            if backend is None
            else file_digest(backend.origin),
            **_get_git_metadata(),
        },
        "results": {r["name"]: r for r in results},
    }
    if comparison_context is not None:
        output["comparison_context"] = comparison_context
    if resource_observations is not None:
        output["resource_observations"] = resource_observations

    # Ensure parent directories exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, sort_keys=True)
