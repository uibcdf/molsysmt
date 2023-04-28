import numpy as np
import numba as nb
from .math import dot_product
from .make_numba_signature import make_numba_signature

arguments=[
    nb.float64[:,:], # coordinates
    [nb.int64[:], None], # atom_indices
    nb.float64[:], # center_rotation 
    nb.float64[:,:], # rotation_matrix
    nb.float64[:,:], # translation
]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments,output))
def rotate_and_translate_single_structure(coordinates, atom_indices, center_rotation, rotation_matrix, translation):

    new_coordinates=np.empty(coors.shape, dtype=nb.float64)

    n_atoms = coors.shape[0]

    rotation_matrix_t = np.ascontiguousarray(np.transpose(rotation_matrix))
    coordinates=np.ascontiguousarray(coordinates)

    if atom_indices is None:

        if translation.shape[0]==1:
            for ii in range(n_atoms):
                new_coordinates[ii,:]=rotation_matrix_t@(coordinates[ii,:]-center_rotation)+translation[0,:]
        else:
            for ii in range(n_atoms):
                new_coordinates[ii,:]=rotation_matrix_t@(coordinates[ii,:]-center_rotation)+translation[ii,:]

    else:

        if translation.shape[0]==1:
            for ii,jj in enumerate(atom_indices):
                new_coordinates[ii,:]=rotation_matrix_t@(coordinates[jj,:]-center_rotation)+translation[0,:]
        else:
            for ii,jj in enumerate(atom_indices):
                new_coordinates[ii,:]=rotation_matrix_t@(coordinates[jj,:]-center_rotation)+translation[ii,:]

    return new_coordinates

arguments=[
    nb.float64[:,:], # coordinates
    [nb.int64[:], None], # atom_indices
    nb.float64[:], # center_rotation 
    nb.float64[:,:] # rotation_matrix
]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments,output))
def rotate_single_structure(coordinates, atom_indices, center_rotation, rotation_matrix, translation):

    new_coordinates=np.empty(coors.shape, dtype=nb.float64)

    n_atoms = coors.shape[0]

    rotation_matrix_t = np.ascontiguousarray(np.transpose(rotation_matrix))
    coordinates=np.ascontiguousarray(coordinates)

    if atom_indices is None:

        if translation.shape[0]==1:
            for ii in range(n_atoms):
                new_coordinates[ii,:]=rotation_matrix_t@(coordinates[ii,:]-center_rotation)+translation[0,:]
        else:
            for ii in range(n_atoms):
                new_coordinates[ii,:]=rotation_matrix_t@(coordinates[ii,:]-center_rotation)+translation[ii,:]

    else:

        if translation.shape[0]==1:
            for ii,jj in enumerate(atom_indices):
                new_coordinates[ii,:]=rotation_matrix_t@(coordinates[jj,:]-center_rotation)+translation[0,:]
        else:
            for ii,jj in enumerate(atom_indices):
                new_coordinates[ii,:]=rotation_matrix_t@(coordinates[jj,:]-center_rotation)+translation[ii,:]

    return new_coordinates



