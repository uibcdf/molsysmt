"""
Unit and regression test for the wrap_to_pbc method of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import math

# Distance between atoms in space and time


def test_wrap_to_pbc_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['chicken villin HP35']['solvated.msmpk'], to_form='molsysmt.MolSys')
    molsys = msm.pbc.wrap_to_mic(molsys, center_of_selection='molecule_type=="peptide"')
    lengths = msm.get(molsys, element='system', box_lengths=True)
    distances = msm.structure.get_distances(molsys, molecular_system_2=[[0.0, 0.0, 0.0]]*msm.puw.unit('nm'), pbc=False)
    max_dist_cube = np.sqrt(3.0*(lengths[0,0]/2.0)**2)
    max_dist = np.max(distances)
    check = (max_dist < max_dist_cube)
    assert check
