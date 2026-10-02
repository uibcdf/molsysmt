"""Measure relevant-frame queries and bounded projection independently of storage."""

import argparse
import json
import platform
import subprocess
import time
import tracemalloc
from pathlib import Path
from statistics import median

import numpy as np

import molsysmt as msm


def trajectory(reused=False):
    evaluated = np.arange(4999)
    frames = np.repeat(evaluated[evaluated % 10 != 1], 5)
    count = len(frames)
    indices = np.arange(count)
    catalog_count = 32 if reused else count
    return msm.Interactions(
        n_atoms=62,
        n_structures=5000,
        evaluated_structure_indices=evaluated,
        relation_types=["hbond"] * catalog_count,
        relation_participant_offsets=np.arange(catalog_count + 1) * 3,
        participant_roles=["donor", "hydrogen", "acceptor"] * catalog_count,
        participant_atom_offsets=np.arange(catalog_count * 3 + 1),
        participant_atoms=(
            (np.arange(catalog_count) % 32)[:, None] + [0, 1, 10]
        ).ravel(),
        occurrence_structures=frames,
        occurrence_relations=indices % catalog_count,
        occurrence_evidence=np.zeros(count, dtype=np.int32),
        evidence_labels=["synthetic"],
        measurements={"distance": np.full(count, 0.2)},
        measure_units={"distance": "nm"},
        method="synthetic_query_probe",
    )


def measure(operation, repeats=5):
    operation()
    times = []
    for _ in range(repeats):
        begin = time.perf_counter()
        value = operation()
        times.append((time.perf_counter() - begin) * 1000)
    tracemalloc.start()
    value = operation()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return dict(median_ms=median(times), allocation_peak_bytes=peak), value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args()
    result = trajectory()
    result.query(atom_indices=[0], structure_indices=[0])
    report = dict(
        python=platform.python_version(),
        platform=platform.platform(),
        numpy=np.__version__,
        molsysmt=msm.__version__,
        source_base_commit=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip(),
        warmup="one untimed call per operation; five timed repetitions; median",
        analysis_numeric_bytes=result.numeric_nbytes,
        queries={},
    )
    for mode in ("incident", "internal", "cross"):
        atoms = list(range(62 if mode == "internal" else 16))
        for name, frames in (
            ("frame0", [0]),
            ("nonconsecutive", [4900, 1, 0]),
            ("all", None),
        ):
            stats, view = measure(
                lambda atoms=atoms, frames=frames, mode=mode: result.query(
                    atom_indices=atoms, structure_indices=frames, mode=mode
                )
            )
            stats["count"] = view.n_interactions
            report["queries"][f"{mode}_{name}"] = stats
    reused = trajectory(reused=True)
    report["recurring_queries"] = {}
    for mode in ("incident", "internal", "cross"):
        for name, frames in (
            ("frame0", [0]),
            ("nonconsecutive", [4900, 1, 0]),
            ("all", None),
        ):
            atoms = list(range(62 if mode == "internal" else 16))
            stats, view = measure(
                lambda atoms=atoms, frames=frames, mode=mode: reused.query(
                    atom_indices=atoms, structure_indices=frames, mode=mode
                )
            )
            stats["count"] = view.n_interactions
            report["recurring_queries"][f"{mode}_{name}"] = stats
    # Reused relation with 50,001 parallel observations, independent of query setup.
    parallel = msm.Interactions(
        method="synthetic_parallel_probe",
        n_atoms=2,
        n_structures=1,
        evaluated_structure_indices=[0],
        relation_types=["pair"],
        relation_participant_offsets=[0, 2],
        participant_roles=["a", "b"],
        participant_atom_offsets=[0, 1, 2],
        participant_atoms=[0, 1],
        occurrence_structures=np.zeros(50001, dtype=np.int64),
        occurrence_relations=np.zeros(50001, dtype=np.int64),
        occurrence_evidence=np.zeros(50001, dtype=np.int32),
        evidence_labels=["synthetic"],
        measurements={"distance": np.full(50001, 0.2)},
        measure_units={"distance": "nm"},
    )
    view = parallel.query(structure_indices=[0])
    report["parallel_analysis_numeric_bytes"] = parallel.numeric_nbytes
    report["query_positions_bytes"] = view._positions.nbytes
    report["full_projection"], _ = measure(view.to_dict)
    if hasattr(view, "to_page"):
        report["one_row_page"], _ = measure(lambda: view.to_page(limit=1))
        report["fifty_row_page"], _ = measure(lambda: view.to_page(limit=50))
    options.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
