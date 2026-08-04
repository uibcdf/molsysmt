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

def test_iterator_yields_molecular_systems_for_a_coordinate_only_form():
    # Without explicit attributes the iterator yields a molecular system per chunk. A DCD
    # provides no 'structure_id' and no 'time', which used to leave the internal iterator
    # unassigned and raise UnboundLocalError before the first item.
    dcd = systems['POPC membrane']['popc_membrane.dcd']
    iterator = msm.Iterator(dcd, chunk=2)

    assert iterator.arguments == ['coordinates', 'box']

    sizes = []
    first_atom = []
    for molecular_system in iterator:
        sizes.append(msm.get(molecular_system, n_structures=True))
        coordinates = msm.get(molecular_system, element='atom', coordinates=True)
        first_atom.append(puw.get_value(coordinates[0, 0]).copy())

    # Five structures in chunks of two, the last one partial.
    assert sizes == [2, 2, 1]
    # The reusable system is genuinely updated: consecutive chunks are not the same data.
    assert not np.allclose(first_atom[0], first_atom[1])


def test_iterator_yields_molecular_systems_for_an_h5msm_trajectory():
    # 'structures/id' is stored as an empty dataset in this file, so reading it indexed an
    # empty dimension. The 'time' branch of the same reader already treated that as absent.
    h5msm = systems['pentalanine']['traj_pentalanine.h5msm']
    iterator = msm.Iterator(h5msm, chunk=1000)

    sizes = [msm.get(molecular_system, n_structures=True) for molecular_system in iterator]
    assert sizes == [1000, 1000, 1000, 1000, 1000]


def test_iterator_preserves_structure_order_and_units():
    # Chunking must not reorder structures nor strip units: the chunks concatenated back
    # together have to reproduce the whole trajectory exactly.
    dcd = systems['POPC membrane']['popc_membrane.dcd']
    whole = msm.get(dcd, element='atom', coordinates=True)

    # The last chunk is partial, so the pieces are stacked by value after checking units.
    chunks = list(msm.Iterator(dcd, chunk=2, coordinates=True))
    assert [len(chunk) for chunk in chunks] == [2, 2, 1]
    assert all(puw.get_unit(chunk) == puw.get_unit(whole) for chunk in chunks)

    rebuilt = np.concatenate([puw.get_value(chunk) for chunk in chunks], axis=0)
    assert np.allclose(rebuilt, puw.get_value(whole))


def test_iterator_yielding_molecular_systems_honors_the_selection():
    dcd = systems['POPC membrane']['popc_membrane.dcd']
    iterator = msm.Iterator(dcd, selection='atom_index < 100', chunk=2)
    for molecular_system in iterator:
        assert msm.get(molecular_system, n_atoms=True) == 100


@pytest.mark.parametrize('arguments', [
    {'coordinates': True, 'time': True},
    {'time': True, 'coordinates': True},
])
def test_iterator_rejects_an_unavailable_attribute_in_any_keyword_order(arguments):
    # A DCD has no 'time'. Depending on the keyword order this used to raise
    # UnboundLocalError or, worse, append the previous iterator twice and yield no item at
    # all without reporting anything.
    dcd = systems['POPC membrane']['popc_membrane.dcd']
    with pytest.raises(msm.NotWithThisFormError, match='time'):
        msm.Iterator(dcd, chunk=2, **arguments)


@pytest.mark.parametrize('reversed_order', [False, True])
def test_iterator_yields_molecular_systems_for_a_topology_plus_trajectory(reversed_order):
    # The H5MSM file holds a single reference structure and the DCD holds twenty. Only the
    # DCD spans the structure axis, so 'structure_id' and 'time' are not iterated and the
    # result must not depend on the order the items were listed in.
    h5msm = systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5msm']
    dcd = systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd']
    composite = [dcd, h5msm] if reversed_order else [h5msm, dcd]

    iterator = msm.Iterator(composite, chunk=10)
    assert iterator.arguments == ['coordinates', 'box']

    sizes = [msm.get(molecular_system, n_structures=True) for molecular_system in iterator]
    assert sizes == [10, 10]


def test_iterator_accepts_structural_attributes_sharing_one_structure_axis():
    composite = [
        systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5msm'],
        systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd'],
    ]
    iterator = msm.Iterator(composite, chunk=10, coordinates=True, box=True)
    sizes = [len(coordinates) for coordinates, _ in iterator]
    assert sizes == [10, 10]


#def test_iterator_3():
#    iterator = msm.Iterator(molsys, selection='atom_name == "P"', coordinates=True)
#    coordinates = []
#    for aux_coordinates in iterator:
#        coordinates.append(aux_coordinates[0])
#    coordinates = puw.utils.sequences.concatenate(coordinates, value_type='numpy.ndarray')
#    assert coordinates.shape == (5, 294, 3)
