from molsysmt.lib import box as libbox
import numpy as np
from molsysmt import puw

def box_lengths_from_box_vectors(box):

    unit = puw.get_unit(box)
    n_frames = box.shape[0]
    tmp_box =  np.asfortranarray(puw.get_value(box), dtype='float64')
    lengths = libbox.length_edges_box(tmp_box, n_frames)
    lengths = np.ascontiguousarray(lengths, dtype='float64')
    del(tmp_box)

    return lengths.round(6)*unit

