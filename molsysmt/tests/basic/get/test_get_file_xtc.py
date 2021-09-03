"""
Unit and regression test for the get module of the molsysmt package on xtc file systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np


def test_get_1():
    molsys = msm.demo.files['nglview_demo_md_1u19.xtc']
    n_atoms, n_frames = msm.get(molsys, target='system', n_atoms=True, n_frames=True)
    assert (n_atoms==5547) and (n_frames==51)

