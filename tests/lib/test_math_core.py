import math
import numpy as np

from molsysmt.lib import math as msm_math


def test_core_math_kernels():
    m = np.array([[2.0, 0.0, 0.0], [1.0, 3.0, 0.0], [4.0, 5.0, 6.0]], dtype=np.float64)
    inv = msm_math.inverse_matrix_3x3(m)
    assert np.allclose(inv @ m, np.eye(3), atol=1e-6)

    v = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    assert np.allclose(msm_math.matmul(m, v), m @ v)
    assert np.allclose(msm_math.transpmatmul(m, v), m.T @ v)

    a = np.array([1.0, 0.0, 0.0], dtype=np.float64)
    b = np.array([0.0, 1.0, 0.0], dtype=np.float64)
    c = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    assert math.isclose(msm_math.dot_product(a, a), 1.0)
    assert np.array_equal(msm_math.cross_product(a, b), c)
    assert math.isclose(msm_math.norm_vector(np.array([3.0, 4.0, 0.0], dtype=np.float64)), 5.0)
    assert np.allclose(msm_math.normalize_vector(np.array([0.0, 3.0, 4.0], dtype=np.float64)), np.array([0.0, 0.6, 0.8]))
    assert math.isclose(msm_math.angle(a, b), math.pi / 2)
    assert math.isclose(msm_math.dihedral_angle(a, b, c), math.pi / 2)

    rot_vec = np.array([1.0, 0.0, 0.0], dtype=np.float64)
    msm_math.rodrigues_rotation(rot_vec, np.array([0.0, 0.0, 1.0], dtype=np.float64), math.pi / 2)
    assert np.allclose(rot_vec, np.array([0.0, 1.0, 0.0]), atol=1e-6)

    q = np.array([math.cos(math.pi/4), 0.0, 0.0, math.sin(math.pi/4)], dtype=np.float64)
    rot = msm_math.quaternion_to_rotation_matrix(q)
    assert rot.shape == (3, 3)
    assert np.allclose(rot @ rot.T, np.eye(3), atol=1e-6)


def test_minimum_distance_helpers():
    coords = np.array([[0.0,0.0,0.0],[1.0,0.0,0.0],[4.0,0.0,0.0]], dtype=np.float64)
    include = np.array([1,1,1], dtype=np.uint8)
    bonded = np.zeros((3,3), dtype=np.uint8)
    bonded[0,1] = bonded[1,0] = 1
    assert math.isclose(msm_math.minimum_distance_masked_not_bonded(coords, include, bonded), 3.0)

    cand = np.array([[10.0,0.0,0.0],[2.0,0.0,0.0]], dtype=np.float64)
    cand_mask = np.array([1,1], dtype=np.uint8)
    bonded2 = np.zeros((3,5), dtype=np.uint8)
    assert math.isclose(msm_math.minimum_distance_between_coordinate_sets(coords, include, cand, cand_mask, 3, bonded2), 1.0)
