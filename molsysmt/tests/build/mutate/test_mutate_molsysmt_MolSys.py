"""
Unit and regression test for the mutate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_mutate_molsysmt_MolSys_1():
    molsys = msm.demo.classes.metenkephalin(to_form='molsysmt.MolSys')
    molsys = msm.build.mutate(molsys, residue_indices=[1,2], to_residue_names=['ALA', 'VAL'])
    seq = msm.convert(molsys, to_form='string:aminoacids3')
    check = (seq == 'TyrAlaValPheMet')
    assert check


