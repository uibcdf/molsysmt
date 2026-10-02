"""Validate a bounded RDKit match count."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_max_matches(max_matches, caller=None):
    if (
        not isinstance(max_matches, (bool, np.bool_))
        and isinstance(max_matches, (int, np.integer))
        and 0 < max_matches < 2**31 - 1
    ):
        return int(max_matches)
    raise ArgumentError("max_matches", value=max_matches, caller=caller)
