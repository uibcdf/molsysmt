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

def test_get_neighbors_from_molsysmt_MolSys_1():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    CA_atoms_list = msm.select(molsys, selection='atom_name=="CA"')
    neighbors, distances = msm.structure.get_neighbors(molsys, selection=CA_atoms_list, n_neighbors=3)
    check_shape_1 = ((5000, 5, 3)==neighbors.shape)
    check_shape_2 = ((5000, 5, 3)==distances.shape)
    print(distances[2000,0,0])
    assert check_shape_1
    assert check_shape_2
    assert np.isclose(puw.get_value(distances[2000,0,0], to_unit='nm'), 0.38743175)

