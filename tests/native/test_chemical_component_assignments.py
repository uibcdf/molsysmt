"""Protect declared component membership and exact metadata correspondence."""

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
    "attribute,values,expected",
    [
        ("component_id", [42, "001"], ["001", "42"]),
        ("component_name", ["tail", "head"], ["head", "tail"]),
        ("component_type", ["ion", "custom"], ["custom", "ion"]),
    ],
)
def test_labels_follow_selected_state_positions_and_leave_other_data_intact(
    states, attribute, values, expected
):
    other = states._states[0].components
    state = states._states[1]
    membership, bonds = state.component_indices, state.bonds
    declaration = (state.component_completeness, state.component_evidence)
    msm.set(states, selection=[1, 0], chemical_state=1, **{attribute: values})
    assert (
        states.get(element="component", chemical_state=1, **{attribute: True})
        == expected
    )
    assert states._states[0].components is other
    assert state.component_indices is membership
    assert state.bonds is bonds
    assert (state.component_completeness, state.component_evidence) == declaration
    assert states.reference_chemical_state_index == 0
    assert str(state.components[attribute].dtype) == "string"


@pytest.mark.parametrize(
    "attribute,value,expected",
    [
        ("component_id", 17, ["17", "17"]),
        ("component_name", "same", ["same", "same"]),
        ("component_type", None, [None, None]),
    ],
)
def test_component_label_broadcast_and_nulls_have_defined_shapes(
    states, attribute, value, expected
):
    msm.set(states, chemical_state=1, **{attribute: value})
    assert (
        states.get(element="component", chemical_state=1, **{attribute: True})
        == expected
    )


def test_atom_label_projection_updates_the_whole_component_and_rejects_conflicts(
    states,
):
    msm.set(
        states, element="atom", selection=[0], chemical_state=1, component_name="shared"
    )
    assert states.get(element="atom", chemical_state=1, component_name=True) == [
        "shared",
        "shared",
        "part-1",
    ]
    msm.set(
        states,
        element="atom",
        selection=[1, 0],
        chemical_state=1,
        component_id=[17, "17"],
    )
    assert states.get(element="component", chemical_state=1, component_id=True) == [
        "17",
        "split-1",
    ]
    before = states._states[1].components
    with pytest.raises(StructuralInconsistencyError, match="conflicting"):
        msm.set(
            states,
            element="atom",
            selection=[0, 1],
            chemical_state=1,
            component_name=["A", "B"],
        )
    assert states._states[1].components is before


def test_unknown_membership_cannot_project_a_label_to_another_row(states):
    wire = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
    wire.data["states"][1]["component_indices"]["null_mask"][1] = True
    states = msm.convert(wire, to_form="molsysmt.ChemicalStates")
    before = states._states[1].components
    with pytest.raises(
        StructuralInconsistencyError, match="known component membership"
    ):
        msm.set(
            states,
            element="atom",
            selection=[0, 1],
            chemical_state=1,
            component_name="wrong",
        )
    assert states._states[1].components is before
    assert states.get(element="atom", chemical_state=1, component_name=True) == [
        "part-0",
        None,
        "part-1",
    ]


@pytest.mark.parametrize(
    "values,expected,ids,names",
    [
        ([1, 1, 0], [1, 1, 0], ["split-1", "split-0"], ["part-1", "part-0"]),
        ([0, None, 1], [0, None, 1], [None, "split-1"], [None, "part-1"]),
        (0, [0, 0, 0], [None, None], [None, None]),
        (None, [None, None, None], [None, None], [None, None]),
    ],
)
def test_membership_retains_only_exact_full_atom_set_labels(
    states, values, expected, ids, names
):
    other = states._states[0].components
    bonds, attributes = states._states[1].bonds, states._states[1].atom_attributes
    msm.set(states, chemical_state=1, component_index=values)
    assert (
        states.get(element="atom", chemical_state=1, component_index=True) == expected
    )
    assert states.get(
        element="component", chemical_state=1, component_id=True, component_name=True
    ) == [ids, names]
    assert states.get(chemical_state=1, n_components=True, component_evidence=True) == [
        2,
        "user_defined",
    ]
    assert states.get(chemical_state=1, component_completeness=True) == (
        "unavailable" if values is None else "partial"
    )
    assert states._states[0].components is other
    assert states._states[1].bonds is bonds
    assert states._states[1].atom_attributes is attributes
    assert states.reference_chemical_state_index == 0


def test_membership_subset_order_and_reconstruction_remain_distinct(states):
    msm.set(states, selection=[2, 0], chemical_state=1, component_index=[None, 1])
    assert states.get(element="atom", chemical_state=1, component_index=True) == [
        1,
        0,
        None,
    ]
    assert states.get(chemical_state=1, n_components=True) == 2
    states.rebuild_components(True, True, False, False, chemical_state=1)
    assert states.get(element="atom", chemical_state=1, component_index=True) == [
        0,
        0,
        1,
    ]
    assert states.get(chemical_state=1, component_evidence=True) == "inferred"


@pytest.mark.parametrize(
    "value", [-1, 2, True, [False], [0.5], [[0]], "all", np.uint64(2**64 - 1)]
)
def test_invalid_membership_cannot_create_rows_or_change_source(states, value):
    before = dict(vars(states._states[1]))
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        msm.set(states, selection=[2], chemical_state=1, component_index=value)
    assert all(vars(states._states[1])[name] is old for name, old in before.items())


def test_state_local_bounds_and_private_explicit_state_do_not_follow_reference(states):
    with pytest.raises(StructuralInconsistencyError, match="existing rows"):
        msm.set(states, selection=[0], chemical_state=0, component_index=1)
    states._set_component_attribute(
        "component_name", "tail", indices=[1], state_index=1
    )
    assert states.get(element="component", chemical_state=1, component_name=True) == [
        "part-0",
        "tail",
    ]
    with pytest.raises(ArgumentError):
        msm.set(
            states,
            element="component",
            selection=[1],
            chemical_state=0,
            component_name="wrong",
        )


def test_no_state_or_component_inventory_is_created_implicitly():
    states = msm.ChemicalStates(n_atoms=2)
    with pytest.raises(StructuralInconsistencyError, match="unavailable"):
        msm.set(states, component_index=0)
    assert states.n_chemical_states == 0
    states.append_state()
    with pytest.raises(StructuralInconsistencyError, match="existing rows"):
        msm.set(states, component_index=0)
    assert states.get(n_components=True) == 0
    assert states.get(element="atom", component_index=True) == [None, None]


def test_identical_and_empty_membership_edits_preserve_coverage_and_declarations(
    system,
):
    analysis = _analysis(system)
    state = system.chemical_states._states[1]
    before = dict(vars(state))
    msm.set(system.chemical_states, chemical_state=1, component_index=[0, 0, 1])
    msm.set(system.chemical_states, selection=[], chemical_state=1, component_index=[])
    msm.set(
        system.chemical_states,
        element="component",
        selection=[],
        chemical_state=1,
        component_name=[],
    )
    assert all(vars(state)[name] is old for name, old in before.items())
    assert system.interactions["control"] is analysis


def test_membership_edit_invalidates_all_coverage_without_changing_coordinates(system):
    analysis = _analysis(system)
    coordinates = system.structures._coordinates
    association = system._structure_chemical_state_indices
    msm.set(
        system.chemical_states, selection=[2], chemical_state=1, component_index=None
    )
    assert system.interactions["control"].evaluated_structure_indices.size == 0
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 2])
    assert system.structures._coordinates is coordinates
    assert system._structure_chemical_state_indices is association


def test_label_edits_do_not_allocate_invalidation_or_copy_geometry(system, monkeypatch):
    analysis = _analysis(system)
    coordinates = system.structures._coordinates

    def forbidden(*args, **kwargs):
        pytest.fail("Label-only assignment entered scientific invalidation")

    monkeypatch.setattr(system, "_invalidating_interaction_frames", forbidden)
    msm.set(system.chemical_states, chemical_state=1, component_id=17)
    msm.set(system.chemical_states, chemical_state=1, component_type="custom")
    assert system.interactions["control"] is analysis
    assert system.structures._coordinates is coordinates


def test_failed_invalidation_does_not_publish_membership_or_metadata(
    system, monkeypatch
):
    analysis = _analysis(system)
    state = system.chemical_states._states[1]
    before = dict(vars(state))

    @contextmanager
    def failed(*args, **kwargs):
        raise MemoryError("Cannot stage membership invalidation")
        yield

    monkeypatch.setattr(system, "_invalidating_interaction_frames", failed)
    with pytest.raises(MemoryError, match="membership invalidation"):
        msm.set(
            system.chemical_states,
            selection=[2],
            chemical_state=1,
            component_index=None,
        )
    assert all(vars(state)[name] is old for name, old in before.items())
    assert system.interactions["control"] is analysis


def test_assignment_perceives_no_graph_and_constructs_no_topology(states, monkeypatch):
    from molsysmt.native._chemical_state import _ChemicalStateStorage

    def forbidden(*args, **kwargs):
        pytest.fail("Component declaration rebuilt a graph or Topology")

    monkeypatch.setattr(Topology, "__init__", forbidden)
    monkeypatch.setattr(_ChemicalStateStorage, "_ensure_compatibility", forbidden)
    monkeypatch.setattr(msm.ChemicalStates, "rebuild_components", forbidden)
    msm.set(states, chemical_state=1, component_index=[1, 1, 0])
    msm.set(states, chemical_state=1, component_name="declared")
    assert states.get(element="atom", chemical_state=1, component_index=True) == [
        1,
        1,
        0,
    ]


def test_component_edits_round_trip_without_claiming_complete_graph_evidence(
    states, tmp_path
):
    from molsysmt.native import MolSys

    msm.set(states, selection=[1], chemical_state=1, component_index=None)
    msm.set(
        states, element="component", selection=[0], chemical_state=1, component_id="001"
    )
    filename = tmp_path / "component-declaration.h5msm"
    msm.convert(
        MolSys._from_partial_domains(chemical_states=states), to_form=str(filename)
    )
    loaded = msm.convert(str(filename), to_form="molsysmt.MolSys").chemical_states
    assert loaded.get(element="atom", chemical_state=1, component_index=True) == [
        0,
        None,
        1,
    ]
    assert loaded.get(element="component", chemical_state=1, component_id=True) == [
        "001",
        "split-1",
    ]
    assert loaded.get(
        chemical_state=1, component_completeness=True, component_evidence=True
    ) == ["partial", "user_defined"]
    pd.testing.assert_frame_equal(
        loaded._states[0].components, states._states[0].components
    )


@pytest.mark.parametrize(
    "attribute,value",
    [
        ("component_id", True),
        ("component_id", 1.5),
        ("component_name", 7),
        ("component_type", [False]),
        ("component_index", [0, 1]),
    ],
)
def test_invalid_component_values_reject_before_publication(states, attribute, value):
    before = dict(vars(states._states[1]))
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        msm.set(states, chemical_state=1, **{attribute: value})
    assert all(vars(states._states[1])[name] is old for name, old in before.items())


@pytest.mark.parametrize("value", ["001", "all", "1 nm"])
def test_id_labels_retain_lexical_spelling_without_quantity_parsing(states, value):
    msm.set(
        states, element="component", selection=[1], chemical_state=1, component_id=value
    )
    assert states.get(element="component", chemical_state=1, component_id=True) == [
        "split-0",
        value,
    ]


@pytest.mark.parametrize(
    "attribute", ["component_id", "component_name", "component_type"]
)
def test_nullable_labels_accept_missing_scalars(states, attribute):
    msm.set(states, chemical_state=1, **{attribute: pd.NA})
    assert states.get(element="component", chemical_state=1, **{attribute: True}) == [
        None,
        None,
    ]


@pytest.mark.parametrize(
    "attribute", ["component_index", "component_id", "component_name"]
)
def test_unit_bearing_component_values_are_rejected(states, attribute):
    value = msm.pyunitwizard.quantity([0], "nm")
    before = dict(vars(states._states[1]))
    with pytest.raises(ArgumentError):
        msm.set(states, selection=[0], chemical_state=1, **{attribute: value})
    assert all(vars(states._states[1])[name] is old for name, old in before.items())


@pytest.mark.parametrize("selection", [[True, 0], [-1], [0.5], [[0]], [0, 0], None])
def test_component_label_write_positions_are_validated(states, selection):
    before = states._states[1].components
    with pytest.raises(ArgumentError):
        msm.set(
            states,
            element="component",
            selection=selection,
            chemical_state=1,
            component_name="wrong",
        )
    assert states._states[1].components is before


def test_zero_atoms_and_empty_edits_do_not_materialize_component_rows():
    states = msm.ChemicalStates(n_atoms=0)
    states.append_state()
    before = dict(vars(states._states[0]))
    msm.set(states, component_index=None)
    msm.set(states, component_name="unused")
    assert all(vars(states._states[0])[name] is old for name, old in before.items())


def test_declared_empty_rows_remain_addressable_as_rows(states):
    wire = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
    table = wire.data["states"][1]["components"]
    table["n_rows"] = 3
    for name, column in table["columns"].items():
        column["values"] = np.append(column["values"], "empty")
        column["null_mask"] = np.append(column["null_mask"], False)
    restored = msm.convert(wire, to_form="molsysmt.ChemicalStates")
    msm.set(
        restored,
        element="component",
        selection=[2],
        chemical_state=1,
        component_name="declared without atoms",
    )
    assert restored.get(
        element="component",
        selection=[2],
        chemical_state=1,
        atom_index=True,
        component_name=True,
    ) == [[[]], ["declared without atoms"]]


def test_small_atom_projected_label_edit_does_not_materialize_full_membership(states):
    import tracemalloc

    wire = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
    size = 1_000_000
    wire.data["n_atoms"] = size
    wire.data["states"] = wire.data["states"][:1]
    record = wire.data["states"][0]
    record["component_indices"] = {
        "dtype": "Int64",
        "values": np.zeros(size, dtype=np.int64),
        "null_mask": np.zeros(size, dtype=np.bool_),
    }
    record["atom_attributes"] = {"n_rows": size, "columns": {}}
    record["component_completeness"] = record["connectivity_completeness"] = "partial"
    states = msm.convert(wire, to_form="molsysmt.ChemicalStates")
    msm.set(states, element="atom", selection=[size - 1], component_name="warm")
    tracemalloc.start()
    try:
        msm.set(states, element="atom", selection=[size - 1], component_name="after")
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert states.get(element="component", component_name=True) == ["after"]
    assert peak < 1_000_000, f"Small label edit allocated {peak:,} bytes"
