"""Benchmarking native topology construction and materialized storage."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

repo_root = str(Path(__file__).resolve().parents[2])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from benchmarks.harness import BenchmarkHarness, save_session_results
from benchmarks.micro.test_topology_expansion import _build_topology


def _dataframe_bytes(dataframe) -> int:
    return int(dataframe.memory_usage(index=True, deep=True).sum())


def _topology_bytes(topology) -> int:
    total = sum(
        _dataframe_bytes(table)
        for table in (
            topology.atoms,
            topology.groups,
            topology.molecules,
            topology.entities,
            topology.chains,
        )
    )
    for state in topology._chemical_states:
        total += int(state.component_indices.memory_usage(index=True, deep=True))
        total += _dataframe_bytes(state.atom_attributes)
        total += _dataframe_bytes(state.components)
        total += _dataframe_bytes(state.bonds)
    return total


def _measure_case(n_atoms: int) -> dict:
    topology = _build_topology(n_atoms=n_atoms)
    stable_bytes = _topology_bytes(topology)
    topology._set_chemical_state_atom_attribute(
        "formal_charge", np.zeros(n_atoms, dtype=np.int16)
    )
    with_formal_charge_bytes = _topology_bytes(topology)

    harness = BenchmarkHarness(
        name=f"topology_construction_{n_atoms}_atoms",
        iterations=3 if n_atoms >= 100_000 else 10,
        repeats=5,
    )
    result = harness.run(
        warmup_func=lambda: _build_topology(n_atoms=n_atoms),
        timed_func=lambda: _build_topology(n_atoms=n_atoms),
    )
    result["materialized_storage_bytes"] = stable_bytes
    result["bytes_per_atom"] = stable_bytes / n_atoms
    result["formal_charge_delta_bytes"] = with_formal_charge_bytes - stable_bytes
    result["formal_charge_delta_bytes_per_atom"] = (
        with_formal_charge_bytes - stable_bytes
    ) / n_atoms
    return result


def run_topology_storage_benchmarks(output_path=None):
    """Measuring representative construction costs and optional-state storage."""

    results = [_measure_case(n_atoms) for n_atoms in (1_000, 100_000)]
    if output_path is not None:
        save_session_results(
            session_name="micro-topology-storage",
            results=results,
            output_path=output_path,
        )
    return results


if __name__ == "__main__":
    output_file = os.path.join(
        repo_root,
        "benchmarks",
        "baselines",
        "topology_storage_session.json",
    )
    run_topology_storage_benchmarks(output_path=output_file)
