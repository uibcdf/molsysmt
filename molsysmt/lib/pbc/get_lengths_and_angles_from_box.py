import numba as nb
import numpy as np
import math
from ..math import norm_vector, dot_product
from ..make_numba_signature import make_numba_signature


arguments=[nb.float64[:,:], # box
          ]
output=[nb.float64[:], # lengths
        nb.float64[:]  # angles
       ]
@nb.njit(make_numba_signature(arguments, output))
def get_lengths_and_angles_from_box_single_structure(box):

    lengths = np.empty((3), dtype=nb.float64)
    angles = np.empty((3), dtype=nb.float64)

    v0 = box[0,:]
    v1 = box[1,:]
    v2 = box[2,:]

    lengths[0] = norm_vector(v0)
    lengths[1] = norm_vector(v1)
    lengths[2] = norm_vector(v2)

    x = norm_vector(v0)
    y = norm_vector(v1)
    z = norm_vector(v2)
    angles[0] = math.acos(dot_product(v1,v2)/(y*z)) # alpha: v2 and v3
    angles[1] = math.acos(dot_product(v2,v0)/(x*z)) # beta: v1 and v3
    angles[2] = math.acos(dot_product(v1,v0)/(x*y)) # gamma: v1 and v2

    return lengths, angles


arguments=[nb.float64[:,:,:], # box
          ]
output=[nb.float64[:,:], # lengths
        nb.float64[:,:]  # angles
       ]
@nb.njit(make_numba_signature(arguments, output))
def get_lengths_and_angles_from_box(box):

    n_structures = box.shape[0]

    lengths = np.zeros((n_structures,3), dtype=nb.float64)
    angles = np.zeros((n_structures,3), dtype=nb.float64)

    for ii in range(n_structures):

        v0 = box[ii,0,:]
        v1 = box[ii,1,:]
        v2 = box[ii,2,:]

        lengths[:,0] = norm_vector(v0)
        lengths[:,1] = norm_vector(v1)
        lengths[:,2] = norm_vector(v2)

        x = norm_vector(v0)
        y = norm_vector(v1)
        z = norm_vector(v2)
        angles[ii,0] = math.acos(dot_product(v1,v2)/(y*z)) # alpha: v2 and v3
        angles[ii,1] = math.acos(dot_product(v2,v0)/(x*z)) # beta: v1 and v3
        angles[ii,2] = math.acos(dot_product(v1,v0)/(x*y)) # gamma: v1 and v2

    return lengths, angles

