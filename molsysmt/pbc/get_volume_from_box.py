from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest()
def get_volume_from_box(box):
    """
    Computing box volume from a box matrix.

    Parameters
    ----------
    box : quantity or None
        Box matrix (single or array), shape (3, 3) or (n, 3, 3).

    Returns
    -------
    quantity or None
        Volume in cubic length units, or `None` if no box.

    .. versionadded:: 1.0.0
    """

    if box is not None:
        units = puw.get_unit(box)
        value = puw.get_value(box)
        volume = np.linalg.det(value)*units**3
    else:
        volume = None

    return volume
