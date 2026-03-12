import numpy as np

from molsysmt.lib.structure.get_distances import (
    get_distance_two_points_single_structure,
    get_distances_single_system_single_structure,
    get_distances_single_system,
    get_distances_single_structure,
    get_distances,
    get_distances_pairs_single_structure,
    get_distances_pairs,
)
from molsysmt.lib.structure.get_mic_distances import (
    get_mic_distance_two_points_single_structure,
    get_mic_distances_single_system_single_structure,
    get_mic_distances_single_system,
    get_mic_distances_single_structure,
    get_mic_distances,
    get_mic_distances_pairs_single_structure,
    get_mic_distances_pairs,
)


def test_distance_shape_variants_for_plain_and_mic_kernels():
    coords = np.array([[0.,0.,0.],[1.,0.,0.],[1.,1.,0.],[1.,1.,1.]], dtype=np.float64)
    batch = np.stack([coords, coords + 0.5])
    box = np.stack([np.diag([3.0,3.0,3.0]), np.diag([3.0,3.0,3.0])]).astype(np.float64)

    assert np.isclose(get_distance_two_points_single_structure(coords[0], coords[1]), 1.0)
    assert get_distances_single_system_single_structure(coords[:3]).shape == (3,3)
    assert get_distances_single_system(batch[:,:3,:]).shape == (2,3,3)
    assert get_distances_single_structure(coords[:2], coords[2:]).shape == (2,2)
    assert get_distances(batch[:,:2,:], batch[:,2:,:]).shape == (2,2,2)
    assert get_distances_pairs_single_structure(coords[:2], coords[2:]).shape == (2,)
    assert get_distances_pairs(batch[:,:2,:], batch[:,2:,:]).shape == (2,2)

    assert np.isclose(get_mic_distance_two_points_single_structure(coords[0], np.array([2.9,0.0,0.0]), box[0], None, None), 0.1)
    assert get_mic_distances_single_system_single_structure(coords[:3], box[0]).shape == (3,3)
    assert get_mic_distances_single_system(batch[:,:3,:], box).shape == (2,3,3)
    assert get_mic_distances_single_structure(coords[:2], coords[2:], box[0]).shape == (2,2)
    assert get_mic_distances(batch[:,:2,:], batch[:,2:,:], box).shape == (2,2,2)
    assert get_mic_distances_pairs_single_structure(coords[:2], coords[2:], box[0]).shape == (2,)
    assert get_mic_distances_pairs(batch[:,:2,:], batch[:,2:,:], box).shape == (2,2)
