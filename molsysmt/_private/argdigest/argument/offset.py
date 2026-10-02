"""Validate a zero-based projection offset."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_offset(offset, caller=None):
    if (
        isinstance(offset, (int, np.integer))
        and not isinstance(offset, (bool, np.bool_))
        and offset >= 0
    ):
        return int(offset)
    raise ArgumentError("offset", value=offset, caller=caller)
