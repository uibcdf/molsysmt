import molsysmt as msm
from molsysmt.native import Structures
from molsysmt import puw
import numpy as np
import pytest


@pytest.fixture()
def structures_with_one_frame():
    coords = np.array([[[1., 2., 3.],
                        [1., 0., 1.]]])
    box = np.array([[[1., 0., 0.],
                     [0., 1., 0.],
                     [0., 0., 1.]]])
    coords = puw.quantity(coords, "nanometers")
    time = puw.quantity(np.array([10.]), "picoseconds")
    box = puw.quantity(box, "nanometers")

    return Structures(coordinates=coords, time=time, box=box)


@pytest.fixture()
def structure_with_five_frames():
    """ Returns a Structures object with five frames and three atoms"""
    coords = np.array(range(45))
    coords = coords.reshape((5, 3, 3)) * 0.1
    coords = puw.quantity(coords, "nanometers")
    box = np.zeros((5, 3, 3))
    for ii in range(box.shape[0]):
        for jj in range(box.shape[1]):
            box[ii, jj, jj] = ii * 1.
    box = puw.quantity(box, "nanometers")
    time = np.array(range(0, 5)) * 10.0
    time = puw.quantity(time, "picoseconds")
    assert time.shape == (5,)

    return Structures(coordinates=coords,
                      time=time,
                      box=box
                      )


def test_structures_constructor(structures_with_one_frame):
    assert structures_with_one_frame.n_atoms == 2
    assert structures_with_one_frame.n_structures == 1


def test_append_structures(structures_with_one_frame):
    coords = np.array([[[0., 1., 1.],
                        [2., 0., 1.]]])
    coords = puw.quantity(coords, "nanometers")
    time = puw.quantity(np.array([20.]), "picoseconds")
    box = np.array([[[1.5, 0., 0.],
                     [0., 1.4, 0.],
                     [0., 0., 1.4]]])
    box = puw.quantity(box, "nanometers")

    structure = structures_with_one_frame.copy()
    structure.append_structures(coordinates=coords,
                                time=time,
                                box=box)

    coords_expected = np.array([
        [[1., 2., 3.],
         [1., 0., 1.]],
        [[0., 1., 1.],
         [2., 0., 1.]]
    ])
    assert coords_expected.shape == (2, 2, 3)
    box_expected = np.array([
        [[1., 0., 0.],
         [0., 1., 0.],
         [0., 0., 1.]],
        [[1.5, 0., 0.],
         [0., 1.4, 0.],
         [0., 0., 1.4]]
    ])
    assert box_expected.shape == (2, 3, 3)

    assert structure.n_structures == 2
    assert structure.n_atoms == 2

    assert structure.time.shape[0] == 2
    assert np.allclose(puw.get_value(structure.time),
                       np.array([10., 20.]))

    assert structure.coordinates.shape == (2, 2, 3)
    assert np.allclose(puw.get_value(structure.coordinates),
                       coords_expected)

    assert structure.box.shape == (2, 3, 3)
    assert np.allclose(puw.get_value(structure.box),
                       box_expected)


def test_copy(structures_with_one_frame):
    structures_copy = structures_with_one_frame.copy()
    assert structures_copy.n_structures == 1
    assert structures_copy.n_atoms == 2
    assert structures_copy.box.shape == (1, 3, 3)
    assert structures_copy.coordinates.shape == (1, 2, 3)


def test_extract_atoms(structure_with_five_frames):
    structures = structure_with_five_frames.copy()
    structures_extracted_atoms = structures.extract(atom_indices=[0, 1])

    assert structures_extracted_atoms.n_atoms == 2
    assert structures_extracted_atoms.n_structures == 5
    assert structures_extracted_atoms.coordinates.shape == (5, 2, 3)
    assert structures_extracted_atoms.box.shape == (5, 3, 3)

    coordinates_expected = np.array(range(45)).reshape((5, 3, 3))
    coordinates_expected = coordinates_expected[:, 0:2, :] * 0.1
    assert np.allclose(puw.get_value(structures_extracted_atoms.coordinates),
                       coordinates_expected)
    assert np.allclose(puw.get_value(structures_extracted_atoms.time),
                       np.array(range(0, 5)) * 10.
                       )


def test_extract_structures(structure_with_five_frames):
    structure_extracted = structure_with_five_frames.copy().extract(
        structure_indices=[0, 2, 4]
    )

    assert structure_extracted.n_atoms == 3
    assert structure_extracted.n_structures == 3
    assert structure_extracted.coordinates.shape == (3, 3, 3)
    assert structure_extracted.box.shape == (3, 3, 3)

    assert np.allclose(puw.get_value(structure_extracted.time),
                       np.array([0., 20., 40.])
                       )
    coordinates_expected = np.array(range(45)).reshape((5, 3, 3))
    coordinates_expected = coordinates_expected[[0, 2, 4], :, :] * 0.1
    assert np.allclose(puw.get_value(structure_extracted.coordinates),
                       coordinates_expected)

    box = puw.get_value(structure_extracted.box)
    assert np.allclose(box[0], np.zeros((3, 3)))
    assert np.allclose(box[1],
                       np.array([[2., 0., 0.],
                                 [0., 2., 0.],
                                 [0., 0., 2.]])
                       )
    assert np.allclose(box[2],
                       np.array([[4., 0., 0.],
                                 [0., 4., 0.],
                                 [0., 0., 4.]])
                       )


def test_add():
    proline = msm.convert(msm.demo['proline dipeptide']['vacuum.msmpk'],
                          to_form='molsysmt.MolSys')
    valine = msm.convert(msm.demo['valine dipeptide']['vacuum.msmpk'],
                         to_form='molsysmt.MolSys')
    lysine = msm.convert(msm.demo['lysine dipeptide']['vacuum.msmpk'],
                         to_form='molsysmt.MolSys')

    structures = Structures()
    structures.add(proline)
    assert structures.n_structures == 1
    assert structures.n_atoms == 26
    assert structures.coordinates.shape == (1, 26, 3)

    structures.add(valine)
    assert structures.n_structures == 1
    assert structures.n_atoms == 54
    assert structures.coordinates.shape == (1, 54, 3)

    structures.add(lysine)
    assert structures.n_structures == 1
    assert structures.n_atoms == 88
    assert structures.coordinates.shape == (1, 88, 3)


def test_append():
    proline = msm.convert(msm.demo['proline dipeptide']['vacuum.msmpk'],
                          to_form='molsysmt.MolSys')

    proline_translated_1 = msm.structure.translate(proline,
                                                   translation='[0.1, 0.1, 0.1] nanometers')
    proline_translated_2 = msm.structure.translate(proline,
                                                   translation='[0.2, 0.2, 0.2] nanometers')
    structures = Structures()
    structures.add(proline)
    structures.append(proline_translated_1)
    assert structures.n_atoms == 26
    assert structures.coordinates.shape == (2, 26, 3)

    structures.append(proline_translated_2)
    assert structures.n_atoms == 26
    assert structures.coordinates.shape == (3, 26, 3)


def iterate_structure(iterator,
                      expected_iterations,
                      start=0,
                      selection=None):
    n_iterations = 0
    end = start * 9
    ii = start
    for step, time, coordinates, box in iterator:
        start = end
        end = start + 9
        expected_coordinates = np.array(range(start, end)).reshape(3, 3) * 0.1

        if selection is not None:
            expected_coordinates = expected_coordinates[selection, :]

        assert step is None
        assert puw.get_value(time) == ii * 10.
        assert np.allclose(puw.get_value(coordinates),
                           expected_coordinates)
        assert np.allclose(puw.get_value(box),
                           np.identity(3) * (ii * 1.))
        ii += 1
        n_iterations += 1

    assert n_iterations == expected_iterations


def test_iter_structures(structure_with_five_frames):
    iterate_structure(structure_with_five_frames,
                      expected_iterations=5)
    iterate_structure(structure_with_five_frames.iterate(),
                      expected_iterations=5)


def test_iterate_structure_with_custom_start(structure_with_five_frames):
    iterator = structure_with_five_frames.iterate(start=2)
    iterate_structure(iterator, expected_iterations=3, start=2)


def test_iterate_structure_with_custom_end(structure_with_five_frames):
    iterator = structure_with_five_frames.iterate(start=0,
                                                  stop=3)
    iterate_structure(iterator,
                      expected_iterations=3,
                      start=0)

    iterator = structure_with_five_frames.iterate(start=2,
                                                  stop=4)
    iterate_structure(iterator,
                      expected_iterations=2,
                      start=2)


def iterate_structure_custom_interval(iterator, start, expected_iterations):

    n_iterations = 0
    ii = start
    for step, time, coordinates, box in iterator:
        expected_coordinates = np.array(range(ii * 9,
                                              (ii * 9) + 9)).reshape(3, 3) * 0.1

        assert puw.get_value(time) == ii * 10.
        assert np.allclose(puw.get_value(box),
                           np.identity(3) * ii * 1.)
        assert np.allclose(puw.get_value(coordinates),
                           expected_coordinates
                           )
        ii += 2
        n_iterations += 1

    assert n_iterations == expected_iterations


def test_iterator_with_custom_interval(structure_with_five_frames):

    structures = structure_with_five_frames.copy()

    # We add an extra frame to the structures
    coords = np.array(range(45, 54)).reshape((1, 3, 3)) * 0.1
    coords = puw.quantity(coords, "nanometers")

    box = np.identity(3) * 5.
    box = box.reshape((1, 3, 3))
    box = puw.quantity(box, "nanometers")

    time = puw.quantity(np.array([50.]), "picoseconds")
    structures.append_structures(step=None,
                                 time=time,
                                 box=box,
                                 coordinates=coords)

    iterate_structure_custom_interval(structures.iterate(interval=2),
                                      start=0,
                                      expected_iterations=3)
    iterate_structure_custom_interval(structures.iterate(start=1, interval=2),
                                      start=1,
                                      expected_iterations=3)


def test_iterate_with_custom_selection(structure_with_five_frames):

    structures = structure_with_five_frames.copy()
    selection = [0, 2]
    iterator_1 = structures.iterate(selection=selection)
    iterate_structure(iterator_1, selection=selection, expected_iterations=5)

    selection = [0]
    iterator_2 = structures.iterate(selection=selection)
    iterate_structure(iterator_2, selection=selection, expected_iterations=5)


def test_iterate_with_custom_chunk_size(structure_with_five_frames):

    structures = structure_with_five_frames.copy()

    iterator_1 = structure_with_five_frames.iterate(chunk_size=3)

    n_iters = 0
    for step, times, coordinates, box in iterator_1:

        if n_iters == 0:
            assert times.shape == (3,)
            assert coordinates.shape == (3, 3, 3)
            assert box.shape == (3, 3, 3)
        else:
            assert times.shape == (2,)
            assert coordinates.shape == (2, 3, 3)
            assert box.shape == (2, 3, 3)

        n_iters += 1
    assert n_iters == 2

    iterator_2 = structure_with_five_frames.iterate(chunk_size=2)
    n_iters = 0
    for step, times, coordinates, box in iterator_2:

        if n_iters == 2:
            assert times.shape == (1,)
            assert coordinates.shape == (1, 3, 3)
            assert box.shape == (1, 3, 3)
        else:
            assert times.shape == (2,)
            assert coordinates.shape == (2, 3, 3)
            assert box.shape == (2, 3, 3)

        n_iters += 1
    assert n_iters == 3

    iterator_3 = structure_with_five_frames.iterate(chunk_size=5)
    n_iters = 0
    for step, times, coordinates, box in iterator_3:
        assert np.all(times == structures.time)
        assert np.all(coordinates == structures.coordinates)
        assert np.all(box == structures.box)
        n_iters += 1

    assert n_iters == 1
