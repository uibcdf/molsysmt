"""Protect reusable image composition for arbitrary singleton role counts."""

import numpy as np
import pytest

from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.pbc._shared_images import join_shared_images


def test_three_leg_join_rejects_inconsistent_repeated_atom_images():
    left = np.zeros((1, 6, 3), dtype=np.int32)
    right = np.zeros((1, 3, 3), dtype=np.int32)
    right[0, 2] = [1, 0, 0]
    atoms = np.array([[0, 1, 2, 3, 4, 5, 5, 6, 0]], dtype=np.int64)
    with pytest.raises(StructuralInconsistencyError):
        join_shared_images(
            left, right, np.array([5]), np.array([0]), atoms=atoms, caller="test"
        )


def test_arbitrary_role_join_preserves_relative_images_and_rejects_overflow():
    left = np.zeros((6, 3), dtype=np.int64)
    left[5] = [3, 0, 0]
    right = np.array([[[2, 0, 0], [3, 0, 0], [4, 0, 0]]], dtype=np.int64)
    atoms = np.array([[0, 1, 2, 3, 4, 5, 5, 6, 7]], dtype=np.int64)
    joined = join_shared_images(
        left, right, 5, np.array([0]), atoms=atoms, caller="test"
    )
    assert joined.shape == (1, 9, 3) and joined.dtype == np.int32
    np.testing.assert_array_equal(joined[0, 6:, 0], [3, 4, 5])
    right[0, 2, 0] = np.iinfo(np.int32).max
    with pytest.raises(StructuralInconsistencyError):
        join_shared_images(left, right, 5, np.array([0]), atoms=atoms, caller="test")
