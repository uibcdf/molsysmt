"""Read state fields against independent nullable records, without inference."""

from functools import partial

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import Topology
from tests.native import test_chemical_domain_separation as contract_fixtures

ATOM_VALUES = {
    "formal_charge": [0, None, -1],
    "atom_is_aromatic": [False, None, True],
    "n_unpaired_electrons": [0, None, 1],
    "n_implicit_hydrogens": [0, None, 2],
    "n_explicit_hydrogens": [1, None, 0],
    "allows_implicit_hydrogens": [False, None, True],
    "atom_stereochemistry": ["R", None, "unknown"],
}
BOND_VALUES = {
    "bond_id": ["same", "same"],
    "bond_order": [1, 0],
    "fractional_bond_order": [1.0, 1.5],
    "bond_type": ["covalent", "dative"],
    "bond_is_aromatic": [False, True],
    "bond_is_conjugated": [False, True],
    "bond_stereochemistry": ["unspecified", "E"],
    "bond_stereo_atom_indices": [[0, 1], [1, 2]],
    "bond_donor_atom_index": [None, 1],
    "bond_acceptor_atom_index": [None, 2],
    "bond_joins_components": [True, False],
    "bond_evidence": ["explicit", "user_defined"],
}
COMPONENT_VALUES = {
    "component_id": ["first", "last"],
    "component_name": ["head", None],
    "component_type": [None, "small molecule"],
}


def _column(dtype, values):
    """Declare missing values through masks, not optional engine defaults."""
    missing = [value is None for value in values]
    fill = "" if dtype == "string" else 0
    storage = (
        np.str_
        if dtype == "string"
        else np.bool_
        if dtype == "boolean"
        else dtype.lower()
    )
    return {
        "dtype": dtype,
        "values": np.asarray(
            [fill if absent else value for absent, value in zip(missing, values)],
            dtype=storage,
        ),
        "null_mask": np.asarray(missing, dtype=np.bool_),
    }


@pytest.fixture
def fields():
    first = contract_fixtures._record("rich", [(0, 1), (1, 2)], [0, 0, 1], [0, 0, -1])
    # Independent fixture spelling deliberately does not import runtime field maps.
    for name, public, dtype in [
        ("formal_charge", "formal_charge", "Int16"),
        ("is_aromatic", "atom_is_aromatic", "boolean"),
        ("n_unpaired_electrons", "n_unpaired_electrons", "UInt8"),
        ("n_implicit_hydrogens", "n_implicit_hydrogens", "UInt8"),
        ("n_explicit_hydrogens", "n_explicit_hydrogens", "UInt8"),
        ("allows_implicit_hydrogens", "allows_implicit_hydrogens", "boolean"),
        ("stereochemistry", "atom_stereochemistry", "string"),
    ]:
        first["atom_attributes"]["columns"][name] = _column(dtype, ATOM_VALUES[public])
    for name, public, dtype in [
        ("bond_id", "bond_id", "string"),
        ("bond_order", "bond_order", "UInt8"),
        ("fractional_bond_order", "fractional_bond_order", "Float64"),
        ("bond_type", "bond_type", "string"),
        ("is_aromatic", "bond_is_aromatic", "boolean"),
        ("is_conjugated", "bond_is_conjugated", "boolean"),
        ("stereochemistry", "bond_stereochemistry", "string"),
        ("donor_atom_index", "bond_donor_atom_index", "Int64"),
        ("acceptor_atom_index", "bond_acceptor_atom_index", "Int64"),
        ("joins_components", "bond_joins_components", "boolean"),
        ("evidence", "bond_evidence", "string"),
    ]:
        first["bonds"]["columns"][name] = _column(dtype, BOND_VALUES[public])
    for offset in [0, 1]:
        first["bonds"]["columns"][f"stereo_atom{offset + 1}_index"] = _column(
            "Int64", [pair[offset] for pair in BOND_VALUES["bond_stereo_atom_indices"]]
        )
    for name, values in COMPONENT_VALUES.items():
        first["components"]["columns"][name] = _column("string", values)
    first["component_indices"] = _column("Int64", [0, None, 1])
    first["component_completeness"] = "partial"
    second = contract_fixtures._record("plain", [(0, 2)], [0, 1, 0], [1, 0, 0])
    del second["atom_attributes"]["columns"]["formal_charge"]
    payload = msm.ChemicalStatesDict(
        {
            "schema": "molsysmt.chemical_states_dict",
            "version": 1,
            "n_atoms": 3,
            "reference_chemical_state_index": 0,
            "states": [first, second],
        }
    )
    return msm.convert(payload, to_form="molsysmt.ChemicalStates")


@pytest.fixture(params=["native", "universal"])
def query(fields, request):
    return fields.get if request.param == "native" else partial(msm.get, fields)


@pytest.mark.parametrize("attribute,expected", ATOM_VALUES.items())
def test_declared_atom_fields_keep_nulls_order_and_repetitions(
    query, attribute, expected
):
    assert query(element="atom", **{attribute: True}) == expected
    assert query(element="atom", selection=[2, 0, 2], **{attribute: True}) == [
        expected[2],
        expected[0],
        expected[2],
    ]
    assert query(element="atom", selection=[], **{attribute: True}) == []


def test_system_formal_charge_is_an_atom_vector_in_elementary_charge_units(query):
    result = query(formal_charge=True)
    assert result == [0, None, -1]
    assert type(result[0]) is int
    assert not msm.pyunitwizard.is_quantity(result)


@pytest.mark.parametrize("attribute,expected", BOND_VALUES.items())
def test_declared_bond_fields_keep_state_row_order_and_repetitions(
    query, attribute, expected
):
    assert query(element="bond", **{attribute: True}) == expected
    assert query(element="bond", selection=[1, 0, 1], **{attribute: True}) == [
        expected[1],
        expected[0],
        expected[1],
    ]
    assert query(element="bond", selection=[], **{attribute: True}) == []


@pytest.mark.parametrize("attribute,expected", COMPONENT_VALUES.items())
def test_component_fields_project_unknown_membership_without_negative_indexing(
    query, attribute, expected
):
    assert query(element="component", selection=[1, 0, 1], **{attribute: True}) == [
        expected[1],
        expected[0],
        expected[1],
    ]
    assert query(element="atom", selection=[1, 2, 0], **{attribute: True}) == [
        None,
        expected[1],
        expected[0],
    ]
    assert query(element="component", selection=[], **{attribute: True}) == []
    assert query(element="atom", selection=[], **{attribute: True}) == []


@pytest.mark.parametrize("attribute", list(ATOM_VALUES))
def test_absent_atom_columns_remain_unavailable_even_for_no_selected_atoms(
    query, attribute
):
    assert query(element="atom", chemical_state=1, **{attribute: True}) is None
    assert (
        query(element="atom", selection=[], chemical_state=1, **{attribute: True})
        is None
    )


@pytest.mark.parametrize(
    "attribute", ["fractional_bond_order", "bond_stereo_atom_indices", "bond_evidence"]
)
def test_missing_bond_fields_retain_edge_cardinality(query, attribute):
    missing = [None, None] if attribute == "bond_stereo_atom_indices" else None
    assert query(element="bond", chemical_state=1, **{attribute: True}) == [missing]
    assert (
        query(element="bond", selection=[], chemical_state=1, **{attribute: True}) == []
    )


def test_availability_follows_selected_state_values_including_zero_and_false(fields):
    for attribute in [*ATOM_VALUES, *BOND_VALUES, *COMPONENT_VALUES]:
        assert msm.has_attribute(fields, attribute, chemical_state=0)
        assert msm.has_attribute(fields, attribute, chemical_state=1, include_none=True)
    assert not msm.has_attribute(fields, "formal_charge", chemical_state=1)
    assert not msm.has_attribute(fields, "bond_is_aromatic", chemical_state=1)
    assert not msm.has_attribute(fields, "isotope", include_none=True)
    zero = msm.ChemicalStates(n_atoms=3)
    assert not msm.has_attribute(zero, "formal_charge")
    assert msm.has_attribute(zero, "formal_charge", include_none=True)
    with pytest.raises(StructuralInconsistencyError, match="unavailable"):
        zero.get(formal_charge=True)


def test_mask_and_active_state_bounds_are_applied_before_reading_fields(query):
    assert query(
        element="bond", selection=[1, 0, 1], mask=[False, True], bond_order=True
    ) == [0]
    with pytest.raises(ArgumentError):
        query(element="bond", selection=[1], chemical_state=1, bond_order=True)
    with pytest.raises(ArgumentError):
        query(element="component", selection=[2], component_id=True)


def test_native_reads_need_no_discovery_topology_repair_or_public_state_table_copies(
    fields, monkeypatch
):
    from molsysmt.native._chemical_state import _ChemicalStateStorage

    def forbidden(*args, **kwargs):
        pytest.fail("Stored-field query entered discovery, repair or table-copy APIs")

    for name in ["get", "get_form", "select", "convert", "where_is_attribute"]:
        monkeypatch.setattr(msm, name, forbidden)
    monkeypatch.setattr(Topology, "__init__", forbidden)
    monkeypatch.setattr(_ChemicalStateStorage, "_ensure_compatibility", forbidden)
    monkeypatch.setattr(msm.ChemicalStates, "get_bonds", forbidden)
    before = [dict(vars(state)) for state in fields._states]
    assert fields.get(
        element="atom", selection=[2, 0], formal_charge=True, atom_is_aromatic=True
    ) == [[-1, 0], [True, False]]
    assert fields.get(element="bond", bond_order=True, bond_id=True) == [
        [1, 0],
        ["same", "same"],
    ]
    assert fields.get(element="atom", component_name=True) == ["head", None, None]
    for state, snapshot in zip(fields._states, before):
        assert vars(state).keys() == snapshot.keys()
        assert all(vars(state)[name] is value for name, value in snapshot.items())


def test_rich_fields_survive_detached_dictionary_round_trip_without_reinterpretation(
    fields,
):
    wire = msm.convert(fields, to_form="molsysmt.ChemicalStatesDict")
    restored = msm.convert(wire, to_form="molsysmt.ChemicalStates")
    for attribute, expected in ATOM_VALUES.items():
        assert restored.get(element="atom", **{attribute: True}) == expected
    for attribute, expected in BOND_VALUES.items():
        assert restored.get(element="bond", **{attribute: True}) == expected
    assert restored.reference_chemical_state_index == 0
    for old, new in zip(fields._states, restored._states):
        pd.testing.assert_frame_equal(old.atom_attributes, new.atom_attributes)
        pd.testing.assert_frame_equal(old.bonds, new.bonds)
        pd.testing.assert_frame_equal(old.components, new.components)


@pytest.mark.parametrize(
    "attribute,column,dtype,values",
    [
        ("formal_charge", "formal_charge", "Int16", [0, 0, 0]),
        ("atom_is_aromatic", "is_aromatic", "boolean", [False, False, False]),
        ("n_explicit_hydrogens", "n_explicit_hydrogens", "UInt8", [0, 0, 0]),
    ],
)
def test_false_and_zero_are_available_but_all_null_is_not(
    fields, attribute, column, dtype, values
):
    wire = msm.convert(fields, to_form="molsysmt.ChemicalStatesDict")
    for declared in [values, [None, None, None]]:
        wire.data["states"][1]["atom_attributes"]["columns"][column] = _column(
            dtype, declared
        )
        restored = msm.convert(wire, to_form="molsysmt.ChemicalStates")
        assert msm.has_attribute(restored, attribute, chemical_state=1) is (
            declared[0] is not None
        )
        assert msm.has_attribute(
            restored, attribute, chemical_state=1, include_none=True
        )
        assert (
            restored.get(element="atom", chemical_state=1, **{attribute: True})
            == declared
        )


def test_stereo_references_remain_independently_nullable(fields):
    wire = msm.convert(fields, to_form="molsysmt.ChemicalStatesDict")
    columns = wire.data["states"][1]["bonds"]["columns"]
    columns["stereo_atom1_index"] = _column("Int64", [1])
    restored = msm.convert(wire, to_form="molsysmt.ChemicalStates")
    assert restored.get(
        element="bond", chemical_state=1, bond_stereo_atom_indices=True
    ) == [[1, None]]
    assert msm.has_attribute(restored, "bond_stereo_atom_indices", chemical_state=1)


def test_empty_graph_and_component_rows_have_field_shapes_without_new_states():
    states = msm.ChemicalStates(n_atoms=2)
    states.append_state()
    assert states.get(element="atom", component_name=True, formal_charge=True) == [
        [None, None],
        None,
    ]
    assert states.get(element="component", component_id=True) == []
    assert states.get(element="bond", bond_id=True, bond_stereo_atom_indices=True) == [
        [],
        [],
    ]
    assert states.n_chemical_states == 1


def test_state_scope_restores_after_field_failure_and_missing_reference(fields):
    fields._set_reference_index(None)
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        fields.get(formal_charge=True)
    assert fields.get(chemical_state=0, formal_charge=True) == [0, None, -1]
    with pytest.raises(ArgumentError):
        fields.get(element="bond", chemical_state=1, selection=[1], bond_id=True)
    assert fields.reference_chemical_state_index is None
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        fields.get(element="bond", bond_id=True)


def test_rich_query_values_and_null_masks_survive_h5msm_05(fields, tmp_path):
    from molsysmt.native import MolSys

    molsys = MolSys._from_partial_domains(chemical_states=fields)
    filename = tmp_path / "chemical-fields.h5msm"
    msm.convert(molsys, to_form=str(filename))
    restored = msm.convert(str(filename), to_form="molsysmt.MolSys").chemical_states
    assert restored.get(element="atom", formal_charge=True, atom_is_aromatic=True) == [
        ATOM_VALUES["formal_charge"],
        ATOM_VALUES["atom_is_aromatic"],
    ]
    assert (
        restored.get(
            element="bond",
            output_type="dictionary",
            **{name: True for name in BOND_VALUES},
        )
        == BOND_VALUES
    )
    assert restored.get(element="atom", component_id=True) == ["first", None, "last"]
    assert restored.get(chemical_state=1, formal_charge=True) is None


def test_small_component_label_queries_do_not_materialize_full_membership():
    import tracemalloc

    # The million-row membership is allocated before tracing. Only query work
    # counts: two requested positions must not allocate a full-axis integer array.
    states = msm.ChemicalStates(n_atoms=1_000_000)
    states.append_state()
    states.get(element="atom", selection=[999_999, 0], component_id=True)
    tracemalloc.start()
    try:
        result = states.get(element="atom", selection=[999_999, 0], component_id=True)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert result == [None, None]
    assert peak < 1_000_000, f"Small label query allocated {peak:,} bytes"


@pytest.mark.parametrize("selection", [[True, 0], [0.5], [-1], [[0]]])
@pytest.mark.parametrize(
    "element,attribute",
    [
        ("atom", "formal_charge"),
        ("bond", "bond_order"),
        ("component", "component_name"),
    ],
)
def test_field_queries_reject_malformed_positions(query, selection, element, attribute):
    with pytest.raises(ArgumentError):
        query(element=element, selection=selection, **{attribute: True})


def test_component_label_projection_rejects_invalid_requested_stored_membership(fields):
    # Direct mutation is unsupported, but it must not turn an invalid reference
    # into a plausible label from another component.
    fields._resolve_chemical_state().component_indices.iloc[1] = -1
    with pytest.raises(StructuralInconsistencyError, match="membership"):
        fields.get(element="atom", selection=[1], component_name=True)
    fields._resolve_chemical_state().component_indices.iloc[1] = 2
    with pytest.raises(StructuralInconsistencyError, match="membership"):
        fields.get(element="atom", selection=[1], component_name=True)


def test_field_results_are_detached_and_reads_preserve_every_state_table(fields):
    before = [
        (
            s.atom_attributes.copy(deep=True),
            s.bonds.copy(deep=True),
            s.components.copy(deep=True),
            s.component_indices.copy(deep=True),
        )
        for s in fields._states
    ]
    charges = fields.get(formal_charge=True)
    charges[0] = 99
    references = fields.get(element="bond", bond_stereo_atom_indices=True)
    references[0][0] = 99
    labels = fields.get(element="atom", component_id=True)
    labels[0] = "changed"
    fields.get(element="bond", chemical_state=1, bond_order=True)
    for state, (atoms, bonds, components, membership) in zip(fields._states, before):
        pd.testing.assert_frame_equal(state.atom_attributes, atoms)
        pd.testing.assert_frame_equal(state.bonds, bonds)
        pd.testing.assert_frame_equal(state.components, components)
        pd.testing.assert_series_equal(state.component_indices, membership)
    assert fields.reference_chemical_state_index == 0
