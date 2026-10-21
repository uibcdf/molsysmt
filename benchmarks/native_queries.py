"""Measuring existing native query routes before implementing issue #128.

Adapter and property timings have narrower contracts than ``basic.get``. They
are diagnostic baselines, never advertised as equivalent public replacements.
"""

from __future__ import annotations

import argparse
import cProfile
import hashlib
import importlib
import importlib.metadata
import json
import platform
import pstats
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from time import perf_counter

import numpy as np

import molsysmt as msm
from molsysmt.native import MolSys, MolSysBuilder


def _measure(function, iterations, repeats):
    function()
    samples = []
    for _ in range(repeats):
        start = perf_counter()
        for _ in range(iterations):
            function()
        samples.append((perf_counter() - start) / iterations)
    return {
        "median_seconds": median(samples),
        "min_seconds": min(samples),
        "max_seconds": max(samples),
    }


def _profile(function):
    profiler = cProfile.Profile()
    profiler.runcall(function)
    counts = {}
    names = {
        "get_form",
        "where_is_attribute",
        "select",
        "_run_digestion",
        "is_quantity",
    }
    for (filename, _, name), (_, total, _, _, _) in pstats.Stats(
        profiler
    ).stats.items():
        if name in names:
            key = f"{Path(filename).parent.name}/{Path(filename).name}:{name}"
            counts[key] = counts.get(key, 0) + total
    return counts


def _objects(n_atoms, n_structures, dictionaries):
    system = MolSys(n_atoms=n_atoms)
    values = (
        np.arange(n_structures * n_atoms * 3, dtype=float).reshape(
            n_structures, n_atoms, 3
        )
        * 1e-5
    )
    system.structures.coordinates = msm.pyunitwizard.quantity(values, "nm")
    interactions = msm.Interactions.from_records(
        [
            {
                "structure_index": index,
                "interaction_type": "synthetic_pair",
                "participants": [
                    {"role": "a", "atom_indices": [0]},
                    {"role": "b", "atom_indices": [n_atoms - 1]},
                ],
            }
            for index in (0, n_structures - 1)
        ],
        n_atoms=n_atoms,
        n_structures=n_structures,
        evaluated_structure_indices=list(range(n_structures)),
        method="benchmark_fixture",
    )
    objects = {
        "MolSys": system,
        "Topology": system.topology,
        "Structures": system.structures,
        "ChemicalStates": system.chemical_states,
        "Interactions": interactions,
        "MolSysBuilder": MolSysBuilder(system),
    }
    if dictionaries:
        for name in (
            "MolSys",
            "Topology",
            "Structures",
            "ChemicalStates",
            "Interactions",
        ):
            objects[name + "Dict"] = msm.convert(
                objects[name], to_form=f"molsysmt.{name}Dict"
            )
    return objects, values


def _routes(name, obj, n_atoms, n_structures, values):
    form = msm.get_form(obj)
    adapter = msm.form._dict_modules[form]

    def public_count():
        return msm.get(obj, n_atoms=True)

    assert public_count() == n_atoms
    routes = {"get_n_atoms": public_count}
    getter = getattr(adapter, "get_n_atoms_from_system", None)
    if getter is not None:
        assert getter(obj) == n_atoms
        routes["adapter_n_atoms_validated"] = lambda: getter(obj)
        routes["adapter_n_atoms_trusted_internal"] = lambda: getter(
            obj, skip_digestion=True
        )
    if hasattr(type(obj), "n_atoms"):
        assert obj.n_atoms == n_atoms
        routes["property_n_atoms"] = lambda: obj.n_atoms
    if hasattr(obj, "get") and name in ("MolSys", "MolSysBuilder"):
        assert obj.get(n_atoms=True) == n_atoms
        routes["method_get_n_atoms"] = lambda: obj.get(n_atoms=True)

    # General info reports molecular attributes, not the domain-specific
    # inventories of chemical states or sparse interaction observations.
    for output_type in ("dataframe", "styler"):

        def info(output_type=output_type):
            return msm.info(obj, output_type=output_type)

        result = info()
        table = result if output_type == "dataframe" else result.data
        assert table["n_atoms"].tolist() == [n_atoms]
        routes["info_" + output_type] = info
    if name in ("MolSys", "Topology"):
        indices = [n_atoms - 1, 0, 2]

        def selected():
            return msm.get(obj, element="atom", selection=indices, atom_index=True)

        assert selected() == indices
        routes["get_selected_atom_indices"] = selected
    if name in ("MolSys", "Structures"):
        atoms = [n_atoms - 1, 0, n_atoms - 1]
        structures = [n_structures - 1, 0, n_structures - 1]
        for kind, kwargs, expected in (
            ("coordinates_all", {}, values),
            (
                "coordinates_selected",
                {"selection": atoms, "structure_indices": structures},
                values[np.ix_(structures, atoms, [0, 1, 2])],
            ),
        ):

            def coordinates(kwargs=kwargs):
                return msm.get(obj, element="atom", coordinates=True, **kwargs)

            np.testing.assert_allclose(
                msm.pyunitwizard.get_value(coordinates(), to_unit="nm"), expected
            )
            routes["get_" + kind] = coordinates
    if name == "ChemicalStates":

        def inventory():
            return msm.get(obj, n_chemical_states=True)

        assert inventory() == 1
        routes["get_n_chemical_states"] = inventory
    if name == "Interactions":

        def query():
            return obj.query(structure_indices=[n_structures - 1, 0], atom_indices=[0])

        assert query().n_interactions == 2
        routes["domain_query_warm"] = query
    return routes


def run(args):
    records = []
    for n_atoms in args.atoms:
        objects, values = _objects(
            n_atoms, args.structures, dictionaries=n_atoms <= args.dictionary_limit
        )
        for name, obj in objects.items():
            print(f"Measuring {name}, {n_atoms} atoms", file=sys.stderr, flush=True)
            routes = _routes(name, obj, n_atoms, args.structures, values)
            records.append(
                {
                    "class": name,
                    "n_atoms": n_atoms,
                    "n_structures": args.structures,
                    "has_get_method": hasattr(obj, "get"),
                    "has_info_method": hasattr(obj, "info"),
                    "routes": {
                        route: _measure(function, args.iterations, args.repeats)
                        for route, function in routes.items()
                    },
                    "count_profile": _profile(routes["get_n_atoms"]),
                }
            )
        print(f"Completed {n_atoms} atoms", file=sys.stderr, flush=True)
    root = Path(__file__).resolve().parents[1]
    packages = {}
    for package in (
        "molsysmt",
        "argdigest",
        "smonitor",
        "pyunitwizard",
        "numpy",
        "pandas",
    ):
        module = importlib.import_module(package)
        path = Path(module.__file__).resolve()
        if path.is_relative_to(root.parent):
            origin = "{CHECKOUT_PARENT}/" + str(path.relative_to(root.parent))
        elif path.is_relative_to(Path(sys.prefix)):
            origin = "{PYTHON_PREFIX}/" + str(path.relative_to(sys.prefix))
        else:
            origin = str(path)
        packages[package] = {
            "version": importlib.metadata.version(package),
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
        "schema": "molsysmt.native_queries_baseline@1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        "benchmark_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "cpu": cpu,
            "packages": packages,
        },
        "iterations": args.iterations,
        "repeats": args.repeats,
        "methodology": {
            "fixtures": "Synthetic unbonded atoms, one reference state, deterministic nm coordinates.",
            "warmup": "Validation and one untimed call per route; imports and construction excluded.",
            "timing": "Sequential routes, normal garbage collection, median/min/max per-call wall time.",
            "info": "Table construction only; no notebook display or HTML rendering.",
            "adapter": "Narrower contract; excludes general selection/output normalization.",
            "trusted": "Internal diagnostic only; public boundary validation excluded.",
            "query": "Warm sparse interaction query; includes validated domain selection, excludes first index build.",
            "limitations": "Single process/environment; no new native implementation, cold start or memory benchmark.",
        },
        "records": records,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atoms", type=int, nargs="+", default=[32, 1000, 100000])
    parser.add_argument("--structures", type=int, default=8)
    parser.add_argument("--dictionary-limit", type=int, default=32)
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args()
    if min(options.atoms) < 3 or options.structures < 2:
        parser.error("Use at least three atoms and two structures.")
    if options.iterations < 1 or options.repeats < 1:
        parser.error("Iterations and repeats must be positive.")
    options.output.write_text(json.dumps(run(options), indent=2) + "\n")
