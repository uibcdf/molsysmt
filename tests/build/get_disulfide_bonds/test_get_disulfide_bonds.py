"""
Unit and regression test for the is solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import pytest
import molsysmt as msm
import numpy as np
import sys

def test_get_disulfide_bonds():

    molsys = msm.convert('5XJH')

    dsbonds1 = msm.build.get_disulfide_bonds(molsys, max_bond_length='2.05 angstroms')
    dsbonds2 = msm.build.get_disulfide_bonds(molsys, max_bond_length=None)

    assert [[1782, 1907]]==dsbonds1
    assert [[1782, 1907]]==dsbonds2

