"""Checking deterministic source-index partitions and chemical-state boundaries."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import Topology


def chain():
    topology = Topology(n_atoms=5)
    topology.bonds = pd.DataFrame(
        {
            "atom1_index": [0, 1, 2],
            "atom2_index": [1, 2, 3],
            "bond_type": ["covalent"] * 3,
        }
    )
    topology._chemical_states[0].connectivity_completeness = "complete"
    return topology


@pytest.mark.parametrize(
    "form",
    [
        "molsysmt.Topology",
        "molsysmt.MolSys",
        "molsysmt.ChemicalStates",
        "molsysmt.ChemicalStatesDict",
    ],
)
def test_partition_source_indices_isolates_and_form_agnostic_input(form):
    topology = chain()
    before = topology.bonds.copy()
    source = msm.convert(topology, to_form=form)
    report = msm.topology.get_rigid_fragments(source, bond_indices=[1, 1])
    np.testing.assert_array_equal(report["fragment_offsets"], [0, 2, 4, 5])
    np.testing.assert_array_equal(report["fragment_atom_indices"], [0, 1, 2, 3, 4])
    np.testing.assert_array_equal(report["atom_fragment_indices"], [0, 0, 1, 1, 2])
    np.testing.assert_array_equal(report["bond_indices"], [1])
    np.testing.assert_array_equal(report["bonded_atom_pairs"], [[1, 2]])
    np.testing.assert_array_equal(report["fragment_pairs"], [[0, 1]])
    pd.testing.assert_frame_equal(topology.bonds, before)


def test_no_cuts_and_empty_graph_have_defined_shapes():
    report = msm.topology.get_rigid_fragments(chain())
    np.testing.assert_array_equal(report["fragment_offsets"], [0, 4, 5])
    empty = msm.topology.get_rigid_fragments(Topology(n_atoms=0))
    assert empty["fragment_offsets"].tolist() == [0]
    assert empty["bonded_atom_pairs"].shape == empty["fragment_pairs"].shape == (0, 2)
    assert empty["atom_fragment_indices"].dtype == np.int64


@pytest.mark.parametrize("cuts", [[-1], [4], [[1]], [True], [0.5]])
def test_invalid_cut_axes_raise(cuts):
    with pytest.raises(ArgumentError):
        msm.topology.get_rigid_fragments(chain(), bond_indices=cuts)


def test_partial_graph_and_dative_cuts_fail():
    topology = chain()
    topology._chemical_states[0].connectivity_completeness = "partial"
    with pytest.raises(StructuralInconsistencyError, match="complete"):
        msm.topology.get_rigid_fragments(topology)
    topology._chemical_states[0].connectivity_completeness = "complete"
    bonds = topology.bonds.copy()
    bonds.loc[1, "bond_type"] = "dative"
    bonds.loc[1, "joins_components"] = False
    topology.bonds = bonds
    with pytest.raises(ArgumentError):
        msm.topology.get_rigid_fragments(topology, bond_indices=[1])


def test_multiple_ring_cuts_do_not_become_rotatable_bonds():
    topology = Topology(n_atoms=3)
    topology.bonds = pd.DataFrame(
        {
            "atom1_index": [0, 1, 0],
            "atom2_index": [1, 2, 2],
            "bond_type": ["covalent"] * 3,
        }
    )
    topology._chemical_states[0].connectivity_completeness = "complete"
    with pytest.raises(ArgumentError, match="bridge"):
        msm.topology.get_rigid_fragments(topology, bond_indices=[0, 1])
