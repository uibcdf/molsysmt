from molsysmt._private.digestion import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest()
def get_shape_from_box(box, skip_digestion=False):
    """
    Inferring the box shape from its matrix.

    Parameters
    ----------
    box : quantity
        Box matrix (single or array), shape (3, 3) or (n, 3, 3).
    skip_digestion : bool, default False
        Whether to skip argument digestion.

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
