import math
import numpy as np

from molsysmt.lib.pbc.get_angles_from_box import get_angles_from_box_single_structure, get_angles_from_box
from molsysmt.lib.pbc.get_lengths_from_box import get_lengths_from_box_single_structure, get_lengths_from_box
from molsysmt.lib.pbc.unwrap import unwrap


def test_box_angle_and_length_helpers():
    box = np.diag([2.0, 3.0, 4.0]).astype(np.float64)
    assert np.allclose(get_lengths_from_box_single_structure(box), np.array([2.0, 3.0, 4.0]))
    assert np.allclose(get_angles_from_box_single_structure(box), np.array([math.pi/2]*3))

    batch = np.stack([box, box * 2.0])
    lengths = get_lengths_from_box(batch)
    angles = get_angles_from_box(batch)
    assert lengths.shape == (2, 3)
    assert angles.shape == (2, 3)
    assert np.allclose(angles[0], np.array([math.pi/2]*3))


def test_unwrap_orthogonal_and_triclinic():
    coords = np.array([
        [[0.1, 0.1, 0.1]],
        [[1.9, 0.1, 0.1]],
        [[0.2, 0.1, 0.1]],
    ], dtype=np.float64)
    box = np.stack([np.diag([2.0,2.0,2.0]) for _ in range(3)]).astype(np.float64)
    unwrap(coords, box)
    assert np.allclose(coords[:,0,0], np.array([0.1, -0.1, 0.2]), atol=1e-6)

    tri = np.array([[2.0, 0.0, 0.0], [0.5, 2.0, 0.0], [0.1, 0.2, 2.0]], dtype=np.float64)
    tri_coords = np.array([
        [[0.1, 0.1, 0.1]],
        [[1.8, 0.1, 0.1]],
    ], dtype=np.float64)
    tri_box = np.stack([tri, tri])
    unwrap(tri_coords, tri_box)
    assert tri_coords.shape == (2, 1, 3)
