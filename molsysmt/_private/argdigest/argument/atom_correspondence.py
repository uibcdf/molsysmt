"""Validating an explicit bijection between two atom-index domains."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_atom_correspondence(atom_correspondence, caller=None):
    try:
        pairs = np.asarray(atom_correspondence)
    except (TypeError, ValueError) as error:
        raise ArgumentError(
            "atom_correspondence", value=atom_correspondence, caller=caller
        ) from error
    if (
        pairs.ndim != 2
        or pairs.shape[1] != 2
        or pairs.dtype.kind not in "iu"
        or np.any(pairs < 0)
        or any(len(np.unique(pairs[:, column])) != len(pairs) for column in (0, 1))
    ):
        raise ArgumentError(
            "atom_correspondence", value=atom_correspondence, caller=caller
        )
    return pairs.copy()
