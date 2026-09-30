"""Packing variable-length integer memberships without padded arrays."""

import numpy as np


def pack_membership(groups):
    """Pack index groups into int64 values and offsets, including empty input."""
    offsets = np.zeros(len(groups) + 1, dtype=np.int64)
    np.cumsum([len(group) for group in groups], out=offsets[1:])
    return np.asarray(
        [atom for group in groups for atom in group], dtype=np.int64
    ), offsets
