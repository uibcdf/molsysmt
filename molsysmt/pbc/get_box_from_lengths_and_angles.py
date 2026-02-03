from molsysmt._private.digestion import arg_digest
from molsysmt import lib as msmlib
import numpy as np
from molsysmt import pyunitwizard as puw

@arg_digest()
def get_box_from_lengths_and_angles(box_lengths, box_angles, skip_digestion=False):
    """
    Building a box matrix from lengths and angles.

    Parameters
    ----------
    box_lengths : quantity
        Box edge lengths (a, b, c) with units.
    box_angles : quantity
        Box angles (alpha, beta, gamma) with units.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    quantity
        Box matrix of shape (3, 3) with the same length units as the input.

    .. versionadded:: 1.0.0
    """

    units = puw.get_unit(box_lengths)
    lengths_value = puw.get_value(box_lengths)
    angles_value = puw.get_value(box_angles, to_unit='radians')

    box = msmlib.pbc.get_box_from_lengths_and_angles(lengths_value, angles_value)
    box = box.round(6)*units

    del(lengths_value, angles_value)

    box = puw.standardize(box)

    return box
