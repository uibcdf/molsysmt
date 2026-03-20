"""
Extended tests for molsysmt.basic.concatenate_structures covering uncovered branches:
- selections list length mismatch raises ArgumentLengthError
- structure_indices list length mismatch raises ArgumentLengthError
- explicit to_form (convert branch)
"""
import molsysmt as msm
from molsysmt._private.smonitor import ArgumentLengthError
import pytest


def test_concatenate_selections_length_mismatch(traj_pentalanine_h5_molsys, proline_molsys):
    """selections list with wrong length raises ArgumentLengthError."""
    with pytest.raises(ArgumentLengthError):
        msm.concatenate_structures([traj_pentalanine_h5_molsys, proline_molsys], selections=['all'])


def test_concatenate_structure_indices_length_mismatch(traj_pentalanine_h5_molsys, proline_molsys):
    """structure_indices list with wrong length raises ArgumentLengthError."""
    with pytest.raises(ArgumentLengthError):
        msm.concatenate_structures([traj_pentalanine_h5_molsys, proline_molsys], structure_indices=['all'])


def test_concatenate_explicit_to_form(traj_pentalanine_h5_molsys):
    """Explicit to_form uses convert branch (not extract)."""
    result = msm.concatenate_structures(
        [traj_pentalanine_h5_molsys, traj_pentalanine_h5_molsys],
        to_form='molsysmt.MolSys'
    )
    assert msm.get_form(result) == 'molsysmt.MolSys'
    n = msm.get(result, element='system', n_structures=True)
    n_orig = msm.get(traj_pentalanine_h5_molsys, element='system', n_structures=True)
    assert n == 2 * n_orig
