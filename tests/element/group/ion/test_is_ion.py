"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_is_ion():

    assert msm.element.group.ion.is_ion('K')
    assert msm.element.group.ion.is_ion('CL')
    assert msm.element.group.ion.is_ion('NA')
