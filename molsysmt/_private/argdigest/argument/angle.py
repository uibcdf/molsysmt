"""Convert one explicitly angular scalar to a trusted float64 kernel angle."""

import numpy as np
from argdigest.core.caller import caller_is_one_of

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError

_CONSTRUCTOR = (
    "molsysmt.structure.get_rotation_matrix_from_axis_angle."
    "get_rotation_matrix_from_axis_angle"
)


def digest_angle(angle, caller=None):
    """Return the axis-angle constructor's radians scalar without changing policy."""
    try:
        if not caller_is_one_of(caller, {_CONSTRUCTOR}):
            raise ValueError(
                "This angle contract is scoped to the axis-angle constructor."
            )
        quantity = puw.ensure_quantity(
            angle, dimensionality={}, standardized=False, caller=caller
        )
        if not (
            puw.has_unit(quantity, "degrees") is True
            or puw.has_unit(quantity, "radians") is True
        ):
            raise ValueError("Supply an explicit degree or radian unit.")
        magnitude = puw.get_value(quantity)
        if isinstance(
            magnitude, (bool, np.bool_, complex, np.complexfloating)
        ) or np.iscomplexobj(magnitude):
            raise ValueError("The angle magnitude must be real and non-boolean.")
        values = np.asarray(magnitude)
        if values.shape != () or values.dtype.kind not in "iuf":
            raise ValueError("The angle must be one real numeric scalar.")
        if not np.isfinite(values):
            raise ValueError("The angle must be finite.")
        canonical = puw.convert(quantity, to_unit="radians")
        with np.errstate(over="raise", invalid="raise"):
            radians = np.float64(puw.get_value(canonical))
        if not np.isfinite(radians):
            raise ValueError("The radians value must be finite in float64.")
        return float(radians)
    except Exception as error:
        raise ArgumentError(
            "angle",
            value=angle,
            caller=caller,
            message="Supply angle as one finite real scalar with explicit degree or radian units.",
            cause=error,
        ) from error
