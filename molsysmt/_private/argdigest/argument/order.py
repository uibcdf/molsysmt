"""Validate the explicitly supported number of mediator waters."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_order(order, caller=None):
    if (
        not isinstance(order, (bool, np.bool_))
        and isinstance(order, (int, np.integer))
        and order in (1, 2)
    ):
        return int(order)
    raise ArgumentError("order", value=order, caller=caller)
