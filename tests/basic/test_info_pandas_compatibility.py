"""Keeping public summaries usable with strict provider deprecation policies."""

import warnings

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Structures


@pytest.mark.parametrize("source_kind", ["molsys", "structures", "water"])
@pytest.mark.parametrize("output_type", ["dataframe", "dictionary", "styler"])
def test_info_preserves_summary_without_future_warnings(source_kind, output_type):
    n_atoms = 3 if source_kind == "water" else 2
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((2, n_atoms, 3)), "nm")
    )
    source = structures
    if source_kind == "molsys":
        source = MolSys(n_atoms=2)
        source.structures = structures
    elif source_kind == "water":
        builder = msm.MolSysBuilder()
        atoms = [
            builder.add_atom(atom_name=name, atom_type=element)
            for name, element in [("O", "O"), ("H1", "H"), ("H2", "H")]
        ]
        group = builder.add_group(atoms, group_name="HOH")
        builder.add_molecule([group], molecule_type="water")
        source = builder.build()
        source.structures = structures

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = msm.info(source, output_type=output_type)
        native_result = source.info(output_type=output_type)
        if output_type == "styler":
            assert 'class="dataframe"' in result.to_html()
            result, native_result = result.data, native_result.data
        if output_type == "dictionary":
            assert result == native_result
            assert result[0]["n_atoms"] == n_atoms
            assert result[0]["n_structures"] == 2
        else:
            pd.testing.assert_frame_equal(result, native_result)
            assert result["n_atoms"].tolist() == [n_atoms]
            assert result["n_structures"].tolist() == [2]

    columns = result[0] if output_type == "dictionary" else result.columns
    if source_kind == "water":
        value = (
            result[0]["n_waters"]
            if output_type == "dictionary"
            else result["n_waters"].iloc[0]
        )
        assert value == 1
    else:
        assert "n_waters" not in columns
    assert "n_ions" not in columns
