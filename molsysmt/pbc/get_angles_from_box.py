from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib

@arg_digest()
def get_angles_from_box(box, skip_digestion=False):
    """
    Extracting box angles from a box matrix.

    Parameters
    ----------
    box : quantity
        Box matrix (single or array), shape (3, 3) or (n, 3, 3).
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    quantity
        Angles (alpha, beta, gamma) in radians.

    .. versionadded:: 1.0.0
    """

    box_value, box_unit  = puw.get_value_and_unit(box)
    import numpy as np
    angles = msmlib.pbc.get_angles_from_box(np.asarray(box_value, dtype=np.float64))
    angles = puw.quantity(angles.round(6), 'radians')
    angles = puw.standardize(angles)

    return angles
