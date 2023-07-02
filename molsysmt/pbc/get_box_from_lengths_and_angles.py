from molsysmt._private.digestion import digest
from molsysmt import lib as msmlib
import numpy as np
from molsysmt import pyunitwizard as puw

@digest()
def get_box_from_lengths_and_angles(box_lengths, box_angles):
    """
    To be written soon...
    """

    units = puw.get_unit(box_lengths)
    lengths_value = puw.get_value(box_lengths)
    angles_value = puw.get_value(box_angles, to_unit='radians')

    box = msmlib.pbc.get_box_from_lengths_and_angles(lengths_value, angles_value)
    box = box.round(6)*units

    del(lengths_value, angles_value)

    box = puw.standardize(box)

    return box

