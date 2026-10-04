"""Validating explicit zero-based residue pairs for disulfide assembly."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_disulfide_group_pairs(disulfide_group_pairs, caller=None):
    if disulfide_group_pairs is None:
        return np.empty((0, 2), dtype=np.int64)
    try:
        pairs = np.asarray(disulfide_group_pairs)
    except (TypeError, ValueError) as error:
        raise ArgumentError(
            "disulfide_group_pairs", value=disulfide_group_pairs, caller=caller
        ) from error
    if (
        pairs.ndim != 2
        or pairs.shape[1] != 2
        or pairs.dtype.kind not in "iu"
        or np.any(pairs < 0)
        or np.any(pairs[:, 0] == pairs[:, 1])
    ):
        raise ArgumentError(
            "disulfide_group_pairs", value=disulfide_group_pairs, caller=caller
        )
    return pairs.copy()
