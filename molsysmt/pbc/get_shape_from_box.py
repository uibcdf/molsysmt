from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_shape_from_box(box):
    """
    To be written soon...
    """

    from molsysmt.pbc.get_lengths_and_angles_from_box import get_lengths_and_angles_from_box
    from molsysmt.pbc.get_shape_from_lengths_and_angles import get_shape_from_lengths_and_angles

    if box is None:
        return None
    else:

        lengths, angles = get_lengths_and_angles_from_box(box)
        return get_shape_from_lengths_and_angles(lengths, angles)

