from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt.lib import box as libbox
import numpy as np

@digest()
def get_lengths_and_angles_from_box(box):

    box_value, box_unit  = puw.get_value_and_unit(box)
    lengths_value, angles_value = msmlib.pbc.get_lengths_and_angles_from_box(box_value)

    n_structures = box.shape[0]
    unit = puw.get_unit(box)
    tmp_box =  np.asfortranarray(puw.get_value(box), dtype='float64')

    lengths = libbox.length_edges_box(tmp_box, n_structures)
    lengths = np.ascontiguousarray(lengths, dtype='float64')

    angles = libbox.angles_box(tmp_box, n_structures)
    angles = np.ascontiguousarray(angles, dtype='float64')

    del(tmp_box)

    return lengths.round(6)*unit, puw.quantity(angles.round(6), 'degrees')

    box_value, box_unit  = puw.get_value_and_unit(box)
    lengths = puw.quantity(lengths_value.round(6), box_unit)
    lengths = puw.standardize(lengths)

    return lengths

