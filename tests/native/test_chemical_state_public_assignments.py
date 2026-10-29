"""Assign public chemical fields through their selected native chemical owner."""

from contextlib import contextmanager

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import Topology
from tests.native import test_chemical_domain_separation as fixtures
from tests.native.test_chemical_state_edits import _analysis

states = fixtures.states
system = fixtures.system


@pytest.mark.parametrize(
    "attribute,value,expected,dtype",
    [
        ("formal_charge", [1, -1], [-1, -1, 1], "Int16"),
        ("atom_is_aromatic", [True, False], [False, None, True], "boolean"),
        ("n_unpaired_electrons", [1, 0], [0, None, 1], "UInt8"),
        ("n_implicit_hydrogens", [1, 2], [2, None, 1], "UInt8"),
        ("n_explicit_hydrogens", [1, 0], [0, None, 1], "UInt8"),
        ("allows_implicit_hydrogens", [False, True], [True, None, False], "boolean"),
        ("atom_stereochemistry", ["S", "R"], ["R", None, "S"], "string"),
    ],
)
def test_atom_assignment_preserves_requested_order_other_state_and_nullable_types(
    states, attribute, value, expected, dtype
):
    original = states._states[0].atom_attributes
    msm.set(states, selection=[2, 0], chemical_state=1, **{attribute: value})
    assert states.get(element="atom", chemical_state=1, **{attribute: True}) == expected
    column = {
        "atom_is_aromatic": "is_aromatic",
        "atom_stereochemistry": "stereochemistry",
    }.get(attribute, attribute)
    assert str(states._states[1].atom_attributes[column].dtype) == dtype
    assert states._states[0].atom_attributes is original
    assert states.reference_chemical_state_index == 0


@pytest.mark.parametrize(
    "attribute,value,expected",
    [
        ("bond_id", 17, "17"),
        ("bond_order", 2, 2),
        ("fractional_bond_order", 1.5, 1.5),
        ("bond_type", "dative", "dative"),
        ("bond_is_aromatic", True, True),
        ("bond_is_conjugated", False, False),
        ("bond_stereochemistry", "E", "E"),
        ("bond_stereo_atom_indices", [[2, 0]], [2, 0]),
        ("bond_donor_atom_index", 0, 0),
        ("bond_acceptor_atom_index", 1, 1),
        ("bond_joins_components", False, False),
        ("bond_evidence", "user_defined", "user_defined"),
    ],
)
def test_each_public_bond_field_uses_the_selected_state(
    states, attribute, value, expected
):
    before = states.get_bonds(chemical_state=0)
    msm.set(states, element="bond", chemical_state=1, bond_evidence="explicit")
    if attribute == "bond_stereochemistry":
        msm.set(
            states, element="bond", chemical_state=1, bond_stereo_atom_indices=[2, 0]
        )
    msm.set(
        states, element="bond", selection=[0], chemical_state=1, **{attribute: value}
    )
    assert states.get(element="bond", chemical_state=1, **{attribute: True}) == [
        expected
    ]
    assert states.get_bonds(chemical_state=0) is before
    assert states.reference_chemical_state_index == 0


@pytest.mark.parametrize(
    "attribute",
    [
        "formal_charge",
        "atom_is_aromatic",
        "n_unpaired_electrons",
        "n_implicit_hydrogens",
        "n_explicit_hydrogens",
        "allows_implicit_hydrogens",
        "atom_stereochemistry",
    ],
)
def test_none_assigns_unknown_without_creating_another_state(states, attribute):
    msm.set(states, selection=[0], chemical_state=1, **{attribute: None})
    result = states.get(element="atom", chemical_state=1, **{attribute: True})
    assert result[0] is None
    assert len(result) == 3
    assert states.n_chemical_states == 2


@pytest.mark.parametrize(
    "element,attribute,value", [("atom", "formal_charge", 1), ("bond", "bond_order", 1)]
)
def test_missing_state_rejects_even_empty_edits_without_creating_a_state(
    element, attribute, value
):
    states = msm.ChemicalStates(n_atoms=3)
    with pytest.raises(StructuralInconsistencyError, match="unavailable"):
        msm.set(states, element=element, selection=[], **{attribute: value})
    assert states.n_chemical_states == 0


@pytest.mark.parametrize("selection", [[True, 0], [-1], [0.5], [[0]], [0, 0], None])
@pytest.mark.parametrize(
    "element,attribute", [("atom", "formal_charge"), ("bond", "bond_order")]
)
def test_malformed_positions_reject_before_publication(
    states, selection, element, attribute
):
    state = states._states[1]
    before = dict(vars(state))
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        msm.set(
            states,
            element=element,
            selection=selection,
            chemical_state=1,
            **{attribute: 1},
        )
    assert all(vars(state)[key] is value for key, value in before.items())


@pytest.mark.parametrize(
    "value", [True, [True], [40000], [-40000], [np.uint64(2**64 - 1)]]
)
def test_formal_charges_reject_booleans_and_integer_overflow(states, value):
    before = states._states[1].atom_attributes
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        msm.set(states, selection=[0], chemical_state=1, formal_charge=value)
    assert states._states[1].atom_attributes is before


@pytest.mark.parametrize(
    "standard_units", [["elementary_charge", "nm"], ["coulomb", "angstrom"]]
)
def test_charge_quantity_is_converted_explicitly_to_elementary_charge(
    states, standard_units
):
    puw = msm.pyunitwizard
    value = puw.convert(puw.quantity([1, -1], "elementary_charge"), to_unit="coulomb")
    with puw.context(standard_units=standard_units):
        msm.set(states, selection=[2, 0], chemical_state=1, formal_charge=value)
    assert states.get(element="atom", chemical_state=1, formal_charge=True) == [
        -1,
        -1,
        1,
    ]


@pytest.mark.parametrize(
    "element,attribute,value",
    [
        ("atom", "formal_charge", [1, 2]),
        ("atom", "n_implicit_hydrogens", 256),
        ("atom", "n_unpaired_electrons", True),
        ("atom", "atom_stereochemistry", "Z"),
        ("bond", "bond_donor_atom_index", 2),
        ("bond", "bond_stereochemistry", "E"),
        ("bond", "bond_stereo_atom_indices", [[0, 1, 2]]),
    ],
)
def test_invalid_values_preserve_source_and_evaluated_empty_coverage(
    system, element, attribute, value
):
    analysis = _analysis(system)
    state = system.chemical_states._states[1]
    before = dict(vars(state))
    geometry = system.structures._coordinates
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        msm.set(
            system.chemical_states,
            element=element,
            selection=[0],
            chemical_state=1,
            **{attribute: value},
        )
    assert all(vars(state)[key] is old for key, old in before.items())
    assert system.interactions["control"] is analysis
    assert system.structures._coordinates is geometry


def test_scientific_alias_assignment_invalidates_all_coverage_without_geometry_copy(
    system,
):
    analysis = _analysis(system)
    coordinates = system.structures._coordinates
    association = system._structure_chemical_state_indices
    msm.set(system.chemical_states, selection=[2], chemical_state=1, formal_charge=2)
    assert system.interactions["control"].evaluated_structure_indices.size == 0
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 2])
    assert system.structures._coordinates is coordinates
    assert system._structure_chemical_state_indices is association


def test_empty_assignment_and_bond_labels_preserve_observations(system):
    analysis = _analysis(system)
    before = system.chemical_states.get_bonds(chemical_state=1)
    msm.set(
        system.chemical_states,
        element="bond",
        selection=[],
        chemical_state=1,
        bond_order=2,
    )
    msm.set(system.chemical_states, selection=[], chemical_state=1, formal_charge=1)
    assert system.chemical_states.get_bonds(chemical_state=1) is before
    msm.set(system.chemical_states, element="bond", chemical_state=1, bond_id=42)
    assert system.interactions["control"] is analysis
    assert system.chemical_states.get(
        element="bond", chemical_state=1, bond_id=True
    ) == ["42"]


def test_invalidation_failure_does_not_publish_assignment(system, monkeypatch):
    analysis = _analysis(system)
    state = system.chemical_states._states[1]
    before = dict(vars(state))

    @contextmanager
    def failed(*args, **kwargs):
        raise MemoryError("Cannot allocate assignment invalidation")
        yield

    monkeypatch.setattr(system, "_invalidating_interaction_frames", failed)
    with pytest.raises(MemoryError, match="assignment invalidation"):
        msm.set(system.chemical_states, chemical_state=1, formal_charge=2)
    assert all(vars(state)[key] is old for key, old in before.items())
    assert system.interactions["control"] is analysis


def test_assignment_needs_no_topology_or_storage_repair(states, monkeypatch):
    from molsysmt.native._chemical_state import _ChemicalStateStorage

    def forbidden(*args, **kwargs):
        pytest.fail("Chemical assignment reconstructed Topology or repaired storage")

    monkeypatch.setattr(Topology, "__init__", forbidden)
    monkeypatch.setattr(_ChemicalStateStorage, "_ensure_compatibility", forbidden)
    msm.set(states, selection=[2], chemical_state=1, formal_charge=2)
    assert states.get(chemical_state=1, formal_charge=True) == [1, -1, 2]


def test_assignments_survive_h5msm_and_restore_state_scope_after_failure(
    states, tmp_path
):
    from molsysmt.native import MolSys

    states._set_reference_index(None)
    msm.set(states, chemical_state=1, atom_is_aromatic=[False, None, True])
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        msm.set(states, formal_charge=1)
    target = tmp_path / "assigned.h5msm"
    msm.convert(
        MolSys._from_partial_domains(chemical_states=states), to_form=str(target)
    )
    restored = msm.convert(str(target), to_form="molsysmt.MolSys").chemical_states
    assert restored.reference_chemical_state_index is None
    assert restored.get(element="atom", chemical_state=1, atom_is_aromatic=True) == [
        False,
        None,
        True,
    ]
    pd.testing.assert_frame_equal(
        restored._states[0].atom_attributes, states._states[0].atom_attributes
    )


def test_label_assignment_cannot_promote_unknown_connectivity_or_invalidate(system):
    wire = msm.convert(system.chemical_states, to_form="molsysmt.ChemicalStatesDict")
    wire.data["states"][1]["connectivity_completeness"] = "unavailable"
    system.chemical_states = msm.convert(wire, to_form="molsysmt.ChemicalStates")
    analysis = _analysis(system)
    msm.set(system.chemical_states, element="bond", chemical_state=1, bond_id="label")
    assert (
        system.chemical_states.get(chemical_state=1, connectivity_completeness=True)
        == "unavailable"
    )
    assert system.interactions["control"] is analysis


def test_participation_assignment_keeps_explicit_reconstruction_separate(states):
    msm.set(states, element="bond", chemical_state=1, bond_evidence="user_defined")
    msm.set(states, element="bond", chemical_state=1, bond_joins_components=False)
    assert states.get(chemical_state=1, n_components=True) == 2
    states.rebuild_components(True, True, False, False, chemical_state=1)
    assert states.get(chemical_state=1, n_components=True) == 3


@pytest.mark.parametrize("kind", ["fractional", "length", "nonfinite"])
def test_invalid_charge_quantities_reject_before_publication(states, kind):
    puw = msm.pyunitwizard
    value = {
        "fractional": puw.quantity([0.5], "elementary_charge"),
        "length": puw.quantity([1.0], "nm"),
        "nonfinite": puw.quantity([float("nan")], "elementary_charge"),
    }[kind]
    before = states._states[1].atom_attributes
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        msm.set(states, selection=[0], chemical_state=1, formal_charge=value)
    assert states._states[1].atom_attributes is before
