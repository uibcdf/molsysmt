"""Validating real unit-bearing observables at native structure boundaries."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError


def digest_structure_series(value, argument, dimensionality, caller=None):
    """Normalize a scalar to one structure, or retain a one-dimensional series."""
    try:
        quantity = puw.ensure_quantity(
            value, dimensionality=dimensionality, standardized=False, caller=caller
        )
        values = puw.get_value(quantity, value_type=np.ndarray)
    except Exception as error:
        # Translate provider parser/unit errors without losing their cause.
        raise ArgumentError(
            argument, value=value, caller=caller, cause=error
        ) from error

    if values.ndim > 1 or values.dtype.kind not in "iuf":
        raise ArgumentError(
            argument,
            value=value,
            caller=caller,
            message="A structure observable must be a real scalar or a one-dimensional quantity.",
        )
    if values.ndim == 0:
        values = values.reshape(1)
    return puw.standardize(puw.change_value(quantity, values))
