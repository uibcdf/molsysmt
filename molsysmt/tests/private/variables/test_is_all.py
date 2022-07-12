"""
Unit and regression test for the _private.is_all module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_is_all_1():
    assert (msm._private.variables.is_all('all') == True)

def test_is_all_2():
    assert (msm._private.variables.is_all('potato') == False)

def test_is_all_3():
    assert (msm._private.variables.is_all([0,0,0]) == False)

def test_is_all_4():
    assert (msm._private.variables.is_all(np.array([0,0,0])) == False)

def test_is_all_5():
    assert (msm._private.variables.is_all('All') == True)

