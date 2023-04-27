import numpy as np
import numba as nb
from .math import dot_product
from .make_numba_signature import make_numba_signature

arguments=[
    nb.float64[:,:], # coordinates
    nb.int64[:], # coordinates
    nb.float64[:,:,:], # coordinates_ref
]
output=None
@nb.njit(make_numba_signature(arguments,output))

@nb.njit(nb.void(nb.float64[:,:], nb.int64[:], nb.float64[:], nb.float64[:,:], nb.float64[:]))
def rotate_and_translate_single_structure(coors, atom_indices, center_rotation, rotation_matrix, translation):

    n_atoms = coors.shape[0]

    rotation_matrix_t = np.ascontiguousarray(np.transpose(rotation_matrix))

    coors=np.ascontiguousarray(coors)

    if atom_indices is None:

        for ii in range(n_atoms):
            coors[ii,:]=rotation_matrix_t@(coors[ii,:]-center_rotation)+translation

    else:

        for ii in atom_indices:
            coors[ii,:]=rotation_matrix_t@(coors[ii,:]-center_rotation)+translation
    pass


