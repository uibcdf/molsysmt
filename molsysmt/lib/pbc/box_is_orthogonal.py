import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature
from ..math import dot_product

arguments=[
        nb.float64[:,:], # box: [3,3]
        ]
output=nb.boolean
@nb.njit(make_numba_signature(arguments, output), cache=True)
def box_is_orthogonal_single_structure(box):

    output = False

    if abs(dot_product(box[0,:], box[1,:]))<=0.0001:
        if abs(dot_product(box[0,:], box[2,:]))<=0.0001:
            if abs(dot_product(box[1,:], box[2,:]))<=0.0001:
                output = True

    return output


arguments=[
        nb.float64[:,:,:], # box: [n_structures,3,3]
        ]
output=nb.boolean[:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def box_is_orthogonal(box):

    n_structures = box.shape[0]

    output = np.zeros((n_structures), dtype=nb.boolean)

    for ii in range(n_structures):

        if abs(dot_product(box[ii,0,:], box[ii,1,:]))<=0.0001:
            if abs(dot_product(box[ii,0,:], box[ii,2,:]))<=0.0001:
                if abs(dot_product(box[ii,1,:], box[ii,2,:]))<=0.0001:
                    output[ii] = True

    return output

