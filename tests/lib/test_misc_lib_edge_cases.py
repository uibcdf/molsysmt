import numpy as np

from molsysmt.lib.pbc.get_box_from_lengths_and_angles import (
    get_box_from_lengths_and_angles_single_structure,
    get_box_from_lengths_and_angles,
)
from molsysmt.lib.pbc.get_lengths_and_angles_from_box import (
    get_lengths_and_angles_from_box_single_structure,
    get_lengths_and_angles_from_box,
)
from molsysmt.lib.pbc.wrap_to_pbc import wrap_to_pbc_center
from molsysmt.lib.series import serialized_lists


def test_box_roundtrip_and_center_wrapping_edge_cases():
    lengths = np.array([2.0, 2.5, 3.0], dtype=np.float64)
    angles = np.array([1.2, 1.1, 1.0], dtype=np.float64)
    box = get_box_from_lengths_and_angles_single_structure(lengths, angles)
    out_lengths, out_angles = get_lengths_and_angles_from_box_single_structure(box)
    assert np.allclose(out_lengths, lengths)
    assert np.allclose(out_angles, angles)

    batch_lengths = np.stack([lengths, lengths + 0.2])
    batch_angles = np.stack([angles, angles])
    batch_box = get_box_from_lengths_and_angles(batch_lengths, batch_angles)
    lengths2, angles2 = get_lengths_and_angles_from_box(batch_box)
    assert np.allclose(lengths2, batch_lengths)
    assert np.allclose(angles2, batch_angles)

    coords = np.array(
        [
            [[-0.1, 0.0, 0.0], [2.4, 2.7, 3.2]],
            [[2.2, -0.3, 0.1], [3.4, 3.5, -0.2]],
        ],
        dtype=np.float64,
    )
    wrap_to_pbc_center(coords, batch_box, np.array([1.0, 1.0, 1.0], dtype=np.float64))
    assert coords.shape == (2, 2, 3)


def test_serialized_array_input():
    arr = np.array([[1, 2], [5, 6, 7], [9]], dtype=object)
    sl = serialized_lists(arr)
    assert sl.n_indices == 3
    assert sl.n_values == 6
