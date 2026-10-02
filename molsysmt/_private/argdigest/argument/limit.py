"""Validate a bounded projection row count."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_limit(limit, caller=None):
    if (
        isinstance(limit, (int, np.integer))
        and not isinstance(limit, (bool, np.bool_))
        and limit >= 0
    ):
        return int(limit)
    raise ArgumentError("limit", value=limit, caller=caller)
