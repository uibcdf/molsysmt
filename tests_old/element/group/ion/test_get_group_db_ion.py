"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_get_group_db():

    K_db = msm.element.group.ion.get_group_db('K')
    CL_db = msm.element.group.ion.get_group_db('CL')
    NA_db = msm.element.group.ion.get_group_db('NA')

    assert K_db['three_letter_code']=='K'
    assert CL_db['three_letter_code']=='CL'
    assert NA_db['three_letter_code']=='NA'
