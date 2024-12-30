"""
Unit and regression test for the get_lengths_and_angles_from_box module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time


def test_get_lengths_and_angles_from_box_cubic_geometry():
    molsys = msm.convert(systems['Met-enkephalin']['met_enkephalin.h5msm'], to_form='molsysmt.MolSys')
    molsys = msm.build.solvate(molsys, box_shape='cubic', clearance='14.0 angstroms', engine='PDBFixer')
    box = msm.get(molsys, element='system', box=True)
    lengths, angles = msm.pbc.get_lengths_and_angles_from_box(box)
    check_lengths = np.allclose(msm.pyunitwizard.get_value(lengths, to_unit='nm'), [[3.1236, 3.1236, 3.1236]])
    check_angles = np.allclose(msm.pyunitwizard.get_value(angles, to_unit='degrees'), [[90.000001, 90.000001, 90.000001]])
    assert check_lengths
    assert check_angles

def test_get_lengths_and_angles_from_box_octahedral_geometry():
    molsys = msm.convert(systems['Met-enkephalin']['met_enkephalin.h5msm'], to_form='molsysmt.MolSys')
    molsys = msm.build.solvate(molsys, box_shape='truncated octahedral', clearance='14.0 angstroms', engine='PDBFixer')
    box = msm.get(molsys, element='system', box=True)
    lengths, angles = msm.pbc.get_lengths_and_angles_from_box(box)
    check_lengths = np.allclose(msm.pyunitwizard.get_value(lengths, to_unit='nm'), [[3.1236, 3.1236, 3.1236]])
    check_angles = np.allclose(msm.pyunitwizard.get_value(angles, to_unit='degrees'), [[70.52878, 109.471221, 70.52878]])
    assert check_lengths
    assert check_angles


def test_get_lengths_and_angles_from_box_dodecahedral_geometry():
    molsys = msm.convert(systems['Met-enkephalin']['met_enkephalin.h5msm'], to_form='molsysmt.MolSys')
    molsys = msm.build.solvate(molsys, box_shape='rhombic dodecahedral', clearance='14.0 angstroms', engine='PDBFixer')
    box = msm.get(molsys, element='system', box=True)
    lengths, angles = msm.pbc.get_lengths_and_angles_from_box(box)
    check_lengths = np.allclose(msm.pyunitwizard.get_value(lengths, to_unit='nm'), [[3.1236, 3.1236, 3.1236]])
    check_angles = np.allclose(msm.pyunitwizard.get_value(angles, to_unit='degrees'), [[60.0, 60.0, 90.000001]])
    assert check_lengths
    assert check_angles

