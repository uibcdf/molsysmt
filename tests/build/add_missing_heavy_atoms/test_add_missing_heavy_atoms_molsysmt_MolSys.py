"""
Unit and regression test for the add_hydrogens module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time

def test_add_hydrogens_molsysmt_MolSys_1():

    molsys = msm.build.build_peptide('AceHisThrNme')
    molsys = msm.remove(molsys, selection='atom_name in ["NE2", "CD2", "OG1"]')
    missing_heavy_atoms = msm.build.get_missing_heavy_atoms(molsys)
    molsys = msm.build.add_missing_heavy_atoms(molsys)
    n_atoms = msm.get(molsys, element='atom', selection='atom_name in ["NE2", "CD2", "OG1"]', n_atoms=True)

    assert missing_heavy_atoms == {1: ['NE2', 'CD2'], 2: ['OG1']}
    assert n_atoms == 3

