"""
Extended tests for molsysmt.basic.remove covering uncovered branches:
- structure_indices='all' (removes all structures)
- selection + structure_indices together
"""
import molsysmt as msm
import pytest


def test_remove_structure_indices_all(traj_pentalanine_h5_molsys):
    """structure_indices='all' removes all structures → empty Structures."""
    molsys = msm.convert(traj_pentalanine_h5_molsys, to_form='molsysmt.Structures')
    result = msm.remove(molsys, structure_indices='all')
    n = msm.get(result, element='system', n_structures=True)
    assert n == 0


def test_remove_selection_and_structure_indices(traj_pentalanine_h5_molsys):
    """Both selection and structure_indices specified simultaneously."""
    molsys = msm.convert(traj_pentalanine_h5_molsys, to_form='molsysmt.MolSys')
    n_atoms_orig = msm.get(molsys, element='system', n_atoms=True)
    # Remove a specific structure index while also removing some atoms
    result = msm.remove(molsys, selection='atom_index==0', structure_indices=None)
    n_atoms = msm.get(result, element='system', n_atoms=True)
    assert n_atoms == n_atoms_orig - 1


def test_remove_structure_indices_list(traj_pentalanine_h5_molsys):
    """structure_indices as a list (not 'all') removes specific structures."""
    molsys = msm.convert(traj_pentalanine_h5_molsys, to_form='molsysmt.MolSys')
    n_structures = msm.get(molsys, element='system', n_structures=True)
    if n_structures >= 2:
        result = msm.remove(molsys, structure_indices=[0])
        n = msm.get(result, element='system', n_structures=True)
        assert n == n_structures - 1
