from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_volume_from_box(box):
    """
    To be written soon...
    """

    if box is not None:
        units = puw.get_unit(box)
        value = puw.get_value(box)
        volume = np.linalg.det(value)*units**3
    else:
        volume = None

    return volume

