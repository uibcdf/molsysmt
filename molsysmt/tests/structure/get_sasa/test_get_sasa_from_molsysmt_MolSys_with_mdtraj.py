"""
Unit and regression test for the get_sasa module of the molsysmt package on molsysmt MolSys molecular
systems with mdtraj
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_get_sasa_from_molsysmt_MolSys_with_mdtraj_1():

    molsys = msm.demo.classes.TcTIM_in_pdbid_1tcd(to_form='molsysmt.MolSys')
    molsys = msm.build.remove_solvent(molsys)
    sasa_per_residue = msm.structure.get_sasa(molsys, target='group', engine='mdtraj')
    sasa_per_molecule = msm.structure.get_sasa(molsys, target='molecule', engine='mdtraj')
    true_value_1 = np.array([0.46785632, 0.14642592, 0.66083997, 0.41626209, 1.01144218])
    check_value_1 = np.allclose(true_value_1, msm.puw.get_value(sasa_per_residue[0,100:105], to_unit='nm**2'))
    true_value_2 = [[194.954040]]
    check_value_2 = np.allclose(true_value_2, msm.puw.get_value(sasa_per_molecule, to_unit='nm**2'))
    assert check_value_1 and check_value_2


