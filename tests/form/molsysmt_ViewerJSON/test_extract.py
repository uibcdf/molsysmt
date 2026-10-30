"""Checking graphics subsets against literal axes, bonds and geometry."""

import json
from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, FormatError
from molsysmt.form.molsysmt_ViewerJSON.extract import extract
from molsysmt.native import MolSys, ViewerJSON


@pytest.fixture
def payload():
    molsys = MolSys(n_atoms=3, n_groups=1, n_molecules=1, n_chains=1)
    topo = molsys.topology
    topo.atoms["atom_id"] = ["007", "010", "C"]
    topo.atoms["atom_name"] = ["C1", "N1", "O1"]
    topo.atoms["atom_type"] = ["C", "N", "O"]
    topo.atoms["group_index"] = [0, 0, 0]
    topo.atoms["chain_index"] = [0, 0, 0]
    topo.groups["group_id"] = ["L"]
    topo.groups["group_name"] = ["LIG"]
    topo.groups["molecule_index"] = [0]
    topo.chains["chain_id"] = ["A"]
    molsys.chemical_states.add_bonds([[0, 1], [1, 2]])
    molsys.structures.coordinates = msm.pyunitwizard.quantity(
        np.arange(27, dtype=float).reshape(3, 3, 3), "nm"
    )
    molsys.structures.time = msm.pyunitwizard.quantity([1.0, 2.0, 3.0], "ps")
    result = msm.convert(molsys, to_form="molsysmt.ViewerJSON")
    result.data["bonds"]["order"] = [1, 2]
    result.data["bonds"]["type"] = ["single", "double"]
    result.data["bonds"]["confidence"] = [0.25, None]
    result.data["atoms"]["partial_charge"] = [None, -0.2, 0.2]
    return result


@pytest.mark.parametrize(
    ("indices", "pairs", "orders", "types"),
    [
        ([1, 2], [[0, 1]], [2], ["double"]),
        ([2, 1], [[1, 0]], [2], ["double"]),
        ([2], [], [], []),
        ([], [], [], []),
    ],
)
def test_atom_subset_remaps_bonds_and_aligned_columns(
    payload, indices, pairs, orders, types
):
    before = deepcopy(payload.data)
    subset = msm.extract(payload, selection=indices, structure_indices=[2, 0])
    bonds = subset.data["bonds"]
    assert bonds["atom_pairs"] == pairs
    assert bonds["indexA"] == [pair[0] for pair in pairs]
    assert bonds["indexB"] == [pair[1] for pair in pairs]
    assert bonds["order"] == orders
    assert bonds["type"] == types
    assert bonds["confidence"] == ([None] if pairs else [])
    assert subset.data["atoms"]["atom_id"] == [
        before["atoms"]["atom_id"][i] for i in indices
    ]
    assert subset.data["atoms"]["partial_charge"] == [
        before["atoms"]["partial_charge"][i] for i in indices
    ]
    assert [structure["time"] for structure in subset.data["structures"]] == [3.0, 1.0]
    assert json.loads(subset.dumps()) == subset.to_dict()
    restored = msm.convert(subset, to_form="molsysmt.MolSys")
    assert restored.topology.n_atoms == len(indices)
    assert restored.chemical_states.get(n_bonds=True) == len(pairs)
    coordinates = msm.pyunitwizard.get_value(
        restored.structures.coordinates, to_unit="nm"
    )
    np.testing.assert_allclose(
        coordinates, np.arange(27).reshape(3, 3, 3)[[2, 0]][:, indices]
    )
    subset.data["structures"][0]["time"] = 99.0
    assert payload.data == before


@pytest.mark.parametrize("structure_key", ["structures", "frames", "estructures"])
def test_structure_selection_preserves_order_and_repetitions(payload, structure_key):
    if structure_key != "structures":
        payload.data[structure_key] = payload.data.pop("structures")
    subset = msm.extract(payload, structure_indices=[2, 0, 2])
    assert [structure["time"] for structure in subset.data["structures"]] == [
        3.0,
        1.0,
        3.0,
    ]
    assert subset.data["bonds"] == payload.data["bonds"]
    empty = msm.extract(payload, structure_indices=[])
    assert empty.data["structures"] == []
    assert empty.data["atoms"] == payload.data["atoms"]


@pytest.mark.parametrize("indices", [[1, 1], [2, 0, 2]])
def test_repeated_atom_indices_are_rejected(payload, indices):
    before = deepcopy(payload.data)
    with pytest.raises(ArgumentError, match="repeat|unique|duplicate"):
        msm.extract(payload, selection=indices)
    assert payload.data == before


@pytest.mark.parametrize("field", ["atom_indices", "structure_indices"])
@pytest.mark.parametrize("indices", [[-1], [3]])
def test_adapter_rejects_out_of_range_indices(payload, field, indices):
    with pytest.raises(ArgumentError, match=field):
        extract(payload, **{field: indices})


@pytest.mark.parametrize("encoding", ["pairs", "legacy", "both"])
def test_endpoint_encodings_are_remapped_together(payload, encoding):
    if encoding == "pairs":
        payload.data["bonds"].pop("indexA")
        payload.data["bonds"].pop("indexB")
    elif encoding == "legacy":
        payload.data["bonds"].pop("atom_pairs")
    subset = msm.extract(payload, selection=[2, 1])
    assert subset.data["bonds"]["atom_pairs"] == [[1, 0]]
    if encoding != "pairs":
        assert subset.data["bonds"]["indexA"] == [1]
        assert subset.data["bonds"]["indexB"] == [0]
    assert msm.get(subset, n_bonds=True) == 1


def test_parallel_bond_sets_are_filtered_independently(payload):
    original = deepcopy(payload.data["bonds"])
    payload.data["bonds"] = {
        "sets": [original, {"atom_pairs": [[0, 2]], "order": [1]}],
        "name": "views",
    }
    subset = msm.extract(payload, selection=[2, 1])
    assert subset.data["bonds"]["name"] == "views"
    assert subset.data["bonds"]["sets"][0]["atom_pairs"] == [[1, 0]]
    assert subset.data["bonds"]["sets"][0]["order"] == [2]
    assert subset.data["bonds"]["sets"][1] == {"atom_pairs": [], "order": []}


@pytest.mark.parametrize("field", ["order", "indexA", "atom_pairs"])
def test_inconsistent_bond_columns_are_rejected(payload, field):
    payload.data["bonds"][field] = [1]
    with pytest.raises(FormatError, match="bond|Bond"):
        msm.extract(payload, selection=[1, 2])


def test_unrestricted_copy_contract_is_preserved(payload):
    assert extract(payload, copy_if_all=False) is payload
    result = extract(payload)
    assert result is not payload
    result.data["atoms"]["atom_id"][0] = "changed"
    assert payload.data["atoms"]["atom_id"][0] == "007"


def test_subset_keeps_independent_wrapper_metadata(payload):
    payload.compression = "gzip"
    payload.compressed = True
    payload.schema["custom"] = "retained"
    subset = msm.extract(payload, selection=[2, 1], copy_if_all=False)
    assert isinstance(subset, ViewerJSON)
    assert subset.compression == "gzip"
    assert subset.compressed is True
    assert subset.schema["custom"] == "retained"
    subset.schema["custom"] = "changed"
    subset.data["atoms"]["atom_id"][0] = "changed"
    assert payload.schema["custom"] == "retained"
    assert payload.data["atoms"]["atom_id"] == ["007", "010", "C"]


def test_subset_does_not_copy_unselected_structure_payloads(payload):
    class Unselected:
        def __deepcopy__(self, memo):
            raise AssertionError("Unselected structure was copied")

    payload.data["structures"][1]["annotation"] = Unselected()
    subset = msm.extract(payload, selection=[1, 2], structure_indices=[0])
    assert len(subset.data["structures"]) == 1
    assert json.loads(subset.dumps())["bonds"]["atom_pairs"] == [[0, 1]]


@pytest.mark.parametrize(
    "target", ["molsysmt.ViewerJSON", "molsysmt.MolSys", "molsysmt.Topology"]
)
def test_target_form_routes_honor_the_same_selection(payload, target):
    result = msm.extract(
        payload, selection=[2, 1], structure_indices=[2, 0], to_form=target
    )
    if target == "molsysmt.ViewerJSON":
        assert result.data["atoms"]["atom_id"] == ["C", "010"]
        assert result.data["bonds"]["atom_pairs"] == [[1, 0]]
        assert [structure["time"] for structure in result.data["structures"]] == [
            3.0,
            1.0,
        ]
    else:
        topo = result.topology if target == "molsysmt.MolSys" else result
        assert topo.atoms["atom_id"].tolist() == ["C", "010"]
        assert msm.get(result, n_bonds=True) == (
            1 if target == "molsysmt.MolSys" else None
        )
        if target == "molsysmt.MolSys":
            np.testing.assert_allclose(
                msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm"),
                np.arange(27).reshape(3, 3, 3)[[2, 0]][:, [2, 1]],
            )
