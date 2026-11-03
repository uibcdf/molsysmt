"""Preserve typed state-local component labels through public extraction (#531)."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import Structures, Topology


def _column(dtype, values):
    missing = pd.isna(values)
    storage = np.str_ if dtype in {"string", "object"} else dtype.lower()
    fill = "" if dtype in {"string", "object"} else 0
    return {
        "dtype": dtype,
        "values": np.asarray(
            [fill if absent else value for value, absent in zip(values, missing)],
            dtype=storage,
        ),
        "null_mask": np.asarray(missing, dtype=bool),
    }


def _system(label_dtype="string", connectivity="complete"):
    """Declare two literal components without deriving expectations from inference."""
    record = {
        "state_id": "declared",
        "connectivity_completeness": connectivity,
        "component_completeness": "complete",
        "component_evidence": "explicit",
        "provenance_index": None,
        "component_indices": _column("Int64", [0, 0, 0, 1, 1]),
        "components": {
            "n_rows": 2,
            "columns": {
                "component_id": _column("string", ["whole-A", "whole-B"]),
                "component_name": _column(label_dtype, ["α chain", None]),
                "component_type": _column(label_dtype, ["peptide", "small molecule"]),
            },
        },
        "atom_attributes": {"n_rows": 5, "columns": {}},
        "bonds": {
            "n_rows": 3,
            "columns": {
                "atom1_index": _column("Int64", [0, 1, 3]),
                "atom2_index": _column("Int64", [1, 2, 4]),
                "bond_order": _column("UInt8", [1, 1, 1]),
                "bond_type": _column("string", ["covalent"] * 3),
            },
        },
    }
    payload = msm.ChemicalStatesDict(
        {
            "schema": "molsysmt.chemical_states_dict",
            "version": 1,
            "n_atoms": 5,
            "reference_chemical_state_index": 0,
            "states": [record],
        }
    )
    topology = Topology(n_atoms=5)
    topology.atoms["atom_id"] = pd.array(["a0", "a1", "a2", "a3", "a4"], dtype="string")
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.arange(60).reshape(4, 5, 3), "nm")
    )
    states = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    return msm.convert([topology, states, structures], to_form="molsysmt.MolSys")


def _columns(system, state_index=0):
    payload = msm.convert(system.chemical_states, to_form="molsysmt.ChemicalStatesDict")
    return payload.to_dict()["states"][state_index]["components"]["columns"]


def _assert_columns(system, ids, names, types, dtype, state_index=0):
    columns = _columns(system, state_index)
    for name, expected, expected_dtype in [
        ("component_id", ids, "string"),
        ("component_name", names, dtype),
        ("component_type", types, dtype),
    ]:
        column = columns[name]
        assert column["dtype"] == expected_dtype
        np.testing.assert_array_equal(column["null_mask"], pd.isna(expected))
        assert column["values"].tolist() == ["" if v is None else v for v in expected]


@pytest.mark.parametrize("dtype", ["string", "object"])
@pytest.mark.parametrize("route", ["basic", "native"])
@pytest.mark.parametrize(
    "indices,ids,names,types,membership,pairs",
    [
        ([3, 4], ["whole-B"], [None], ["small molecule"], [0, 0], [[0, 1]]),
        ([0, 2], ["0", "1"], [None, None], [None, None], [0, 1], []),
        (
            [0, 1, 3, 4],
            ["0", "whole-B"],
            [None, None],
            [None, "small molecule"],
            [0, 0, 1, 1],
            [[0, 1], [2, 3]],
        ),
        ([], [], [], [], [], []),
    ],
)
def test_public_extraction_preserves_typed_labels_and_induced_correspondence(
    dtype, route, indices, ids, names, types, membership, pairs
):
    source = _system(dtype)
    before = source.chemical_states._states[0].components.copy(deep=True)
    coordinates = msm.pyunitwizard.get_value(
        msm.get(source, coordinates=True), to_unit="nm"
    ).copy()
    selected = (
        msm.extract(source, selection=indices)
        if route == "basic"
        else source.extract(atom_indices=indices)
    )
    _assert_columns(selected, ids, names, types, dtype)
    assert selected.get(element="atom", component_index=True) == membership
    assert selected.get(element="atom", atom_id=True) == [f"a{i}" for i in indices]
    assert (
        selected.chemical_states.get_bonds()[
            ["atom1_index", "atom2_index"]
        ].values.tolist()
        == pairs
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(msm.get(selected, coordinates=True), to_unit="nm"),
        coordinates[:, indices, :],
    )
    pd.testing.assert_frame_equal(source.chemical_states._states[0].components, before)
    _assert_columns(
        source,
        ["whole-A", "whole-B"],
        ["α chain", None],
        ["peptide", "small molecule"],
        dtype,
    )


@pytest.mark.parametrize("connectivity", ["partial", "unavailable"])
def test_incomplete_graph_keeps_declared_typed_labels_without_reconstruction(
    connectivity,
):
    source = _system(connectivity=connectivity)
    selected = msm.extract(source, selection=[2, 0])
    _assert_columns(selected, ["whole-A"], ["α chain"], ["peptide"], "string")
    assert selected.get(element="atom", component_index=True) == [0, 0]
    assert selected.get(component_completeness=True) == "partial"


def test_independent_state_dtypes_and_nonconsecutive_structures_are_preserved():
    source = _system()
    payload = msm.convert(source.chemical_states, to_form="molsysmt.ChemicalStatesDict")
    second = deepcopy(payload.data["states"][0])
    second["state_id"] = "second"
    for name in ("component_name", "component_type"):
        second["components"]["columns"][name]["dtype"] = "object"
    payload.data["states"].append(second)
    payload.data["reference_chemical_state_index"] = 1
    source.chemical_states = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    msm.set(source, structure_chemical_state_index=[0, 1, 0, 1])
    selected = msm.extract(source, selection=[3, 4], structure_indices=[3, 0])
    for index, dtype in enumerate(["string", "object"]):
        _assert_columns(selected, ["whole-B"], [None], ["small molecule"], dtype, index)
    assert selected.chemical_states.reference_chemical_state_index == 1
    assert selected.get(structure_chemical_state_index=True) == [1, 0]
    assert source.get(structure_chemical_state_index=True) == [0, 1, 0, 1]


def test_public_merge_then_extract_and_dictionary_h5msm_roundtrips(tmp_path):
    source = _system()
    original = source.chemical_states._states[0].components.copy(deep=True)
    merged = msm.merge([source, source], keep_ids=True)
    merged_before = merged.chemical_states._states[0].components.copy(deep=True)
    selected = msm.extract(merged, selection=[5, 6, 7, 8, 9])
    # Group-free union has no stable context from which to infer labels.
    _assert_columns(
        selected, ["whole-A", "whole-B"], [None, None], [None, None], "string"
    )
    assert selected.get(element="atom", component_index=True) == [0, 0, 0, 1, 1]
    assert selected.get(element="atom", atom_id=True) == ["a0", "a1", "a2", "a3", "a4"]
    for restored in [
        msm.convert(
            msm.convert(selected, to_form="molsysmt.MolSysDict"),
            to_form="molsysmt.MolSys",
        ),
        msm.convert(
            msm.convert(selected, to_form=str(tmp_path / "selected.h5msm")),
            to_form="molsysmt.MolSys",
        ),
    ]:
        _assert_columns(
            restored, ["whole-A", "whole-B"], [None, None], [None, None], "string"
        )
        assert restored.get(element="atom", component_index=True) == [0, 0, 0, 1, 1]
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].components, original
    )
    pd.testing.assert_frame_equal(
        merged.chemical_states._states[0].components, merged_before
    )


@pytest.mark.parametrize("dtype", ["string", "object"])
def test_public_permutation_preserves_typed_component_labels(dtype):
    source = _system(dtype)
    selected = msm.permute_atoms(source, atom_indices=[4, 3, 2, 1, 0])
    _assert_columns(
        selected,
        ["whole-A", "whole-B"],
        ["α chain", None],
        ["peptide", "small molecule"],
        dtype,
    )
    assert selected.get(element="atom", component_index=True) == [1, 1, 0, 0, 0]
    assert selected.get(element="atom", atom_id=True) == ["a4", "a3", "a2", "a1", "a0"]


def test_reported_rdkit_conversion_and_extraction_preserve_string_descriptors():
    pytest.importorskip("rdkit")
    source = msm.convert(
        msm.convert("smiles:CC.CC", to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
    )
    selected = msm.extract(source, selection=[0, 1])
    for system in [source, selected]:
        columns = _columns(system)
        assert columns["component_name"]["dtype"] == "string"
        assert columns["component_type"]["dtype"] == "string"
