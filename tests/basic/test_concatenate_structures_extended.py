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


def test_concatenate_flat_structure_indices_are_per_system(traj_pentalanine_h5_molsys):
    """A flat list selects one distinct frame from each input trajectory."""
    result = msm.concatenate_structures(
        [traj_pentalanine_h5_molsys, traj_pentalanine_h5_molsys],
        structure_indices=[0, 1],
    )
    assert msm.get(result, element='system', n_structures=True) == 2


def test_concatenate_accepts_multiple_topology_free_xtc_sources(md_1u19_pdb_molsys):
    """A native topology can lead several coordinate-only trajectory sources."""
    xtc = msm.systems['nglview']['md_1u19.xtc']
    result = msm.concatenate_structures(
        [md_1u19_pdb_molsys, xtc, xtc],
        structure_indices=[[0], [0, 1], [2, 3]],
        to_form='molsysmt.MolSys',
    )

    assert msm.get(result, n_atoms=True) == msm.get(xtc, n_atoms=True)
    assert msm.get(result, n_structures=True) == 5
    assert result._structure_chemical_state_indices is None
    assert msm.get(result, structure_chemical_state_index=True) == [0] * 5
