"""Validating an explicit caller declaration of complete covalent connectivity."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_assume_complete_connectivity(assume_complete_connectivity, caller=None):
    if isinstance(assume_complete_connectivity, (bool, np.bool_)):
        return bool(assume_complete_connectivity)
    raise ArgumentError(
        argument="assume_complete_connectivity",
        value=assume_complete_connectivity,
        caller=caller,
    )
