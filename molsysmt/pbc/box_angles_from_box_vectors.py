from molsysmt.lib import box as libbox
import numpy as np
from molsysmt import puw

def box_angles_from_box_vectors(box):

    n_frames = box.shape[0]
    tmp_box =  np.asfortranarray(puw.get_value(box), dtype='float64')
    angles = libbox.angles_box(tmp_box, n_frames)
    angles = np.ascontiguousarray(angles, dtype='float64')
    del(tmp_box)

    return puw.quantity(angles.round(6), 'degrees')

