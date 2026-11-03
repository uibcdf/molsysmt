"""Protect typed chemical assignment authority and scoped selected-state access."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import Topology
from tests.native import test_chemical_domain_separation as contract_fixtures
from tests.native.test_chemical_state_edits import _analysis

states = contract_fixtures.states
system = contract_fixtures.system


@pytest.mark.parametrize(
    "method,args",
    [
        ("_get_chemical_state_atom_attribute", ("formal_charge",)),
        ("_set_chemical_state_atom_attribute", ("formal_charge", [])),
        ("_remove_chemical_state_atom_attribute", ("formal_charge",)),
        ("_get_component_indices", ()),
        ("_set_component_indices", ([],)),
        ("_get_chemical_state_bonds", ()),
        ("_set_chemical_state_bond_attribute", ("bond_order", [])),
        ("_set_chemical_state_bond_stereo_atom_indices", ([],)),
        ("_set_chemical_state_bonds", (pd.DataFrame(),)),
    ],
)
def test_private_access_on_zero_states_does_not_invent_chemistry(method, args):
    collection = msm.ChemicalStates(n_atoms=3)
    with pytest.raises(StructuralInconsistencyError, match="unavailable"):
        getattr(collection, method)(*args)
    assert collection.n_chemical_states == 0
    assert collection.reference_chemical_state_index is None


def test_scoped_resolution_restores_on_failure_and_explicit_index_wins(states):
    states._set_reference_index(None)
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        states._get_component_indices()
    with states._using_chemical_state(1):
        assert states._get_component_indices().tolist() == [0, 0, 1]
        with pytest.raises(RuntimeError):
            with states._using_chemical_state(0):
                assert states._get_component_indices().tolist() == [0, 0, 0]
                raise RuntimeError("Abort inner workflow")
        assert states._get_component_indices().tolist() == [0, 0, 1]
        assert states._get_component_indices(state_index=0).tolist() == [0, 0, 0]
        with pytest.raises(StructuralInconsistencyError):
            with states._using_chemical_state(7):
                pytest.fail("Invalid scope was entered")
        assert states._get_component_indices().tolist() == [0, 0, 1]
    assert states.reference_chemical_state_index is None
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        states._get_chemical_state_bonds()


def test_scoped_resolution_is_collection_and_thread_local(states):
    other = states.copy()
    barrier = Barrier(2)

    def read(index):
        with states._using_chemical_state(index):
            barrier.wait(timeout=10)
            return len(states._get_chemical_state_bonds()), len(
                other._get_chemical_state_bonds()
            )

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert list(pool.map(read, [0, 1])) == [(2, 2), (1, 2)]
    assert states.reference_chemical_state_index == 0
    assert len(states._get_chemical_state_bonds()) == 2


def test_public_selected_state_resolution_uses_the_collection_context(
    system, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Public resolution entered the Topology state context")

    monkeypatch.setattr(
        system.topology, "_using_chemical_state", forbidden, raising=False
    )
    assert system.get(
        element="atom", selection=[2, 0], chemical_state=1, formal_charge=True
    ) == [0, 1]
    assert msm.get(
        system,
        element="atom",
        selection=[2, 0],
        chemical_state="structure",
        structure_indices=[3, 1, 3],
        formal_charge=True,
    ) == [0, 1]
    msm.set(system, element="atom", selection=[0], chemical_state=1, formal_charge=2)
    assert system.chemical_states._get_chemical_state_atom_attribute(
        "formal_charge", state_index=1
    ).tolist() == [2, -1, 0]
    assert system.chemical_states.reference_chemical_state_index == 0


def test_public_resolution_accepts_standalone_chemical_owners(states):
    assert states.get(n_atoms=True, chemical_state=1) == 3
    with pytest.raises(StructuralInconsistencyError):
        states.get(n_atoms=True, chemical_state=7)
    assert states.reference_chemical_state_index == 0


@pytest.mark.parametrize(
    "name,value,dtype",
    [
        ("formal_charge", 2, "Int16"),
        ("is_aromatic", True, "boolean"),
        ("n_unpaired_electrons", 1, "UInt8"),
        ("n_implicit_hydrogens", 2, "UInt8"),
        ("n_explicit_hydrogens", 1, "UInt8"),
        ("allows_implicit_hydrogens", False, "boolean"),
        ("stereochemistry", "R", "string"),
    ],
)
def test_atom_assignment_uses_chemical_owner_without_topology_or_legacy_repair(
    states, monkeypatch, name, value, dtype
):
    def forbidden(*args, **kwargs):
        pytest.fail("Chemical assignment traversed Topology or repaired storage")

    from molsysmt.native._chemical_state import _ChemicalStateStorage

    monkeypatch.setattr(Topology, "__init__", forbidden)
    monkeypatch.setattr(_ChemicalStateStorage, "_ensure_compatibility", forbidden)
    original = states._states[0].atom_attributes
    untouched = states._states[1].atom_attributes.copy(deep=True)
    states._set_chemical_state_atom_attribute(
        name, value, atom_indices=[2], state_index=1
    )
    column = states._get_chemical_state_atom_attribute(name, state_index=1)
    assert column.iloc[2] == value
    assert str(column.dtype) == dtype
    if name == "formal_charge":
        assert column.iloc[:2].tolist() == untouched[name].iloc[:2].tolist()
    else:
        assert column.iloc[:2].isna().all()
    assert states._states[0].atom_attributes is original
    assert states.reference_chemical_state_index == 0
    assert states._has_chemical_state_atom_attribute(name, state_index=1)
    states._remove_chemical_state_atom_attribute(name, state_index=1)
    assert not states._has_chemical_state_atom_attribute(
        name, state_index=1, include_none=True
    )
    assert column.iloc[2] == value


@pytest.mark.parametrize(
    "name,value,dtype",
    [
        ("bond_order", 2, "UInt8"),
        ("fractional_bond_order", 1.5, "Float64"),
        ("is_aromatic", True, "boolean"),
        ("is_conjugated", False, "boolean"),
        ("evidence", "explicit", "string"),
        ("bond_id", 19, "string"),
    ],
)
def test_bond_assignment_preserves_untouched_rows_and_metadata(
    states, name, value, dtype
):
    before = states.get_bonds(chemical_state=0)
    other = states.get_bonds(chemical_state=1)
    states._set_chemical_state_bond_attribute(
        name, value, bond_indices=[1], state_index=0
    )
    after = states.get_bonds(chemical_state=0)
    expected = "19" if name == "bond_id" else value
    assert after.loc[1, name] == expected
    assert str(after[name].dtype) == dtype
    if name in before:
        assert after.loc[0, name] == before.loc[0, name]
    else:
        assert pd.isna(after.loc[0, name])
    assert states.get_bonds(chemical_state=1) is other
    assert before is not after
    assert before.bond_order.tolist() == [1, 1]


def test_label_assignment_preserves_lossless_column_presence_and_row_positions(states):
    payload = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
    columns = payload.data["states"][0]["bonds"]["columns"]
    for column in columns.values():
        column["values"] = column["values"][::-1].copy()
        column["null_mask"] = column["null_mask"][::-1].copy()
    columns["is_aromatic"] = {
        "dtype": "boolean",
        "values": np.zeros(2, dtype=bool),
        "null_mask": np.ones(2, dtype=bool),
    }
    collection = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    before = collection.get_bonds(chemical_state=0)
    collection._set_chemical_state_bond_attribute("bond_id", "new", [1], state_index=0)
    after = collection.get_bonds(chemical_state=0)
    assert type(after) is type(before)
    pd.testing.assert_frame_equal(after.drop(columns="bond_id"), pd.DataFrame(before))
    assert after.bond_id.tolist()[1] == "new"
    assert after.is_aromatic.isna().all()
    assert "joins_components" not in after


@pytest.mark.parametrize("indices", [[0.5], [False], [True, 0], [[0]], -1, 2])
def test_private_bond_indices_reject_before_publishing(states, indices):
    before = states.get_bonds(chemical_state=0)
    with pytest.raises(StructuralInconsistencyError):
        states._set_chemical_state_bond_attribute(
            "bond_order", 2, indices, state_index=0
        )
    assert states.get_bonds(chemical_state=0) is before


@pytest.mark.parametrize(
    "operation", ["atom", "remove_attribute", "bond", "stereo", "component", "table"]
)
def test_assignment_invalidation_failure_keeps_every_state_field(
    system, monkeypatch, operation
):
    analysis = _analysis(system)
    collection = system.chemical_states
    state = collection._states[1]
    before = dict(vars(state))
    coordinates = system.structures._coordinates

    def failed(*args, **kwargs):
        raise MemoryError("Cannot stage assignment invalidation")

    monkeypatch.setattr(msm.Interactions, "invalidate_structures", failed)
    with pytest.raises(MemoryError, match="assignment invalidation"):
        if operation == "atom":
            collection._set_chemical_state_atom_attribute(
                "formal_charge", 2, [0], state_index=1
            )
        elif operation == "remove_attribute":
            collection._remove_chemical_state_atom_attribute(
                "formal_charge", state_index=1
            )
        elif operation == "bond":
            collection._set_chemical_state_bond_attribute(
                "bond_order", 2, state_index=1
            )
        elif operation == "stereo":
            collection._set_chemical_state_bond_stereo_atom_indices(
                [2, 0], state_index=1
            )
        elif operation == "component":
            collection._set_component_indices([0, 1, 1], state_index=1)
        else:
            table = state.bonds.copy()
            table["bond_order"] = pd.array([2], dtype="UInt8")
            collection._set_chemical_state_bonds(table, state_index=1)
    assert vars(state).keys() == before.keys()
    assert all(vars(state)[name] is value for name, value in before.items())
    assert system.interactions["control"] is analysis
    assert system.structures._coordinates is coordinates


def test_failed_atom_assignment_does_not_normalize_source_storage(system):
    collection = system.chemical_states
    state = collection._states[1]
    # A raw external write is not a supported edit. Validation must reject it
    # without a compatibility repair changing the source before the failure.
    state.atom_attributes["is_aromatic"] = ["invalid", "invalid", "invalid"]
    before = state.atom_attributes
    before_membership = state.component_indices
    with pytest.raises(StructuralInconsistencyError):
        collection._set_chemical_state_atom_attribute("formal_charge", 2, state_index=1)
    assert state.atom_attributes is before
    assert state.component_indices is before_membership
    assert state.atom_attributes.is_aromatic.tolist() == ["invalid"] * 3


def test_empty_bond_assignment_and_label_only_edit_retain_evaluated_empty_coverage(
    system,
):
    analysis = _analysis(system)
    collection = system.chemical_states
    with collection._using_chemical_state(1):
        original = collection._get_chemical_state_bonds()
        collection._set_chemical_state_bond_attribute("bond_order", [], [])
        assert collection._get_chemical_state_bonds() is original
        collection._set_chemical_state_bond_attribute("bond_id", 42)
    assert system.interactions["control"] is analysis
    assert collection.get_bonds(chemical_state=1).bond_id.tolist() == ["42"]
    collection._set_chemical_state_atom_attribute(
        "formal_charge", 2, [0], state_index=1
    )
    assert system.interactions["control"].evaluated_structure_indices.size == 0
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 2])
