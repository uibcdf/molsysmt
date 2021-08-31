"""
Unit and regression test for the get module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np


# Get on molsysmt.MolSys

def test_get_1():
    molsys = msm.demo.files['1tcd.mmtf']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    output = msm.get(molsys, indices=[32,33,34], name=True)
    assert np.all(output == np.array(['N', 'CA', 'C'], dtype=object))


