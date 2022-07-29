from molsysmt._private.digestion import digest
from molsysmt import puw
import numpy as np

@digest()
def box_volume_from_box_vectors(box):

    if box is not None:
        units = puw.get_unit(box)
        value = puw.get_value(box)
        volume = np.linalg.det(value)*units**3
    else:
        volume = None

    return volume

