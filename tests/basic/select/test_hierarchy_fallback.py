"""Protecting public hierarchy selection through real attribute delivery routes."""

import numpy as np
import pytest

import molsysmt as msm


@pytest.mark.parametrize(
    "element", ["group", "component", "chain", "molecule", "entity"]
)
def test_file_pdb_rich_hierarchy_selection_matches_native_delivery(element):
    source = msm.systems["T4 lysozyme L99A"]["181l.pdb"]
    native = msm.convert(source, to_form="molsysmt.MolSys")
    selection = 'group_name=="ALA"'
    atoms = msm.select(native, selection=selection)
    expected = np.unique(
        msm.get(native, selection=atoms, **{element + "_index": True})
    ).tolist()
    assert msm.select(source, element=element, selection=selection) == expected
    assert msm.select(source, element=element, selection="atom_index==-1") == []


def test_nested_atom_selections_preserve_hierarchy_result_groups(monkeypatch):
    from molsysmt.basic.selector import _dict_select

    source = msm.systems["T4 lysozyme L99A"]["181l.pdb"]
    monkeypatch.setitem(_dict_select, "MolSysMT", lambda *args: [[0, 1], [3, 4]])
    assert msm.select(source, element="group", selection="nested") == [[0], [0]]
