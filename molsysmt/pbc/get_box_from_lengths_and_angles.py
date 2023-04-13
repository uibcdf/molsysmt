from molsysmt._private.digestion import digest
from molsysmt.lib import box as libbox
import numpy as np
from molsysmt import pyunitwizard as puw

@digest()
def get_box_from_lengths_and_angles(box_lengths, box_angles):

    units = puw.get_unit(box_lengths)
    lengths_value = puw.get_value(box_lengths)
    angles_value = puw.get_value(box_angles, to_unit='degrees')
    lengths_value =  np.asfortranarray(lengths_value, dtype='float64')
    angles_value =  np.asfortranarray(angles_value, dtype='float64')
    n_structures = box_lengths.shape[0]

    
    box = libbox.lengths_and_angles_to_box(lengths_value, angles_value)
    box = box.round(6)*units

    del(lengths_value, angles_value)

    return box

