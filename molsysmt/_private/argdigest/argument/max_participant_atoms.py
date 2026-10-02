"""Validate an interaction projection's constituent-atom budget."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_max_participant_atoms(max_participant_atoms, caller=None):
    if (
        isinstance(max_participant_atoms, (int, np.integer))
        and not isinstance(max_participant_atoms, (bool, np.bool_))
        and max_participant_atoms >= 0
    ):
        return int(max_participant_atoms)
    raise ArgumentError(
        "max_participant_atoms", value=max_participant_atoms, caller=caller
    )
