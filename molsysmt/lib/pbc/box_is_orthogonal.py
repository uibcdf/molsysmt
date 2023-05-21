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

    if abs(dot_product(box[0,:], box[1,:]))<=0.00001:
        if abs(dot_product(box[0,:], box[2,:]))<=0.00001:
            if abs(dot_product(box[1,:], box[2,:]))<=0.00001:
                output = True

    return output


arguments=[
        nb.float64[:,:,:], # box: [n_structures,3,3]
        ]
output=nb.boolean
@nb.njit(make_numba_signature(arguments, output), cache=True)
def box_is_orthogonal(box):

    output = False

    if abs(dot_product(box[0,0,:], box[0,1,:]))<=0.00001:
        if abs(dot_product(box[0,0,:], box[0,2,:]))<=0.00001:
            if abs(dot_product(box[0,1,:], box[0,2,:]))<=0.00001:
                output = True

    return output

