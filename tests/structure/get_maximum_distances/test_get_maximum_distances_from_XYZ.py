"""
Unit and regression tests for get_maximum_distances on XYZ molecular systems.
Covers as_entity=False, as_entity_2=False, and pairs=True branches.
"""

import molsysmt as msm
from molsysmt import systems, pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentConflictError
import numpy as np
import pytest


def _get_molsys():
    return msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')


def test_as_entity_false_as_entity_2_true():
    """Lines 114-128: each atom in sel1 paired with its farthest atom in sel2."""
    molsys = _get_molsys()
    pairs, dists = msm.structure.get_maximum_distances(
        molsys,
        selection=[0, 1, 2],
        selection_2=[0, 1, 2, 3],
        as_entity=False,
        as_entity_2=True,
        structure_indices=[1],
    )
    dists_nm = puw.get_value(dists, to_unit='nm')
    assert pairs.shape == (1, 3)
    assert dists_nm.shape == (1, 3)
    assert np.array_equal(pairs[0], [2, 0, 0])
    assert np.allclose(dists_nm[0], [3.74165739, 3.46410162, 3.74165739], atol=1e-5)


def test_as_entity_true_as_entity_2_false():
    """Lines 130-144: each atom in sel2 paired with its farthest atom in sel1."""
    molsys = _get_molsys()
    pairs, dists = msm.structure.get_maximum_distances(
        molsys,
        selection=[0, 1, 2],
        selection_2=[0, 1, 2, 3],
        as_entity=True,
        as_entity_2=False,
        structure_indices=[1],
    )
    dists_nm = puw.get_value(dists, to_unit='nm')
    assert pairs.shape == (1, 4)
    assert dists_nm.shape == (1, 4)
    assert np.array_equal(pairs[0], [2, 0, 0, 0])
    assert np.allclose(dists_nm[0], [3.74165739, 3.46410162, 3.74165739, 2.44948974], atol=1e-5)


def test_as_entity_false_as_entity_2_false_raises():
    """Lines 146-152: both as_entity=False raises ArgumentConflictError."""
    molsys = _get_molsys()
    with pytest.raises(ArgumentConflictError):
        msm.structure.get_maximum_distances(
            molsys,
            selection=[0, 1, 2],
            selection_2=[0, 1, 2, 3],
            as_entity=False,
            as_entity_2=False,
            structure_indices=[1],
        )


def test_pairs_true_as_entity_true():
    """Lines 154-173: pairs=True returns index and distance of the maximum pair."""
    molsys = _get_molsys()
    pairs, dists = msm.structure.get_maximum_distances(
        molsys,
        selection=[0, 0, 1, 1, 2],
        selection_2=[1, 2, 2, 3, 3],
        pairs=True,
        structure_indices=[1],
    )
    dists_nm = puw.get_value(dists, to_unit='nm')
    assert np.array_equal(pairs, [1])
    assert np.allclose(dists_nm, [3.74165739], atol=1e-5)


def test_pairs_true_as_entity_false_raises():
    """Line 176: pairs=True with as_entity=False raises ArgumentConflictError."""
    molsys = _get_molsys()
    with pytest.raises(ArgumentConflictError):
        msm.structure.get_maximum_distances(
            molsys,
            selection=[0, 0, 1, 1, 2],
            selection_2=[1, 2, 2, 3, 3],
            pairs=True,
            as_entity=False,
            structure_indices=[1],
        )
