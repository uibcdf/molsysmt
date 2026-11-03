"""Checking legacy graphics bond imports against literal connectivity."""

from copy import deepcopy

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError
from molsysmt.form.molsysmt_ViewerJSON.has_attribute import has_attribute
from molsysmt.native import ViewerJSON


def _payload(bonds):
    return ViewerJSON(
        data={
            "atoms": {
                "atom_id": ["A", "B", "C"],
                "atom_name": ["C", "N", "O"],
                "element_symbol": ["C", "N", "O"],
            },
            "bonds": bonds,
        }
    )


@pytest.mark.parametrize("encoding", ["pairs", "legacy", "both"])
@pytest.mark.parametrize("wrapped", [False, True])
def test_direct_import_preserves_literal_endpoints_and_orders(encoding, wrapped):
    bonds = {"order": [2, 1], "type": ["double", "single"]}
    if encoding != "legacy":
        bonds["atom_pairs"] = [[0, 2], [1, 2]]
    if encoding != "pairs":
        bonds.update(indexA=[0, 1], indexB=[2, 2])
    payload = _payload({"sets": [bonds]} if wrapped else bonds)
    before = deepcopy(payload.data)
    assert msm.get(payload, n_bonds=True) == 2
    assert has_attribute(payload, attribute="bonded_atoms") is True
    assert msm.get(payload, element="bond", bond_order=True) == [2, 1]
    assert msm.get(payload, element="bond", bond_type=True) == ["double", "single"]
    topo = msm.convert(payload, to_form="molsysmt.MolSys")
    assert topo.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [
        [0, 2],
        [1, 2],
    ]
    assert topo.chemical_states.get_bonds()["bond_order"].tolist() == [2, 1]
    assert payload.data == before


@pytest.mark.parametrize(
    ("bonds", "expected"),
    [
        ({}, 0),
        (None, 0),
        ({"atom_pairs": [], "order": []}, 0),
        ({"indexA": [], "indexB": [], "order": []}, 0),
        ({"sets": []}, 0),
        ({"sets": [{}]}, 0),
        ({"sets": [{"atom_pairs": []}]}, 0),
        (
            {
                "atom_pairs": [],
                "order": [],
                "sets": [{"atom_pairs": [[0, 2]], "order": [2]}],
            },
            1,
        ),
    ],
)
def test_empty_and_placeholder_wrappers_have_explicit_bond_counts(bonds, expected):
    payload = _payload(bonds)
    assert msm.get(payload, n_bonds=True) == expected
    assert msm.convert(payload, to_form="molsysmt.MolSys").get(n_bonds=True) == expected


@pytest.mark.parametrize(
    "operation", ["convert", "count", "order", "type", "availability"]
)
def test_multiple_bond_sets_require_explicit_selection(operation):
    payload = _payload(
        {
            "sets": [
                {"atom_pairs": [[0, 1]], "order": [1]},
                {"atom_pairs": [[1, 2]], "order": [2]},
            ]
        }
    )
    before = deepcopy(payload.data)
    with pytest.raises(
        FormatError, match="[Mm]ultiple bond sets|more than one bond set"
    ):
        if operation == "convert":
            msm.convert(payload, to_form="molsysmt.MolSys")
        elif operation == "count":
            msm.get(payload, n_bonds=True)
        elif operation == "availability":
            has_attribute(payload, attribute="bonded_atoms")
        else:
            msm.get(payload, element="bond", **{f"bond_{operation}": True})
    assert payload.data == before


def test_explicit_set_selection_imports_only_the_declared_connectivity():
    payload = _payload(
        {
            "sets": [
                {"atom_pairs": [[0, 1]], "order": [1]},
                {"indexA": [1], "indexB": [2], "order": [2]},
            ]
        }
    )
    chosen = payload.copy()
    chosen.data["bonds"] = chosen.data["bonds"]["sets"][1]
    topo = msm.convert(chosen, to_form="molsysmt.MolSys")
    assert topo.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[1, 2]]
    assert topo.chemical_states.get_bonds()["bond_order"].tolist() == [2]
    graphics = msm.extract(payload, selection=[2, 1])
    assert graphics.data["bonds"]["sets"][0]["atom_pairs"] == []
    assert graphics.data["bonds"]["sets"][1]["atom_pairs"] == [[1, 0]]
    assert len(payload.data["bonds"]["sets"]) == 2


@pytest.mark.parametrize(
    "bonds",
    [
        {"indexA": [0]},
        {"indexA": [0], "indexB": [1, 2]},
        {"atom_pairs": [[0, 2]], "indexA": [0], "indexB": [1]},
        {"atom_pairs": [[0, 3]]},
        {"atom_pairs": [[0, 0.5]]},
        {"atom_pairs": [[False, 2]]},
        {"atom_pairs": [[0]]},
        {"atom_pairs": [[0, 2]], "order": [1, 2]},
        {"atom_pairs": [[0, 2]], "type": ["a", "b"]},
        {"order": [1]},
        {"sets": "invalid"},
        {"sets": [{"atom_pairs": [[0, 2]]}], "atom_pairs": [[0, 1]]},
    ],
)
@pytest.mark.parametrize("operation", ["convert", "count"])
def test_invalid_bond_encodings_fail_consistently(bonds, operation):
    payload = _payload(bonds)
    with pytest.raises(FormatError, match="[Bb]ond"):
        if operation == "convert":
            msm.convert(payload, to_form="molsysmt.MolSys")
        else:
            msm.get(payload, n_bonds=True)


def test_nullable_orders_and_unique_nested_wrappers_are_preserved():
    payload = _payload(
        {
            "sets": [
                {
                    "sets": [
                        {
                            "indexA": [0, 1],
                            "indexB": [1, 2],
                            "order": [None, 2],
                            "type": [],
                        }
                    ]
                }
            ]
        }
    )
    assert msm.get(payload, element="bond", bond_order=True) == [None, 2]
    topo = msm.convert(payload, to_form="molsysmt.MolSys")
    assert topo.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [
        [0, 1],
        [1, 2],
    ]
    assert topo.chemical_states.get_bonds()["bond_order"].isna().tolist() == [
        True,
        False,
    ]
    assert topo.chemical_states.get_bonds().loc[1, "bond_order"] == 2
