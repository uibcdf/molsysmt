import molsysmt as msm
from molsysmt import puw
import molsysmt._private.exceptions.value_errors as exc
import mdtraj as mdt
import numpy as np
import pytest


@pytest.fixture()
def pentalanine_iterator():

    pentalanine_file = msm.demo["pentalanine"]["traj.h5"]
    return msm.structure.Iterator(pentalanine_file)


@pytest.fixture()
def pentalanine_structures():
    pentalanine = msm.convert(msm.demo["pentalanine"]["traj.h5"])
    return pentalanine.structures.copy()


def test_iterator_constructor(pentalanine_iterator, pentalanine_structures):

    assert pentalanine_iterator.molecular_system.structures.n_atoms == 62
    assert pentalanine_iterator.molecular_system.structures.n_structures == 5000
    assert pentalanine_iterator._form == "molsysmt.MolSys"

    pentalanine_file = msm.demo["pentalanine"]["traj.h5"]
    pentalanine = msm.convert(pentalanine_file)
    iterator = msm.structure.Iterator(pentalanine)
    assert iterator.molecular_system.structures.n_atoms == 62
    assert iterator.molecular_system.structures.n_structures == 5000
    assert iterator._form == "molsysmt.MolSys"

    iterator = msm.structure.Iterator(pentalanine_structures)
    assert iterator.molecular_system.n_atoms == 62
    assert iterator.molecular_system.n_structures == 5000
    assert iterator._form == "molsysmt.Structures"


def test_setting_iterator_properties(pentalanine_iterator):

    iterator = pentalanine_iterator
    iterator.start = 4
    iterator.interval = 2
    iterator.stop = 50
    iterator.selection = list(range(31))


def test_setting_invalid_properties_raises_error(pentalanine_iterator):

    with pytest.raises(exc.IteratorStartError):
        pentalanine_iterator.start = 5100

    with pytest.raises(exc.IteratorIntervalError):
        pentalanine_iterator.interval = -2

    with pytest.raises(exc.IteratorChunkSizeError):
        pentalanine_iterator.chunk_size = 200000

    with pytest.raises(exc.IteratorStopError):
        pentalanine_iterator.stop = 5100


def test_iterator_number_of_atoms(pentalanine_iterator,
                                  pentalanine_structures):

    assert pentalanine_iterator._get_num_atoms() == 62

    iterator = msm.structure.Iterator(pentalanine_structures)
    assert iterator._get_num_atoms() == 62


def test_iterator_number_of_structures(pentalanine_iterator,
                                  pentalanine_structures):

    assert pentalanine_iterator._get_num_structures() == 5000

    iterator = msm.structure.Iterator(pentalanine_structures)
    assert iterator._get_num_structures() == 5000


def check_iterator_coordinates_time_and_box(iterator,
                                            expected_time,
                                            expected_coords,
                                            expected_coords_shape,
                                            expected_box):

    _, time, coordinates, box = next(iterator)
    assert puw.get_value(time) == expected_time
    assert coordinates.shape == expected_coords_shape
    assert np.allclose(puw.get_value(coordinates[0:5]),
                       expected_coords)

    assert box.shape == (3, 3)
    assert np.allclose(puw.get_value(box),
                       expected_box)


def test_iterator_with_h5_file():
    pentalanine_file = msm.demo["pentalanine"]["traj.h5"]

    iterator = msm.structure.Iterator(pentalanine_file)
    # We only test the first 5 atoms for simplicity
    timestep_coords = np.array([[0.7249491, 0.28118464, -0.06514733],
                                [0.8183724, 0.33541468, -0.07971666],
                                [0.82463497, 0.38432965, -0.17692305],
                                [0.88794595, 0.25160828, -0.08384151],
                                [0.8513755, 0.42293516, 0.03777996]])
    timestep_box = np.array([[2., 0., 0.],
                             [0., 2., 0.],
                             [0., 0., 2.]])
    check_iterator_coordinates_time_and_box(
        iterator,
        10.,
        timestep_coords,
        (62, 3),
        timestep_box
    )

    timestep_coords = np.array([[0.49193183, 0.3567681, 0.28309438],
                                [0.49901953, 0.46519688, 0.2916948],
                                [0.58446306, 0.4869771, 0.35577384],
                                [0.41150057, 0.51321983, 0.33545825],
                                [0.5144549, 0.5183858, 0.15133896]])
    check_iterator_coordinates_time_and_box(
        iterator,
        20.,
        timestep_coords,
        (62, 3),
        timestep_box
    )

    timestep_coords = np.array([[1.6990486, 1.0393645, 0.43421224, ],
                                [1.6204891, 0.98685825, 0.37987524],
                                [1.6354617, 0.88034177, 0.36223724],
                                [1.6188515, 1.0372851, 0.28325504],
                                [1.4931669, 0.99599355, 0.46171018]])
    check_iterator_coordinates_time_and_box(
        iterator,
        30.,
        timestep_coords,
        (62, 3),
        timestep_box
    )

    # Check that the iterator finishes after the 4998 remaining iterations
    current_frame = 2
    current_time = 30.
    for _, time, coordinates, box in iterator:
        current_frame += 1
        current_time += 10
        assert puw.get_value(time) == current_time
        assert coordinates.shape == (62, 3)
        assert box.shape == (3, 3)

    assert current_frame == 4999
    assert current_time == 50000.0


def test_iterator_with_mdtraj():
    topology_file = msm.demo['nglview']['md_1u19.gro']
    traj_file = msm.demo['nglview']['md_1u19.xtc']

    traj = mdt.load(traj_file, top=topology_file)

    iterator = msm.structure.Iterator(traj)
    assert iterator._n_atoms == 5547
    assert iterator._n_structures == 51

    current_frame = 0
    current_time = 0

    for _, time, coordinates, box in iterator:

        assert puw.get_value(time) == current_time
        assert coordinates.shape == (5547, 3)
        assert box.shape(3, 3)
        current_frame += 1
        current_time += 20

    assert current_frame == 50
    assert current_time == 1000.0
    final_box = np.array([[7.988997, 0., 0.],
                          [0., 7.988997, 0.],
                          [0., 0., 9.910033]])
    assert np.allclose(box, final_box)
