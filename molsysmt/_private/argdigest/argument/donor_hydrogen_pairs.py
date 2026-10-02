"""Validate explicit source donor/H pairs without silently coercing indices."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_donor_hydrogen_pairs(donor_hydrogen_pairs, caller=None):
    if donor_hydrogen_pairs is None:
        return None
    try:
        array = np.asarray(donor_hydrogen_pairs)
    except (TypeError, ValueError):
        raise ArgumentError(
            "donor_hydrogen_pairs", value=donor_hydrogen_pairs, caller=caller
        ) from None
    if isinstance(donor_hydrogen_pairs, (list, tuple)) and any(
        isinstance(item, (bool, np.bool_))
        for item in np.asarray(donor_hydrogen_pairs, dtype=object).flat
    ):
        raise ArgumentError(
            "donor_hydrogen_pairs", value=donor_hydrogen_pairs, caller=caller
        )
    if array.size == 0 and array.shape in {(0,), (0, 2)}:
        return np.empty((0, 2), dtype=np.int64)
    if (
        array.ndim == 2
        and array.shape[1] == 2
        and array.dtype.kind in "iu"
        and np.all(array >= 0)
        and np.all(array < 2**63)
    ):
        return np.unique(array.astype(np.int64), axis=0)
    raise ArgumentError(
        "donor_hydrogen_pairs", value=donor_hydrogen_pairs, caller=caller
    )
