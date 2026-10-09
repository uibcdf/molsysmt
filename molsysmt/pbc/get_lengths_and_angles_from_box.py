import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
from molsysmt._private.argdigest import arg_digest


@arg_digest()
def get_lengths_and_angles_from_box(box, skip_digestion=False):
    """
    Extracting edge lengths and crystallographic angles from box matrices.


    Parameters
    ----------
    box : quantity or numpy.ndarray
        Periodic box vectors with shape ``(n_structures, 3, 3)``, with vectors
        stored as rows. A quantity must have units of length; bare arrays are
        interpreted in nanometers. A single ``(3, 3)`` matrix is also accepted.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    lengths : quantity
        Edge lengths with shape ``(n_structures, 3)`` in the active PyUnitWizard
        standard-length unit. Columns are the norms of rows ``v0``, ``v1`` and
        ``v2``, conventionally named ``a``, ``b`` and ``c``.
    angles : quantity
        Angles with shape ``(n_structures, 3)`` in the active PyUnitWizard
        standard-angle unit. Columns are ``alpha`` between ``v1`` and ``v2``,
        ``beta`` between ``v0`` and ``v2``, and ``gamma`` between ``v0`` and ``v1``.

    Notes
    -----
    Both outputs follow the application/user policy, including ``puw.context``;
    lengths need not retain the input unit, and angles need not be in radians.
    Extract numerical values with an explicit target unit using
    ``puw.get_value(lengths, to_unit="nm")`` or
    ``puw.get_value(angles, to_unit="radians")``. Normal argument validation
    converts box values to nanometers. The computation rounds lengths in
    nanometers and angles in radians to six decimal places before standardizing
    the quantities.

    Examples
    --------
    >>> from molsysmt import pyunitwizard as puw
    >>> box = puw.quantity(np.eye(3)[None, :, :], 'angstrom')
    >>> with puw.context(standard_units=['pm', 'fs', 'degrees']):
    ...     lengths, angles = get_lengths_and_angles_from_box(box)
    ...     np.allclose(puw.get_value(lengths), [[100., 100., 100.]])
    True
    >>> puw.get_unit(angles) == puw.unit('degrees')
    True
    >>> np.allclose(puw.get_value(angles, to_unit='radians'), np.pi / 2)
    True

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_lengths_and_angles_from_box` for box geometry.

    .. versionadded:: 1.0.0
    """

    if isinstance(box, np.ndarray):
        box_value = box
        box_unit = puw.unit("nm")
    else:
        box_value, box_unit = puw.get_value_and_unit(box)
    lengths_value, angles_value = _kernels.get_lengths_and_angles_from_box(
        box_value.astype(np.float64)
    )
    lengths = puw.quantity(lengths_value.round(6), box_unit)
    lengths = puw.standardize(lengths)
    angles = puw.quantity(angles_value.round(6), "radians")
    angles = puw.standardize(angles)

    return lengths, angles
