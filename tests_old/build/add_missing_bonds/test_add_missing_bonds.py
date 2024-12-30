"""
Unit and regression test for the is solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import pytest
import molsysmt as msm
from molsysmt import systems
import numpy as np


def test_add_missing_bonds_molsysmt_MolSys_1():

    molsys = msm.convert(systems['T4 lysozyme L99A']['t4_lysozyme_L99A.h5msm'])
    n_bonds_before = msm.get(molsys, n_bonds=True)
    msm.build.remove_bonds(molsys)
    msm.build.add_missing_bonds(molsys)
    n_bonds_after = msm.get(molsys, n_bonds=True)

    assert n_bonds_before==n_bonds_after

def test_add_missing_bonds_molsysmt_MolSys_2():

    molsys = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    molsys = msm.convert(molsys)
    bonded_atom_pairs = msm.get(molsys, bonded_atom_pairs=True)
    msm.build.remove_bonds(molsys)
    msm.build.add_missing_bonds(molsys)
    new_bonded_atom_pairs = msm.get(molsys, bonded_atom_pairs=True)
    
    assert new_bonded_atom_pairs == bonded_atom_pairs
