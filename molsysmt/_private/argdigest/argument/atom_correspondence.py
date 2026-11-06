"""Validating an explicit bijection between two atom-index domains."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError

from ._correspondence_axes import _has_units


def digest_atom_correspondence(atom_correspondence, caller=None):
    invalid = _has_units(atom_correspondence)
    if isinstance(atom_correspondence, (list, tuple)):
        for row in atom_correspondence:
            invalid |= _has_units(row)
            if isinstance(row, np.ndarray):
                invalid |= row.dtype.kind == "b"
            elif isinstance(row, (list, tuple)):
                invalid |= any(
                    isinstance(value, (bool, np.bool_)) or _has_units(value)
                    for value in row
                )
    if invalid:
        raise ArgumentError(
            "atom_correspondence", value=atom_correspondence, caller=caller
        )
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
        or np.any(pairs > np.iinfo(np.int64).max)
        or any(len(np.unique(pairs[:, column])) != len(pairs) for column in (0, 1))
    ):
        raise ArgumentError(
            "atom_correspondence", value=atom_correspondence, caller=caller
        )
    return pairs.astype(np.int64, copy=True)
