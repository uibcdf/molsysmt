"""Selecting the structure axis of system-level alternate-site queries."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys


@pytest.mark.parametrize(
    "structure_indices, expected",
    [([2, 0, 2], [[1], [0], [1]]), ([1], [[]]), ([], [])],
)
def test_system_alternate_location_preserves_structure_selection(
    structure_indices, expected
):
    molsys = MolSys(n_atoms=2)
    molsys.structures.coordinates = msm.pyunitwizard.quantity(np.zeros((3, 2, 3)), "nm")
    molsys.structures.alternate_location = [
        {0: {"atom_id": ["100"]}},
        {},
        {1: {"atom_id": ["200"]}},
    ]
    result = msm.get(
        molsys,
        element="system",
        structure_indices=structure_indices,
        alternate_location=True,
    )
    assert [list(sites) for sites in result] == expected
    assert [list(sites) for sites in molsys.structures.alternate_location] == [
        [0],
        [],
        [1],
    ]
