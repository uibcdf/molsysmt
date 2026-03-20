"""
Extended tests for msm.structure.get_rmsd covering additional branches:
- atom count mismatch raises StructuralInconsistencyError
- engine != 'MolSysMT' raises NotImplementedMethodError
- multi-frame reference RMSD (both arrays are multi-frame)
- reference_selection different from selection
- reference_molecular_system explicitly specified
"""
import molsysmt as msm
from molsysmt import systems
import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def pentalanine():
    return msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------

def test_get_rmsd_unsupported_engine(pentalanine):
    """engine='NotAnEngine' raises ArgumentError (caught at arg-digest level)."""
    from molsysmt._private.smonitor import ArgumentError
    with pytest.raises(ArgumentError):
        msm.structure.get_rmsd(pentalanine, engine='NotAnEngine')


def test_get_rmsd_atom_count_mismatch(pentalanine):
    """Mismatched atom counts between selection and reference raises StructuralInconsistencyError."""
    from molsysmt._private.smonitor import StructuralInconsistencyError
    # selection='backbone' (fewer atoms) vs reference using 'all' atoms
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.get_rmsd(
            pentalanine,
            selection='backbone',
            reference_molecular_system=pentalanine,
            reference_selection='all',
            reference_structure_index=0,
        )


# ---------------------------------------------------------------------------
# reference_molecular_system different from molecular_system
# ---------------------------------------------------------------------------

def test_get_rmsd_explicit_reference_system(pentalanine):
    """reference_molecular_system=same_system gives same result as default."""
    rmsd_default = msm.structure.get_rmsd(
        pentalanine, selection='backbone',
        structure_indices=100, reference_structure_index=0
    )
    rmsd_explicit = msm.structure.get_rmsd(
        pentalanine, selection='backbone',
        structure_indices=100,
        reference_molecular_system=pentalanine,
        reference_selection='backbone',
        reference_structure_index=0,
    )
    val_d = msm.pyunitwizard.get_value(rmsd_default, to_unit='nm')
    val_e = msm.pyunitwizard.get_value(rmsd_explicit, to_unit='nm')
    assert np.allclose(val_d, val_e)


# ---------------------------------------------------------------------------
# multi-frame vs multi-frame RMSD
# ---------------------------------------------------------------------------

def test_get_rmsd_multi_frame_reference(pentalanine):
    """Both selection and reference have multiple frames → pairwise RMSD."""
    molsys_1 = msm.extract(pentalanine, structure_indices=range(0, 50))
    molsys_2 = msm.extract(pentalanine, structure_indices=range(100, 150))
    rmsd = msm.structure.get_rmsd(
        molsys_1, selection='backbone',
        reference_molecular_system=molsys_2,
        reference_selection='backbone',
        reference_structure_index=0,
    )
    val = msm.pyunitwizard.get_value(rmsd, to_unit='nm')
    assert val.shape == (50,)
    assert np.all(val >= 0)
    assert np.all(np.isfinite(val))


# ---------------------------------------------------------------------------
# basic sanity: RMSD of a frame against itself = 0
# ---------------------------------------------------------------------------

def test_get_rmsd_self_comparison_is_zero(pentalanine):
    """RMSD of frame 0 against itself must be 0."""
    rmsd = msm.structure.get_rmsd(
        pentalanine, selection='backbone',
        structure_indices=0,
        reference_structure_index=0,
    )
    val = msm.pyunitwizard.get_value(rmsd, to_unit='nm')
    assert np.allclose(val, 0.0, atol=1e-10)


# ---------------------------------------------------------------------------
# return shape checks
# ---------------------------------------------------------------------------

def test_get_rmsd_shape_single_structure(pentalanine):
    """Single structure_index → result has shape (1,)."""
    rmsd = msm.structure.get_rmsd(
        pentalanine, selection='backbone',
        structure_indices=10,
        reference_structure_index=0,
    )
    val = msm.pyunitwizard.get_value(rmsd, to_unit='nm')
    assert val.shape == (1,)


def test_get_rmsd_shape_all_structures(pentalanine):
    """structure_indices='all' → result has shape (n_structures,)."""
    n_structures = msm.get(pentalanine, element='system', n_structures=True)
    rmsd = msm.structure.get_rmsd(
        pentalanine, selection='backbone',
        structure_indices='all',
        reference_structure_index=0,
    )
    val = msm.pyunitwizard.get_value(rmsd, to_unit='nm')
    assert val.shape == (n_structures,)
    assert np.all(val >= 0)


def test_get_rmsd_nonnegative(pentalanine):
    """RMSD values must always be non-negative."""
    rmsd = msm.structure.get_rmsd(
        pentalanine, selection='backbone',
        structure_indices=list(range(100)),
        reference_structure_index=0,
    )
    val = msm.pyunitwizard.get_value(rmsd, to_unit='nm')
    assert np.all(val >= 0)
