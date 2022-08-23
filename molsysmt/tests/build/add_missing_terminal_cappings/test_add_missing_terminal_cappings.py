"""
Unit and regression test for the add_terminal_cappings of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Distance between atoms in space and time

def test_add_missing_terminal_cappings_molsysmt_MolSys_1():
    seq = 'AlaValPro'
    molsys = msm.build.build_peptide(seq)
    n_atoms_before = msm.get(molsys, element='system', n_atoms=True)
    groups_before = msm.get(molsys, element='group', name=True)
    molsys = msm.build.add_missing_terminal_cappings(molsys, N_terminal=None, C_terminal=None)
    n_atoms_after = msm.get(molsys, element='system', n_atoms=True)
    groups_after = msm.get(molsys, element='group', name=True)
    #charge_groups = msm.physchem.charge([molsys, {'forcefield':'AMBER14'}], element='group')
    check_before = (n_atoms_before==40 and np.all(np.array(['ALA', 'VAL', 'PRO'], dtype=object)==groups_before))
    check_after = (n_atoms_after==43 and np.all(np.array(['ALA', 'VAL', 'PRO'], dtype=object)==groups_after))
    #check_charges = np.allclose([1.0, 0.0, -1.0], msm.pyunitwizard.get_value(charge_groups))
    assert check_before and check_after

def test_add_missing_terminal_cappings_molsysmt_MolSys_2():
    seq = 'AlaValPro'
    molsys = msm.build.build_peptide(seq)
    n_atoms_before = msm.get(molsys, element='system', n_atoms=True)
    groups_before = msm.get(molsys, element='group', name=True)
    molsys = msm.build.add_missing_terminal_cappings(molsys, N_terminal='ACE', C_terminal='NME')
    n_atoms_after = msm.get(molsys, element='system', n_atoms=True)
    groups_after = msm.get(molsys, element='group', name=True)
    #charge_groups = msm.physchem.charge([molsys, {'forcefield':'AMBER14'}], element='group')
    check_before = (n_atoms_before==40 and np.all(np.array(['ALA', 'VAL', 'PRO'], dtype=object)==groups_before))
    check_after = (n_atoms_after==52 and np.all(np.array(['ACE', 'ALA', 'VAL', 'PRO', 'NME'], dtype=object)==groups_after))
    #check_charges = np.allclose([0.0, 0.0, 0.0, 0.0, 0.0], msm.pyunitwizard.get_value(charge_groups))
    assert check_before and check_after

