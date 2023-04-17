import numba as nb
import numpy as np
import math
from ..linalg import norm_vector
from ..make_numba_signature import make_numba_signature

arguments=[
        nb.float64[:,:,:], # box
        ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output))
def get_lengths_from_box(box):

    n_structures = box.shape[0]

    lengths = np.zeros((n_frames,3), dtype=nb.float64)

    for ii in range(n_structures):
        lengths[:,0] = norm_vector(box[ii,0,:])
        lengths[:,1] = norm_vector(box[ii,1,:])
        lengths[:,2] = norm_vector(box[ii,2,:])

    return lengths

