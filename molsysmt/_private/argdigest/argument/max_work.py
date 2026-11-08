"""Validate a positive bounded-operation work estimate."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_max_work(max_work, caller=None):
    if (
        isinstance(max_work, (int, np.integer))
        and not isinstance(max_work, (bool, np.bool_))
        and max_work > 0
    ):
        return int(max_work)
    raise ArgumentError("max_work", caller=caller)
