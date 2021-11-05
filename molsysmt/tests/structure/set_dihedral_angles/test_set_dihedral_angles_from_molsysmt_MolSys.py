"""
Unit and regression test for the shift_dihedral_angles module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_shift_dihedral_angles_from_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    phi_chains = msm.topology.get_covalent_dihedral_quartets(molsys, dihedral_angle='phi')
    molecular_system = msm.structure.set_dihedral_angles(molsys, quartets=phi_chains[2],
                                                           angles='0.0 degrees', pbc=False)
    dihedral_angles = msm.structure.get_dihedral_angles(molecular_system, quartets=phi_chains[2])
    true_value = np.array([[0.00]])
    check = np.allclose(true_value,msm.puw.get_value(dihedral_angles, to_unit='degrees'))
    assert check

