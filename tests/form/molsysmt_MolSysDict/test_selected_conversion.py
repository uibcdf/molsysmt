"""Preserving declared axes when a dictionary is reconstructed as MolSys."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys


@pytest.mark.parametrize("operation", [msm.convert, msm.extract])
def test_selected_conversion_preserves_atom_and_structure_correspondence(operation):
    source = MolSys(n_atoms=4)
    source.topology.atoms["atom_id"] = ["10", "20", "30", "40"]
    source.topology.atoms["atom_name"] = ["C", "N", "O", "S"]
    source.topology.atoms["atom_type"] = ["C", "N", "O", "S"]
    values = np.arange(36.0).reshape(3, 4, 3)
    source.structures.coordinates = msm.pyunitwizard.quantity(values, "nm")
    source.structures.structure_id = np.array([10, 20, 30])
    data = msm.convert(source, to_form="molsysmt.MolSysDict")
    original = data.to_dict(copy=True)
    result = operation(
        data,
        selection=[2, 0],
        structure_indices=[2, 0, 2],
        to_form="molsysmt.MolSys",
    )
    assert result.topology.n_atoms == 2
    assert result.topology.atoms["atom_id"].tolist() == ["10", "30"]
    np.testing.assert_array_equal(result.structures.structure_id, [30, 10, 30])
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm"),
        values[np.ix_([2, 0, 2], [0, 2], [0, 1, 2])],
    )
    assert data.to_dict(copy=True) == original


def test_adapter_retains_legacy_positional_skip_argument():
    from molsysmt.form.molsysmt_MolSysDict.to_molsysmt_MolSys import to_molsysmt_MolSys

    source = MolSys(n_atoms=2)
    data = msm.convert(source, to_form="molsysmt.MolSysDict")
    assert to_molsysmt_MolSys(data, False, atom_indices=[1]).topology.n_atoms == 1
