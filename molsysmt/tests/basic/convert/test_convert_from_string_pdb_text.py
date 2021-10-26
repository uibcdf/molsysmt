"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import os

# Whole systems (selection='all' and frame_indices='all')

# Selection
def test_string_pdb_text_to_openmm_Topology():
    molsys = msm.convert(msm.demo.t4_lysozyme_L99A['181l.pdb'], to_form='string:pdb_text')
    molsys = msm.convert(molsys, to_form='openmm.Topology', selection='molecule_type=="protein"')
    is_composed_of = msm.is_composed_of(molsys, proteins=1)
    form = msm.get_form(molsys)
    assert ('openmm.Topology'==form) and (is_composed_of==True)

## Multiple outputs


