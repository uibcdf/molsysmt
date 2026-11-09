"""Keep numeric stored-charge queries usable across admitted missing markers."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolecularMechanics, MolSys


def _source(dtype="Float64", missing=pd.NA):
    mechanics = MolecularMechanics()
    mechanics.atoms_ff = pd.DataFrame(
        {"partial_charge": pd.array([0.25, missing, -0.25], dtype=dtype)}
    )
    return mechanics


@pytest.mark.parametrize("form", ["mechanics", "molsys", "file"])
def test_mixed_nullable_charges_preserve_selected_order_repetitions_and_missing(
    tmp_path, form
):
    mechanics = _source()
    source = mechanics
    if form != "mechanics":
        source = MolSys(n_atoms=3)
        source.molecular_mechanics = mechanics
    if form == "file":
        path = tmp_path / "nullable.h5msm"
        msm.h5msm.write(source, path, format_version="0.6")
        source = path
    for selection, expected in (
        ("all", [0.25, np.nan, -0.25]),
        ([2, 0, 2], [-0.25, 0.25, -0.25]),
        ([1], [np.nan]),
        ([], []),
    ):
        result = msm.get(
            source, element="atom", selection=selection, partial_charge=True
        )
        assert result.dtype == np.dtype("float64")
        assert result.shape == (len(expected),)
        np.testing.assert_array_equal(result, expected)
        if form == "molsys":
            native = source.get(
                element="atom", selection=selection, partial_charge=True
            )
            np.testing.assert_array_equal(native, expected)
    pd.testing.assert_frame_equal(mechanics.atoms_ff, _source().atoms_ff)


@pytest.mark.parametrize(
    "dtype,missing",
    [
        ("Float32", pd.NA),
        (object, pd.NA),
        (object, None),
        (object, np.nan),
        ("float64", np.nan),
    ],
)
def test_supported_nullable_columns_return_detached_numeric_arrays(dtype, missing):
    source = _source(dtype, missing)
    before = source.atoms_ff.copy(deep=True)
    result = msm.get(source, element="atom", partial_charge=True)
    np.testing.assert_array_equal(result, [0.25, np.nan, -0.25])
    assert result.dtype == np.dtype("float64")
    result[0] = 99
    pd.testing.assert_frame_equal(source.atoms_ff, before)


@pytest.mark.parametrize("values", [[pd.NA] * 3, [None] * 3, [np.nan] * 3])
def test_entirely_missing_charge_columns_keep_the_existing_none_contract(values):
    source = MolecularMechanics(partial_charge=values)
    assert msm.get(source, element="atom", partial_charge=True) is None
