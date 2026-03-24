"""
Heavy-mode (chunked execution) tests for msm.structure.get_center.

These tests exercise the heavy-path code (lines 118-131, 162-176, 195 in
get_center.py) by using heavy_mode='force' on a file:h5msm molecular system,
which is the only form that declares _heavy_support for coordinates.

Two code paths are exercised:
  1. Flat selection  (is_iterable_of_iterables is False) — lines 117-131
  2. Groups-of-atoms selection (is_iterable_of_iterables is True) — lines 161-176

Parity strategy: compute center eagerly on a molsysmt.MolSys object (heavy_mode='off'),
then compute the same center on the h5msm file path with heavy_mode='force', and assert
numerical agreement within atol=1e-6 nm.
"""
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def pentalanine_molsys():
    """Eager MolSys used as the reference for all parity checks."""
    return msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')


@pytest.fixture(scope="module")
def pentalanine_h5msm():
    """Path to the pentalanine h5msm file (file:h5msm form, supports heavy mode)."""
    return systems['pentalanine']['traj_pentalanine.h5msm']


# ---------------------------------------------------------------------------
# Flat selection — heavy path (lines 117-131)
# ---------------------------------------------------------------------------

def test_get_center_heavy_mode_parity_flat(pentalanine_molsys, pentalanine_h5msm):
    """Heavy-mode center on CA atoms equals eager center at three spot-checked frames."""
    structure_indices = [0, 100, 1000]

    center_eager = msm.structure.get_center(
        pentalanine_molsys,
        selection='atom_name=="CA"',
        structure_indices=structure_indices,
        heavy_mode='off',
    )
    center_heavy = msm.structure.get_center(
        pentalanine_h5msm,
        selection='atom_name=="CA"',
        structure_indices=structure_indices,
        heavy_mode='force',
    )

    eager_val = puw.get_value(center_eager, to_unit='nm')
    heavy_val = puw.get_value(center_heavy, to_unit='nm')

    assert eager_val.shape == heavy_val.shape
    assert np.allclose(eager_val, heavy_val, atol=1e-6)


def test_get_center_heavy_mode_flat_shape(pentalanine_h5msm):
    """Heavy-mode flat center: shape is (n_sel_structures, 1, 3)."""
    structure_indices = [0, 10, 20, 30]
    center = msm.structure.get_center(
        pentalanine_h5msm,
        selection='atom_name=="CA"',
        structure_indices=structure_indices,
        heavy_mode='force',
    )
    val = puw.get_value(center, to_unit='nm')
    assert val.shape == (4, 1, 3)


def test_get_center_heavy_mode_flat_is_finite(pentalanine_h5msm):
    """Heavy-mode flat center values are finite."""
    center = msm.structure.get_center(
        pentalanine_h5msm,
        selection='atom_name=="CA"',
        structure_indices=list(range(50)),
        heavy_mode='force',
    )
    val = puw.get_value(center, to_unit='nm')
    assert np.all(np.isfinite(val))


def test_get_center_heavy_mode_flat_all_structures(pentalanine_h5msm):
    """Heavy-mode flat center over all structures has shape (n_structures, 1, 3)."""
    n_structures = msm.get(pentalanine_h5msm, element='system', n_structures=True)
    center = msm.structure.get_center(
        pentalanine_h5msm,
        selection='atom_name=="CA"',
        structure_indices='all',
        heavy_mode='force',
    )
    val = puw.get_value(center, to_unit='nm')
    assert val.shape == (n_structures, 1, 3)
    assert np.all(np.isfinite(val))


# ---------------------------------------------------------------------------
# Flat selection with weights — still exercises the heavy flat path
# ---------------------------------------------------------------------------

def test_get_center_heavy_mode_flat_with_equal_weights_parity(pentalanine_molsys, pentalanine_h5msm):
    """Heavy-mode center with uniform weights equals unweighted center (parity)."""
    ca_indices = msm.select(pentalanine_molsys, selection='atom_name=="CA"')
    n_ca = len(ca_indices)
    weights = np.ones(n_ca, dtype=np.float64)
    structure_indices = [0, 100, 500]

    center_no_w_eager = msm.structure.get_center(
        pentalanine_molsys,
        selection='atom_name=="CA"',
        structure_indices=structure_indices,
        heavy_mode='off',
    )
    center_with_w_heavy = msm.structure.get_center(
        pentalanine_h5msm,
        selection='atom_name=="CA"',
        weights=weights,
        structure_indices=structure_indices,
        heavy_mode='force',
    )

    eager_val = puw.get_value(center_no_w_eager, to_unit='nm')
    heavy_val = puw.get_value(center_with_w_heavy, to_unit='nm')

    assert np.allclose(eager_val, heavy_val, atol=1e-6)


# ---------------------------------------------------------------------------
# Groups-of-atoms selection — heavy path (lines 161-176)
# ---------------------------------------------------------------------------

def test_get_center_heavy_mode_parity_groups(pentalanine_molsys, pentalanine_h5msm):
    """Heavy-mode groups-of-atoms center equals eager center at spot-checked frames."""
    # Use residue-level groups (one group per residue)
    list_groups = msm.get(pentalanine_molsys, element='group', selection='all', atom_index=True)
    structure_indices = [0, 100, 500]

    center_eager = msm.structure.get_center(
        pentalanine_molsys,
        selection=list_groups,
        structure_indices=structure_indices,
        heavy_mode='off',
    )
    center_heavy = msm.structure.get_center(
        pentalanine_h5msm,
        selection=list_groups,
        structure_indices=structure_indices,
        heavy_mode='force',
    )

    eager_val = puw.get_value(center_eager, to_unit='nm')
    heavy_val = puw.get_value(center_heavy, to_unit='nm')

    assert eager_val.shape == heavy_val.shape
    assert np.allclose(eager_val, heavy_val, atol=1e-6)


def test_get_center_heavy_mode_groups_shape(pentalanine_molsys, pentalanine_h5msm):
    """Heavy-mode groups center: shape is (n_sel_structures, n_groups, 3)."""
    list_groups = msm.get(pentalanine_molsys, element='group', selection='all', atom_index=True)
    n_groups = len(list_groups)
    structure_indices = [0, 10, 20]

    center = msm.structure.get_center(
        pentalanine_h5msm,
        selection=list_groups,
        structure_indices=structure_indices,
        heavy_mode='force',
    )
    val = puw.get_value(center, to_unit='nm')
    assert val.shape == (3, n_groups, 3)


def test_get_center_heavy_mode_groups_is_finite(pentalanine_molsys, pentalanine_h5msm):
    """Heavy-mode groups center values are all finite."""
    list_groups = msm.get(pentalanine_molsys, element='group', selection='all', atom_index=True)
    center = msm.structure.get_center(
        pentalanine_h5msm,
        selection=list_groups,
        structure_indices=list(range(30)),
        heavy_mode='force',
    )
    val = puw.get_value(center, to_unit='nm')
    assert np.all(np.isfinite(val))


def test_get_center_heavy_mode_groups_all_structures(pentalanine_molsys, pentalanine_h5msm):
    """Heavy-mode groups center over all structures has correct shape."""
    list_groups = msm.get(pentalanine_molsys, element='group', selection='all', atom_index=True)
    n_groups = len(list_groups)
    n_structures = msm.get(pentalanine_h5msm, element='system', n_structures=True)

    center = msm.structure.get_center(
        pentalanine_h5msm,
        selection=list_groups,
        structure_indices='all',
        heavy_mode='force',
    )
    val = puw.get_value(center, to_unit='nm')
    assert val.shape == (n_structures, n_groups, 3)
    assert np.all(np.isfinite(val))


# ---------------------------------------------------------------------------
# Groups-of-atoms with weights — still exercises the groups heavy path
# ---------------------------------------------------------------------------

def test_get_center_heavy_mode_groups_with_equal_weights_parity(pentalanine_molsys, pentalanine_h5msm):
    """Heavy-mode groups center with uniform weights matches unweighted center."""
    list_groups = msm.get(pentalanine_molsys, element='group', selection='all', atom_index=True)
    weights = [np.ones(len(g), dtype=np.float64) for g in list_groups]
    structure_indices = [0, 100]

    center_no_w = msm.structure.get_center(
        pentalanine_molsys,
        selection=list_groups,
        structure_indices=structure_indices,
        heavy_mode='off',
    )
    center_with_w_heavy = msm.structure.get_center(
        pentalanine_h5msm,
        selection=list_groups,
        weights=weights,
        structure_indices=structure_indices,
        heavy_mode='force',
    )

    eager_val = puw.get_value(center_no_w, to_unit='nm')
    heavy_val = puw.get_value(center_with_w_heavy, to_unit='nm')

    assert np.allclose(eager_val, heavy_val, atol=1e-6)
