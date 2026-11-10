"""Small complete records for testing the benchmark evidence contract."""

import hashlib
import json

from benchmarks.telemetry import (
    CONTEXT_SCHEMA,
    DEPENDENCIES,
    THREAD_VARIABLES,
    WORKLOAD_SCHEMA,
)


def session(value=1.0, name="product"):
    lock = [{"name": "test-numpy", "version": "1", "record_sha256": "1" * 64}]
    return {
        "environment": {"git_commit": "0" * 40, "git_dirty": False},
        "comparison_context": {
            "schema": CONTEXT_SCHEMA,
            "runtime": {
                "python": "3.14.7",
                "implementation": "cpython",
                "os": "Linux",
                "os_release": "test-kernel",
                "machine": "x86_64",
            },
            "hardware": {
                "cpu_model": "test CPU",
                "logical_cpus": 4,
                "affinity_cpus": 2,
                "memory_bytes": 16 * 1024**3,
            },
            "limits": {
                "cpu.max": "100000 100000",
                "memory.max": str(2 * 1024**3),
                "memory.swap.max": "0",
            },
            "threads": dict.fromkeys(THREAD_VARIABLES, "1"),
            "dependencies": {
                key: {
                    "version": "test-1",
                    "kind": "installed_record",
                    "origin_matches": True,
                    "module_sha256": "1" * 64,
                    "record_sha256": "1" * 64,
                }
                for key in DEPENDENCIES
            },
            "environment_lock": {
                "kind": "distribution_records",
                "records": lock,
                "sha256": hashlib.sha256(
                    json.dumps(lock, sort_keys=True, separators=(",", ":")).encode()
                ).hexdigest(),
            },
            "molsysmt_policy": {
                "parallel_mode": False,
                "num_threads": 1,
                "gpu_mode": False,
                "precision": "double",
                "heavy_mode": "off",
            },
            "unit_policy": {
                "default_form": "pint",
                "default_parser": "pint",
                "standard_units": ["nm"],
            },
        },
        "results": {
            name: {
                "median_seconds": value,
                "samples_seconds": [value] * 3,
                "repeats": 3,
                "iterations": 1,
                "measurement": {
                    "harness_sha256": "2" * 64,
                    "statistic": "median of per-call block means",
                    "timer": "time.perf_counter",
                    "process": "fork",
                    "warmup_calls": 1,
                    "gc_during_timing": False,
                },
                "workload": {
                    "schema": WORKLOAD_SCHEMA,
                    "operation": "unaligned_rmsd",
                    "producer_sha256": "3" * 64,
                    "inputs": {
                        "files": {"coordinates": "4" * 64},
                        "n_atoms": 4,
                        "n_structures": 3,
                    },
                    "semantics": {"unit": "nm", "pbc": False, "superposition": False},
                    "route": {
                        "provider": "mdtraj" if "mdtraj" in name else "molsysmt",
                        "call": "explicit test route",
                        "input_dtype": "float64",
                        "output": "ndarray",
                    },
                },
            }
        },
    }
