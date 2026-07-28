"""Distance kernels implemented by the bundled Rust extension."""

import numpy as np

from molsysmt._private.rust_backend import (
    get_distances,
    get_distances_pairs,
    get_distances_pairs_single_structure,
    get_distances_single_structure,
    get_distances_single_system,
    get_distances_single_system_single_structure,
)


def get_distance_two_points_single_structure(point1, point2):
    """Returning the Euclidean distance between two points."""
    return float(np.linalg.norm(np.asarray(point2) - np.asarray(point1)))


__all__ = [
    "get_distance_two_points_single_structure",
    "get_distances",
    "get_distances_pairs",
    "get_distances_pairs_single_structure",
    "get_distances_single_structure",
    "get_distances_single_system",
    "get_distances_single_system_single_structure",
]
