"""
Unit and regression test for the box_angles_from_box_vectors module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_box_angles_from_box_vectors_1():
    molsys = msm.demo.classes.metenkephalin()
    molsys = msm.build.solvate(molsys, box_geometry='cubic', clearance='14.0 angstroms', engine='PDBFixer')
    box = msm.get(molsys, target='system', box=True)
    angles = msm.pbc.box_angles_from_box_vectors(box)
    check = np.allclose(msm.puw.get_value(angles, to_unit='degrees'), [[90.000001, 90.000001, 90.000001]])
    assert check

def test_box_angles_from_box_vectors_2():
    molsys = msm.demo.classes.metenkephalin()
    molsys = msm.build.solvate(molsys, box_geometry='truncated octahedral', clearance='14.0 angstroms', engine='PDBFixer')
    box = msm.get(molsys, target='system', box=True)
    angles = msm.pbc.box_angles_from_box_vectors(box)
    check = np.allclose(msm.puw.get_value(angles, to_unit='degrees'), [[70.52878, 109.471221, 70.52878]])
    assert check

def test_box_angles_from_box_vectors_3():
    molsys = msm.demo.classes.metenkephalin()
    molsys = msm.build.solvate(molsys, box_geometry='rhombic dodecahedral', clearance='14.0 angstroms', engine='PDBFixer')
    box = msm.get(molsys, target='system', box=True)
    angles = msm.pbc.box_angles_from_box_vectors(box)
    check = np.allclose(msm.puw.get_value(angles, to_unit='degrees'), [[60.0, 60.0, 90.000001]])
    assert check

