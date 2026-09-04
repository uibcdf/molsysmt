"""Benchmarking the Rust-only release runtime with correctness checks.

This script measures startup, first and repeated calls, peak memory, explicit
thread scaling, and bounded nested concurrency. Each workload runs in an
isolated child process and validates its scientific result before reporting a
timing.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import importlib.util
from importlib import metadata
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
from time import perf_counter
import types


REPOSITORY = Path(__file__).resolve().parents[2]
INSTALLED_EXTENSION_ENV = "MOLSYSMT_BENCHMARK_INSTALLED_EXTENSION"


def _rust_module():
    """Returning the source or isolated installed Rust extension."""

    if os.environ.get(INSTALLED_EXTENSION_ENV) != "1":
        import molsysmt._rust as rust

        return rust

    distribution = metadata.distribution("molsysmt")
    candidates = [
        distribution.locate_file(item).resolve()
        for item in distribution.files or ()
        if item.parent.as_posix() == "molsysmt"
        and item.name.startswith("_rust.")
        and item.suffix in {".so", ".pyd", ".dylib"}
    ]
    if len(candidates) != 1:
        raise RuntimeError(
            "expected exactly one installed molsysmt._rust extension, "
            f"found {len(candidates)}"
        )
    extension_path = candidates[0]
    package = types.ModuleType("molsysmt")
    package.__path__ = [str(extension_path.parent)]
    package.__package__ = "molsysmt"
    package.__spec__ = importlib.util.spec_from_loader(
        "molsysmt", loader=None, is_package=True
    )
    sys.modules["molsysmt"] = package
    spec = importlib.util.spec_from_file_location("molsysmt._rust", extension_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load extension from {extension_path}")
    rust = importlib.util.module_from_spec(spec)
    sys.modules["molsysmt._rust"] = rust
    spec.loader.exec_module(rust)
    return rust


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
            if line.startswith("model name"):
                return line.split(":", maxsplit=1)[1].strip()
    except OSError:
        pass
    return platform.processor()


def _peak_rss_mb() -> float:
    """Returning the process high-water resident memory in MiB."""

    try:
        for line in Path("/proc/self/status").read_text(encoding="utf-8").splitlines():
            if line.startswith("VmHWM:"):
                return float(line.split()[1]) / 1024.0
    except OSError:
        pass

    try:
        import resource

        value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return value / (1024.0 if sys.platform != "darwin" else 1024.0**2)
    except (ImportError, OSError):
        return 0.0


def _minimum_time(function, repeats: int = 5) -> tuple[float, list[float]]:
    samples = []
    for _ in range(repeats):
        started = perf_counter()
        function()
        samples.append(perf_counter() - started)
    return min(samples), samples


def _startup_worker() -> dict:
    import_started = perf_counter()
    import numpy as np
    rust = _rust_module()

    import_seconds = perf_counter() - import_started
    coordinates = np.arange(18_000, dtype=np.float64).reshape(2_000, 3, 3)
    weights = np.ones(3, dtype=np.float64)

    started = perf_counter()
    first = np.asarray(rust.get_center(coordinates, weights, 1))
    first_call_seconds = perf_counter() - started
    warm_seconds, warm_samples = _minimum_time(
        lambda: rust.get_center(coordinates, weights, 1)
    )

    expected = coordinates.mean(axis=1, keepdims=True)
    np.testing.assert_allclose(first, expected, rtol=1e-14, atol=1e-14)
    cache_files = [
        str(path)
        for suffix in ("*.nbi", "*.nbc")
        for path in Path.cwd().rglob(suffix)
    ]
    if cache_files:
        raise AssertionError(f"JIT cache files were created: {cache_files}")

    return {
        "coordinates_shape": list(coordinates.shape),
        "dtype": str(coordinates.dtype),
        "import_seconds": import_seconds,
        "first_call_seconds": first_call_seconds,
        "warm_min_seconds": warm_seconds,
        "warm_samples_seconds": warm_samples,
        "first_to_warm_ratio": first_call_seconds / warm_seconds,
        "jit_cache_files_created": 0,
    }


def _memory_worker() -> dict:
    import numpy as np
    rust = _rust_module()

    baseline_mb = _peak_rss_mb()
    rng = np.random.default_rng(20260728)
    coordinates = rng.random((600, 2_000, 3), dtype=np.float64)
    weights = np.ones(2_000, dtype=np.float64)
    payload_mb = (coordinates.nbytes + weights.nbytes) / 1024.0**2
    after_payload_mb = _peak_rss_mb()

    result = np.asarray(rust.get_center(coordinates, weights, 4))
    expected = coordinates.mean(axis=1, keepdims=True)
    np.testing.assert_allclose(result, expected, rtol=1e-13, atol=1e-13)
    after_call_mb = _peak_rss_mb()

    return {
        "coordinates_shape": list(coordinates.shape),
        "dtype": str(coordinates.dtype),
        "payload_mb": payload_mb,
        "baseline_rss_mb": baseline_mb,
        "after_payload_rss_mb": after_payload_mb,
        "after_call_rss_mb": after_call_mb,
        "call_incremental_peak_mb": max(0.0, after_call_mb - after_payload_mb),
        "output_mb": result.nbytes / 1024.0**2,
    }


def _thread_worker() -> dict:
    import numpy as np
    rust = _rust_module()

    rng = np.random.default_rng(20260728)
    coordinates = rng.random((1_200, 2_500, 3), dtype=np.float64)
    weights = np.ones(2_500, dtype=np.float64)
    expected = coordinates.mean(axis=1, keepdims=True)
    timings = {}
    reference = None

    for num_threads in (1, 2, 4):
        def call(selected_threads=num_threads):
            return np.asarray(
                rust.get_center(coordinates, weights, selected_threads)
            )

        output = call()
        np.testing.assert_allclose(output, expected, rtol=1e-13, atol=1e-13)
        if reference is None:
            reference = output
        else:
            np.testing.assert_allclose(output, reference, rtol=0.0, atol=0.0)
        minimum, samples = _minimum_time(call)
        timings[str(num_threads)] = {
            "min_seconds": minimum,
            "median_seconds": statistics.median(samples),
            "samples_seconds": samples,
        }

    serial = timings["1"]["min_seconds"]
    return {
        "coordinates_shape": list(coordinates.shape),
        "dtype": str(coordinates.dtype),
        "timings": timings,
        "speedup_vs_one_thread": {
            "2": serial / timings["2"]["min_seconds"],
            "4": serial / timings["4"]["min_seconds"],
        },
    }


def _oversubscription_worker() -> dict:
    import numpy as np
    rust = _rust_module()

    rng = np.random.default_rng(20260728)
    coordinates = rng.random((400, 1_500, 3), dtype=np.float64)
    weights = np.ones(1_500, dtype=np.float64)
    expected = coordinates.mean(axis=1, keepdims=True)
    pool_threads = 2
    concurrent_calls = 4

    def calculate():
        return np.asarray(rust.get_center(coordinates, weights, pool_threads))

    started = perf_counter()
    with ThreadPoolExecutor(max_workers=concurrent_calls) as executor:
        outputs = list(executor.map(lambda _: calculate(), range(concurrent_calls)))
    elapsed = perf_counter() - started

    for output in outputs:
        np.testing.assert_allclose(output, expected, rtol=1e-13, atol=1e-13)

    return {
        "coordinates_shape": list(coordinates.shape),
        "dtype": str(coordinates.dtype),
        "concurrent_calls": concurrent_calls,
        "rayon_threads_per_call": pool_threads,
        "maximum_native_threads_requested": concurrent_calls * pool_threads,
        "elapsed_seconds": elapsed,
        "all_results_equal": True,
    }


WORKERS = {
    "startup": _startup_worker,
    "memory": _memory_worker,
    "threads": _thread_worker,
    "oversubscription": _oversubscription_worker,
}


def _run_isolated(case: str) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"molsysmt-rust-{case}-") as directory:
        environment = os.environ.copy()
        existing = environment.get("PYTHONPATH")
        environment["PYTHONPATH"] = (
            str(REPOSITORY)
            if not existing
            else os.pathsep.join((str(REPOSITORY), existing))
        )
        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--worker", case],
            cwd=directory,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
    if result.returncode != 0:
        raise RuntimeError(
            f"{case} benchmark failed with exit code {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return json.loads(result.stdout)


def _git_metadata() -> dict:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return {"commit": commit, "dirty": bool(status.strip())}


def _environment() -> dict:
    import numpy as np
    rust = _rust_module()

    extension_path = Path(rust.__file__).resolve()
    distribution = metadata.distribution("molsysmt")

    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "molsysmt": distribution.version,
        "molsysmt_import_path": str(extension_path.parent),
        "rust_extension_path": str(extension_path),
        "rust_extension_sha256": _sha256(extension_path),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": _cpu_model(),
        "logical_cpus": os.cpu_count(),
        **_git_metadata(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", choices=WORKERS)
    parser.add_argument(
        "--installed-extension",
        action="store_true",
        help="load the installed extension without importing MolSysMT's public package",
    )
    arguments = parser.parse_args()

    if arguments.installed_extension:
        os.environ[INSTALLED_EXTENSION_ENV] = "1"

    if arguments.worker:
        print(json.dumps(WORKERS[arguments.worker](), sort_keys=True))
        return 0

    report = {
        "schema_version": 1,
        "environment": _environment(),
        "results": {case: _run_isolated(case) for case in WORKERS},
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
