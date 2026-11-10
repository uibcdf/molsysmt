"""Collect explicit evidence for conservative, advisory timing comparisons."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from urllib.parse import unquote, urlparse

CONTEXT_SCHEMA = "molsysmt.benchmark-context@1"
WORKLOAD_SCHEMA = "molsysmt.benchmark-workload@1"
THREAD_VARIABLES = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "RAYON_NUM_THREADS",
    "OPENMM_CPU_THREADS",
    "NUMEXPR_NUM_THREADS",
)
DEPENDENCIES = (
    "numpy",
    "scipy",
    "pandas",
    "mdtraj",
    "MDAnalysis",
    "pint",
    "pyunitwizard",
    "argdigest",
    "depdigest",
    "smonitor",
)


def file_digest(path):
    """Hash a file in bounded buffers, without publishing its local pathname."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(128 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def array_identity(array):
    """Identify the actual prepared array, including precision and dimensions."""
    view = memoryview(array)
    if not view.c_contiguous:
        raise ValueError("Benchmark array fingerprints require contiguous input.")
    return {
        "shape": list(view.shape),
        "format": view.format,
        "sha256": hashlib.sha256(view.cast("B")).hexdigest(),
    }


def _dependency_identity(name):
    try:
        distribution = importlib.metadata.distribution(name)
    except importlib.metadata.PackageNotFoundError:
        return {"version": None, "kind": "unavailable"}
    module = importlib.import_module(name)
    origin = Path(module.__file__).resolve()
    result = {
        "version": distribution.version,
        "module_sha256": file_digest(origin),
        "runtime_version": getattr(module, "__version__", None),
    }
    direct = json.loads(distribution.read_text("direct_url.json") or "{}")
    if direct.get("dir_info", {}).get("editable"):
        source = urlparse(direct.get("url", ""))
        directory = Path(unquote(source.path))
        result.update(kind="editable_git", commit=None, dirty=None)
        result["origin_matches"] = source.scheme == "file" and origin.is_relative_to(
            directory.resolve()
        )
        # Use the explicitly recorded project root, never an enclosing clone.
        if source.scheme == "file" and (directory / ".git").exists():
            try:

                def git(*arguments):
                    return subprocess.check_output(
                        ["git", "-c", "core.fsmonitor=false", *arguments],
                        cwd=directory,
                        text=True,
                        stderr=subprocess.DEVNULL,
                    ).strip()

                result.update(
                    commit=git("rev-parse", "HEAD"),
                    dirty=bool(git("status", "--porcelain")),
                )
            except (OSError, subprocess.CalledProcessError):
                pass
    else:
        record = distribution.read_text("RECORD")
        result.update(
            kind="installed_record",
            record_sha256=None
            if not record
            else hashlib.sha256(record.encode()).hexdigest(),
        )
        result["origin_matches"] = (
            origin == Path(distribution.locate_file(name + "/__init__.py")).resolve()
        )
    return result


def _environment_lock():
    """Fingerprint package/build records, excluding the product under comparison."""
    directory = Path(sys.prefix) / "conda-meta"
    records = []
    if directory.is_dir():
        for path in sorted(directory.glob("*.json")):
            entry = json.loads(path.read_text())
            if entry.get("name") != "molsysmt":
                records.append(
                    {
                        key: entry.get(key)
                        for key in ("name", "version", "build", "sha256", "md5")
                    }
                )
        kind = "conda_records"
    else:
        for distribution in importlib.metadata.distributions():
            name = distribution.metadata.get("Name", "").lower().replace("_", "-")
            if name != "molsysmt":
                raw = (
                    distribution.read_text("RECORD")
                    or distribution.read_text("METADATA")
                    or ""
                )
                records.append(
                    {
                        "name": name,
                        "version": distribution.version,
                        "record_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                    }
                )
        kind = "distribution_records"
    records.sort(key=lambda item: json.dumps(item, sort_keys=True))
    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return {
        "kind": kind,
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "records": records,
    }


def comparison_context():
    """Record execution conditions; missing facts remain explicitly unknown."""
    model = platform.processor() or None
    memory_bytes = None
    if Path("/proc/cpuinfo").exists():
        model = next(
            (
                line.split(":", 1)[1].strip()
                for line in Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")
            ),
            model,
        )
    if Path("/proc/meminfo").exists():
        memory_bytes = (
            int(
                next(
                    line.split()[1]
                    for line in Path("/proc/meminfo").read_text().splitlines()
                    if line.startswith("MemTotal:")
                )
            )
            * 1024
        )
    limits = {"cpu.max": None, "memory.max": None, "memory.swap.max": None}
    membership = Path("/proc/self/cgroup")
    if membership.exists():
        entry = next(
            (
                line[3:]
                for line in membership.read_text().splitlines()
                if line.startswith("0::")
            ),
            None,
        )
        if entry is not None:
            directory = Path("/sys/fs/cgroup") / entry.lstrip("/")
            for name in limits:
                values = []
                while directory.is_relative_to("/sys/fs/cgroup"):
                    path = directory / name
                    if path.is_file():
                        values.append(path.read_text().strip())
                    directory = directory.parent
                directory = Path("/sys/fs/cgroup") / entry.lstrip("/")
                if values:
                    if name == "cpu.max":
                        bounded = [
                            value for value in values if not value.startswith("max ")
                        ]
                        limits[name] = (
                            min(bounded, key=lambda v: Fraction(*map(int, v.split())))
                            if bounded
                            else values[0]
                        )
                    else:
                        bounded = [int(value) for value in values if value != "max"]
                        limits[name] = str(min(bounded)) if bounded else "max"
    import molsysmt as msm

    policy = msm.pyunitwizard.configure.report()
    return {
        "schema": CONTEXT_SCHEMA,
        "runtime": {
            "python": platform.python_version(),
            "implementation": sys.implementation.name,
            "os": platform.system(),
            "os_release": platform.release(),
            "machine": platform.machine(),
        },
        "hardware": {
            "cpu_model": model,
            "logical_cpus": os.cpu_count(),
            "affinity_cpus": len(os.sched_getaffinity(0))
            if hasattr(os, "sched_getaffinity")
            else None,
            "memory_bytes": memory_bytes,
        },
        "limits": limits,
        "threads": {name: os.environ.get(name) for name in THREAD_VARIABLES},
        "dependencies": {name: _dependency_identity(name) for name in DEPENDENCIES},
        "environment_lock": _environment_lock(),
        "molsysmt_policy": {
            name: getattr(msm.configure, name)
            for name in (
                "parallel_mode",
                "num_threads",
                "gpu_mode",
                "precision",
                "heavy_mode",
            )
        },
        "unit_policy": {
            name: policy[name]
            for name in ("default_form", "default_parser", "standard_units")
        },
    }


def workload(operation, *, inputs, semantics, route, producer):
    """Describe actual prepared inputs and the explicitly validated observable."""
    return {
        "schema": WORKLOAD_SCHEMA,
        "operation": operation,
        "producer_sha256": file_digest(producer),
        "inputs": inputs,
        "semantics": semantics,
        "route": route,
    }


def resource_observation():
    """Retain changing host conditions separately from compatibility identities."""
    observation = {
        "load_average": list(os.getloadavg()) if hasattr(os, "getloadavg") else None
    }
    for name in ["meminfo", "pressure/memory", "vmstat"]:
        path = Path("/proc") / name
        if path.is_file():
            if name == "meminfo":
                observation["memory_kib"] = {
                    line.split(":")[0]: int(line.split()[1])
                    for line in path.read_text().splitlines()
                    if line.startswith(("MemAvailable:", "SwapFree:"))
                }
            elif name == "vmstat":
                observation["swap_pages"] = {
                    parts[0]: int(parts[1])
                    for line in path.read_text().splitlines()
                    if (parts := line.split())[0] in {"pswpin", "pswpout"}
                }
            else:
                observation["memory_pressure"] = path.read_text().strip()
    return observation
