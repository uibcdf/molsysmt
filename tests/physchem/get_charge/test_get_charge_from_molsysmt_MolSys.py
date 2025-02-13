"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

def test_get_charge_from_molsysmt_MolSys_1():
    molsys = msm.systems['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(molsys, selection='molecule_type=="protein"')
    charge_residues = msm.physchem.get_charge(molsys, element='group', definition='physical_pH7')
    charge_residues = puw.get_value(charge_residues, to_unit='elementary_charge')
    good_charges_residues = np.array([ 0. ,  0. ,  0. ,  0. , -1. ,  0. ,  0. ,  1. ,  0. , -1. , -1. ,
                                       0. ,  0. ,  1. ,  0. ,  1. ,  0. ,  0. ,  1. , -1. ,  0. , -1. ,
                                       0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.1,  0. ,  0. ,
                                       0. ,  1. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ,  0. ,
                                      -1. ,  0. , -1. ,  1. ,  0. ,  0. ,  0. ,  1. ,  0. ,  0. ,  0. ,
                                       0. ,  0. ,  0. ,  0. ,  1. , -1. , -1. ,  0. , -1. ,  1. ,  0. ,
                                       0. ,  0. ,  0. , -1. ,  0. , -1. ,  0. ,  0. ,  0. ,  1. ,  0. ,
                                       0. ,  0. ,  1. ,  0. ,  0. ,  1. ,  0. ,  1. ,  0. ,  0. ,  0. ,
                                      -1. ,  0. ,  0. , -1. ,  0. ,  0. ,  1. ,  1. ,  0. ,  0. ,  0. ,
                                       0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , -1. ,  0. ,  0. ,
                                       0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ,  0. ,  0. ,
                                       0. ,  0. ,  1. ,  1. ,  0. , -1. , -1. ,  0. ,  0. ,  0. ,  0. ,
                                       0. ,  0. ,  1. ,  0. ,  1. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,
                                       0. ,  1. ,  0. ,  1. ,  1. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ,
                                       0. ,  0. ,  0. ,  0. , -1. ,  0. ,  0. ,  1. ])
    charge_system = msm.physchem.get_charge(molsys, element='system', definition='physical_pH7')
    charge_system = puw.get_value(charge_system, to_unit='elementary_charge')
    good_charge_system = 8.1

    assert np.allclose(charge_residues, good_charges_residues)
    assert np.allclose(charge_system, good_charge_system)

