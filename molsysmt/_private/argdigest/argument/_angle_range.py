"""Normalize a unit-bearing angular interval at a public boundary."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError

from ._quantity_parsing import parse_quantity_string


def digest_angle_range(value, argument, caller):
    if value is None:
        return None
    if isinstance(value, str):
        value = parse_quantity_string(argument, value, caller=caller)
    if puw.is_quantity(value) and puw.are_compatible(value, "0 radians"):
        values = np.asarray(puw.get_value(value, to_unit="radians"))
        if (
            values.shape == (2,)
            and np.isfinite(values).all()
            and 0 <= values[0] <= values[1] <= np.pi
        ):
            return puw.standardize(value)
    raise ArgumentError(
        argument,
        value=value,
        caller=caller,
        message="Supply a finite ordered two-value angular quantity within zero to pi radians.",
    )
