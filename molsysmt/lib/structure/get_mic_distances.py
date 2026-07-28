"""Minimum-image distance kernels implemented by the bundled Rust extension."""

import numpy as np

from molsysmt._private.rust_backend import (
    get_mic_distances,
    get_mic_distances_pairs,
    get_mic_distances_pairs_single_structure,
    get_mic_distances_single_structure,
    get_mic_distances_single_system,
    get_mic_distances_single_system_single_structure,
    wrap_to_mic_vector_single_structure,
)


def get_mic_distance_two_points_single_structure(
    point1,
    point2,
    box,
    inv_box=None,
    orthogonal=None,
):
    """Returning the minimum-image distance between two points."""
    displacement = np.asarray(point2, dtype=np.float64) - np.asarray(
        point1, dtype=np.float64
    )
    wrapped = wrap_to_mic_vector_single_structure(displacement, box)
    return float(np.linalg.norm(wrapped))


__all__ = [
    "get_mic_distance_two_points_single_structure",
    "get_mic_distances",
    "get_mic_distances_pairs",
    "get_mic_distances_pairs_single_structure",
    "get_mic_distances_single_structure",
    "get_mic_distances_single_system",
    "get_mic_distances_single_system_single_structure",
]
