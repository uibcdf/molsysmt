"""
Unit and regression test for the is solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import pytest
import molsysmt as msm
from molsysmt import systems
import numpy as np


def test_add_bonds_molsysmt_MolSys_1():

    molsys = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    molsys = msm.convert(molsys)
    msm.build.remove_bonds(molsys)
    msm.build.add_bonds(molsys, bonded_atom_pairs=[[0,1], [0,2], [1,4]])
    n_bonds, bonded_atom_pairs = msm.get(molsys, n_bonds=True, bonded_atom_pairs=True)

    assert n_bonds==3
    assert bonded_atom_pairs==[[0,1], [0,2], [1,4]]
