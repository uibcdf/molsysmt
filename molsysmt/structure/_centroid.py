"""Compute arithmetic centroids from packed, nonempty atom memberships."""

import numpy as np


def packed_centroids(coordinates, offsets, positions):
    """Reduce projected coordinate blocks without padded membership arrays."""
    return (
        np.add.reduceat(coordinates[:, positions], offsets[:-1], axis=1)
        / np.diff(offsets)[None, :, None]
    )
