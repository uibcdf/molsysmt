"""
Unit and regression test for the get_geometric_center module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np
import importlib

get_center_module = importlib.import_module("molsysmt.structure.get_center")

# Distance between atoms in space and time

def test_get_center_molsysmt_MolSys_1():

    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    list_CAs = msm.select(molsys, selection='atom_name=="CA"')
    n_atoms_CAs = len(list_CAs)
    center = msm.structure.get_center(molsys, selection=list_CAs, weights=np.ones(n_atoms_CAs))
    n_structures = msm.get(molsys, element='system', n_structures=True)
    check_shape = np.all((n_structures,1,3)==center.shape)
    true_values = np.array([[[ 0.79670861,  1.07878454, -0.02861541]],
       [[ 0.83204994,  1.10665931, -0.06361365]],
       [[ 0.77414551,  0.99350907,  0.01043041]]])
    check_values = np.allclose(true_values, msm.pyunitwizard.get_value(center[1007:1010], to_unit='nm'))
    assert check_shape and check_values


def test_get_center_uses_canonical_coordinate_arrays_without_reextracting(monkeypatch):

    molsys = msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')
    call_count = {'n': 0}

    original = get_center_module.extract_coordinates_value_and_unit

    def _counting_helper(*args, **kwargs):
        call_count['n'] += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(get_center_module, 'extract_coordinates_value_and_unit', _counting_helper)

    center = msm.structure.get_center(molsys)

    assert center.shape == (3, 1, 3)
    assert call_count['n'] == 1
