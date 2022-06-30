"""
Unit and regression test for the get_rmsd module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_get_rmsd_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['pentalanine']['traj.h5'], to_form='molsysmt.MolSys')
    rmsd = msm.structure.get_rmsd(molsys, selection='backbone', structure_indices=100,
            reference_structure_index=0)
    true_value_1 = [0.7381704258064243]
    check_value_1 = np.allclose(true_value_1, msm.puw.get_value(rmsd, to_unit='nm'))
    assert check_value_1

def test_get_rmsd_molsysmt_MolSys_2():
    molsys = msm.convert(msm.demo['pentalanine']['traj.h5'], to_form='molsysmt.MolSys')
    rmsd = msm.structure.get_rmsd(molsys, selection='backbone', structure_indices='all',
            reference_structure_index=0)
    true_value_1 = np.array([0.89216228, 0.86888688, 1.017914  , 1.05838683, 0.87139639,
       0.85209277, 1.08759923, 1.01077526, 0.88728621, 0.73084385])
    check_value_1 = np.allclose(true_value_1, msm.puw.get_value(rmsd[1000:1010], to_unit='nm'))
    assert check_value_1

def test_get_rmsd_molsysmt_MolSys_3():
    molsys = msm.convert(msm.demo['pentalanine']['traj.h5'], to_form='molsysmt.MolSys')
    molsys_1 = msm.extract(molsys, structure_indices=range(0, 100))
    molsys_2 = msm.extract(molsys, structure_indices=range(200, 300))
    rmsd = msm.structure.get_rmsd(molsys_1, selection='backbone', structure_indices=80,
                reference_molecular_system=molsys_2, reference_selection='backbone',
                reference_structure_index=20)
    true_value_1 = [0.945975307377399]
    check_value_1 = np.allclose(true_value_1, msm.puw.get_value(rmsd, to_unit='nm'))
    assert check_value_1

