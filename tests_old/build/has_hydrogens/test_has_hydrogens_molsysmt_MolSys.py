"""
Unit and regression test for the is solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import pytest
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time

def test_has_hydrogens_molsysmt_MolSys_1():
    molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
    output_before = msm.build.has_hydrogens(molsys)
    output_before_with_mask = msm.build.has_hydrogens(molsys, selection='molecule_type=="protein"')
    molsys = msm.build.add_missing_terminal_cappings(molsys)
    molsys = msm.build.add_missing_heavy_atoms(molsys)
    molsys = msm.build.add_missing_hydrogens(molsys)
    output_after = msm.build.has_hydrogens(molsys)
    output_after_with_mask = msm.build.has_hydrogens(molsys, selection='molecule_type=="protein"')
    check_before = (output_before == False)
    check_after = (output_after == True)
    check_before_with_mask = (output_before_with_mask == False)
    check_after_with_mask = (output_after_with_mask == True)
    assert check_before and check_after
    assert check_before_with_mask and check_after_with_mask

