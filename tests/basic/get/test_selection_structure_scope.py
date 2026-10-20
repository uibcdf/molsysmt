"""Ensure get delegates its requested structures to selection and mask queries."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Structures


@pytest.mark.parametrize("argument", ["selection", "mask"])
def test_spatial_scope_uses_requested_structure(argument):
    molsys = MolSys(n_atoms=3)
    coordinates = np.zeros((2, 3, 3))
    coordinates[:, :, 0] = [[0, 0.1, 2], [0, 2, 0.1]]
    molsys.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(coordinates, "nm")
    )
    scope = {argument: "atom_index != 0 within 0.3 nm of atom_index == 0"}
    first = msm.get(
        molsys, element="atom", structure_indices=0, atom_index=True, **scope
    )
    second = msm.get(
        molsys, element="atom", structure_indices=1, atom_index=True, **scope
    )
    assert first == [1]
    assert second == [2]
