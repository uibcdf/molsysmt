"""Reject unestablished workload/runtime equivalence without restricting APIs."""

import hashlib
import json
import math
import re
from statistics import median

try:
    from .telemetry import (
        CONTEXT_SCHEMA,
        DEPENDENCIES,
        THREAD_VARIABLES,
        WORKLOAD_SCHEMA,
    )
except ImportError:  # Standalone CLI beside these files, without package imports.
    from telemetry import (
        CONTEXT_SCHEMA,
        DEPENDENCIES,
        THREAD_VARIABLES,
        WORKLOAD_SCHEMA,
    )


def _require(condition, reason):
    if not condition:
        raise ValueError(reason)


def _positive_integer(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _mapping(value, label):
    _require(isinstance(value, dict), f"{label}: expected a mapping.")
    return value


def _digest(value, size=64):
    return (
        isinstance(value, str)
        and re.fullmatch(r"[0-9a-f]{%d}" % size, value) is not None
    )


def validate_context(data, label):
    """Require recorded, known conditions rather than treating missing == missing."""
    context = data.get("comparison_context")
    _require(
        isinstance(context, dict) and context.get("schema") == CONTEXT_SCHEMA,
        f"{label}: missing supported comparison_context; historical timings are unevaluable.",
    )
    environment = _mapping(data.get("environment", {}), label)
    _require(
        _digest(environment.get("git_commit"), 40)
        and environment.get("git_dirty") is False,
        f"{label}: product source must identify a clean committed input.",
    )
    runtime = _mapping(context.get("runtime", {}), label)
    _require(
        all(
            _text(runtime.get(k))
            for k in ("python", "implementation", "os", "os_release", "machine")
        ),
        f"{label}: incomplete interpreter/OS identity.",
    )
    hardware = _mapping(context.get("hardware", {}), label)
    _require(
        _text(hardware.get("cpu_model"))
        and all(
            _positive_integer(hardware.get(k))
            for k in ("logical_cpus", "affinity_cpus", "memory_bytes")
        ),
        f"{label}: incomplete CPU/affinity/memory identity.",
    )
    _require(
        hardware["affinity_cpus"] <= hardware["logical_cpus"],
        f"{label}: impossible CPU affinity count.",
    )
    limits = _mapping(context.get("limits", {}), label)
    _require(
        all(_text(limits.get(k)) for k in ("cpu.max", "memory.max", "memory.swap.max")),
        f"{label}: unknown process-tree resource limits.",
    )
    cpu = limits["cpu.max"].split()
    _require(
        len(cpu) == 2
        and (cpu[0] == "max" or (cpu[0].isdecimal() and int(cpu[0]) > 0))
        and cpu[1].isdecimal()
        and int(cpu[1]) > 0,
        f"{label}: invalid effective CPU quota.",
    )
    for key in ("memory.max", "memory.swap.max"):
        value = limits[key]
        _require(
            value == "max"
            or (
                value.isdecimal()
                and (int(value) > 0 or (key == "memory.swap.max" and value == "0"))
            ),
            f"{label}: invalid effective {key}.",
        )
    threads = _mapping(context.get("threads", {}), label)
    _require(
        all(
            isinstance(threads.get(k), str)
            and threads[k].isdecimal()
            and int(threads[k]) > 0
            for k in THREAD_VARIABLES
        ),
        f"{label}: explicit positive thread settings are required.",
    )
    dependencies = _mapping(context.get("dependencies", {}), label)
    for name in DEPENDENCIES:
        identity = _mapping(dependencies.get(name, {}), label)
        _require(
            _text(identity.get("version")),
            f"{label}: missing dependency identity for {name}.",
        )
        _require(
            identity.get("origin_matches") is True
            and _digest(identity.get("module_sha256")),
            f"{label}: {name} metadata does not identify the actual imported module.",
        )
        known = (
            identity.get("kind") == "editable_git"
            and _digest(identity.get("commit"), 40)
            and identity.get("dirty") is False
        ) or (
            identity.get("kind") == "installed_record"
            and _digest(identity.get("record_sha256"))
        )
        _require(
            known,
            f"{label}: {name} needs a clean editable commit or installed RECORD identity.",
        )
    lock = _mapping(context.get("environment_lock", {}), label)
    records = lock.get("records")
    _require(
        lock.get("kind") in {"conda_records", "distribution_records"}
        and isinstance(records, list)
        and bool(records),
        f"{label}: missing environment package/build manifest.",
    )
    _require(
        all(
            isinstance(item, dict)
            and _text(item.get("name"))
            and _text(item.get("version"))
            for item in records
        ),
        f"{label}: invalid environment package/build entries.",
    )
    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    _require(
        lock.get("sha256") == hashlib.sha256(encoded).hexdigest(),
        f"{label}: environment manifest digest does not describe its records.",
    )
    policy = _mapping(context.get("molsysmt_policy", {}), label)
    _require(
        type(policy.get("parallel_mode")) is bool
        and type(policy.get("gpu_mode")) is bool
        and _positive_integer(policy.get("num_threads"))
        and policy
        == {
            "parallel_mode": False,
            "num_threads": 1,
            "gpu_mode": False,
            "precision": "double",
            "heavy_mode": "off",
        },
        f"{label}: this protocol requires explicit serial float64 CPU/eager policy.",
    )
    units = _mapping(context.get("unit_policy", {}), label)
    _require(
        all(_text(units.get(k)) for k in ("default_form", "default_parser"))
        and isinstance(units.get("standard_units"), list)
        and bool(units["standard_units"])
        and all(_text(v) for v in units["standard_units"]),
        f"{label}: incomplete unit policy.",
    )
    return context


def validate_measurement(entry, label):
    """Check raw repetitions, the summary and the actual timing protocol."""
    samples = entry.get("samples_seconds")
    _require(
        isinstance(samples, list) and len(samples) >= 3,
        f"{label}: at least three raw repeat samples are required.",
    )
    _require(
        all(
            isinstance(v, (int, float))
            and not isinstance(v, bool)
            and math.isfinite(v)
            and v > 0
            for v in samples
        ),
        f"{label}: repeat samples must be finite and positive.",
    )
    _require(
        _positive_integer(entry.get("iterations"))
        and _positive_integer(entry.get("repeats"))
        and entry["repeats"] == len(samples),
        f"{label}: repeat/iteration metadata does not match samples.",
    )
    _require(
        math.isclose(
            entry["median_seconds"], median(samples), rel_tol=1e-12, abs_tol=0
        ),
        f"{label}: median does not describe its raw samples.",
    )
    protocol = _mapping(entry.get("measurement", {}), label)
    _require(
        _digest(protocol.get("harness_sha256")),
        f"{label}: missing measurement implementation hash.",
    )
    expected = {
        "statistic": "median of per-call block means",
        "timer": "time.perf_counter",
        "warmup_calls": 1,
        "gc_during_timing": False,
    }
    _require(
        all(
            type(protocol.get(k)) is type(v) and protocol[k] == v
            for k, v in expected.items()
        ),
        f"{label}: unsupported or incomplete measurement protocol.",
    )
    _require(
        protocol.get("process") in {"fork", "spawn_factory"},
        f"{label}: unknown worker process model.",
    )
    workload = entry.get("workload", {})
    _require(
        isinstance(workload, dict)
        and workload.get("schema") == WORKLOAD_SCHEMA
        and _text(workload.get("operation"))
        and _digest(workload.get("producer_sha256")),
        f"{label}: missing versioned workload/producer identity.",
    )
    inputs = _mapping(workload.get("inputs", {}), label)
    _require(
        _positive_integer(inputs.get("n_atoms"))
        and _positive_integer(inputs.get("n_structures")),
        f"{label}: actual molecular workload dimensions are required.",
    )
    files = inputs.get("files")
    _require(
        isinstance(files, dict)
        and bool(files)
        and all(_text(k) and _digest(v) for k, v in files.items()),
        f"{label}: actual input file hashes are required.",
    )
    semantics = _mapping(workload.get("semantics", {}), label)
    route = _mapping(workload.get("route", {}), label)
    _require(
        _text(semantics.get("unit")) and type(semantics.get("pbc")) is bool,
        f"{label}: explicit unit and periodic semantics are required.",
    )
    _require(
        all(_text(route.get(k)) for k in ("provider", "call", "input_dtype", "output")),
        f"{label}: explicit implementation/precision/output identity is required.",
    )
    return {
        "protocol": protocol,
        "iterations": entry["iterations"],
        "repeats": entry["repeats"],
        "workload": workload,
    }


def require_comparable(baseline, current, base_results, current_results):
    first = validate_context(baseline, "Reference")
    second = validate_context(current, "Current")
    _require(
        first == second,
        "Execution contexts differ; no attributed timing comparison is supported.",
    )
    for name, entry in current_results.items():
        current_identity = validate_measurement(entry, f"Current {name}")
        if name in base_results:
            reference_identity = validate_measurement(
                base_results[name], f"Reference {name}"
            )
            _require(
                reference_identity == current_identity,
                f"{name}: workload, precision, input, repeats or protocol differ.",
            )
