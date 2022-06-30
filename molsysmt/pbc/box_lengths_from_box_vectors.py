from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt import puw
from molsysmt.lib import box as libbox
import numpy as np

def box_lengths_from_box_vectors(box, check=True):

    if check:

        box = digest_box(box)

    unit = puw.get_unit(box)
    n_structures = box.shape[0]
    tmp_box =  np.asfortranarray(puw.get_value(box), dtype='float64')
    lengths = libbox.length_edges_box(tmp_box, n_structures)
    lengths = np.ascontiguousarray(lengths, dtype='float64')
    del(tmp_box)

    return lengths.round(6)*unit

