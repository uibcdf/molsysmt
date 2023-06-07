"""
Unit and regression test for the convert module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np
import os

def test_convert_file_psf_and_file_dcd_to_molsysmt_Topology():
    psf_file = tests_systems['POPC membrane']['popc_membrane.psf']
    dcd_file = tests_systems['POPC membrane']['popc_membrane.dcd']
    molsys = msm.convert([psf_file, dcd_file], to_form='molsysmt.Topology')
    form = msm.get_form(molsys)
    n_atoms, n_structures = msm.get(molsys, n_atoms=True, n_structures=True)
    assert 'molsysmt.Topology'==form
    assert n_atoms==78974
    assert n_structures==None

