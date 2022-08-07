"""
Unit and regression test for the box_from_box_lengths_and_angles module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_box_from_box_lengths_and_angles_1():
    angles = [[60.0, 60.0, 90.0]] * msm.puw.unit('degrees')
    lengths = [[2.0, 2.0, 2.0]] * msm.puw.unit('nm')
    box = msm.pbc.box_from_box_lengths_and_angles(lengths, angles)
    true_box = np.array([[[2.0, 0.0, 0.0],
                        [0.0, 2.0, 0.0],
                        [1.0, 1.0, 1.414214]]])
    check = np.allclose(true_box, msm.puw.get_value(box, to_unit='nm'))
    assert check

