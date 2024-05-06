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

def test_is_solvate_molsysmt_MolSys_1():
    molsys = msm.convert(systems['Met-enkephalin']['met_enkephalin.pdb'], to_form='molsysmt.MolSys')
    molsys = msm.build.add_missing_terminal_cappings(molsys)
    molsys = msm.build.add_missing_hydrogens(molsys)
    output_before = msm.build.is_solvated(molsys)
    molsys = msm.build.solvate(molsys, box_shape='cubic', clearance='14.0 angstroms')
    output_after = msm.build.is_solvated(molsys)
    check_before = (output_before == False)
    check_after = (output_after == True)
    assert check_before and check_after

