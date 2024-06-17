from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_shape_from_box(box, skip_digestion=False):
    """
    To be written soon...
    """

    from molsysmt.pbc.get_angles_from_box import get_angles_from_box
    from molsysmt.pbc.get_shape_from_angles import get_shape_from_angles

    if box is None:
        return None
    else:

        angles = get_angles_from_box(box, skip_digestion=True)
        return get_shape_from_angles(angles, skip_digestion=True)

