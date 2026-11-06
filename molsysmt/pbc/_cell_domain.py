"""Validate physical length/angle declarations independently of display units."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def validate_lengths(values, *, argument="box_lengths", caller):
    """Require finite, strictly positive lengths without a dimensional cutoff."""
    if not np.isfinite(values).all() or np.any(values <= 0):
        raise ArgumentError(
            argument,
            caller=caller,
            message=f"{argument} must contain finite, strictly positive lengths.",
        )


def validate_angles(angles, *, caller):
    """Require a nondegenerate angle triple for three independent vectors.

    Angles are radians. Their strict triangle inequalities and sum below 2*pi
    give a positive Gram determinant. Numerical construction is checked again
    by the consumer, after its own precision/rounding operations.
    """
    if not np.isfinite(angles).all() or np.any(angles <= 0) or np.any(angles >= np.pi):
        raise ArgumentError(
            "box_angles",
            caller=caller,
            message="box_angles must be finite angles strictly between zero and pi radians.",
        )
    semiperimeter = np.sum(angles, axis=-1) / 2
    if np.any(semiperimeter >= np.pi) or np.any(semiperimeter[..., None] <= angles):
        raise ArgumentError(
            "box_angles",
            caller=caller,
            message="box_angles must satisfy strict triangle inequalities and sum to less than two pi radians.",
        )
