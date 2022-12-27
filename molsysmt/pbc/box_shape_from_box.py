from molsysmt._private.digestion import digest
from molsysmt.lib import box as libbox
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def box_shape_from_box(box):

    from molsysmt.pbc.box_shape_from_box_angles import box_shape_from_box_angles

    if box is None:
        return None
    else:
        tmp_box = np.asfortranarray(puw.get_value(box), dtype='float64')
        n_structures = tmp_box.shape[0]
        angles = libbox.angles_box(tmp_box, n_structures) * puw.unit('degrees')
        return box_shape_from_box_angles(angles)

