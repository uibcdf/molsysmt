"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np
import os

def test_convert_molsysmt_Topology_and_molsysmt_Structures_to_string_pdb_text():
    molsys = msm.convert(tests_systems['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys')
    molsys = msm.convert(molsys, to_form=['molsysmt.Topology', 'molsysmt.Structures'])
    molsys = msm.convert(molsys, to_form='string:pdb_text')
    form = msm.get_form(molsys)
    assert 'string:pdb_text'==form

