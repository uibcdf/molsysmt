"""
Contract and parity tests for networkx.Graph form.

Uses MolSysBuilder to declare a minimal system with fully known topology:
  - 4 atoms:  N (0), CA (1), C (2), O (3)
  - 2 bonds:  N-CA (0-1), CA-C (1-2)
  - 1 chain, 2 groups (ALA + HOH), 2 molecules

Contract: Topology → networkx.Graph produces a graph with the correct number
of nodes (atoms) and edges (bonds).

Parity: graph node/edge count and edge endpoints match the source Topology
exactly — the graph faithfully encodes the molecular topology.
"""

import pytest
import networkx as nx
import numpy as np
import pandas as pd
import molsysmt as msm
from molsysmt import pyunitwizard as puw

N_ATOMS = 4
N_BONDS = 2
BONDS = [(0, 1), (1, 2)]   # N-CA, CA-C


@pytest.fixture()
def builder_graph(builder_pdb_molsys):
    return msm.convert(builder_pdb_molsys, to_form='networkx.Graph')


@pytest.fixture()
def builder_topology(builder_pdb_molsys):
    return builder_pdb_molsys.topology


# ---------------------------------------------------------------------------
# Contract
# ---------------------------------------------------------------------------

def test_is_networkx_graph(builder_graph):
    assert isinstance(builder_graph, nx.Graph)


def test_node_count(builder_graph):
    assert builder_graph.number_of_nodes() == N_ATOMS


def test_edge_count(builder_graph):
    assert builder_graph.number_of_edges() == N_BONDS


def test_nodes_are_zero_indexed(builder_graph):
    assert set(builder_graph.nodes()) == set(range(N_ATOMS))


def test_declared_bonds_are_edges(builder_graph):
    for a1, a2 in BONDS:
        assert builder_graph.has_edge(a1, a2)


def test_unbonded_atom_is_isolated(builder_graph):
    # O (index 3) has no bonds in the declared system
    assert builder_graph.degree(3) == 0


def test_ca_has_degree_two(builder_graph):
    # CA (index 1) bonds to both N and C
    assert builder_graph.degree(1) == 2


def test_get_atom_indices(builder_graph):
    assert msm.get(builder_graph, element='atom', atom_index=True) == [0, 1, 2, 3]
    assert msm.get(
        builder_graph,
        element='atom',
        selection=[3, 1],
        atom_index=True,
    ) == [3, 1]


def test_get_connectivity(builder_graph):
    bond_indices, bonded_atoms = msm.get(
        builder_graph,
        element='atom',
        bond_index=True,
        bonded_atoms=True,
    )

    assert bond_indices == [[0], [0, 1], [1], []]
    assert bonded_atoms == [[1], [0, 2], [1], []]


def test_get_connectivity_from_system(builder_graph):
    bond_indices, bonded_atoms = msm.get(
        builder_graph,
        element='system',
        bond_index=True,
        bonded_atoms=True,
    )

    assert bond_indices == [0, 1]
    assert bonded_atoms == [0, 1, 2]


# ---------------------------------------------------------------------------
# Parity: graph ↔ topology
# ---------------------------------------------------------------------------

def test_parity_node_count_matches_topology(builder_graph, builder_topology):
    assert builder_graph.number_of_nodes() == builder_topology.n_atoms


def test_parity_edge_count_matches_topology(builder_graph, builder_topology):
    assert builder_graph.number_of_edges() == builder_topology.n_bonds


def test_parity_all_bonds_present_as_edges(builder_graph, builder_topology):
    bonds = builder_topology.bonds[['atom1_index', 'atom2_index']].to_numpy()
    for a1, a2 in bonds:
        assert builder_graph.has_edge(int(a1), int(a2))


def test_parity_no_extra_edges(builder_graph, builder_topology):
    topology_edges = {
        (int(min(a1, a2)), int(max(a1, a2)))
        for a1, a2 in builder_topology.bonds[['atom1_index', 'atom2_index']].to_numpy()
    }
    graph_edges = {(min(u, v), max(u, v)) for u, v in builder_graph.edges()}
    assert graph_edges == topology_edges


def test_canonical_graph_preserves_node_edge_and_state_metadata(builder_topology):
    builder_topology._set_chemical_state_atom_attribute(
        'formal_charge', pd.array([0, 1, -1, pd.NA], dtype='Int16')
    )
    bonds = builder_topology._get_chemical_state_bonds().copy()
    bonds['bond_order'] = pd.array([1, 2], dtype='UInt8')
    bonds['is_aromatic'] = pd.array([False, True], dtype='boolean')
    bonds['evidence'] = pd.array(['explicit', 'inferred'], dtype='string')
    builder_topology._set_chemical_state_bonds(bonds)
    builder_topology._reference_chemical_state.connectivity_completeness = 'partial'

    graph, report = msm.convert(
        builder_topology,
        to_form='networkx.Graph',
        return_report=True,
    )

    assert report.outcome == 'equivalent'
    assert report.issues == ()
    assert graph.graph['molsysmt_contract'] == 'canonical_attribute_graph_v1'
    assert graph.graph['connectivity_completeness'] == 'partial'
    assert graph.nodes[1]['formal_charge'] == 1
    assert graph.edges[1, 2]['bond_order'] == 2
    assert graph.edges[1, 2]['bond_is_aromatic'] is True
    assert graph.edges[1, 2]['bond_evidence'] == 'inferred'
    assert msm.get(graph, element='atom', formal_charge=True) == [0, 1, -1, None]
    assert msm.get(graph, element='bond', bond_order=True) == [1, 2]


def test_canonical_graph_supports_atom_subsets(builder_topology):
    graph = msm.convert(
        builder_topology,
        to_form='networkx.Graph',
        selection=[0, 1, 2],
    )

    assert list(graph.nodes) == [0, 1, 2]
    assert [graph.nodes[index]['atom_id'] for index in graph.nodes] == ['0', '1', '2']
    assert set(graph.edges) == {(0, 1), (1, 2)}
