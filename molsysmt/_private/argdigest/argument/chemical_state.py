"""Validating the public chemical-state resolver argument."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_chemical_state(chemical_state, caller=None):
    """Return the reference sentinel or a non-negative chemical-state index."""

    if chemical_state is None:
        return 'reference'
    if isinstance(chemical_state, str) and chemical_state.lower() in {
        'reference', 'structure'
    }:
        return chemical_state.lower()
    if isinstance(chemical_state, (int, np.integer)) and not isinstance(
        chemical_state, (bool, np.bool_)
    ):
        chemical_state = int(chemical_state)
        if chemical_state >= 0:
            return chemical_state
    raise ArgumentError(
        argument='chemical_state', value=chemical_state, caller=caller, message=None
    )
