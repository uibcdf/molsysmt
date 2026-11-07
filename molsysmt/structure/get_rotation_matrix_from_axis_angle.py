"""Constructing a proper rotation without reading or editing a molecular system."""

import numpy as np
from smonitor import signal

from molsysmt._private import rust_backend as _kernels
from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "structure"])
@arg_digest()
def get_rotation_matrix_from_axis_angle(axis, angle, skip_digestion=False):
    """
    Constructing an active right-handed rotation from one axis and angle.

    The result can be passed directly to :func:`molsysmt.structure.rotate`.
    The axis magnitude does not affect the result; its sign determines the
    positive rotation direction. Inputs are never modified.

    Parameters
    ----------
    axis : array-like
        One finite nonzero unit-free real vector with shape (3,). Numeric
        components must be representable as finite float64 values. Boolean,
        complex, string and object-dtype components are not accepted.
        Normalization preserves the direction at very small or large scales.
    angle : quantity or str
        One finite real scalar carrying explicit degree or radian units,
        including their unit-owner aliases. Bare numbers and generic
        dimensionless quantities are not interpreted as angles. Negative
        angles reverse the rotation direction. Zero is accepted with a
        valid nonzero axis.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated internal
        calls. Such calls must supply a normalized float64 axis with shape
        (3,) and a finite float64-compatible scalar angle already in radians.

    Returns
    -------
    numpy.ndarray
        New dimensionless float64 proper rotation matrix with shape (3, 3).
        A column vector transforms as ``R @ vector``; row-vector coordinates
        transform as ``coordinates @ R.T``.

    Raises
    ------
    ArgumentError
        If the axis is zero, nonfinite, unit-bearing, non-real or has an
        unsupported type/shape, or if the angle lacks explicit angular units,
        is not a finite real scalar, or cannot be represented in float64.

    Notes
    -----
    Positive 90 degrees about +z maps +x to +y. Axis normalization divides by
    the largest absolute component before taking a norm; there is no small
    magnitude cutoff. Even a zero angle requires a defined axis.

    Explicit angles are converted to radians through PyUnitWizard without
    modifying the application's unit policy or requiring an angular standard.
    The bundled Rodrigues kernel rotates the three Cartesian basis vectors;
    those images are columns of the returned matrix. No molecular coordinates,
    centers or boxes are read or modified, and no periodic wrapping is applied.
    Computation uses float64 and its representable numerical precision.

    See Also
    --------
    molsysmt.structure.rotate : Applying a rotation to selected coordinates.
    molsysmt.structure.get_center : Computing a geometric or weighted center.

    Examples
    --------
    >>> import molsysmt as msm
    >>> import numpy as np
    >>> rotation = msm.structure.get_rotation_matrix_from_axis_angle(
    ...     [0, 0, 2], '90 degree')
    >>> np.allclose(np.array([1.0, 0.0, 0.0]) @ rotation.T, [0.0, 1.0, 0.0])
    True

    .. admonition:: Tutorial

       See :ref:`Tutorial_Rotate` for applying rotations around a chosen center.

    .. versionadded:: 1.0.0
    """

    basis = np.eye(3, dtype=np.float64)
    return np.column_stack(
        [_kernels.rodrigues_rotation(vector, axis, angle) for vector in basis]
    )
