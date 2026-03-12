import numpy as np

from molsysmt.lib.pbc.wrap_to_mic import wrap_to_mic
from molsysmt.lib.pbc.wrap_to_pbc import wrap_to_pbc, wrap_to_pbc_center
from molsysmt.lib.pbc.unwrap import unwrap


def test_batch_wrap_helpers_modify_coordinates_in_place_consistently():
    box = np.stack([np.diag([2.0, 2.0, 2.0]), np.diag([2.0, 2.0, 2.0])]).astype(np.float64)
    coords = np.array(
        [
            [[2.1, -0.1, 0.2], [1.9, 2.2, -0.3]],
            [[-0.2, 2.4, 2.1], [3.1, -1.9, 0.0]],
        ],
        dtype=np.float64,
    )

    mic_coords = coords.copy()
    wrap_to_mic(mic_coords, box, np.zeros(3, dtype=np.float64))
    assert mic_coords.shape == coords.shape
    assert np.all(np.abs(mic_coords) <= 1.0 + 1e-8)

    pbc_coords = coords.copy()
    wrap_to_pbc(pbc_coords, box, np.zeros(3, dtype=np.float64))
    assert np.all(pbc_coords >= -1e-8)
    assert np.all(pbc_coords < 2.0 + 1e-8)

    centered_coords = coords.copy()
    wrap_to_pbc_center(centered_coords, box, np.array([1.0, 1.0, 1.0], dtype=np.float64))
    assert centered_coords.shape == coords.shape


def test_unwrap_keeps_continuity_for_multiframe_trace():
    box = np.stack([np.diag([2.0, 2.0, 2.0]) for _ in range(4)]).astype(np.float64)
    coords = np.array(
        [
            [[0.1, 0.0, 0.0]],
            [[1.9, 0.0, 0.0]],
            [[0.2, 0.0, 0.0]],
            [[1.8, 0.0, 0.0]],
        ],
        dtype=np.float64,
    )
    unwrap(coords, box)
    deltas = np.diff(coords[:, 0, 0])
    assert np.all(np.abs(deltas) < 0.5)
