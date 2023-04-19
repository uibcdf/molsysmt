import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature
from ..math import dot_product

arguments=[
        nb.float64[:,:,:], # box
        ]
output=nb.boolean
@nb.njit(make_numba_signature(arguments, output))
def box_is_orthogonal(box):

    p01=dot_product(box[0,0,:], box[0,1,:])
    p02=dot_product(box[0,0,:], box[0,2,:])
    p12=dot_product(box[0,1,:], box[0,2,:])

    orthogonal = np.allclose([p01,p02,12],[0.0,0.0,0.0])

    return orthogonal


