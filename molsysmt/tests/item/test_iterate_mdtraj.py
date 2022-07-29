from molsysmt.item.mdtraj_Trajectory.iterate import iterate_mdtraj_trajectory
import molsysmt as msm
from molsysmt import puw
import numpy as np
import mdtraj as mdt
import mdtraj.core.element as mdt_element
import pytest


@pytest.fixture()
def mdtraj_trajectory_with_five_frames():
    """ Returns a mdtraj trajectory with five frames and
        five atoms
    """
    coordinates = np.ones((5, 5, 3), dtype="float")
    for ii in range(coordinates.shape[0]):
        coordinates[ii] *= (ii * 1.)

    angles = np.ones((5, 3), dtype="float")
    lengths = np.ones((5, 3), dtype="float")
    for ii in range(angles.shape[0]):
        angles[ii] *= np.radians(ii + 1 * 20.)
        lengths[ii] *= (ii * 1.)

    time = np.arange(50., step=10.)

    # The trajectory needs a topology to be instantiated. We create
    # a mock topology with five atoms.
    topology = mdt.Topology()
    chain = topology.add_chain()
    residue = topology.add_residue("ALA", chain)
    element = mdt_element.carbon
    for ii in range(coordinates.shape[0]):
        topology.add_atom("CA", element, residue)

    return mdt.Trajectory(xyz=coordinates,
                          time=time,
                          topology=topology,
                          unitcell_angles=angles,
                          unitcell_lengths=lengths
                          )


def iterate_structure(iterator,
                      expected_iterations,
                      start=0,
                      selection=None,
                      interval=1):
    n_iterations = 0
    ii = start
    for time, coordinates, box in iterator:

        expected_coordinates = np.ones((5, 3), dtype="float") * ii * 1.

        if selection is not None:
            expected_coordinates = expected_coordinates[selection, :]
            assert coordinates.shape == (len(selection), 3)
        else:
            assert coordinates.shape == (5, 3)

        assert puw.get_value(time) == ii * 10.
        assert np.allclose(puw.get_value(coordinates),
                           expected_coordinates)
        assert box.shape == (3, 3)

        ii += interval
        n_iterations += 1

    assert n_iterations == expected_iterations


def test_iterate_mdtraj_trajectory(mdtraj_trajectory_with_five_frames):

    iterator = iterate_mdtraj_trajectory(mdtraj_trajectory_with_five_frames)
    iterate_structure(iterator,
                      expected_iterations=5)

    # Iterate with a custom stop
    iterator = iterate_mdtraj_trajectory(mdtraj_trajectory_with_five_frames,
                                         stop=3)
    iterate_structure(iterator,
                      expected_iterations=3)

    # Iterate with custom start
    iterator = iterate_mdtraj_trajectory(mdtraj_trajectory_with_five_frames,
                                         start=2)
    iterate_structure(iterator,
                      expected_iterations=3,
                      start=2)

    # Iterate with custom start and stop
    iterator = iterate_mdtraj_trajectory(mdtraj_trajectory_with_five_frames,
                                         start=1,
                                         stop=4)
    iterate_structure(iterator,
                      expected_iterations=3,
                      start=1)

    # Iterate with custom selection
    iterator = iterate_mdtraj_trajectory(mdtraj_trajectory_with_five_frames,
                                         selection=[0, 2, 4])
    iterate_structure(iterator,
                      expected_iterations=5,
                      selection=[0, 2, 4],
                      )

    # Iterate with custom interval
    iterator = iterate_mdtraj_trajectory(mdtraj_trajectory_with_five_frames,
                                         interval=2)
    iterate_structure(iterator,
                      expected_iterations=3,
                      interval=2
                      )


def test_iterate_mdtraj_with_custom_chunk_size(mdtraj_trajectory_with_five_frames):
    iterator = iterate_mdtraj_trajectory(mdtraj_trajectory_with_five_frames,
                                         chunk_size=2)

    time, coords, box = next(iterator)
    assert np.all(puw.get_value(time) == np.array([0., 10.]))
    assert box.shape == (2, 3, 3)
    assert coords.shape == (2, 5, 3)
    assert np.all(puw.get_value(coords[0]) == np.zeros((5, 3), dtype="float"))
    assert np.all(puw.get_value(coords[1]) == np.ones((5, 3), dtype="float"))

    time, coords, box = next(iterator)
    assert np.all(puw.get_value(time) == np.array([20., 30.]))
    assert box.shape == (2, 3, 3)
    assert coords.shape == (2, 5, 3)
    assert np.all(puw.get_value(coords[0]) == np.ones((5, 3), dtype="float") * 2.)
    assert np.all(puw.get_value(coords[1]) == np.ones((5, 3), dtype="float") * 3.)

    time, coords, box = next(iterator)
    assert np.all(puw.get_value(time) == np.array([40.]))
    assert box.shape == (1, 3, 3)
    assert coords.shape == (1, 5, 3)
    assert np.all(puw.get_value(coords[0]) == np.ones((1, 5, 3), dtype="float") * 4.)


def test_iterate_pentalanine_with_mdtraj_trajectory():
    traj = mdt.load(msm.demo["pentalanine"]["traj.h5"])

    n_iterations = 0
    expected_time = 10.
    iterator = iterate_mdtraj_trajectory(traj)
    for time, coordinates, box in iterator:
        assert puw.get_value(time) == expected_time
        assert coordinates.shape == (62, 3)
        assert box.shape == (3, 3)

        expected_time += 10.
        n_iterations += 1

    assert puw.get_unit(time) == "picosecond"
    assert puw.get_unit(coordinates) == "nanometer"
    assert puw.get_unit(box) == "nanometer"

    assert n_iterations == 5000
