"""
Unit and regression test for the merge module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

def test_has_attribute_1():
    molsys = msm.demo['pentalanine']['pentalanine.inpcrd']
    assert msm.has_attribute(molsys, 'box')==True
    assert msm.has_attribute(molsys, 'group_name')==False

def test_has_attribute_2():
    molsys = msm.demo['membrane']['membrane.psf']
    assert msm.has_attribute(molsys, 'topological')==True
    assert msm.has_attribute(molsys, 'structural')==False

def test_has_attribute_3():
    molsys = msm.demo['membrane']['membrane.dcd']
    assert msm.has_attribute(molsys, 'topological')==False
    assert msm.has_attribute(molsys, 'structural')==True
