"""Preserve declared legacy inventories through structure-only selection."""

import pytest

import molsysmt as msm


@pytest.mark.parametrize("structure_indices", ["all", [1]])
@pytest.mark.parametrize("copy_if_all", [True, False])
def test_atom_free_legacy_inventory_survives_structure_selection(
    structure_indices, copy_if_all
):
    source = msm.MolSysDict(
        data={
            "format": "molsysmt",
            "kind": "molsys",
            "version": "0.1",
            "metadata": {"source": ["original"]},
            "topology": {
                "atoms": [],
                "groups": [{"group_name": "ALA", "group_id": "07", "atom_indices": []}],
                "chains": [{"chain_id": "A", "group_indices": [0]}],
            },
            "structures": {"time": [2.0, 4.0], "structure_id": [10, 20]},
        }
    )
    result = msm.extract(
        source, structure_indices=structure_indices, copy_if_all=copy_if_all
    )
    assert result.data["topology"] == source.data["topology"]
    assert result.data["structures"] == (
        source.data["structures"]
        if structure_indices == "all"
        else {"time": [4.0], "structure_id": [20]}
    )
    alias = structure_indices == "all" and not copy_if_all
    assert (result is source) == alias
    if not alias:
        result.data["metadata"]["source"].append("changed")
        result.data["topology"]["groups"][0]["group_name"] = "GLY"
        assert source.data["metadata"] == {"source": ["original"]}
        assert source.data["topology"]["groups"][0]["group_name"] == "ALA"
