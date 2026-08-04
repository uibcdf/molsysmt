"""Analytic graph truth tests for stable topology operations."""

import numpy as np
import pytest

import molsysmt as msm


@pytest.fixture(scope="module")
def branched_truth_system():
    """Build a seven-atom peptide-like path plus one isolated atom."""

    builder = msm.MolSysBuilder()
    names = ["C", "N", "CA", "C", "N", "CA", "C", "O"]
    atoms = [
        builder.add_atom(atom_name=name, atom_type=name)
        for name in names
    ]
    builder.add_group([atoms[0]], group_name="CAP")
    builder.add_group(atoms[1:4], group_name="ALA")
    builder.add_group(atoms[4:7], group_name="GLY")
    builder.add_group([atoms[7]], group_name="ION")
    for atom_1, atom_2 in zip(atoms[:6], atoms[1:7]):
        builder.add_bond(atom_1, atom_2)
    return builder.build()


def test_bondgraph_matches_explicit_nodes_and_edges(branched_truth_system):
    """Recover exactly the declared path graph and isolated node."""

    graph = msm.topology.get_bondgraph(branched_truth_system)

    assert set(graph.nodes) == set(range(8))
    assert {frozenset(edge) for edge in graph.edges} == {
        frozenset((index, index + 1)) for index in range(6)
    }


def test_covalent_blocks_match_closed_form_connected_components(branched_truth_system):
    """Identify the seven-node path and isolated atom as separate blocks."""

    blocks = msm.topology.get_covalent_blocks(branched_truth_system)

    assert {frozenset(block) for block in blocks} == {
        frozenset(range(7)),
        frozenset({7}),
    }


def test_covalent_paths_match_explicit_named_paths(branched_truth_system):
    """Find the two C-N-CA-C paths encoded in the synthetic graph."""

    chains = msm.topology.get_covalent_paths(
        branched_truth_system,
        path=[
            'atom_name=="C"',
            'atom_name=="N"',
            'atom_name=="CA"',
            'atom_name=="C"',
        ],
    )

    np.testing.assert_array_equal(chains, np.array([[0, 1, 2, 3], [3, 4, 5, 6]]))


def test_dihedral_quartets_match_explicit_phi_paths(branched_truth_system):
    """Translate the named phi convention into the two known graph quartets."""

    quartets = msm.topology.get_dihedral_quartets(branched_truth_system, phi=True)

    assert quartets == [[0, 1, 2, 3], [3, 4, 5, 6]]
