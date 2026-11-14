"""Reject invalid explicit structure scopes before every selection branch."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys


@pytest.fixture(params=["native", "h5msm"])
def source(request, tmp_path):
    molsys = MolSys(n_atoms=2)
    molsys.structures.coordinates = msm.pyunitwizard.quantity(np.zeros((3, 2, 3)), "nm")
    if request.param == "native":
        return molsys
    filename = str(tmp_path / "scope.h5msm")
    msm.convert(molsys, to_form=filename)
    return filename


@pytest.mark.parametrize("selection", [0, [0], "all", "atom_index==0"])
@pytest.mark.parametrize("structure_indices", [[-1], [3]])
def test_all_selection_branches_refuse_invalid_structure_indices(
    source, selection, structure_indices
):
    with pytest.raises(msm.ArgumentError, match="out-of-range structure indices"):
        msm.select(source, selection=selection, structure_indices=structure_indices)


def test_valid_repeated_structure_scope_preserves_numeric_atom_order(source):
    assert msm.select(source, selection=[1, 0], structure_indices=[2, 0, 2]) == [1, 0]
