"""
Unit and regression test for the get_dihedral_angles module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time

def test_set_dihedral_angles_from_molsysmt_MolSys_1():

    molecular_system = msm.systems['Met-enkephalin']['met_enkephalin.h5msm']
    molecular_system = msm.convert(molecular_system)
    phi_chains = msm.topology.get_dihedral_quartets(molecular_system, phi=True)
    ang1 = msm.structure.get_dihedral_angles(molecular_system, quartets=phi_chains[2])
    molecular_system = msm.structure.set_dihedral_angles(molecular_system, quartets=phi_chains[2],
                                                     angles='0.0 degrees', pbc=False)
    ang2 = msm.structure.get_dihedral_angles(molecular_system, quartets=phi_chains[2])
    assert np.isclose(abs(msm.pyunitwizard.get_value(ang1[0][0])), 180)
    assert np.isclose(msm.pyunitwizard.get_value(ang2[0][0]), 0)
