"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_get_group_db():

    A_db = msm.element.group.amino_acid.get_group_db('ALA')
    V_db = msm.element.group.amino_acid.get_group_db('VAL')
    H_db = msm.element.group.amino_acid.get_group_db('HIS')

    assert A_db['name']=='ALANINE'
    assert V_db['name']=='VALINE'
    assert H_db['name']=='HISTIDINE'
