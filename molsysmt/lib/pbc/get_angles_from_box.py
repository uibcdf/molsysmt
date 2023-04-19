import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature
import math
from .math import norm_vector, dot_product

arguments=[
        nb.float64[:,:,:], # box
        ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output))
def get_angles_from_box(box):

    n_frames = box.shape[0]
    angles = np.zeros((n_frames,3), dtype=nb.float64)

    for ii in range(n_frames):

        v0 = box[ii,0,:]
        v1 = box[ii,1,:]
        v2 = box[ii,2,:]
        x = norm_vector(v0)
        y = norm_vector(v1)
        z = norm_vector(v2)
        angles[ii,0] = math.acos(dot_product(v1,v2)/(y*z)) # alpha: v2 and v3
        angles[ii,1] = math.acos(dot_product(v2,v0)/(x*z)) # beta: v1 and v3
        angles[ii,2] = math.acos(dot_product(v1,v0)/(x*y)) # gamma: v1 and v2

    return angles

