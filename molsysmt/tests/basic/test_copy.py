"""
Unit and regression test for the copy module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np
import os


def test_copy_1():
    molsys = tests_systems['pentalanine']['traj_pentalanine.h5']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys_2 = msm.copy(molsys)
    output = msm.compare(molsys, molsys_2, attributes_type='topological', coordinates=True, box=True)
    assert output==True

def test_copy_2():
    molsys = tests_systems['pentalanine']['traj_pentalanine.h5']
    molsys_2 = msm.copy(molsys, 'traj.h5')
    form = msm.get_form(molsys_2)
    os.remove(molsys_2)
    assert 'file:h5'==form

