"""Validating explicit residue-state names without choosing aliases or protonation."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_residue_names(residue_names, caller=None):
    if isinstance(residue_names, np.ndarray) and residue_names.ndim != 1:
        raise ArgumentError("residue_names", value=residue_names, caller=caller)
    if isinstance(residue_names, (list, tuple, np.ndarray)):
        values = list(residue_names)
        if values and all(isinstance(value, str) and value for value in values):
            return values
    raise ArgumentError("residue_names", value=residue_names, caller=caller)
