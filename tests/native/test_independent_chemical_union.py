"""Literal chemical-union guards before coordinated molecular publication."""

from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Topology
from molsysmt.native._chemical_merge import union
from tests.native import test_chemical_domain_separation as fixtures

states = fixtures.states


def sources(states):
    left, right = states.copy(), states.copy()
    left._replace_states([left._states[0]], 0)
    right._replace_states([right._states[1]], 0)
    topology = Topology(n_atoms=6, n_molecules=2)
    topology.set_atom_molecules([0, 0, 0, 1, 1, 1])
    return left, right, topology


@pytest.mark.parametrize(
    "participates,expected",
    [
        (True, [0, 0, 0, 1, 1, 2]),
        (False, [0, 0, 0, 1, 2, 3]),
    ],
)
def test_union_offsets_all_chemical_references_and_retains_stable_molecules(
    states, participates, expected
):
    left, right, topology = sources(states)
    msm.set(right, element="bond", bond_evidence="explicit")
    msm.set(
        right,
        element="bond",
        bond_joins_components=participates,
        bond_donor_atom_index=0,
        bond_acceptor_atom_index=1,
        bond_stereo_atom_indices=[2, 0],
    )
    original_left = left.get_bonds()
    original_right = right.get_bonds()
    result = union(left, right, "all", topology, True)
    assert result.get(n_atoms=True, n_bonds=True) == [6, 3]
    assert result.get(bonded_atom_pairs=True) == [[0, 1], [1, 2], [3, 4]]
    assert result.get(formal_charge=True) == [0, 0, 0, 1, -1, 0]
    assert result.get(element="atom", component_index=True) == expected
    assert result.get(
        element="bond",
        selection=[2],
        bond_donor_atom_index=True,
        bond_acceptor_atom_index=True,
        bond_stereo_atom_indices=True,
    ) == [[3], [4], [[5, 3]]]
    assert topology.get(element="atom", molecule_index=True) == [0, 0, 0, 1, 1, 1]
    assert topology.n_molecules == 2
    assert left.get_bonds() is original_left and right.get_bonds() is original_right
    assert right.get(element="bond", bond_stereo_atom_indices=True) == [[2, 0]]


def test_union_uses_the_selected_induced_source_domain(states):
    left, right, topology = sources(states)
    topology = Topology(n_atoms=5)
    result = union(left, right, [2, 0], topology, True)
    assert result.get(bonded_atom_pairs=True) == [[0, 1], [1, 2]]
    assert result.get(formal_charge=True) == [0, 0, 0, 0, 1]
    assert right.n_atoms == 3


@pytest.mark.parametrize("missing", ["absent", "zero", "multiple"])
def test_unsupported_state_alignment_is_rejected_without_source_changes(
    states, missing
):
    left, right, topology = sources(states)
    right = (
        None
        if missing == "absent"
        else msm.ChemicalStates(n_atoms=3)
        if missing == "zero"
        else states
    )
    original = deepcopy(left.get_bonds())
    with pytest.raises(msm.StructuralInconsistencyError, match="alignment"):
        union(left, right, "all", topology, True)
    assert np.array_equal(
        left.get_bonds()[["atom1_index", "atom2_index"]],
        original[["atom1_index", "atom2_index"]],
    )


def test_reconstruction_failure_does_not_publish_into_either_source(
    states, monkeypatch
):
    left, right, topology = sources(states)
    before = left._states[0], right._states[0]

    def fail(*args, **kwargs):
        raise MemoryError("injected union reconstruction failure")

    monkeypatch.setattr(msm.ChemicalStates, "rebuild_components", fail)
    with pytest.raises(MemoryError, match="injected"):
        union(left, right, "all", topology, True)
    assert (left._states[0], right._states[0]) == before
    assert left.get_bonds().shape[0] == 2 and right.get_bonds().shape[0] == 1


def molecular_sources(states):
    from molsysmt import pyunitwizard as puw
    from molsysmt.native import MolSys, Structures

    left, right, _ = sources(states)
    result = []
    for chemistry in (left, right):
        topology = Topology(n_atoms=3, n_molecules=1)
        topology.set_atom_molecules([0, 0, 0])
        result.append(
            MolSys._from_partial_domains(
                topology=topology,
                chemical_states=chemistry,
                structures=Structures(
                    coordinates=puw.quantity(np.zeros((4, 3, 3)), "nm")
                ),
            )
        )
    return result


def test_molecular_union_publishes_all_independent_axes_together(states):
    left, right = molecular_sources(states)
    original = right.chemical_states.get_bonds()
    left.add(right)
    assert left.get(n_atoms=True, n_bonds=True, n_molecules=True) == [6, 3, 2]
    assert left.get(formal_charge=True) == [0, 0, 0, 1, -1, 0]
    assert left.structures.coordinates.shape == (4, 6, 3)
    assert right.chemical_states.get_bonds() is original
    assert right.get(n_atoms=True, n_bonds=True) == [3, 1]
    for domain in (left.topology, left.chemical_states, left.structures):
        assert domain._molsys_owner_ref() is left


def test_molecular_union_rejects_state_alignment_before_publication(states):
    left, right = molecular_sources(states)
    right.chemical_states.append_state()
    before = left.topology, left.chemical_states, left.structures
    with pytest.raises(msm.StructuralInconsistencyError, match="alignment"):
        left.add(right)
    assert (left.topology, left.chemical_states, left.structures) == before
    assert left.get(n_atoms=True, n_bonds=True) == [3, 2]


def test_molecular_union_allocation_failure_preserves_domains(states, monkeypatch):
    from molsysmt.native import Structures

    left, right = molecular_sources(states)
    before = left.topology, left.chemical_states, left.structures
    calls = []
    copy = Structures.copy

    def copying(self, deep=True, **kwargs):
        calls.append(deep)
        return copy(self, deep=deep, **kwargs)

    def fail(*args, **kwargs):
        raise MemoryError("injected structure union failure")

    monkeypatch.setattr(Structures, "copy", copying)
    monkeypatch.setattr(Structures, "add", fail)
    with pytest.raises(MemoryError, match="injected"):
        left.add(right)
    assert calls == [False]
    assert (left.topology, left.chemical_states, left.structures) == before
