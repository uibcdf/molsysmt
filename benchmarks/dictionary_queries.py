"""Measuring stored atom queries against their native reconstruction fallback.

The fallback control disables only the private direct-read capability for the
same public calls. It preserves validation, diagnostics and converter semantics.
Large cases measure direct reads only; reconstruction is deliberately bounded.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import platform
import subprocess
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from native_queries import _measure

import molsysmt as msm
from molsysmt.form import _dict_atom_queries


@contextmanager
def _reconstruction():
    original = _dict_atom_queries.can_read
    _dict_atom_queries.can_read = lambda *args, **kwargs: False
    try:
        yield
    finally:
        _dict_atom_queries.can_read = original


def _fixture(cls, n_atoms):
    topology = {
        "atoms": [
            {"atom_id": str(index), "atom_name": "C", "atom_type": "C"}
            for index in range(n_atoms)
        ]
    }
    return cls(data={"topology": topology} if cls is msm.MolSysDict else topology)


def _routes(item, n_atoms):
    indices = [n_atoms - 1, 0, n_atoms - 1]
    return {
        "count": (lambda: msm.get(item, n_atoms=True), n_atoms),
        "selected_labels": (
            lambda: msm.get(
                item,
                element="atom",
                selection=indices,
                atom_id=True,
                atom_name=True,
                atom_type=True,
            ),
            [[str(index) for index in indices], ["C"] * 3, ["C"] * 3],
        ),
        "all_names": (
            lambda: msm.get(item, element="atom", atom_name=True),
            ["C"] * n_atoms,
        ),
    }


def run(args):
    records = []
    for n_atoms in args.atoms:
        for cls in (msm.TopologyDict, msm.MolSysDict):
            item = _fixture(cls, n_atoms)
            print(
                f"Measuring {cls.__name__}, {n_atoms} atoms",
                file=sys.stderr,
                flush=True,
            )
            routes = _routes(item, n_atoms)
            direct = {}
            for name, (function, expected) in routes.items():
                assert function() == expected
                direct[name] = _measure(function, args.iterations, args.repeats)
            fallback = {}
            if n_atoms <= args.reconstruction_limit:
                with _reconstruction():
                    for name, (function, expected) in routes.items():
                        assert function() == expected
                        fallback[name] = _measure(
                            function, args.iterations, args.repeats
                        )
            records.append(
                {
                    "class": cls.__name__,
                    "n_atoms": n_atoms,
                    "direct": direct,
                    "reconstruction_control": fallback,
                }
            )
    root = Path(__file__).resolve().parents[1]
    packages = {}
    for name in (
        "molsysmt",
        "numpy",
        "pandas",
        "argdigest",
        "smonitor",
        "pyunitwizard",
    ):
        path = Path(importlib.import_module(name).__file__).resolve()
        if path.is_relative_to(root.parent):
            origin = "{CHECKOUT_PARENT}/" + str(path.relative_to(root.parent))
        elif path.is_relative_to(Path(sys.prefix)):
            origin = "{PYTHON_PREFIX}/" + str(path.relative_to(sys.prefix))
        else:
            origin = str(path)
        packages[name] = {
            "version": importlib.metadata.version(name),
            "import_path": origin,
        }
    cpu = platform.processor()
    if Path("/proc/cpuinfo").exists():
        cpu = next(
            (
                line.split(":", 1)[1].strip()
                for line in Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")
            ),
            cpu,
        )
    return {
        "schema": "molsysmt.dictionary_queries_benchmark@1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        "benchmark_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "cpu": cpu,
            "packages": packages,
        },
        "iterations": args.iterations,
        "repeats": args.repeats,
        "reconstruction_limit": args.reconstruction_limit,
        "methodology": {
            "fixture": "Declared unbonded C atoms with string IDs/names/types; no structures.",
            "warmup": "Independent expected-value assertions and one untimed call per route.",
            "timing": "Sequential, normal GC, median/min/max wall time per call in repeated blocks.",
            "control": "Same public queries with only the private stored-read capability disabled; complete native conversion retained.",
            "limitations": "One environment; synthetic atom queries only. No full info, coordinates, disk IO, cold startup, memory peaks or client throughput.",
        },
        "records": records,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atoms", type=int, nargs="+", default=[32, 1000, 100000])
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--reconstruction-limit", type=int, default=32)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if min(args.atoms) < 1 or min(args.iterations, args.repeats) < 1:
        parser.error("Atom counts, iterations and repeats must be positive.")
    args.output.write_text(json.dumps(run(args), indent=2) + "\n")
