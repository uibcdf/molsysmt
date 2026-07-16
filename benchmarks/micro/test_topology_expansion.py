"""Benchmarking direct topology gathers against the former merge pipeline."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

repo_root = str(Path(__file__).resolve().parents[2])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from benchmarks.harness import BenchmarkHarness, save_session_results
from molsysmt._private.topology_expansion import expand_atom_dataframe
from molsysmt.native import Topology


def _build_topology(n_atoms=100_000):
    n_groups = max(n_atoms // 10, 1)
    n_components = max(n_atoms // 1_000, 1)
    n_molecules = max(n_atoms // 100, 1)
    n_entities = 4
    n_chains = 8
    topology = Topology(
        n_atoms=n_atoms,
        n_groups=n_groups,
        n_components=n_components,
        n_molecules=n_molecules,
        n_entities=n_entities,
        n_chains=n_chains,
        skip_digestion=True,
    )

    topology.atoms['atom_name'] = np.where(np.arange(n_atoms) % 10 == 0, 'CA', 'C')
    topology.atoms['group_index'] = np.arange(n_atoms) // 10
    topology._set_component_indices(np.arange(n_atoms) % n_components)
    topology.atoms['chain_index'] = np.arange(n_atoms) % n_chains
    topology.groups['group_name'] = np.where(np.arange(n_groups) % 2 == 0, 'ALA', 'GLY')
    topology.groups['molecule_index'] = np.arange(n_groups) % n_molecules
    topology.components['component_type'] = 'component'
    topology.molecules['molecule_type'] = np.where(
        np.arange(n_molecules) % 2 == 0,
        'protein',
        'water',
    )
    topology.molecules['entity_index'] = np.arange(n_molecules) % n_entities
    topology.entities['entity_name'] = [f'entity {index}' for index in range(n_entities)]
    topology.chains['chain_name'] = [f'chain {index}' for index in range(n_chains)]
    return topology


def _direct_expansion(topology):
    return expand_atom_dataframe(
        topology,
        atom_columns=['atom_name', 'group_index', 'component_index', 'chain_index'],
        group_columns=['group_name', 'molecule_index'],
        component_columns=['component_type'],
        molecule_columns=['molecule_type', 'entity_index'],
        entity_columns=['entity_name'],
        chain_columns=['chain_name'],
    )


def _merge_expansion(topology):
    output = pd.merge(
        topology.molecules[['molecule_type', 'entity_index']],
        topology.entities[['entity_name']],
        left_on='entity_index',
        right_index=True,
    )
    output = pd.merge(
        topology.groups[['group_name', 'molecule_index']],
        output,
        left_on='molecule_index',
        right_index=True,
    )
    atoms = topology.atoms[['atom_name', 'group_index', 'chain_index']].copy()
    atoms['component_index'] = topology._get_component_indices().array
    atoms = atoms[['atom_name', 'group_index', 'component_index', 'chain_index']]
    output = pd.merge(
        atoms,
        output,
        left_on='group_index',
        right_index=True,
    )
    output = pd.merge(
        output,
        topology.components[['component_type']],
        left_on='component_index',
        right_index=True,
    )
    return pd.merge(
        output,
        topology.chains[['chain_name']],
        left_on='chain_index',
        right_index=True,
    )


def run_topology_expansion_benchmarks(output_path=None, n_atoms=100_000):
    """Measure direct gathering and merge expansion on the same topology."""

    topology = _build_topology(n_atoms=n_atoms)
    direct_output = _direct_expansion(topology)
    merge_output = _merge_expansion(topology)
    pd.testing.assert_frame_equal(direct_output, merge_output)

    direct_harness = BenchmarkHarness(
        name=f'topology_direct_gather_{n_atoms}_atoms',
        iterations=10,
        repeats=5,
    )
    merge_harness = BenchmarkHarness(
        name=f'topology_merge_expansion_{n_atoms}_atoms',
        iterations=10,
        repeats=5,
    )
    results = [
        direct_harness.run(
            warmup_func=lambda: _direct_expansion(topology),
            timed_func=lambda: _direct_expansion(topology),
        ),
        merge_harness.run(
            warmup_func=lambda: _merge_expansion(topology),
            timed_func=lambda: _merge_expansion(topology),
        ),
    ]

    if output_path is not None:
        save_session_results(
            session_name='micro-topology-expansion',
            results=results,
            output_path=output_path,
        )
    return results


if __name__ == '__main__':
    output_file = os.path.join(
        repo_root,
        'benchmarks',
        'baselines',
        'topology_expansion_session.json',
    )
    run_topology_expansion_benchmarks(output_path=output_file)
