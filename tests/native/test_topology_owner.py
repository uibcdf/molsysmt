"""Keep attached interaction snapshots consistent with controlled chemical edits."""

import copy
import gc
import pickle
import weakref

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from tests.form.molsysmt_MolSys.test_chemistry_edit_interactions import (
    ionic_system as ionic_system,
)


class _SlottedStates(msm.ChemicalStates):
    __slots__ = ("extra",)


class _ExternalTopology(msm.native.Topology):
    pass


@pytest.mark.parametrize(
    "operation", ["charge", "aromatic", "order", "add", "remove", "replace"]
)
def test_controlled_topology_edits_invalidate_owner_even_empty_coverage(
    ionic_system, operation
):
    system = ionic_system
    previous = system.interactions["ionic"]
    previous_view = previous.query(structure_indices=[0])
    if operation == "charge":
        msm.set(system.topology, selection=[0], formal_charge=[0])
    elif operation == "aromatic":
        msm.set(system.topology, selection=[3], atom_is_aromatic=[True])
    elif operation == "order":
        msm.set(system.topology, element="bond", bond_order=[2])
    elif operation == "add":
        system.topology.add_bonds([[0, 1]])
    elif operation == "remove":
        system.topology.remove_bonds([0])
    else:
        candidate = system.topology.bonds.copy()
        candidate["bond_order"] = pd.array([2], dtype="Int8")
        system.topology.bonds = candidate
    for analysis in system.interactions.values():
        assert analysis.evaluated_structure_indices.size == 0
        assert analysis.n_interactions == 0
        assert analysis.software == previous.software
        np.testing.assert_array_equal(
            analysis.atom_source_indices, previous.atom_source_indices
        )
    np.testing.assert_array_equal(previous.evaluated_structure_indices, [0, 1, 2])
    assert previous_view.n_interactions == 1


def test_bond_labels_and_empty_selections_preserve_analyses(ionic_system):
    system = ionic_system
    previous = system.interactions["ionic"]
    msm.set(system.topology, element="bond", bond_id=["007"])
    msm.set(system.topology, selection=[], atom_is_aromatic=[])
    msm.set(system.topology, element="bond", selection=[], bond_order=[])
    system.topology.add_bonds([])
    system.topology.remove_bonds([])
    assert system.interactions["ionic"] is previous
    assert system.topology.bonds["bond_id"].tolist() == ["007"]


@pytest.mark.parametrize("operation", ["atom", "bond", "add", "remove", "replace"])
def test_rejected_native_chemistry_keeps_tables_and_analyses(ionic_system, operation):
    system = ionic_system
    before_bonds = system.topology.bonds.copy()
    before_atoms = system.chemical_states._states[0].atom_attributes.copy()
    previous = system.interactions["ionic"]
    with pytest.raises(
        (ArgumentError, StructuralInconsistencyError, ValueError, IndexError, KeyError)
    ):
        if operation == "atom":
            msm.set(system.topology, selection=[3], n_implicit_hydrogens=[-1])
        elif operation == "bond":
            msm.set(system.topology, element="bond", bond_order=[-1])
        elif operation == "add":
            system.topology.add_bonds([[0, 0]])
        elif operation == "remove":
            system.topology.remove_bonds([99])
        else:
            system.topology.bonds = pd.DataFrame(
                {"atom1_index": [0], "atom2_index": [99]}
            )
    pd.testing.assert_frame_equal(system.topology.bonds, before_bonds)
    pd.testing.assert_frame_equal(
        system.chemical_states._states[0].atom_attributes, before_atoms
    )
    assert system.interactions["ionic"] is previous


@pytest.mark.parametrize("operation", ["atom", "bond", "remove"])
def test_invalidation_allocation_failure_does_not_publish_chemistry(
    ionic_system, operation, monkeypatch
):
    system = ionic_system
    before = system.topology.bonds.copy()
    atoms = system.chemical_states._states[0].atom_attributes.copy()
    previous = system.interactions["ionic"]

    def fail(*args, **kwargs):
        raise MemoryError("Cannot stage chemical invalidation")

    monkeypatch.setattr(msm.Interactions, "invalidate_structures", fail)
    with pytest.raises(MemoryError, match="chemical invalidation"):
        if operation == "atom":
            msm.set(system.topology, selection=[0], formal_charge=[0])
        elif operation == "bond":
            msm.set(system.topology, element="bond", bond_order=[2])
        else:
            system.topology.remove_bonds([0])
    pd.testing.assert_frame_equal(system.topology.bonds, before)
    pd.testing.assert_frame_equal(
        system.chemical_states._states[0].atom_attributes, atoms
    )
    assert system.interactions["ionic"] is previous


@pytest.mark.parametrize(
    "copier", [copy.copy, copy.deepcopy, lambda x: x.copy(deep=False)]
)
def test_standalone_topology_detaches_and_system_copy_notifies_only_its_owner(
    ionic_system, copier
):
    system = ionic_system
    isolated = (
        copier(system.topology)
        if copier in (copy.copy, copy.deepcopy)
        else system.topology.copy()
    )
    msm.set(isolated, selection=[0], formal_charge=[0])
    duplicate = copier(system)
    msm.set(duplicate.topology, selection=[0], formal_charge=[0])
    assert duplicate.interactions["ionic"].evaluated_structure_indices.size == 0
    np.testing.assert_array_equal(
        system.interactions["ionic"].evaluated_structure_indices, [0, 1, 2]
    )
    assert msm.get(system, selection=[0], formal_charge=True)[0] == 1


@pytest.mark.parametrize("route", ["pickle", "h5msm"])
def test_restored_topology_notifies_restored_owner(ionic_system, route, tmp_path):
    if route == "pickle":
        system = pickle.loads(pickle.dumps(ionic_system))
    else:
        path = str(tmp_path / "chemistry.h5msm")
        msm.convert(ionic_system, to_form=path)
        system = msm.convert(path, to_form="molsysmt.MolSys")
    msm.set(system.topology, selection=[0], formal_charge=[0])
    assert system.interactions["ionic"].evaluated_structure_indices.size == 0
    assert ionic_system.interactions["ionic"].n_interactions == 2


def test_public_system_delegation_invalidates_each_analysis_once(
    ionic_system, monkeypatch
):
    original = msm.Interactions.invalidate_structures
    calls = []

    def counted(self, structure_indices, **kwargs):
        calls.append(self)
        return original(self, structure_indices, **kwargs)

    monkeypatch.setattr(msm.Interactions, "invalidate_structures", counted)
    msm.set(ionic_system, selection=[0], formal_charge=[0])
    assert len(calls) == len(ionic_system.interactions)


def test_chemical_edit_does_not_copy_or_materialize_geometry(ionic_system, monkeypatch):
    from molsysmt.native._structure_array import _StructureArray

    coordinates = ionic_system.structures._coordinates

    def forbidden(*args, **kwargs):
        pytest.fail("Chemical owner publication touched protected coordinate payloads")

    monkeypatch.setattr(_StructureArray, "_dense", forbidden)
    monkeypatch.setattr(_StructureArray, "_fork", forbidden)
    msm.set(ionic_system.topology, selection=[0], formal_charge=[0])
    assert ionic_system.structures._coordinates is coordinates
    assert ionic_system.interactions["ionic"].evaluated_structure_indices.size == 0


@pytest.mark.parametrize(
    "value", [[[True, 1]], [[0.5, 1]], [["0", "1"]], [[0]], [0, 1]]
)
def test_native_bond_addition_rejects_noninteger_or_malformed_pairs(
    ionic_system, value
):
    previous = ionic_system.interactions["ionic"]
    with pytest.raises(ArgumentError):
        ionic_system.topology.add_bonds(value)
    assert ionic_system.topology.n_bonds == 1
    assert ionic_system.interactions["ionic"] is previous


@pytest.mark.parametrize("value", [True, [True], [0.5], ["0"], [[0]]])
def test_native_bond_removal_rejects_noninteger_or_nested_indices(ionic_system, value):
    previous = ionic_system.interactions["ionic"]
    with pytest.raises(ArgumentError):
        ionic_system.topology.remove_bonds(value)
    assert ionic_system.topology.n_bonds == 1
    assert ionic_system.interactions["ionic"] is previous


def test_component_membership_edit_notifies_owner(ionic_system):
    msm.set(ionic_system.topology, element="atom", selection=[3], component_index=[0])
    assert ionic_system.interactions["ionic"].evaluated_structure_indices.size == 0


def test_nonreference_state_edit_still_invalidates_all_owner_coverage(ionic_system):
    states = ionic_system.chemical_states
    states.append_state()
    with ionic_system.topology._using_chemical_state(1):
        msm.set(ionic_system.topology, selection=[0], formal_charge=[0])
    assert states._states[0].atom_attributes.loc[0, "formal_charge"] == 1
    assert states._states[1].atom_attributes.loc[0, "formal_charge"] == 0
    assert ionic_system.interactions["ionic"].evaluated_structure_indices.size == 0


def test_failed_private_atom_assignment_does_not_materialize_a_new_column(ionic_system):
    before = ionic_system.chemical_states._states[0].atom_attributes.copy()
    previous = ionic_system.interactions["ionic"]
    with pytest.raises(StructuralInconsistencyError):
        ionic_system.topology._set_chemical_state_atom_attribute(
            "n_implicit_hydrogens", [-1], atom_indices=[3]
        )
    pd.testing.assert_frame_equal(
        ionic_system.chemical_states._states[0].atom_attributes, before
    )
    assert ionic_system.interactions["ionic"] is previous


@pytest.mark.parametrize("operation", ["add", "remove"])
def test_component_rebuilding_failure_keeps_published_bonds_and_invalidated_analyses(
    ionic_system, operation, monkeypatch
):
    def fail(*args, **kwargs):
        raise RuntimeError("Component rebuilding failed after bond publication")

    monkeypatch.setattr(ionic_system.topology, "rebuild_components", fail)
    with pytest.raises(RuntimeError, match="after bond publication"):
        if operation == "add":
            ionic_system.topology.add_bonds([[0, 1]])
        else:
            ionic_system.topology.remove_bonds([0])
    assert ionic_system.topology.n_bonds == (2 if operation == "add" else 0)
    assert ionic_system.interactions["ionic"].evaluated_structure_indices.size == 0


def test_assigning_another_owners_chemistry_creates_an_independent_authority(
    ionic_system,
):
    other = ionic_system.copy(deep=False)
    source_states = ionic_system.chemical_states
    previous_states = other.chemical_states
    other.chemical_states = source_states
    assert other.chemical_states is not source_states
    assert other.topology._chemical_states_domain is other.chemical_states
    assert source_states._molsys_owner_ref() is ionic_system
    assert other.chemical_states._molsys_owner_ref() is other
    assert previous_states._molsys_owner_ref is None
    msm.set(other.topology, selection=[0], formal_charge=[0])
    assert msm.get(ionic_system, selection=[0], formal_charge=True)[0] == 1
    assert ionic_system.interactions["ionic"].evaluated_structure_indices.size == 3


@pytest.mark.parametrize(
    "copier", [copy.copy, copy.deepcopy, lambda x: pickle.loads(pickle.dumps(x))]
)
def test_standalone_chemical_states_do_not_retain_an_owner(ionic_system, copier):
    duplicate = copier(ionic_system.chemical_states)
    assert getattr(duplicate, "_molsys_owner_ref", None) is None
    assert ionic_system.chemical_states._molsys_owner_ref() is ionic_system


def test_retaining_chemical_states_does_not_retain_its_owner(ionic_system):
    system = ionic_system.copy(deep=False)
    states = system.chemical_states
    owner = weakref.ref(system)
    del system
    gc.collect()
    assert owner() is None
    assert states.n_atoms == 4


def test_partial_chemical_domain_owns_its_collection_independently(ionic_system):
    from molsysmt.native import MolSys

    partial = MolSys._from_partial_domains(chemical_states=ionic_system.chemical_states)
    assert partial.chemical_states is not ionic_system.chemical_states
    assert partial.chemical_states._molsys_owner_ref() is partial
    restored = pickle.loads(pickle.dumps(partial))
    assert restored.chemical_states._molsys_owner_ref() is restored


def test_chemical_state_pickle_preserves_subclass_slots_without_an_owner():
    states = _SlottedStates(n_atoms=2, skip_digestion=True)
    states.extra = {"values": [1]}
    restored = pickle.loads(pickle.dumps(states))
    assert type(restored) is _SlottedStates
    assert restored.extra == {"values": [1]}
    assert restored.extra is not states.extra


def test_inherited_native_bond_methods_preserve_their_validation_contract():
    topology = _ExternalTopology(n_atoms=3, skip_digestion=True)
    topology.add_bonds(((0, 1),))
    assert topology.n_bonds == 1
    with pytest.raises(ArgumentError):
        topology.add_bonds([[True, 2]])
    with pytest.raises(ArgumentError):
        topology.remove_bonds([0.5])
    topology.remove_bonds(np.int32(0))
    assert topology.n_bonds == 0
