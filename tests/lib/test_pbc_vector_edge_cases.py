import numpy as np

from molsysmt.lib.pbc import (
    box_is_orthogonal_single_structure,
    box_is_orthogonal,
    get_lengths_and_angles_from_box_single_structure,
    get_lengths_and_angles_from_box,
    wrap_to_mic_vector_single_structure,
    wrap_to_pbc_vector_single_structure,
    wrap_to_pbc_center_vector_single_structure,
)


def test_pbc_vector_helpers_on_orthogonal_and_triclinic_boxes():
    ortho = np.diag([2.0, 3.0, 4.0]).astype(np.float64)
    tri = np.array([[2.0, 0.0, 0.0], [0.5, 2.0, 0.0], [0.1, 0.2, 2.0]], dtype=np.float64)

    assert box_is_orthogonal_single_structure(ortho)
    assert not box_is_orthogonal_single_structure(tri)
    assert np.array_equal(box_is_orthogonal(np.stack([ortho, tri])), np.array([True, False]))

    lengths_o, angles_o = get_lengths_and_angles_from_box_single_structure(ortho)
    assert lengths_o.shape == (3,)
    assert angles_o.shape == (3,)

    lengths_b, angles_b = get_lengths_and_angles_from_box(np.stack([ortho, tri]))
    assert lengths_b.shape == (2, 3)
    assert angles_b.shape == (2, 3)

    vector = np.array([2.8, -1.7, 0.0], dtype=np.float64)
    mic = wrap_to_mic_vector_single_structure(vector, ortho, None, None)
    assert mic.shape == (3,)
    assert np.all(np.abs(mic) <= np.array([1.0, 1.5, 2.0]) + 1e-8)

    pbc = wrap_to_pbc_vector_single_structure(np.array([-0.1, 3.1, 4.2], dtype=np.float64), ortho, None, None)
    assert np.all(pbc >= -1e-8)
    assert np.all(pbc < np.array([2.0, 3.0, 4.0]) + 1e-8)

    center_pbc = wrap_to_pbc_center_vector_single_structure(np.array([2.8, -1.2, 4.1], dtype=np.float64), ortho, None, None)
    assert center_pbc.shape == (3,)

    tri_mic = wrap_to_mic_vector_single_structure(np.array([2.2, -1.4, 0.6], dtype=np.float64), tri, None, None)
    assert tri_mic.shape == (3,)
