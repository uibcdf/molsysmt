"""Checking the anchor-relative criterion independently of interaction chemistry."""

import numpy as np
import pytest

from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt.pbc._whole_participants import require_whole_participants


def test_whole_and_single_atom_groups_require_no_internal_images():
    xyz = np.array([[0.9, 0, 0], [0.95, 0, 0], [0.1, 0, 0]])
    require_whole_participants(
        xyz, np.eye(3), np.array([0, 2, 3]), np.array([0, 1, 2]), "test"
    )


def test_split_group_is_rejected_without_modifying_coordinates():
    xyz = np.array([[0.9, 0, 0], [0.05, 0, 0]])
    original = xyz.copy()
    with pytest.raises(NotImplementedMethodError):
        require_whole_participants(
            xyz, np.eye(3), np.array([0, 2]), np.array([0, 1]), "test"
        )
    np.testing.assert_array_equal(xyz, original)
