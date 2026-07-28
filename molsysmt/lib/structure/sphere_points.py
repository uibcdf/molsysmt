"""Geometry helpers shared by solvent-accessibility implementations."""

import math

import numpy as np


def get_fibonacci_sphere_points(n_points: int) -> np.ndarray:
    """Generating evenly distributed points on a unit sphere."""
    indices = np.arange(n_points, dtype=np.float64)
    golden_ratio = (1.0 + math.sqrt(5.0)) / 2.0
    theta = np.arccos(1.0 - 2.0 * (indices + 0.5) / n_points)
    phi = 2.0 * math.pi * indices / golden_ratio
    return np.column_stack(
        (
            np.sin(theta) * np.cos(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(theta),
        )
    )
