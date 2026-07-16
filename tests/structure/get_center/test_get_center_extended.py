"""
Extended tests for msm.structure.get_center covering additional branches:
- groups-of-atoms (is_iterable_of_iterables) path
- weights parameter
- specific structure_indices (not 'all')
- engine != 'MolSysMT' raises NotImplementedMethodError
"""
import molsysmt as msm
from molsysmt import systems
import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def pentalanine():
    return msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')


@pytest.fixture(scope="module")
def tctim():
    return msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')


# ---------------------------------------------------------------------------
# is_iterable_of_iterables branch (groups-of-atoms selection)
# ---------------------------------------------------------------------------

def test_get_center_groups_of_atoms_shape(pentalanine):
    """Groups-of-atoms selection → output shape (n_structures, n_groups, 3)."""
    list_groups = msm.get(pentalanine, element='group', selection='all', atom_index=True)
    n_structures = msm.get(pentalanine, element='system', n_structures=True)
    n_groups = len(list_groups)
    center = msm.structure.get_center(pentalanine, selection=list_groups)
    assert center.shape == (n_structures, n_groups, 3)


def test_get_center_groups_of_atoms_values(pentalanine):
    """Groups-of-atoms center values are consistent for a fixed frame."""
    list_groups = msm.get(pentalanine, element='group', selection='all', atom_index=True)
    center = msm.structure.get_center(pentalanine, selection=list_groups, structure_indices=0)
    # Shape: (1, n_groups, 3)
    assert center.shape[0] == 1
    assert center.shape[2] == 3
    # All centers must be finite
    val = msm.pyunitwizard.get_value(center, to_unit='nm')
    assert np.all(np.isfinite(val))


def test_get_center_groups_of_atoms_with_weights(pentalanine):
    """Groups-of-atoms with per-atom weights returns sensible shape."""
    list_groups = msm.get(pentalanine, element='group', selection='all', atom_index=True)
    n_structures = msm.get(pentalanine, element='system', n_structures=True)
    n_groups = len(list_groups)
    # Build equal weights per group (same as unweighted, just exercises the path)
    weights = [np.ones(len(g)) for g in list_groups]
    center_weighted = msm.structure.get_center(pentalanine, selection=list_groups, weights=weights)
    center_plain = msm.structure.get_center(pentalanine, selection=list_groups)
    val_w = msm.pyunitwizard.get_value(center_weighted, to_unit='nm')
    val_p = msm.pyunitwizard.get_value(center_plain, to_unit='nm')
    assert np.allclose(val_w, val_p)


# ---------------------------------------------------------------------------
# weights parameter on flat selection
# ---------------------------------------------------------------------------

def test_get_center_flat_with_weights(pentalanine):
    """Flat selection with equal weights = unweighted center."""
    ca_indices = msm.select(pentalanine, selection='atom_name=="CA"')
    n_ca = len(ca_indices)
    weights = np.ones(n_ca)
    center_w = msm.structure.get_center(pentalanine, selection=ca_indices,
                                         weights=weights, structure_indices=0)
    center_p = msm.structure.get_center(pentalanine, selection=ca_indices,
                                         structure_indices=0)
    val_w = msm.pyunitwizard.get_value(center_w, to_unit='nm')
    val_p = msm.pyunitwizard.get_value(center_p, to_unit='nm')
    assert np.allclose(val_w, val_p, atol=1e-10)


def test_get_center_flat_with_nonuniform_weights(pentalanine):
    """Non-uniform weights shift the center toward heavier atoms."""
    ca_indices = msm.select(pentalanine, selection='atom_name=="CA"')
    n_ca = len(ca_indices)
    weights_uniform = np.ones(n_ca)
    weights_skewed = np.ones(n_ca)
    weights_skewed[0] = 1000.0  # First atom dominates
    center_uniform = msm.structure.get_center(
        pentalanine, selection=ca_indices, weights=weights_uniform, structure_indices=0)
    center_skewed = msm.structure.get_center(
        pentalanine, selection=ca_indices, weights=weights_skewed, structure_indices=0)
    val_u = msm.pyunitwizard.get_value(center_uniform, to_unit='nm')
    val_s = msm.pyunitwizard.get_value(center_skewed, to_unit='nm')
    # Skewed center must differ from uniform center
    assert not np.allclose(val_u, val_s)


def test_get_center_accepts_mass_weights(pentalanine):
    """The declared 'masses' mode computes a finite center of mass."""

    center = msm.structure.get_center(
        pentalanine,
        selection='atom_name=="CA"',
        weights="masses",
        structure_indices=0,
    )
    values = msm.pyunitwizard.get_value(center, to_unit="nm")

    assert values.shape == (1, 1, 3)
    assert np.all(np.isfinite(values))


# ---------------------------------------------------------------------------
# specific structure_indices (not 'all')
# ---------------------------------------------------------------------------

def test_get_center_single_structure_index(pentalanine):
    """structure_indices=0 returns a (1, 1, 3) array."""
    center = msm.structure.get_center(pentalanine, selection='atom_name=="CA"',
                                       structure_indices=0)
    assert center.shape[0] == 1
    assert center.shape[2] == 3


def test_get_center_multiple_structure_indices(pentalanine):
    """structure_indices=[0, 1, 2] returns shape (3, 1, 3)."""
    center = msm.structure.get_center(pentalanine, selection='atom_name=="CA"',
                                       structure_indices=[0, 1, 2])
    assert center.shape == (3, 1, 3)


# ---------------------------------------------------------------------------
# unsupported engine raises NotImplementedMethodError
# ---------------------------------------------------------------------------

def test_get_center_unsupported_engine(pentalanine):
    """engine='NotAnEngine' raises ArgumentError (caught at arg-digest level)."""
    from molsysmt._private.smonitor import ArgumentError
    with pytest.raises(ArgumentError):
        msm.structure.get_center(pentalanine, engine='NotAnEngine')


# ---------------------------------------------------------------------------
# static system (single structure): TcTIM
# ---------------------------------------------------------------------------

def test_get_center_static_system_shape(tctim):
    """Static system (1 structure): center has shape (1, 1, 3)."""
    center = msm.structure.get_center(tctim, selection='all')
    assert center.shape == (1, 1, 3)


def test_get_center_static_system_is_finite(tctim):
    """Center coordinates of TcTIM are finite floats."""
    center = msm.structure.get_center(tctim, selection='all')
    val = msm.pyunitwizard.get_value(center, to_unit='nm')
    assert np.all(np.isfinite(val))
