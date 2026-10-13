"""Selecting native B-factor rows through public source structure indices."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.fixture
def molecular_system_with_factors(hp35_pdb_molsys):
    source = msm.extract(hp35_pdb_molsys, selection=[0, 1, 2])
    second = msm.copy(source)
    msm.append_structures(source, second)
    msm.append_structures(source, second)
    factors = np.array([[1, 2, 3], [11, 12, 13], [21, 22, 23]], dtype=float)
    msm.set(source, b_factor=puw.quantity(factors, "angstrom**2"))
    return source, factors / 100


@pytest.mark.parametrize("selection", [0, 2, [2, 0], [1, 1, 0], []])
@pytest.mark.parametrize("element", ["system", "atom"])
def test_public_b_factor_query_retains_requested_rows(
    selection, element, molecular_system_with_factors
):
    source, factors = molecular_system_with_factors
    rows = np.atleast_1d(selection).astype(int)
    result = msm.get(
        source, element=element, structure_indices=selection, b_factor=True
    )
    np.testing.assert_array_equal(puw.get_value(result, to_unit="nm**2"), factors[rows])
    assert puw.check(result, dimensionality={"[L]": 2})


def test_mixed_query_and_extract_agree_on_both_axes(molecular_system_with_factors):
    source, factors = molecular_system_with_factors
    coordinates, selected = msm.get(
        source,
        element="atom",
        selection=[0, 2],
        structure_indices=[2, 0, 2],
        coordinates=True,
        b_factor=True,
    )
    assert puw.get_value(coordinates).shape == (3, 2, 3)
    np.testing.assert_array_equal(
        puw.get_value(selected, to_unit="nm**2"), factors[np.ix_([2, 0, 2], [0, 2])]
    )
    extracted = msm.extract(source, selection=[0, 2], structure_indices=[2, 0, 2])
    np.testing.assert_array_equal(
        puw.get_value(msm.get(extracted, b_factor=True), to_unit="nm**2"),
        puw.get_value(selected, to_unit="nm**2"),
    )


def test_b_factors_obey_nondefault_length_policy(molecular_system_with_factors):
    source, factors = molecular_system_with_factors
    puw.configure.set_standard_units(
        [
            "angstrom",
            "ps",
            "K",
            "mole",
            "dalton",
            "e",
            "kJ/mol",
            "kJ/(mol*angstrom)",
            "kJ/(mol*angstrom**2)",
            "radians",
        ]
    )
    result = msm.get(source, structure_indices=[2, 0], b_factor=True)
    assert puw.has_unit(result, "angstrom**2") is True
    np.testing.assert_allclose(
        puw.get_value(result, to_unit="angstrom**2"), factors[[2, 0]] * 100
    )


def test_b_factor_h5msm_roundtrip_preserves_query_rows(
    molecular_system_with_factors, tmp_path
):
    source, factors = molecular_system_with_factors
    path = str(tmp_path / "factors.h5msm")
    msm.convert(source, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    result = msm.get(restored, structure_indices=[2, 0, 2], b_factor=True)
    np.testing.assert_array_equal(
        puw.get_value(result, to_unit="nm**2"), factors[[2, 0, 2]]
    )
