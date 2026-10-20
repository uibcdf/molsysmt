"""Scoped summary contracts using the public selection-mask semantics."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm


def test_atom_mask_intersects_and_retains_source_indices(t4_h5msm_molsys):
    result = msm.info(
        t4_h5msm_molsys,
        element="atom",
        selection=[9, 3, 8],
        mask=[9, 3, 3],
        output_type="dataframe",
    )
    assert result["index"].tolist() == [3, 9]
    expected = msm.info(
        t4_h5msm_molsys, element="atom", selection=[3, 9], output_type="dataframe"
    )
    pd.testing.assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "element", ["atom", "group", "component", "chain", "molecule", "entity"]
)
def test_mask_uses_the_requested_element_axis(t4_h5msm_molsys, element):
    result = msm.info(
        t4_h5msm_molsys,
        element=element,
        selection="all",
        mask=[1, 0],
        output_type="dataframe",
    )
    assert result["index"].tolist() == [0, 1]
    expected = msm.info(
        t4_h5msm_molsys, element=element, selection=[0, 1], output_type="dataframe"
    )
    pd.testing.assert_frame_equal(result, expected)


def test_boolean_and_expression_group_masks(t4_h5msm_molsys):
    n_groups = msm.get(t4_h5msm_molsys, n_groups=True)
    mask = np.zeros(n_groups, dtype=bool)
    mask[[2, 5]] = True
    boolean = msm.info(
        t4_h5msm_molsys, element="group", mask=mask, output_type="dataframe"
    )
    expression = msm.info(
        t4_h5msm_molsys,
        element="group",
        selection="group_index<4",
        mask="group_index>=2",
        output_type="dataframe",
    )
    assert boolean["index"].tolist() == [2, 5]
    assert expression["index"].tolist() == [2, 3]


@pytest.mark.parametrize("output_type", ["styler", "dataframe", "dictionary"])
def test_empty_mask_preserves_output_schema(t4_h5msm_molsys, output_type):
    result = msm.info(t4_h5msm_molsys, element="atom", mask=[], output_type=output_type)
    if output_type == "dictionary":
        assert result == []
    else:
        table = result.data if output_type == "styler" else result
        assert table.empty
        assert "index" in table.columns and "group index" in table.columns


@pytest.mark.parametrize("mask", [None, "all"])
def test_unrestricted_mask_preserves_existing_selection_order(t4_h5msm_molsys, mask):
    result = msm.info(
        t4_h5msm_molsys,
        element="atom",
        selection=[9, 3, 8],
        mask=mask,
        output_type="dataframe",
    )
    assert result["index"].tolist() == [9, 3, 8]


def test_system_mask_summarizes_atoms_and_keeps_structure_axis(t4_h5msm_molsys):
    result = msm.info(
        t4_h5msm_molsys,
        selection=[0, 1, 10],
        mask=[1, 10],
        structure_indices=[0, 0],
        output_type="dataframe",
    )
    assert result["n_atoms"].tolist() == [2]
    assert result["n_structures"].tolist() == [2]
    expected = msm.info(
        t4_h5msm_molsys,
        selection=[1, 10],
        structure_indices=[0, 0],
        output_type="dataframe",
    )
    pd.testing.assert_frame_equal(result, expected)


@pytest.mark.parametrize("mask", [[-1], [100000], [True, False], [[0, 1]], {"atom": 0}])
def test_invalid_masks_raise_catalog_argument_errors(t4_h5msm_molsys, mask):
    with pytest.raises(msm.ArgumentError):
        msm.info(t4_h5msm_molsys, element="group", mask=mask)


def test_atom_mask_is_not_silently_reinterpreted_as_group_indices(t4_h5msm_molsys):
    n_groups = msm.get(t4_h5msm_molsys, n_groups=True)
    assert n_groups < msm.get(t4_h5msm_molsys, n_atoms=True)
    with pytest.raises(msm.ArgumentError):
        msm.info(t4_h5msm_molsys, element="group", mask=[n_groups])


def test_native_shortcut_forwards_mask_and_validation(t4_h5msm_molsys):
    result = t4_h5msm_molsys.info(element="groups", selection=[0, 1, 2], mask=[1])
    assert result.data["index"].tolist() == [1]
    with pytest.raises(msm.ArgumentError):
        t4_h5msm_molsys.info(element="group", mask=[-1])


@pytest.mark.parametrize("form", ["file:pdb", "molsysmt.Topology", "molsysmt.MolSys"])
def test_masks_are_form_agnostic(form):
    filename = msm.systems["T4 lysozyme L99A"]["181l.pdb"]
    molsys = filename if form == "file:pdb" else msm.convert(filename, to_form=form)
    table = msm.info(molsys, element="atom", mask=[0, 3], output_type="dataframe")
    assert table["index"].tolist() == [0, 3]


def test_mask_with_explicit_trusted_delegation(t4_h5msm_molsys):
    table = msm.info(
        t4_h5msm_molsys,
        element="atom",
        selection=[0, 1, 2],
        mask=[1, 2],
        output_type="dataframe",
        skip_digestion=True,
    )
    assert table["index"].tolist() == [1, 2]


def test_mask_preserves_legacy_positional_calls(t4_h5msm_molsys):
    table = msm.info(
        t4_h5msm_molsys,
        "atom",
        [0, 1],
        "all",
        "MolSysMT",
        "dataframe",
        False,
        mask=[1],
    )
    assert table["index"].tolist() == [1]
    assert t4_h5msm_molsys.info("atom", [0, 1], "MolSysMT", False, mask=[1]).data[
        "index"
    ].tolist() == [1]


def test_complementary_forms_and_source_values_are_preserved(t4_h5msm_molsys):
    molsys = t4_h5msm_molsys
    atoms = molsys.topology.atoms.copy(deep=True)
    coordinates = msm.pyunitwizard.get_value(molsys.structures.coordinates).copy()
    table = msm.info(
        [molsys.topology, molsys.structures],
        element="atom",
        mask=[0, 3],
        output_type="dataframe",
    )
    assert table["index"].tolist() == [0, 3]
    pd.testing.assert_frame_equal(molsys.topology.atoms, atoms)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(molsys.structures.coordinates), coordinates
    )
