"""
Unit and regression test for the get_least_rmsd module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np

# Distance between atoms in space and time

def test_get_least_rmsd_molsysmt_MolSys_1():

    molsys = msm.convert(tests_systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    rmsd = msm.structure.get_least_rmsd(molsys, selection='backbone', structure_indices='all',
            reference_structure_indices=0)
    true_value_1 = np.array([0.270763  , 0.22951274, 0.26526436, 0.24263974, 0.23508047])
    check_value_1 = np.allclose(true_value_1, msm.pyunitwizard.get_value(rmsd[1000:1005], to_unit='nm'))
    assert check_value_1

