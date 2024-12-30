"""
Unit and regression test for the get_neighbors module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

# Distance between atoms in space and time

def test_1():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    d = msm.structure.get_distances(molsys, selection=8, selection_2=18, structure_indices=2000)
    print(d[0,0,0])
    assert np.isclose(puw.get_value(d[0,0,0], to_unit='nm'), 0.38743175)

