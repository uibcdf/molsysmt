"""Preserving partial hierarchy after protein and ligand composition."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm


@pytest.fixture
def joined():
    protein = msm.convert(
        msm.systems["chicken villin HP35"]["1vii.pdb"],
        structure_indices=[0],
        to_form="molsysmt.MolSys",
    )
    ligand = msm.convert(
        msm.systems["caffeine"]["caffeine.sdf"], to_form="molsysmt.MolSys"
    )
    expected = {
        f"{level}_{attribute}": msm.get(
            protein, element="atom", **{f"{level}_{attribute}": True}
        )
        for level in ["group"]
        for attribute in ["id", "name", "type", "index"]
    }
    ligand_parents = {
        f"{level}_{attribute}": msm.get(
            ligand, element="atom", **{f"{level}_{attribute}": True}
        )
        for level in ("molecule", "entity")
        for attribute in ("index", "id", "name", "type")
    }
    offsets = {
        "molecule_index": protein.topology.n_molecules,
        "entity_index": protein.topology.n_entities,
    }
    for attribute, offset in offsets.items():
        ligand_parents[attribute] = [
            value + offset for value in ligand_parents[attribute]
        ]
    msm.add(protein, ligand, keep_ids=True, in_place=True)
    return protein, expected, ligand_parents


def assert_mapped(source, expected):
    for attribute, values in expected.items():
        result = msm.get(source, element="atom", **{attribute: True})
        assert len(result) == 620
        assert result[:596] == values
        assert all(pd.isna(value) for value in result[596:])


def test_public_composition_preserves_real_and_unknown_atom_parents(joined):
    source, expected, ligand_parents = joined
    assert_mapped(source, expected)
    for level in ["molecule", "entity"]:
        for attribute in ["index", "id", "name", "type"]:
            values = msm.get(source, element="atom", **{f"{level}_{attribute}": True})
            assert len(values) == 620
            assert all(pd.notna(value) for value in values[:596])
            assert values[596:] == ligand_parents[f"{level}_{attribute}"]
    assert source.topology.atoms["group_index"].isna().sum() == 24
    assert source.topology.n_groups == 36
    selected = msm.get(source, element="atom", selection=[0, 596, 619], group_id=True)
    assert selected == [expected["group_id"][0], None, None]
    assert msm.get(source, element="atom", selection=[], group_id=True) == []


def test_partial_hierarchy_survives_extraction_and_h5msm(joined, tmp_path):
    source, expected, ligand_parents = joined
    path = tmp_path / "partial.h5msm"
    msm.convert(source, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    assert_mapped(restored, expected)
    selected = msm.extract(restored, selection=[0, 596, 619])
    result = msm.get(selected, element="atom", group_id=True)
    assert result == [expected["group_id"][0], None, None]
    np.testing.assert_array_equal(
        selected.topology.atoms["group_index"].isna(), [False, True, True]
    )
