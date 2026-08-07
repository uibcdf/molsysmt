from molsysmt._private.argdigest import arg_digest
from molsysmt._private import rust_backend as _kernels
import numpy as np
from molsysmt import pyunitwizard as puw

@arg_digest()
def get_box_from_lengths_and_angles(box_lengths, box_angles=None, skip_digestion=False):
    """
    Building a box matrix from lengths and angles.

    Parameters
    ----------
    box_lengths : quantity
        Box edge lengths (a, b, c) with units.
    box_angles : quantity, optional
        Box angles (alpha, beta, gamma) with units. If None, 90 degrees are assumed.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    quantity
        Box matrix of shape (3, 3) with the same length units as the input.

    .. versionadded:: 1.0.0
    """

    if box_angles is None:
        box_angles = np.array([90.0, 90.0, 90.0]) * puw.unit('degree')

    if isinstance(box_lengths, np.ndarray):
        units = puw.unit('nm')
        lengths_value = box_lengths
    else:
        units = puw.get_unit(box_lengths)
        lengths_value = puw.get_value(box_lengths)
    angles_value = puw.get_value(box_angles, to_unit='radians')

    box = _kernels.get_box_from_lengths_and_angles(np.array(lengths_value, dtype=np.float64), np.array(angles_value, dtype=np.float64))
    box = box.round(6)*units

    del(lengths_value, angles_value)

    box = puw.standardize(box)

    return box
