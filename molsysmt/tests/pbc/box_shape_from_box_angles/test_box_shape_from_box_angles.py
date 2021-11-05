"""
Unit and regression test for the box_shape_from_box_angles module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_box_shape_from_box_angles_1():
    angles = [[90.0, 90.0, 90.0]] * msm.puw.unit('degrees')
    shape = msm.pbc.box_shape_from_box_angles(angles)
    assert (shape == 'cubic')

def test_box_shape_from_box_angles_2():
    angles = [[70.52878, 109.471221, 70.52878]] * msm.puw.unit('degrees')
    shape = msm.pbc.box_shape_from_box_angles(angles)
    assert (shape == 'truncated octahedral')

def test_box_shape_from_box_angles_3():
    angles = [[60.0, 60.0, 90.0]] * msm.puw.unit('degrees')
    shape = msm.pbc.box_shape_from_box_angles(angles)
    assert (shape == 'rhombic dodecahedral')

def test_box_shape_from_box_angles_4():
    angles = [[70.0, 80.0, 90.0]] * msm.puw.unit('degrees')
    shape = msm.pbc.box_shape_from_box_angles(angles)
    assert (shape == 'triclinic')

