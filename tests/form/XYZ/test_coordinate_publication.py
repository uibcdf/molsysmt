"""Protect the public coordinate-publication boundary, not only transform callers."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralInconsistencyError


@pytest.mark.parametrize("rank", [1, 2, 3])
def test_set_coordinates_accepts_each_declared_xyz_rank(rank):
    shape = (3,) if rank == 1 else (2, 3) if rank == 2 else (2, 2, 3)
    source = puw.quantity(np.zeros(shape), "angstrom")
    target = np.full((1, 1, 3), 0.125)
    msm.set(
        source,
        selection=[0],
        structure_indices=[0],
        coordinates=puw.quantity(target, "nm"),
    )
    actual = puw.get_value(source, to_unit="nm")
    expected = np.zeros(shape)
    expected.reshape((-1, 1 if rank == 1 else 2, 3))[0, 0] = 0.125
    np.testing.assert_allclose(actual, expected)


@pytest.mark.parametrize("rank", [1, 2, 3])
def test_integer_xyz_rejects_fractional_publication_without_editing_any_atom(rank):
    shape = (3,) if rank == 1 else (2, 3) if rank == 2 else (2, 2, 3)
    source = puw.quantity(np.zeros(shape, dtype=np.int64), "nm")
    before = puw.get_value(source).copy()
    with pytest.raises(StructuralInconsistencyError, match="integer"):
        msm.set(source, coordinates=puw.quantity(np.full(shape, 0.25), "nm"))
    np.testing.assert_array_equal(puw.get_value(source), before)
