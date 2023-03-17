"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

def test_convert_file_gro_and_file_xtc_to_mdtraj_Trajectory():
    molsys_1 = msm.demo['nglview']['md_1u19.gro']
    molsys_2 = msm.demo['nglview']['md_1u19.xtc']
    molsys = msm.convert([molsys_1, molsys_2], to_form='mdtraj.Trajectory')
    form = msm.get_form(molsys)
    assert 'mdtraj.Trajectory'==form

