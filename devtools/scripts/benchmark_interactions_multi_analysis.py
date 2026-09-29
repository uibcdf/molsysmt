#!/usr/bin/env python3
"""Measure separate analysis results against a grouped HDF5 container probe."""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import tempfile
import time
from pathlib import Path

import h5py
import numpy as np
from benchmark_interactions_contract import (
    UNITS,
    expected,
    generate_fixture,
    materialize,
)

import molsysmt as msm


def _copy_analysis(source, target):
    with h5py.File(source, "r") as source_file:
        for key, value in source_file.attrs.items():
            target.attrs[key] = value
        for key in source_file:
            if key != "source_maps_probe":
                source_file.copy(key, target)


def _check_copy(source, grouped, method):
    with h5py.File(source, "r") as original, h5py.File(grouped, "r") as file:
        copied = file[f"analyses/{method}"]
        if json.loads(copied.attrs["metadata"]) != json.loads(
            original.attrs["metadata"]
        ):
            raise AssertionError(f"{method} metadata changed")
        def check_dataset(name, item):
            if (isinstance(item, h5py.Dataset)
                    and not name.startswith("source_maps_probe/")):
                if not np.array_equal(item[:], copied[name][:]):
                    raise AssertionError(f"{method}/{name} changed")
        original.visititems(check_dataset)
        for name in ("atom_indices", "structure_indices"):
            if not np.array_equal(
                original[f"source_maps_probe/{name}"][:],
                file[f"source_maps_probe/{name}"][:],
            ):
                raise AssertionError(f"{method} shared {name} changed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=1000)
    args = parser.parse_args()
    n_atoms = 500
    records, evaluated = generate_fixture(
        args.frames, n_atoms, 8, "mixed", 251
    )
    methods = sorted({row["interaction_type"] for row in records})
    results = {}
    rows_by_method = {}
    coverage_by_method = {}
    for method in methods:
        coverage = [frame for frame in evaluated
                    if method != "disulfide_candidate" or frame % 2 == 0]
        covered = set(coverage)
        rows = [row for row in records
                if row["interaction_type"] == method
                and row["structure_index"] in covered]
        result = msm.Interactions.from_records(
            rows, n_atoms=n_atoms, n_structures=args.frames,
            evaluated_structure_indices=coverage, method=f"detector:{method}",
            measure_units=UNITS, parameters={"seed": 251, "kind": method},
            source_id="synthetic_contract",
        )
        results[method] = result
        rows_by_method[method] = rows
        coverage_by_method[method] = coverage
        for frames in ([7, 2, 7], [0], [args.frames - 1]):
            if materialize(result.query(structure_indices=frames)) != expected(
                rows, coverage, frames=frames
            ):
                raise AssertionError(f"{method} frame contract differs")
        if materialize(result.query(atom_indices=[0])) != expected(
            rows, coverage, atoms=[0]
        ):
            raise AssertionError(f"{method} atom contract differs")
    rng = np.random.default_rng(255)
    frame_samples = []
    atom_samples = []
    for frame in rng.integers(0, args.frames, size=100):
        start = time.perf_counter_ns()
        for result in results.values():
            result.query(structure_indices=[int(frame)]).to_dict()
        frame_samples.append((time.perf_counter_ns() - start) / 1e6)
    for atom in rng.integers(0, n_atoms, size=20):
        start = time.perf_counter_ns()
        for result in results.values():
            result.query(atom_indices=[int(atom)]).to_dict()
        atom_samples.append((time.perf_counter_ns() - start) / 1e6)
    with tempfile.TemporaryDirectory() as directory:
        base = Path(directory)
        files = {}
        for method, result in results.items():
            path = base / f"{method}.h5i"
            result.save(path)
            with h5py.File(path, "r+") as file:
                source = file.create_group("source_maps_probe")
                source.create_dataset("atom_indices", data=np.arange(n_atoms),
                                      compression="gzip")
                source.create_dataset("structure_indices",
                                      data=np.arange(args.frames),
                                      compression="gzip")
            files[method] = path
            loaded = msm.Interactions.load(path)
            if materialize(loaded.query(atom_indices=[0])) != expected(
                rows_by_method[method], coverage_by_method[method], atoms=[0]
            ):
                raise AssertionError(f"{method} standalone round trip differs")
        grouped = base / "grouped.h5i"
        with h5py.File(grouped, "w") as file:
            file.attrs["format"] = "molsysmt.interactions.multiple_probe"
            file.attrs["schema_version"] = 1
            source = file.create_group("source_maps_probe")
            source.create_dataset("atom_indices", data=np.arange(n_atoms),
                                  compression="gzip")
            source.create_dataset("structure_indices",
                                  data=np.arange(args.frames),
                                  compression="gzip")
            analyses = file.create_group("analyses")
            for method, path in files.items():
                _copy_analysis(path, analyses.create_group(method))
        for method, path in files.items():
            _check_copy(path, grouped, method)
        separate_bytes = sum(path.stat().st_size for path in files.values())
        grouped_bytes = grouped.stat().st_size
        print(json.dumps({
            "platform": platform.platform(), "frames": args.frames,
            "methods": methods,
            "observations_per_method": {name: len(rows)
                                        for name, rows in rows_by_method.items()},
            "evaluated_per_method": {name: len(frames)
                                     for name, frames in coverage_by_method.items()},
            "four_separate_files_bytes": separate_bytes,
            "one_grouped_file_bytes": grouped_bytes,
            "grouped_saving_pct": round(
                100 * (separate_bytes - grouped_bytes) / separate_bytes, 2
            ),
            "collection_warm_frame_median_ms": round(
                statistics.median(frame_samples), 4
            ),
            "collection_warm_atom_median_ms": round(
                statistics.median(atom_samples), 4
            ),
            "note": "Grouped file is a storage probe, not a public loader",
        }, indent=2))


if __name__ == "__main__":
    main()
