"""Normalize finite nonzero Cartesian vectors without norm overflow/underflow."""

import numpy as np


def unit_vectors(values):
    """Return independent float64 rows; reject undefined Cartesian directions."""
    if hasattr(values, "unit") or hasattr(values, "units"):
        raise ValueError("Directions must be unit-free Cartesian vectors.")
    if np.iscomplexobj(values):
        raise ValueError("Directions must be real Cartesian vectors.")
    vectors = np.array(values, dtype=np.float64, copy=True)
    if vectors.shape == (3,):
        vectors = vectors.reshape(1, 3)
    if (
        vectors.ndim != 2
        or vectors.shape[1] != 3
        or vectors.shape[0] == 0
        or not np.all(np.isfinite(vectors))
    ):
        raise ValueError("Directions must contain finite nonzero Cartesian vectors.")
    scale = np.max(np.abs(vectors), axis=1, keepdims=True)
    if np.any(scale == 0):
        raise ValueError("A zero vector has no displacement direction.")
    vectors /= scale
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors
