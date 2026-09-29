"""Validate indices for appended H5MSM structure-to-state links."""

import numpy as np
from argdigest.core.caller import caller_matches

from molsysmt._private.smonitor import ArgumentError


def digest_structure_state_indices(structure_state_indices, caller=None):
    if not caller_matches(caller, "append_structures") or structure_state_indices is None:
        return structure_state_indices
    values = np.asarray(structure_state_indices)
    if values.size == 0:
        values = np.asarray(structure_state_indices, dtype=np.int64)
    if values.ndim != 1 or values.dtype.kind not in "iu":
        raise ArgumentError(
            "structure_state_indices", value=structure_state_indices, caller=caller
        )
    return structure_state_indices
