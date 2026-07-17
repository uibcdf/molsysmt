"""
Unit and regression test for the iterator module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
import os
import pytest

def test_iterator_1():
    psf = systems['POPC membrane']['popc_membrane.psf']
    dcd = systems['POPC membrane']['popc_membrane.dcd']
    atoms_P = msm.select(psf, selection='atom_name == "P"')
    iterator = msm.Iterator(dcd, selection=atoms_P, coordinates=True)
    coordinates = []
    for aux_coordinates in iterator:
        coordinates.append(aux_coordinates[0])
    coordinates = puw.utils.sequences.concatenate(coordinates, value_type='numpy.ndarray')
    assert coordinates.shape == (5, 294, 3)

def test_iterator_2():
    psf = systems['POPC membrane']['popc_membrane.psf']
    dcd = systems['POPC membrane']['popc_membrane.dcd']
    iterator = msm.Iterator([psf, dcd], selection='atom_name == "P"', coordinates=True)
    coordinates = []
    for aux_coordinates in iterator:
        coordinates.append(aux_coordinates[0])
    coordinates = puw.utils.sequences.concatenate(coordinates, value_type='numpy.ndarray')
    assert coordinates.shape == (5, 294, 3)


def test_iterator_does_not_hide_backend_failures():
    structures = msm.convert(
        systems['pentalanine']['traj_pentalanine.h5'],
        to_form='molsysmt.Structures',
        structure_indices=[0],
    )
    iterator = msm.Iterator(structures, coordinates=True)

    class BrokenIterator:
        def __next__(self):
            raise RuntimeError('backend failure')

    iterator._iterators = [BrokenIterator()]

    with pytest.raises(RuntimeError, match='backend failure'):
        next(iterator)

#def test_iterator_3():
#    iterator = msm.Iterator(molsys, selection='atom_name == "P"', coordinates=True)
#    coordinates = []
#    for aux_coordinates in iterator:
#        coordinates.append(aux_coordinates[0])
#    coordinates = puw.utils.sequences.concatenate(coordinates, value_type='numpy.ndarray')
#    assert coordinates.shape == (5, 294, 3)
