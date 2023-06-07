"""
Unit and regression test for the iterator module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
from molsysmt import pyunitwizard as puw
import numpy as np
import os

def test_iterator_1():
    psf = tests_systems['POPC membrane']['popc_membrane.psf']
    dcd = tests_systems['POPC membrane']['popc_membrane.dcd']
    atoms_P = msm.select(psf, selection='atom_name == "P"')
    iterator = msm.Iterator(dcd, selection=atoms_P, coordinates=True)
    coordinates = []
    for aux_coordinates in iterator:
        coordinates.append(aux_coordinates[0])
    coordinates = puw.concatenate(coordinates, type_value='numpy.ndarray')
    assert coordinates.shape == (50, 294, 3)

def test_iterator_2():
    psf = tests_systems['POPC membrane']['popc_membrane.psf']
    dcd = tests_systems['POPC membrane']['popc_membrane.dcd']
    iterator = msm.Iterator([psf, dcd], selection='atom_name == "P"', coordinates=True)
    coordinates = []
    for aux_coordinates in iterator:
        coordinates.append(aux_coordinates[0])
    coordinates = puw.concatenate(coordinates, type_value='numpy.ndarray')
    assert coordinates.shape == (50, 294, 3)

def test_iterator_3():
    msmpk = tests_systems['POPC membrane']['popc_membrane.msmpk']
    molsys = msm.convert(msmpk)
    iterator = msm.Iterator(molsys, selection='atom_name == "P"', coordinates=True)
    coordinates = []
    for aux_coordinates in iterator:
        coordinates.append(aux_coordinates[0])
    coordinates = puw.concatenate(coordinates, type_value='numpy.ndarray')
    assert coordinates.shape == (50, 294, 3)

