"""Check chemical-axis queries against independent analytical state records."""

from functools import partial

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    NotWithThisFormError,
    StructuralInconsistencyError,
)
from molsysmt.native import Topology
from tests.native import test_chemical_domain_separation as contract_fixtures

states = contract_fixtures.states


@pytest.fixture(params=["native", "universal"])
def query(states, request):
    return states.get if request.param == "native" else partial(msm.get, states)


def test_selected_counts_and_collection_inventory_have_distinct_scopes(query, states):
    assert query(
        chemical_state=1,
        n_bonds=True,
        n_components=True,
        chemical_state_index=True,
        chemical_state_id=True,
        reference_chemical_state_index=True,
        connectivity_completeness=True,
        component_evidence=True,
        output_type="dictionary",
    ) == {
        "n_bonds": 1,
        "n_components": 2,
        "chemical_state_index": [0, 1],
        "chemical_state_id": ["path", "split"],
        "reference_chemical_state_index": 0,
        "connectivity_completeness": "complete",
        "component_evidence": "explicit",
    }
    assert states.reference_chemical_state_index == 0


@pytest.mark.parametrize(
    "element,state_index,selection,attribute,expected",
    [
        ("atom", 1, [2, 0, 2], "atom_index", [2, 0, 2]),
        ("atom", 1, [2, 0, 2], "component_index", [1, 0, 1]),
        ("atom", 0, [2, 0, 2], "bond_index", [[1], [0], [1]]),
        ("atom", 1, [2, 0, 2], "bond_index", [[], [0], []]),
        ("atom", 0, [1, 0, 1], "n_bonds", [2, 1, 2]),
        ("atom", 1, [1, 0, 1], "n_bonds", [1, 1, 1]),
        ("bond", 0, [1, 0, 1], "bond_index", [1, 0, 1]),
        ("component", 1, [1, 0, 1], "component_index", [1, 0, 1]),
        ("component", 1, [1, 0, 1], "atom_index", [[2], [0, 1], [2]]),
        ("component", 1, [1, 0, 1], "n_atoms", [1, 2, 1]),
        ("component", 1, [1, 0, 1], "n_bonds", [0, 1, 0]),
        ("component", 0, [0], "n_bonds", [2]),
        ("atom", 1, [2, 0, 2], "n_components", 2),
        ("atom", 0, [2, 0, 2], "n_components", 1),
    ],
)
def test_indices_projections_and_counts_preserve_selection_meaning(
    query, element, state_index, selection, attribute, expected
):
    assert (
        query(
            element=element,
            selection=selection,
            chemical_state=state_index,
            **{attribute: True},
        )
        == expected
    )


@pytest.mark.parametrize(
    "element,attribute", [("bond", "bond_index"), ("component", "component_index")]
)
def test_bounds_are_resolved_in_the_requested_state(query, element, attribute):
    valid_state = 0 if element == "bond" else 1
    assert query(
        element=element, selection=[1], chemical_state=valid_state, **{attribute: True}
    ) == [1]
    with pytest.raises(ArgumentError):
        query(
            element=element,
            selection=[1],
            chemical_state=1 - valid_state,
            **{attribute: True},
        )


@pytest.mark.parametrize("element", ["atom", "bond", "component"])
@pytest.mark.parametrize(
    "selection", [[True, 0], [np.bool_(False), 1], [0.5], [-1], [[0]]]
)
def test_malformed_indices_reject_instead_of_becoming_positions(
    query, element, selection
):
    with pytest.raises(ArgumentError):
        query(
            element=element,
            selection=selection,
            chemical_state=1,
            **{element + "_index": True},
        )


def test_masks_use_the_selected_state_axis_and_keep_set_semantics(query):
    assert query(
        element="bond",
        selection=[1, 0, 1],
        mask=[False, True],
        chemical_state=0,
        bond_index=True,
    ) == [1]
    with pytest.raises(ArgumentError):
        query(element="bond", mask=[False, True], chemical_state=1, bond_index=True)
    assert query(
        element="component",
        selection=[1, 0, 1],
        mask=[1],
        chemical_state=1,
        component_index=True,
    ) == [1]


@pytest.mark.parametrize(
    "element,attribute,expected",
    [
        ("atom", "atom_index", []),
        ("atom", "component_index", []),
        ("atom", "n_bonds", []),
        ("atom", "n_components", 0),
        ("bond", "bond_index", []),
        ("component", "component_index", []),
        ("component", "atom_index", []),
        ("component", "n_atoms", []),
        ("component", "n_bonds", []),
    ],
)
def test_empty_selection_shapes_are_defined(query, element, attribute, expected):
    assert (
        query(element=element, selection=[], chemical_state=1, **{attribute: True})
        == expected
    )


def test_ambiguous_reference_does_not_hide_collection_inventory_or_choose_zero(states):
    states._set_reference_index(None)
    assert states.get(chemical_state_index=True, chemical_state_id=True) == [
        [0, 1],
        ["path", "split"],
    ]
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        states.get(n_bonds=True)
    assert states.get(chemical_state=1, n_bonds=True) == 1
    with pytest.raises(StructuralInconsistencyError):
        states.get(chemical_state=9, n_bonds=True)
    assert states.reference_chemical_state_index is None


def test_zero_states_retain_an_atom_domain_without_chemical_counts():
    states = msm.ChemicalStates(n_atoms=3)
    assert states.get(element="atom", selection=[2, 0], atom_index=True) == [2, 0]
    assert states.get(
        n_atoms=True, n_chemical_states=True, chemical_state_index=True
    ) == [3, 0, []]
    assert not msm.has_attribute(states, "n_bonds")
    assert msm.has_attribute(states, "n_bonds", include_none=True)
    with pytest.raises(StructuralInconsistencyError, match="unavailable"):
        states.get(n_bonds=True)
    assert states.n_chemical_states == 0


def test_unknown_membership_and_connectivity_are_read_without_inference():
    states = msm.ChemicalStates(n_atoms=3)
    states.append_state()
    assert states.get(element="atom", component_index=True, n_bonds=True) == [
        [None] * 3,
        [0] * 3,
    ]
    assert states.get(
        n_bonds=True,
        n_components=True,
        connectivity_completeness=True,
        component_completeness=True,
    ) == [0, 0, "unavailable", "unavailable"]
    assert states.get(n_groups=True, n_molecules=True, coordinates=True) == [
        None,
        None,
        None,
    ]
    assert not msm.has_attribute(states, "component_index")
    assert msm.has_attribute(states, "component_index", include_none=True)


def test_native_numeric_queries_need_no_universal_dispatch_or_topology(
    states, monkeypatch
):
    from molsysmt.native._chemical_state import _ChemicalStateStorage

    def forbidden(*args, **kwargs):
        pytest.fail("Native query entered discovery, conversion, repair or Topology")

    for name in ["get", "get_form", "where_is_attribute", "select", "convert"]:
        monkeypatch.setattr(msm, name, forbidden)
    monkeypatch.setattr(Topology, "__init__", forbidden)
    monkeypatch.setattr(_ChemicalStateStorage, "_ensure_compatibility", forbidden)
    assert states.get(
        element="component",
        selection=[1, 0, 1],
        chemical_state=1,
        atom_index=True,
        n_atoms=True,
    ) == [[[2], [0, 1], [2]], [1, 2, 1]]
    assert states.get(element="bond", chemical_state=1, bond_index=True) == [0]


def test_component_summaries_retain_missing_stable_hierarchy(states):
    result = states.info(element="component", selection=[0], output_type="dataframe")
    assert result["index"].tolist() == [0]
    assert result["n atoms"].tolist() == [3]
    assert pd.isna(result.loc[0, "n groups"])
    assert pd.isna(result.loc[0, "molecule index"])
    with pytest.raises(NotWithThisFormError):
        states.get(element="group", n_atoms=True)


def test_queries_leave_all_state_storage_and_evidence_untouched(query, states):
    before = [dict(vars(state)) for state in states._states]
    query(chemical_state=1, n_bonds=True, connectivity_completeness=True)
    query(element="component", chemical_state=1, atom_index=True, n_bonds=True)
    for state, snapshot in zip(states._states, before):
        assert vars(state).keys() == snapshot.keys()
        assert all(vars(state)[name] is value for name, value in snapshot.items())


def test_incident_counts_include_declared_cross_component_edges_without_rebuilding(
    states,
):
    payload = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
    record = payload.data["states"][1]
    record["bonds"]["n_rows"] = 2
    for name, values in {
        "atom1_index": [0, 1],
        "atom2_index": [1, 2],
        "bond_order": [1, 1],
        "bond_type": ["covalent", "dative"],
    }.items():
        column = record["bonds"]["columns"][name]
        column["values"] = np.asarray(values, dtype=column["values"].dtype)
        column["null_mask"] = np.zeros(2, dtype=bool)
    record["bonds"]["columns"]["joins_components"] = {
        "dtype": "boolean",
        "values": np.array([True, False]),
        "null_mask": np.zeros(2, dtype=bool),
    }
    collection = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    assert collection.get(chemical_state=1, n_components=True) == 2
    assert collection.get(element="component", chemical_state=1, n_bonds=True) == [2, 1]
    assert collection.get(element="atom", chemical_state=1, n_bonds=True) == [1, 2, 1]
    assert collection.get(element="atom", chemical_state=1, component_index=True) == [
        0,
        0,
        1,
    ]


def test_empty_declared_components_and_unknown_membership_remain_distinct(states):
    payload = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
    record = payload.data["states"][1]
    record["component_completeness"] = "partial"
    record["component_indices"]["null_mask"][2] = True
    record["components"]["n_rows"] = 3
    for name, value in {
        "component_id": "declared-empty",
        "component_name": "empty",
        "component_type": "small molecule",
    }.items():
        column = record["components"]["columns"][name]
        column["values"] = np.concatenate([column["values"], np.asarray([value])])
        column["null_mask"] = np.zeros(3, dtype=bool)
    collection = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    assert collection.get(chemical_state=1, n_components=True) == 3
    assert collection.get(element="atom", chemical_state=1, component_index=True) == [
        0,
        0,
        None,
    ]
    assert (
        collection.get(
            element="atom", selection=[0, 2], chemical_state=1, n_components=True
        )
        == 1
    )
    assert collection.get(
        element="component",
        selection=[2, 1, 0],
        chemical_state=1,
        atom_index=True,
        n_atoms=True,
    ) == [[[], [], [0, 1]], [0, 0, 2]]


def test_full_atom_count_does_not_materialize_a_million_positions():
    import tracemalloc

    collection = msm.ChemicalStates(n_atoms=1_000_000)
    collection.get(element="atom", n_atoms=True)  # Warm dispatch and validators.
    own_trace = not tracemalloc.is_tracing()
    if own_trace:
        tracemalloc.start()
    baseline = tracemalloc.get_traced_memory()[0]
    tracemalloc.reset_peak()
    try:
        assert collection.get(element="atom", n_atoms=True) == 1_000_000
        peak = tracemalloc.get_traced_memory()[1] - baseline
    finally:
        if own_trace:
            tracemalloc.stop()
    # A million Python positions requires tens of MiB. This generous allowance
    # permits ordinary API bookkeeping while rejecting axis materialization.
    assert peak < 1_000_000, peak
    assert collection.n_chemical_states == 0
