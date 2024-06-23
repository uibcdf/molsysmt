"""
Unit and regression test for the merge module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_has_attribute_1():
    molsys = systems['pentalanine']['pentalanine.inpcrd']
    assert msm.has_attribute(molsys, 'box')==True
    assert msm.has_attribute(molsys, 'group_name')==False

