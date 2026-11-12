"""Protect native stable-inventory traversal without coordinates or chemistry."""

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import Topology
from tests.native.test_topology_operations import build_minimal_topology


@pytest.fixture(params=["molsysmt.Topology", "molsysmt.MolSys"])
def source(request):
    topology = build_minimal_topology()
    if request.param == "molsysmt.Topology":
        return topology
    return msm.convert(topology, to_form="molsysmt.MolSys")


@pytest.mark.parametrize("indices", ["all", [3, 0, 3, 1], []])
@pytest.mark.parametrize(
    "element,attribute,labels",
    [("atom", "atom_name", ["N", "CA", "O", "H"]), ("group", "group_id", ["10", "11"])],
)
def test_native_inventory_iterator_preserves_requested_positions(
    source, indices, element, attribute, labels
):
    import importlib

    selected = indices
    if element == "group" and indices == [3, 0, 3, 1]:
        selected = [1, 0, 1, 0]
    adapter = importlib.import_module(
        "molsysmt.form.molsysmt_Topology"
        if isinstance(source, Topology)
        else "molsysmt.form.molsysmt_MolSys"
    )
    topology = source if isinstance(source, Topology) else source.topology
    before = topology.atoms.copy(deep=True)
    iterator = adapter.TopologyIterator(
        source,
        element=element,
        indices=selected,
        chunk=2,
        output_type="dictionary",
        **{attribute: True},
    )
    chunks = list(iterator)
    expected_indices = list(range(len(labels))) if selected == "all" else selected
    actual = [value for chunk in chunks for value in chunk[attribute]]
    assert actual == [labels[i] for i in expected_indices]
    assert [len(chunk[attribute]) for chunk in chunks] == [
        len(expected_indices[i : i + 2]) for i in range(0, len(expected_indices), 2)
    ]
    with pytest.raises(StopIteration):
        next(iterator)
    pd.testing.assert_frame_equal(topology.atoms, before)


def test_public_inventory_iterator_keeps_chunk_traversal(source):
    chunks = list(
        msm.Iterator(
            source,
            element="atom",
            selection="all",
            atom_name=True,
            start=1,
            stop=4,
            step=2,
            chunk=2,
            output_type="dictionary",
        )
    )
    assert len(chunks) == 1
    assert chunks[0]["atom_name"] == ["CA", "H"]


@pytest.mark.parametrize("output_type", ["values", "dictionary"])
def test_direct_iterator_keeps_value_order_and_selection_window(source, output_type):
    import importlib

    adapter = importlib.import_module(
        "molsysmt.form.molsysmt_Topology"
        if isinstance(source, Topology)
        else "molsysmt.form.molsysmt_MolSys"
    )
    chunks = list(
        adapter.TopologyIterator(
            source,
            indices=[3, 0, 2, 1],
            start=1,
            stop=99,
            step=2,
            chunk=2,
            atom_name=True,
            atom_id=True,
            output_type=output_type,
        )
    )
    assert len(chunks) == 1
    expected = {"atom_name": ["N", "CA"], "atom_id": ["0", "1"]}
    assert chunks[0] == (
        expected if output_type == "dictionary" else list(expected.values())
    )


@pytest.mark.parametrize("indices", [[4], [-1], [1.5], [True]])
def test_direct_iterator_rejects_invalid_source_positions(source, indices):
    import importlib

    from molsysmt._private.smonitor import ArgumentError

    adapter = importlib.import_module(
        "molsysmt.form.molsysmt_Topology"
        if isinstance(source, Topology)
        else "molsysmt.form.molsysmt_MolSys"
    )
    with pytest.raises(ArgumentError):
        adapter.TopologyIterator(source, indices=indices, atom_name=True)


def test_direct_iterator_rejects_unknown_attributes_and_nonboolean_flags(source):
    import importlib

    from argdigest.core.errors import UnknownArgumentError

    from molsysmt._private.smonitor import ArgumentError

    adapter = importlib.import_module(
        "molsysmt.form.molsysmt_Topology"
        if isinstance(source, Topology)
        else "molsysmt.form.molsysmt_MolSys"
    )
    with pytest.raises(UnknownArgumentError):
        adapter.TopologyIterator(source, not_an_attribute=True)
    with pytest.raises(ArgumentError):
        adapter.TopologyIterator(source, atom_name="yes")


@pytest.mark.parametrize("attribute", ["formal_charge", "n_atoms"])
def test_direct_iterator_refuses_unavailable_or_aggregate_values(source, attribute):
    import importlib

    from molsysmt._private.smonitor import NotWithThisFormError

    adapter = importlib.import_module(
        "molsysmt.form.molsysmt_Topology"
        if isinstance(source, Topology)
        else "molsysmt.form.molsysmt_MolSys"
    )
    with pytest.raises(NotWithThisFormError):
        adapter.TopologyIterator(source, **{attribute: True})


def test_public_index_only_inventory_uses_the_topology_axis():
    source = build_minimal_topology()
    chunks = [
        row["atom_index"]
        for row in msm.Iterator(
            source, element="atom", atom_index=True, chunk=2, output_type="dictionary"
        )
    ]
    assert chunks == [[0, 1], [2, 3]]


def test_direct_iterator_supports_native_query_aliases(source):
    import importlib

    adapter = importlib.import_module(
        "molsysmt.form.molsysmt_Topology"
        if isinstance(source, Topology)
        else "molsysmt.form.molsysmt_MolSys"
    )
    result = list(
        adapter.TopologyIterator(
            source,
            indices=[2, 0],
            element="atom",
            chunk=2,
            name=True,
            index=True,
            output_type="dictionary",
        )
    )
    assert result == [{"atom_name": ["O", "N"], "atom_index": [2, 0]}]
