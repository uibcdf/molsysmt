"""Protect stable molecule ownership independently of a chemical partition."""

import copy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys, Topology


def _membership(topology):
    return topology.get(element="atom", molecule_index=True)


def test_unknown_membership_does_not_consult_chemistry(monkeypatch):
    topology = Topology(n_atoms=3)

    def forbidden(*args, **kwargs):
        pytest.fail("A stable molecule query consulted a chemical state")

    monkeypatch.setattr(topology, "_resolve_reference_chemical_state", forbidden)
    assert _membership(topology) == [None, None, None]
    assert topology._atom_molecule_membership is None


def test_declarations_are_nullable_positional_and_do_not_create_groups():
    topology = Topology(n_atoms=4, n_molecules=3)
    topology.molecules["molecule_id"] = ["m2", "m0", "m1"]
    topology.set_atom_molecules([2, None, 0, 2])
    assert _membership(topology) == [2, None, 0, 2]
    assert topology.get(element="atom", molecule_id=True) == ["m1", None, "m2", "m1"]
    assert topology.get(element="molecule", atom_index=True) == [[2], [], [0, 3]]
    assert topology.n_groups == 0
    assert topology._atom_molecule_membership.dtype == np.int64
    assert topology._atom_molecule_membership.nbytes == 4 * 8


def test_partial_assignment_preserves_others_and_clear_releases_optional_storage():
    topology = Topology(n_atoms=4, n_molecules=2)
    topology.set_atom_molecules([1, 0], atom_indices=[3, 1])
    assert _membership(topology) == [None, 0, None, 1]
    topology.set_atom_molecules(1, atom_indices=0)
    assert _membership(topology) == [1, 0, None, 1]
    topology.set_atom_molecules(None, atom_indices=[0, 1])
    assert _membership(topology) == [None, None, None, 1]
    topology.set_atom_molecules(None)
    assert _membership(topology) == [None] * 4
    assert topology._atom_molecule_membership is None


def test_grouped_and_ungrouped_owners_are_disjoint():
    topology = Topology(n_atoms=4, n_groups=1, n_molecules=2)
    topology.groups["molecule_index"] = pd.array([1], dtype="Int64")
    topology.atoms["group_index"] = pd.array([0, None, None, 0], dtype="Int64")
    topology.set_atom_molecules([1, 0, None, 1])
    assert _membership(topology) == [1, 0, None, 1]
    assert topology._atom_molecule_membership.tolist() == [-1, 0, -1, -1]
    before = topology._atom_molecule_membership
    with pytest.raises(StructuralInconsistencyError):
        topology.set_atom_molecules([0], atom_indices=[0])
    assert topology._atom_molecule_membership is before
    assert _membership(topology) == [1, 0, None, 1]


def test_explicit_group_reconciliation_preserves_agreed_owner():
    topology = Topology(n_atoms=2, n_groups=1, n_molecules=2)
    topology.set_atom_molecules([1, 0])
    topology.groups["molecule_index"] = pd.array([1], dtype="Int64")
    topology.atoms.loc[0, "group_index"] = 0
    with pytest.raises(StructuralInconsistencyError):
        _membership(topology)
    topology.set_atom_molecules([1], atom_indices=[0])
    assert _membership(topology) == [1, 0]
    assert topology._atom_molecule_membership.tolist() == [-1, 0]


@pytest.mark.parametrize(
    "values,indices",
    [
        ([True, 0], "all"),
        ([False, None], "all"),
        ([0.0, 1], "all"),
        ([0, -1], "all"),
        (["0", 1], "all"),
        ([[0], [1]], "all"),
        ([0], "all"),
        ([0, 1], [0, 0]),
        ([0], [0.5]),
        ([0], [True]),
        ([0], [-1]),
        ([0], [2]),
    ],
)
def test_invalid_assignment_is_rejected_before_publication(values, indices):
    topology = Topology(n_atoms=2, n_molecules=2)
    topology.set_atom_molecules([1, 1])
    before = topology._atom_molecule_membership
    with pytest.raises(ArgumentError):
        topology.set_atom_molecules(values, atom_indices=indices)
    assert topology._atom_molecule_membership is before
    assert _membership(topology) == [1, 1]


def test_labels_do_not_qualify_as_indices_and_unitful_assignments_are_rejected():
    topology = Topology(n_atoms=1, n_molecules=1)
    topology.molecules["molecule_id"] = ["9"]
    with pytest.raises(StructuralInconsistencyError):
        topology.set_atom_molecules([9])
    with pytest.raises(ArgumentError):
        topology.set_atom_molecules(msm.pyunitwizard.quantity([0], "nm"))
    assert topology._atom_molecule_membership is None


@pytest.mark.parametrize("copying", [copy.copy, copy.deepcopy, lambda x: x.copy()])
def test_copies_own_independent_membership(copying):
    topology = Topology(n_atoms=2, n_molecules=2)
    topology.set_atom_molecules([0, 1])
    clone = copying(topology)
    assert not np.shares_memory(
        clone._atom_molecule_membership, topology._atom_molecule_membership
    )
    clone.set_atom_molecules([1, 0])
    assert _membership(topology) == [0, 1]
    assert _membership(clone) == [1, 0]


def test_state_and_component_changes_cannot_redefine_molecule_ownership():
    system = MolSys(n_atoms=3, n_molecules=1)
    system.topology.set_atom_molecules([0, 0, 0])
    system.topology.add_bonds([[0, 1], [1, 2]])
    system.topology.remove_bonds([0])
    assert system.topology.n_components == 2
    assert _membership(system.topology) == [0, 0, 0]
    system.chemical_states.append_state()
    assert _membership(system.topology) == [0, 0, 0]


def test_extraction_remaps_declared_molecules_without_using_components():
    topology = Topology(n_atoms=4, n_molecules=3, n_entities=1)
    topology.molecules["molecule_id"] = ["a", "empty", "b"]
    topology.molecules["entity_index"] = pd.array([0, 0, 0], dtype="Int64")
    topology.set_atom_molecules([2, 0, 2, None])
    subset = topology.extract([0, 2, 3], copy_if_all=True)
    assert subset.molecules.molecule_id.tolist() == ["b"]
    assert _membership(subset) == [0, 0, None]
    assert subset.n_entities == 1
    assert _membership(topology) == [2, 0, 2, None]


def test_permutation_reorders_atoms_but_keeps_the_molecule_axis():
    system = MolSys(n_atoms=3, n_molecules=2)
    system.topology.molecules["molecule_id"] = ["first", "second"]
    system.topology.set_atom_molecules([0, 0, 1])
    permuted = msm.permute_atoms(system, atom_indices=[2, 0, 1])
    assert _membership(permuted.topology) == [1, 0, 0]
    assert permuted.topology.molecules.molecule_id.tolist() == ["first", "second"]
    assert _membership(system.topology) == [0, 0, 1]


def test_addition_offsets_molecule_positions_independently_of_labels():
    first = Topology(n_atoms=1, n_molecules=1)
    second = Topology(n_atoms=2, n_molecules=2)
    first.molecules["molecule_id"] = ["same"]
    second.molecules["molecule_id"] = ["same", "other"]
    first.set_atom_molecules([0])
    second.set_atom_molecules([1, 0])
    first.add(second)
    assert _membership(first) == [0, 2, 1]
    assert first.molecules.molecule_id.tolist() == ["same", "same", "other"]
    assert _membership(second) == [1, 0]


def test_declared_membership_participates_in_native_comparison():
    first = Topology(n_atoms=2, n_molecules=2)
    first.set_atom_molecules([0, 1])
    second = first.copy()
    second.set_atom_molecules([1, 0])
    assert not first.compare(second, molecule_index=True)
    assert first.compare(first, molecule_index=True, output_type="dictionary") == {
        "molecule_index": True
    }


@pytest.mark.parametrize("conversion", ["molsysmt.TopologyDict", "molsysmt.MolSysDict"])
def test_old_dictionary_schema_rejects_unrepresentable_membership(conversion):
    system = MolSys(n_atoms=3, n_molecules=2)
    system.topology.set_atom_molecules([1, None, 0])
    source = system.topology if conversion == "molsysmt.TopologyDict" else system
    with pytest.raises(ValueError, match="0.1 cannot preserve independent"):
        msm.convert(source, to_form=conversion)
    assert _membership(system.topology) == [1, None, 0]


def test_builder_retains_two_declared_molecules_when_their_components_merge():
    from rdkit import Chem

    source = msm.convert(Chem.MolFromSmiles("CC.CC"), to_form="molsysmt.MolSys")
    builder = msm.MolSysBuilder(source)
    builder.add_bond(1, 2, bond_order=1, bond_type="covalent")
    result = builder.build()
    assert result.topology.n_components == 1
    assert result.topology.n_molecules == 2
    assert _membership(result.topology) == [0, 0, 1, 1]
    assert _membership(source.topology) == [0, 0, 1, 1]


@pytest.mark.parametrize("failure", [False, True])
def test_controlled_membership_edits_stage_invalidation_without_copying_coordinates(
    failure, monkeypatch
):
    system = MolSys(n_atoms=2, n_molecules=2)
    system.structures.coordinates = msm.pyunitwizard.quantity(np.zeros((3, 2, 3)), "nm")
    original = msm.Interactions.from_records(
        [],
        n_atoms=2,
        n_structures=3,
        evaluated_structure_indices=[0, 2],
        method="ownership_control",
    )
    system.interactions = {"control": original}
    geometry = system.structures._coordinates
    if failure:

        def failed(*args, **kwargs):
            raise MemoryError("Cannot prepare invalidated analysis")

        monkeypatch.setattr(msm.Interactions, "invalidate_structures", failed)
        with pytest.raises(MemoryError, match="invalidated analysis"):
            system.topology.set_atom_molecules([0, 1])
        assert system.topology._atom_molecule_membership is None
        assert system.interactions["control"] is original
    else:
        system.topology.set_atom_molecules([0, 1])
        assert system.interactions["control"].evaluated_structure_indices.size == 0
        assert original.evaluated_structure_indices.tolist() == [0, 2]
        current = system.interactions["control"]
        system.topology.set_atom_molecules([0, 1])
        assert system.interactions["control"] is current
    assert system.structures._coordinates is geometry
