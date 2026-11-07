"""Validate and normalize one Cartesian rotation axis at the public boundary."""

from collections.abc import Mapping, Set

import numpy as np
from argdigest.core.caller import caller_is_one_of

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.vector_normalization import unit_vectors

_CONSTRUCTOR = (
    "molsysmt.structure.get_rotation_matrix_from_axis_angle."
    "get_rotation_matrix_from_axis_angle"
)


def digest_axis(axis, caller=None):
    """Return the axis-angle constructor's one independent unit float64 vector."""
    try:
        if not caller_is_one_of(caller, {_CONSTRUCTOR}):
            raise ValueError(
                "This axis contract is scoped to the axis-angle constructor."
            )
        if puw.is_quantity(axis):
            raise ValueError("A rotation axis must be unit-free.")
        if isinstance(axis, (str, Mapping, Set)):
            raise ValueError("Axis components must be real numeric values.")
        if isinstance(axis, np.ndarray) and axis.dtype.kind not in "iuf":
            raise ValueError("Axis arrays must have a real numeric dtype.")
        components = list(axis)
        if any(
            isinstance(value, (bool, np.bool_, complex, np.complexfloating))
            or puw.is_quantity(value)
            for value in components
        ):
            raise ValueError("Axis components must be unit-free real numbers.")
        values = np.asarray(components)
        if values.shape != (3,) or values.dtype.kind not in "iuf":
            raise ValueError("Supply one real numeric axis with shape (3,).")
        with np.errstate(over="raise", invalid="raise"):
            return unit_vectors(values)[0]
    except (TypeError, ValueError, OverflowError, FloatingPointError) as error:
        raise ArgumentError(
            "axis",
            value=axis,
            caller=caller,
            message="Supply one finite nonzero unit-free real axis with shape (3,).",
            cause=error,
        ) from error
