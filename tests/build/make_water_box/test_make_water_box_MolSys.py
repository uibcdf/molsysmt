"""
Unit and regression test for the solvate module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import pytest
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time

def test_make_water_box_MolSys_1():

    box = np.zeros((3,3))
    box[0,0] = 5.0
    box[1,1] = 5.0
    box[2,2] = 3.0
    box = msm.pyunitwizard.quantity(box, 'nm')

    molsys = msm.build.make_water_box(box)

    n_waters = msm.get(molsys, n_waters=True)
    coordinates = msm.get(molsys, target='atom', coordinates=True)
    coordinates_value = msm.pyunitwizard.get_value(coordinates, to_unit='nm')

    assert n_waters==2536
    assert coordinates_value[0,:,0].min() >= -0.1
    assert coordinates_value[0,:,1].min() >= -0.1
    assert coordinates_value[0,:,2].min() >= -0.1
    assert coordinates_value[0,:,0].max() <= 5.1
    assert coordinates_value[0,:,1].max() <= 5.1
    assert coordinates_value[0,:,2].max() <= 3.1

