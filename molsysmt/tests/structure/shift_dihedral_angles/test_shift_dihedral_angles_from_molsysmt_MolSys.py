"""
Unit and regression test for the shift_dihedral_angles module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_shift_dihedral_angles_from_molsysmt_MolSys_1():
    molsys = msm.demo.classes.metenkephalin(to_form='molsysmt.MolSys')
    covalent_chains = msm.topology.get_covalent_chains(molsys, chain=['atom_name=="C"', 'atom_name=="N"',
                                                               'atom_name=="CA"', 'atom_name=="C"'])
    dihedral_angles = msm.structure.get_dihedral_angles(molsys, quartets=covalent_chains[2])
    true_value = np.array([[-179.99999499]])
    check = np.allclose(true_value,msm.puw.get_value(dihedral_angles, to_unit='degrees'))
    assert check

