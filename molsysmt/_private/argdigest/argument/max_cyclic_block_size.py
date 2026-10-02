"""Validating a bound on cycle-basis subproblems."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_max_cyclic_block_size(max_cyclic_block_size, caller=None):
    if (
        isinstance(max_cyclic_block_size, (int, np.integer))
        and not isinstance(max_cyclic_block_size, (bool, np.bool_))
        and max_cyclic_block_size >= 3
    ):
        return int(max_cyclic_block_size)
    raise ArgumentError(
        "max_cyclic_block_size", value=max_cyclic_block_size, caller=caller
    )
