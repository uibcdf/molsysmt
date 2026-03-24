"""
Heavy-mode (chunked execution) tests for msm.structure.get_rmsd.

These tests exercise the heavy-path code (lines 154-176, 191, 199-203, 214
in get_rmsd.py) by using heavy_mode='force' on a file:h5msm molecular system,
which is the only form that declares _heavy_support for coordinates.

Parity strategy: compute RMSD eagerly on a molsysmt.MolSys object (the eager
reference path), then compute the same RMSD on the h5msm file path with
heavy_mode='force', and assert numerical agreement within atol=1e-6 nm.
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
# Parity: heavy path matches eager path on backbone atoms
# ---------------------------------------------------------------------------

def test_get_rmsd_heavy_mode_parity_backbone(pentalanine_molsys, pentalanine_h5msm):
    """Heavy-mode RMSD on backbone equals eager RMSD at three spot-checked frames."""
    structure_indices = [0, 100, 1000]

    rmsd_eager = msm.structure.get_rmsd(
        pentalanine_molsys,
        selection='backbone',
        structure_indices=structure_indices,
        reference_structure_index=0,
        heavy_mode='off',
    )
    rmsd_heavy = msm.structure.get_rmsd(
        pentalanine_h5msm,
        selection='backbone',
        structure_indices=structure_indices,
        reference_structure_index=0,
        heavy_mode='force',
    )

    eager_val = puw.get_value(rmsd_eager, to_unit='nm')
    heavy_val = puw.get_value(rmsd_heavy, to_unit='nm')

    assert eager_val.shape == heavy_val.shape
    assert np.allclose(eager_val, heavy_val, atol=1e-6)


def test_get_rmsd_heavy_mode_known_values(pentalanine_h5msm):
    """Heavy-mode RMSD matches numerically known ground-truth values."""
    rmsd_heavy = msm.structure.get_rmsd(
        pentalanine_h5msm,
        selection='backbone',
        structure_indices=[0, 100, 1000],
        reference_structure_index=0,
        heavy_mode='force',
    )
    val = puw.get_value(rmsd_heavy, to_unit='nm')
    # Ground truth from test_get_rmsd_from_molsysmt_MolSys.py
    expected = np.array([0.0, 0.7381704258064243, 0.89216228])
    assert np.allclose(val, expected, atol=1e-5)


def test_get_rmsd_heavy_mode_self_is_zero(pentalanine_h5msm):
    """Heavy-mode: RMSD of frame 0 against itself must be zero."""
    rmsd = msm.structure.get_rmsd(
        pentalanine_h5msm,
        selection='backbone',
        structure_indices=[0],
        reference_structure_index=0,
        heavy_mode='force',
    )
    val = puw.get_value(rmsd, to_unit='nm')
    assert np.allclose(val, 0.0, atol=1e-10)


# ---------------------------------------------------------------------------
# Shape and non-negativity with heavy mode
# ---------------------------------------------------------------------------

def test_get_rmsd_heavy_mode_shape(pentalanine_h5msm):
    """Heavy-mode RMSD with three explicit indices returns shape (3,)."""
    rmsd = msm.structure.get_rmsd(
        pentalanine_h5msm,
        selection='backbone',
        structure_indices=[0, 50, 200],
        reference_structure_index=0,
        heavy_mode='force',
    )
    val = puw.get_value(rmsd, to_unit='nm')
    assert val.shape == (3,)


def test_get_rmsd_heavy_mode_nonnegative(pentalanine_h5msm):
    """Heavy-mode RMSD values are always non-negative."""
    rmsd = msm.structure.get_rmsd(
        pentalanine_h5msm,
        selection='backbone',
        structure_indices=list(range(50)),
        reference_structure_index=0,
        heavy_mode='force',
    )
    val = puw.get_value(rmsd, to_unit='nm')
    assert np.all(val >= 0.0)
    assert np.all(np.isfinite(val))


# ---------------------------------------------------------------------------
# Heavy mode parity: all-atoms selection
# ---------------------------------------------------------------------------

def test_get_rmsd_heavy_mode_parity_all_atoms(pentalanine_molsys, pentalanine_h5msm):
    """Heavy-mode parity holds for the default all-heavy-atoms selection."""
    structure_indices = [10, 50, 500]

    rmsd_eager = msm.structure.get_rmsd(
        pentalanine_molsys,
        structure_indices=structure_indices,
        reference_structure_index=0,
        heavy_mode='off',
    )
    rmsd_heavy = msm.structure.get_rmsd(
        pentalanine_h5msm,
        structure_indices=structure_indices,
        reference_structure_index=0,
        heavy_mode='force',
    )

    eager_val = puw.get_value(rmsd_eager, to_unit='nm')
    heavy_val = puw.get_value(rmsd_heavy, to_unit='nm')

    assert np.allclose(eager_val, heavy_val, atol=1e-6)


# ---------------------------------------------------------------------------
# Heavy mode: structure_indices='all'
# ---------------------------------------------------------------------------

def test_get_rmsd_heavy_mode_all_structures_shape(pentalanine_h5msm):
    """Heavy-mode RMSD over all structures has shape (n_structures,)."""
    n_structures = msm.get(pentalanine_h5msm, element='system', n_structures=True)
    rmsd = msm.structure.get_rmsd(
        pentalanine_h5msm,
        selection='backbone',
        structure_indices='all',
        reference_structure_index=0,
        heavy_mode='force',
    )
    val = puw.get_value(rmsd, to_unit='nm')
    assert val.shape == (n_structures,)
    assert np.all(val >= 0.0)
