import numpy as np

import molsysmt as msm


def test_iterator_with_h5_file():
    pentalanine_file = msm.demo["pentalanine"]["traj.h5"]

    iterator = msm.structure.Iterator(pentalanine_file)
    assert iterator.n_atoms == 62
    assert iterator.n_frames == 5000

    frame, time, coordinates, box = next(iterator)
    assert frame == 0
    assert time == 10.
    assert coordinates.shape == (62, 3)
    # We only test coordinates of first five atoms for simplicity
    timestep_coords = np.array([[0.7249491, 0.28118464, -0.06514733],
                                [0.8183724, 0.33541468, -0.07971666],
                                [0.82463497, 0.38432965, -0.17692305],
                                [0.88794595, 0.25160828, -0.08384151],
                                [0.8513755, 0.42293516, 0.03777996]])
    assert np.allclose(coordinates[0:5], timestep_coords)

    assert box.shape == (3, 3)
    timestep_box = np.array([[2., 0., 0.],
                             [0., 2., 0.],
                             [0., 0., 2.]])
    assert np.allclose(box, timestep_box)

    frame, time, coordinates, box = next(iterator)
    assert frame == 1
    assert time == 20.
    assert coordinates.shape == (62, 3)
    # We only test coordinates of first five atoms for simplicity
    timestep_coords = np.array([[0.49193183, 0.3567681, 0.28309438],
                                [0.49901953, 0.46519688, 0.2916948],
                                [0.58446306, 0.4869771, 0.35577384],
                                [0.41150057, 0.51321983, 0.33545825],
                                [0.5144549, 0.5183858, 0.15133896]])
    assert np.allclose(coordinates[0:5], timestep_coords)

    assert box.shape == (3, 3)
    timestep_box = np.array([[2., 0., 0.],
                             [0., 2., 0.],
                             [0., 0., 2.]])
    assert np.allclose(box, timestep_box)

    frame, time, coordinates, box = next(iterator)
    assert frame == 2
    assert time == 30.
    assert coordinates.shape == (62, 3)
    # We only test coordinates of first five atoms for simplicity
    timestep_coords = np.array([[1.6990486, 1.0393645, 0.43421224, ],
                                [1.6204891, 0.98685825, 0.37987524],
                                [1.6354617, 0.88034177, 0.36223724],
                                [1.6188515, 1.0372851, 0.28325504],
                                [1.4931669, 0.99599355, 0.46171018]])
    assert np.allclose(coordinates[0:5], timestep_coords)

    # Check that the iterator finishes after the 4998 iterations
    current_frame = 2
    current_time = 30.
    for frame, time, coordinates, box in iterator:
        current_frame += 1
        current_time += 10
        assert frame == current_frame
        assert time == current_time
        assert coordinates.shape == (62, 3)
        assert box.shape(3, 3)

    assert current_frame == 4999
    assert current_time == 50000.0


def test_iterator_with_gromacs_file():
    traj_file = msm.demo['nglview']['md_1u19.gro']
    topology_file = msm.demo['nglview']['md_1u19.gro']

    iterator = msm.structure.Iterator([traj_file, topology_file])
    assert iterator.n_atoms == 5547
    assert iterator.n_frames == 51

    current_frame = 0
    current_time = 0

    for frame, time, coordinates, box in iterator:
        assert frame == current_frame
        assert time == current_time
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
