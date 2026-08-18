from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest()
def get_shape_from_box(box, skip_digestion=False):
    """
    Inferring the box shape from its matrix.


    Parameters
    ----------
    box : object
        Argument box.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    str or None
        Shape label inferred from the box angles, or `None` if no box.


    .. versionadded:: 1.0.0
    """

    from molsysmt.pbc.get_angles_from_box import get_angles_from_box
    from molsysmt.pbc.get_shape_from_angles import get_shape_from_angles

    if box is None:
        return None
    else:

        angles = get_angles_from_box(box, skip_digestion=True)
        return get_shape_from_angles(angles, skip_digestion=True)
