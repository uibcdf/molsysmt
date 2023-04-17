import numba as nb
import numpy as np
import math
from .math import inverse_matrix_3x3, norm_vector, dot_product


@nb.njit(nb.float64[:,:](nb.float64[:,:,:]))
def angles_box(box):

    n_frames = box.shape[0]
    angles = np.zeros((n_frames,3), dtype=nb.float64)

    for ii in range(n_frames):

        v0 = box[ii,0,:]
        v1 = box[ii,1,:]
        v2 = box[ii,2,:]
        x = norm_vector(v0)
        y = norm_vector(v1)
        z = norm_vector(v2)
        a=math.acos(dot_product(v1,v2)/(y*z)) # alpha: v2 and v3
        b=math.acos(dot_product(v2,v0)/(x*z)) # beta: v1 and v3
        c=math.acos(dot_product(v1,v0)/(x*y)) # gamma: v1 and v2
        angles[ii,0] = math.degrees(a)
        angles[ii,1] = math.degrees(b)
        angles[ii,2] = math.degrees(c)

    return angles

