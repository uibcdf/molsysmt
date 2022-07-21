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


def test_extract():
    pass


def test_add():
    pass
