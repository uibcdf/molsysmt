"""
Unit and regression test for the get_dihedral_angles module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_get_dihedral_angles_from_molsysmt_MolSys_1():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    covalent_chains = msm.topology.get_covalent_chains(molsys, chain=['atom_name=="C"', 'atom_name=="N"',
                                                               'atom_name=="CA"', 'atom_name=="C"'])
    dihedral_angles = msm.structure.get_dihedral_angles(molsys, quartets=covalent_chains[2])
    check1 = np.allclose(np.array([[-180.0]]), msm.pyunitwizard.get_value(dihedral_angles, to_unit='degrees'))
    check2 = np.allclose(np.array([[180.0]]), msm.pyunitwizard.get_value(dihedral_angles, to_unit='degrees'))
    assert (check1 or check2)

def test_get_dihedral_angles_from_molsysmt_MolSys_2():
    molsys = msm.convert(msm.demo['Met-enkephalin']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    covalent_chains = msm.topology.get_dihedral_quartets(molsys, phi=True)
    dihedral_angles = msm.structure.get_dihedral_angles(molsys, quartets=covalent_chains)
    true_value = np.array([[-180.0, -180.0, -180.0, -180.0]])
    check1 = np.allclose(true_value,msm.pyunitwizard.get_value(dihedral_angles, to_unit='degrees'))
    true_value = np.array([[180.0, 180.0, 180.0, 180.0]])
    check2 = np.allclose(true_value,msm.pyunitwizard.get_value(dihedral_angles, to_unit='degrees'))
    assert (check1 or check2)

def test_get_dihedral_angles_from_molsysmt_MolSys_3():
    molsys = msm.convert(msm.demo['pentalanine']['traj.h5'], to_form='molsysmt.MolSys')
    phi_angles, psi_angles = msm.structure.get_dihedral_angles(molsys, selection='group_index==[3,4]', phi=True, psi=True)
    dihedral_angles = np.hstack([phi_angles, psi_angles])
    true_shape = (5000, 2)
    true_values_1 = np.array([[ -72.00828191,  135.54164973],
       [ -73.23111834,  116.08019998],
       [-149.48606282, -138.74536681],
       [ -56.40506617,  -54.83413539],
       [-148.49096248,  -53.21114699]])
    true_values_2 = np.array([[-144.99215202,  133.44230978],
       [-154.89774428,  124.53546743],
       [-144.51390298,  155.38000731],
       [-151.18403997,  165.1925445 ],
       [-158.63503642,  156.74708408]])
    true_values_3 = np.array([[-115.83193832,  -32.86894649],
       [ -55.74428402,  -44.34198217],
       [ -57.74793021,  -44.0842576 ],
       [ -93.01243813,  -43.00716069],
       [-112.66513177,  -28.18984838]])
    check_shape = np.all(true_shape==dihedral_angles.shape)
    check_value_1 = np.allclose(true_values_1,msm.pyunitwizard.get_value(dihedral_angles[0:5], to_unit='degrees'))
    check_value_2 = np.allclose(true_values_2,msm.pyunitwizard.get_value(dihedral_angles[1000:1005], to_unit='degrees'))
    check_value_3 = np.allclose(true_values_3,msm.pyunitwizard.get_value(dihedral_angles[2000:2005], to_unit='degrees'))
    assert check_shape
    assert check_value_1
    assert check_value_2
    assert check_value_3

def test_get_dihedral_angles_from_molsysmt_MolSys_4():
    molsys = msm.convert(msm.demo['pentalanine']['traj.h5'], to_form='molsysmt.MolSys')
    dihedral_angles = msm.structure.get_dihedral_angles(molsys, phi=True)
    true_shape = (5000, 5)
    check_shape = np.all(true_shape==dihedral_angles.shape)
    assert check_shape

