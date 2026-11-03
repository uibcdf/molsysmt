"""Query typed chemical columns against literal state-local expectations."""

from concurrent.futures import ThreadPoolExecutor
from functools import partial
from threading import Barrier

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from tests.native import test_chemical_domain_separation as records
from tests.native import test_chemical_state_field_queries as rich_records

fields = rich_records.fields


@pytest.fixture
def wire():
    return msm.ChemicalStatesDict(
        {
            "schema": "molsysmt.chemical_states_dict",
            "version": 1,
            "n_atoms": 3,
            "reference_chemical_state_index": 0,
            "states": [
                records._record("path", [(0, 1), (1, 2)], [0, 0, 0], [0, 0, 0]),
                records._record("split", [(0, 1)], [0, 0, 1], [1, -1, 0]),
            ],
        }
    )


@pytest.fixture(params=["native", "universal"])
def query(wire, request):
    return wire.get if request.param == "native" else partial(msm.get, wire)


def test_selected_counts_inventory_and_declarations_remain_distinct(query, wire):
    assert query(
        chemical_state=1,
        n_atoms=True,
        n_bonds=True,
        n_components=True,
        chemical_state_index=True,
        chemical_state_id=True,
        reference_chemical_state_index=True,
        connectivity_completeness=True,
        component_evidence=True,
        output_type="dictionary",
    ) == {
        "n_atoms": 3,
        "n_bonds": 1,
        "n_components": 2,
        "chemical_state_index": [0, 1],
        "chemical_state_id": ["path", "split"],
        "reference_chemical_state_index": 0,
        "connectivity_completeness": "complete",
        "component_evidence": "explicit",
    }
    assert wire.data["reference_chemical_state_index"] == 0


@pytest.mark.parametrize(
    "element,state,selection,attribute,expected",
    [
        ("atom", 1, [2, 0, 2], "atom_index", [2, 0, 2]),
        ("atom", 1, [2, 0, 2], "component_index", [1, 0, 1]),
        ("atom", 0, [1, 0, 1], "n_bonds", [2, 1, 2]),
        ("atom", 1, [2, 0, 2], "bond_index", [[], [0], []]),
        ("atom", 1, [2, 0, 2], "formal_charge", [0, 1, 0]),
        ("atom", 1, [2, 0, 2], "n_components", 2),
        ("bond", 0, [1, 0, 1], "bond_index", [1, 0, 1]),
        ("bond", 0, [1, 0, 1], "bond_order", [1, 1, 1]),
        ("component", 1, [1, 0, 1], "atom_index", [[2], [0, 1], [2]]),
        ("component", 1, [1, 0, 1], "n_atoms", [1, 2, 1]),
        ("component", 1, [1, 0, 1], "n_bonds", [0, 1, 0]),
        ("component", 1, [1, 0, 1], "component_id", ["split-1", "split-0", "split-1"]),
    ],
)
def test_direct_array_projections_preserve_positions_and_repetitions(
    query, element, state, selection, attribute, expected
):
    assert (
        query(
            element=element,
            selection=selection,
            chemical_state=state,
            **{attribute: True},
        )
        == expected
    )


@pytest.mark.parametrize(
    "element,attribute,expected",
    [
        ("atom", "formal_charge", []),
        ("atom", "atom_is_aromatic", None),
        ("atom", "component_index", []),
        ("atom", "n_components", 0),
        ("bond", "bond_order", []),
        ("bond", "bond_stereo_atom_indices", []),
        ("component", "atom_index", []),
        ("component", "component_name", []),
    ],
)
def test_empty_selection_and_missing_column_shapes_match_native_contract(
    query, element, attribute, expected
):
    assert (
        query(element=element, selection=[], chemical_state=1, **{attribute: True})
        == expected
    )


def test_masks_and_bounds_use_the_selected_state_axes(query):
    assert query(
        element="bond", selection=[1, 0, 1], mask=[False, True], bond_index=True
    ) == [1]
    with pytest.raises(ArgumentError):
        query(element="bond", selection=[1], chemical_state=1, bond_order=True)
    with pytest.raises(ArgumentError):
        query(element="component", selection=[1], chemical_state=0, component_name=True)


@pytest.mark.parametrize("selection", [[True, 0], [-1], [0.5], [[0]]])
def test_malformed_positions_reject_without_decoding(query, selection):
    with pytest.raises(ArgumentError):
        query(element="atom", selection=selection, formal_charge=True)


@pytest.mark.parametrize("attribute,expected", rich_records.ATOM_VALUES.items())
def test_rich_atom_fields_retain_native_scalars_and_null_masks(
    fields, attribute, expected
):
    wire = msm.convert(fields, to_form="molsysmt.ChemicalStatesDict")
    assert wire.get(element="atom", **{attribute: True}) == expected
    assert msm.get(wire, element="atom", selection=[2, 0, 2], **{attribute: True}) == [
        expected[2],
        expected[0],
        expected[2],
    ]


@pytest.mark.parametrize("attribute,expected", rich_records.BOND_VALUES.items())
def test_rich_bond_fields_and_nullable_stereo_pairs_are_direct(
    fields, attribute, expected
):
    wire = msm.convert(fields, to_form="molsysmt.ChemicalStatesDict")
    assert wire.get(element="bond", **{attribute: True}) == expected
    assert msm.get(wire, element="bond", selection=[1, 0, 1], **{attribute: True}) == [
        expected[1],
        expected[0],
        expected[1],
    ]


def test_availability_and_atom_label_projection_distinguish_unknown_membership(fields):
    wire = msm.convert(fields, to_form="molsysmt.ChemicalStatesDict")
    assert wire.get(element="atom", component_id=True) == ["first", None, "last"]
    assert msm.has_attribute(wire, "atom_is_aromatic")
    assert not msm.has_attribute(wire, "formal_charge", chemical_state=1)
    assert msm.has_attribute(wire, "formal_charge", chemical_state=1, include_none=True)
    assert not msm.has_attribute(wire, "isotope", include_none=True)
    assert wire.get(chemical_state=1, formal_charge=True) is None


def test_zero_states_and_unknown_empty_state_remain_distinct(wire):
    wire.data["states"] = []
    wire.data["reference_chemical_state_index"] = None
    assert wire.get(
        n_atoms=True, n_chemical_states=True, chemical_state_index=True
    ) == [3, 0, []]
    assert not msm.has_attribute(wire, "n_bonds")
    assert msm.has_attribute(wire, "n_bonds", include_none=True)
    with pytest.raises(StructuralInconsistencyError, match="unavailable"):
        wire.get(n_bonds=True)


def test_ambiguous_scope_is_restored_and_collection_inventory_stays_readable(wire):
    wire.data["reference_chemical_state_index"] = None
    assert wire.get(chemical_state_index=True, chemical_state_id=True) == [
        [0, 1],
        ["path", "split"],
    ]
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        wire.get(n_bonds=True)
    assert wire.get(chemical_state=1, n_bonds=True) == 1
    with pytest.raises(ArgumentError):
        wire.get(element="bond", selection=[1], chemical_state=1, bond_order=True)
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        wire.get(n_bonds=True)
    assert wire.data["reference_chemical_state_index"] is None


def test_context_is_nested_and_thread_local_without_native_record_decoding(wire):
    barrier = Barrier(2)

    def run(index):
        with wire._using_chemical_state(index):
            barrier.wait(timeout=10)
            return wire.get(n_bonds=True)

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert list(pool.map(run, [0, 1])) == [2, 1]
    with wire._using_chemical_state(1):
        with pytest.raises(RuntimeError):
            with wire._using_chemical_state(0):
                assert wire.get(n_bonds=True) == 2
                raise RuntimeError("abort nested scope")
        assert wire.get(n_bonds=True) == 1
    assert wire.get(n_bonds=True) == 2


def test_native_query_and_info_need_no_discovery_conversion_or_native_storage(
    wire, monkeypatch
):
    from molsysmt.native import chemical_states_dict as codec
    from molsysmt.native._chemical_state import _ChemicalStateStorage

    def forbidden(*args, **kwargs):
        pytest.fail(
            "Typed query entered discovery, decoding or native state construction"
        )

    for name in ["get", "get_form", "convert", "select", "where_is_attribute"]:
        monkeypatch.setattr(msm, name, forbidden)
    monkeypatch.setattr(codec, "_decode_chemical_states", forbidden)
    monkeypatch.setattr(codec, "_decode_series", forbidden)
    monkeypatch.setattr(msm.ChemicalStates, "__init__", forbidden)
    monkeypatch.setattr(_ChemicalStateStorage, "__init__", forbidden)
    assert wire.get(
        element="atom", selection=[2, 0], chemical_state=1, formal_charge=True
    ) == [0, 1]
    assert wire.get(element="component", chemical_state=1, atom_index=True) == [
        [0, 1],
        [2],
    ]
    assert wire.info(element="component", output_type="dictionary")[0]["n atoms"] == 3


def test_unrequested_state_and_history_are_not_decoded(wire):
    class Untouched(dict):
        def get(self, *args):
            pytest.fail("Unrequested state was visited")

        def __getitem__(self, key):
            pytest.fail("Unrequested state was visited")

    wire.data["states"][0] = Untouched()
    wire.data["version"] = 2
    wire.data["states"][1]["preparation_history"] = object()
    assert wire.get(chemical_state=1, n_bonds=True, formal_charge=True) == [
        1,
        [1, -1, 0],
    ]


def test_direct_results_are_detached_and_readonly_source_arrays_are_untouched(wire):
    def freeze(value):
        if isinstance(value, np.ndarray):
            value.flags.writeable = False
        elif isinstance(value, dict):
            for item in value.values():
                freeze(item)
        elif isinstance(value, list):
            for item in value:
                freeze(item)

    freeze(wire.data)
    result = wire.get(element="atom", chemical_state=1, formal_charge=True)
    result[0] = 99
    assert wire.get(element="atom", chemical_state=1, formal_charge=True) == [1, -1, 0]
    assert not wire.data["states"][1]["atom_attributes"]["columns"]["formal_charge"][
        "values"
    ].flags.writeable


@pytest.mark.parametrize(
    "fault",
    [
        "mask_shape",
        "mask_dtype",
        "value_dtype",
        "row_count",
        "membership",
        "endpoint",
        "version",
    ],
)
def test_malformed_requested_data_rejects_without_repair(wire, fault):
    state = wire.data["states"][1]
    attribute = "formal_charge"
    element = "atom"
    col = state["atom_attributes"]["columns"]["formal_charge"]
    if fault == "mask_shape":
        col["null_mask"] = np.zeros(2, dtype=bool)
    elif fault == "mask_dtype":
        col["null_mask"] = np.zeros(3, dtype=int)
    elif fault == "value_dtype":
        col["values"] = np.array([True, False, True])
    elif fault == "row_count":
        state["atom_attributes"]["n_rows"] = 2
    elif fault == "membership":
        state["component_indices"]["values"][2] = 2
        attribute = "component_index"
    elif fault == "endpoint":
        state["bonds"]["columns"]["atom2_index"]["values"][0] = 3
        attribute = "n_bonds"
    else:
        wire.data["version"] = True
    with pytest.raises(StructuralInconsistencyError):
        wire.get(element=element, chemical_state=1, **{attribute: True})


def test_small_typed_queries_do_not_decode_or_materialize_full_atom_columns(wire):
    import tracemalloc

    size = 1_000_000
    wire.data["n_atoms"] = size
    wire.data["states"] = wire.data["states"][:1]
    state = wire.data["states"][0]
    state["connectivity_completeness"] = state["component_completeness"] = "partial"
    state["atom_attributes"]["n_rows"] = size
    state["atom_attributes"]["columns"]["formal_charge"] = {
        "dtype": "Int16",
        "values": np.zeros(size, dtype=np.int16),
        "null_mask": np.zeros(size, dtype=bool),
    }
    state["component_indices"] = {
        "dtype": "Int64",
        "values": np.zeros(size, dtype=np.int64),
        "null_mask": np.zeros(size, dtype=bool),
    }
    wire.get(
        element="atom", selection=[size - 1, 0], formal_charge=True, component_id=True
    )
    tracemalloc.start()
    try:
        observed = wire.get(
            element="atom",
            selection=[size - 1, 0],
            formal_charge=True,
            component_id=True,
        )
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert observed == [[0, 0], ["path-0", "path-0"]]
    assert peak < 1_000_000, f"Small typed query allocated {peak:,} bytes"


def test_zero_state_cardinality_does_not_enumerate_a_million_positions(wire):
    import tracemalloc

    wire.data["states"] = []
    wire.data["reference_chemical_state_index"] = None
    wire.data["n_atoms"] = 1_000_000
    wire.get(element="atom", n_atoms=True)
    tracemalloc.start()
    try:
        value = wire.get(element="atom", n_atoms=True)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert value == 1_000_000
    assert peak < 1_000_000, f"Cardinality query allocated {peak:,} bytes"


@pytest.mark.parametrize(
    "attribute,value,expected",
    [
        ("formal_charge", [1, -1], [-1, -1, 1]),
        ("atom_is_aromatic", [True, False], [False, None, True]),
        ("n_unpaired_electrons", [1, 0], [0, None, 1]),
        ("n_implicit_hydrogens", [1, 2], [2, None, 1]),
        ("n_explicit_hydrogens", [1, 0], [0, None, 1]),
        ("allows_implicit_hydrogens", [False, True], [True, None, False]),
        ("atom_stereochemistry", ["S", "R"], ["R", None, "S"]),
    ],
)
def test_controlled_dictionary_atom_assignment(wire, attribute, value, expected):
    original = wire.data["states"][0]
    msm.set(wire, selection=[2, 0], chemical_state=1, **{attribute: value})
    assert wire.get(chemical_state=1, **{attribute: True}) == expected
    assert wire.data["states"][0] is original
    assert wire.data["reference_chemical_state_index"] == 0


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
def test_controlled_dictionary_bond_assignment(wire, attribute, value, expected):
    msm.set(wire, element="bond", chemical_state=1, bond_stereo_atom_indices=[2, 0])
    msm.set(wire, element="bond", chemical_state=1, bond_evidence="explicit")
    original = wire.data["states"][0]
    msm.set(wire, element="bond", chemical_state=1, **{attribute: value})
    assert wire.get(element="bond", chemical_state=1, **{attribute: True}) == [expected]
    assert wire.data["states"][0] is original


@pytest.mark.parametrize("element", ["atom", "component"])
@pytest.mark.parametrize(
    "attribute,value,expected",
    [
        ("component_id", 42, "42"),
        ("component_name", "fragment", "fragment"),
        ("component_type", "small molecule", "small molecule"),
    ],
)
def test_dictionary_component_label_assignment(
    wire, element, attribute, value, expected
):
    msm.set(
        wire, element=element, selection=[0], chemical_state=1, **{attribute: value}
    )
    assert wire.get(element="atom", chemical_state=1, **{attribute: True}) == [
        expected,
        expected,
        {
            "component_id": "split-1",
            "component_name": "part-1",
            "component_type": "small molecule",
        }[attribute],
    ]


def test_dictionary_membership_assignment_and_rejection_are_atomic(wire, monkeypatch):
    msm.set(wire, selection=[1], chemical_state=1, component_index=None)
    assert wire.get(element="atom", chemical_state=1, component_index=True) == [
        0,
        None,
        1,
    ]
    assert wire.get(chemical_state=1, component_completeness=True) == "partial"
    before = wire.data
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        msm.set(wire, selection=[0], chemical_state=1, component_index=2)
    assert wire.data is before
    from molsysmt.native import _chemical_dict_assignments as writer

    def failure(*args):
        raise MemoryError("injected encoding failure")

    monkeypatch.setattr(writer, "_encode_chemical_states", failure)
    with pytest.raises(MemoryError, match="injected"):
        msm.set(wire, chemical_state=1, formal_charge=0)
    assert wire.data is before


@pytest.mark.parametrize(
    "form", ["molsysmt.ChemicalStates", "molsysmt.ChemicalStatesDict"]
)
def test_predicates_follow_selected_chemical_state(wire, form):
    item = msm.convert(wire, to_form=form)
    assert msm.contains(item, n_components=2, chemical_state=1)
    assert not msm.contains(item, n_components=2, chemical_state=0)
    assert msm.is_composed_of(item, n_components=2, chemical_state=1)
    assert not msm.is_composed_of(item, n_components=2, chemical_state=0)
    assert item.get(reference_chemical_state_index=True) == 0
