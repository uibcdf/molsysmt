"""Measure numeric triplets in one explicitly observed image."""

import numpy as np


def triplet_geometry(observed):
    """Return all three distances and angles at atoms 0 and 1 in radians.

    Lengths retain the input coordinate unit. Undefined zero-length angles
    return NaN. No chemistry, PBC reconstruction or interaction rule is applied.
    """
    ab, ac, bc = (
        observed[:, 1] - observed[:, 0],
        observed[:, 2] - observed[:, 0],
        observed[:, 2] - observed[:, 1],
    )
    dab, dac, dbc = [np.linalg.norm(vector, axis=1) for vector in (ab, ac, bc)]
    cosine_a = np.divide(
        np.einsum("ij,ij->i", ab, ac),
        dab * dac,
        out=np.full(len(observed), np.nan),
        where=dab * dac > 0,
    )
    cosine_b = np.divide(
        np.einsum("ij,ij->i", -ab, bc),
        dab * dbc,
        out=np.full(len(observed), np.nan),
        where=dab * dbc > 0,
    )
    return (
        dab,
        dac,
        dbc,
        np.arccos(np.clip(cosine_a, -1, 1)),
        np.arccos(np.clip(cosine_b, -1, 1)),
    )
