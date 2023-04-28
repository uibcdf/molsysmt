import numpy as np
import numba as nb
from .math import dot_product
from .make_numba_signature import make_numba_signature

arguments=[
    nb.float64[:,:], # coordinates [n_atoms,3]
    nb.float64[:,:], # center_rotation  [n_atoms,3]
    nb.float64[:,:,:] # rotation_matrix [n_atoms, 3, 3]
    [nb.int64[:], None], # atom_indices [n_atoms] or None
]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments,output))
def rotate_single_structure(coordinates, center_rotation, rotation_matrix, atom_indices=None):

    n_atoms = coors.shape[0]

    rotation_matrix_t = np.ascontiguousarray(np.transpose(rotation_matrix))
    coordinates=np.ascontiguousarray(coordinates)

    if atom_indices is None:

        new_coordinates=np.empty((n_atoms,3), dtype=nb.float64)

        if center_rotation.shape[0]==1:
            if rotation_matrix.shape[0]==1:
                for ii in range(n_atoms):
                    new_coordinates[ii,:]=rotation_matrix_t[0,:,:]@(coordinates[ii,:]-center_rotation[0,:])
            else:
                for ii in range(n_atoms):
                    new_coordinates[ii,:]=rotation_matrix_t[ii,:,:]@(coordinates[ii,:]-center_rotation[0,:])
        else:
            if rotation_matrix.shape[0]==1:
                for ii in range(n_atoms):
                    new_coordinates[ii,:]=rotation_matrix_t[0,:,:]@(coordinates[ii,:]-center_rotation[ii,:])
            else:
                for ii in range(n_atoms):
                    new_coordinates[ii,:]=rotation_matrix_t[ii,:,:]@(coordinates[ii,:]-center_rotation[ii,:])

    else:

        new_coordinates=coordinates.copy()

        if center_rotation.shape[0]==1:
            if rotation_matrix.shape[0]==1:
                for ii in atom_indices:
                    new_coordinates[ii,:]=rotation_matrix_t[0,:,:]@(coordinates[ii,:]-center_rotation[0,:])
            else:
                for aa,ii in enumerate(atom_indices):
                    new_coordinates[ii,:]=rotation_matrix_t[aa,:,:]@(coordinates[ii,:]-center_rotation[0,:])
        else:
            if rotation_matrix.shape[0]==1:
                for aa,ii in enumerate(atom_indices):
                    new_coordinates[ii,:]=rotation_matrix_t[0,:,:]@(coordinates[ii,:]-center_rotation[aa,:])
            else:
                for aa,ii in enumerate(atom_indices):
                    new_coordinates[ii,:]=rotation_matrix_t[aa,:,:]@(coordinates[ii,:]-center_rotation[aa,:])

    return new_coordinates



arguments=[
    nb.float64[:,:,:], # coordinates [n_structures,n_atoms,3]
    nb.float64[:,:,:], # center_rotation  [n_structures,n_atoms,3]
    nb.float64[:,:,:,:] # rotation_matrix [n_structures,n_atoms, 3, 3]
    [nb.int64[:], None], # atom_indices [n_atoms] or None
    [nb.int64[:], None], # atom_indices [n_structures] or None
]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments,output))
def rotate_single_structure(coordinates, center_rotation, rotation_matrix, atom_indices=None, structure_indices=None):

    n_structures, n_atoms = coordinates.shape[:-1]

    n_s_cr, n_a_cr = center_rotation[:-1]
    n_s_rm, n_a_rm = rotation_matrix[:-2]
    w_s_cr=False if n_s_cr==1 else True
    w_a_cr=False if n_a_cr==1 else True
    w_s_rm=False if n_s_rm==1 else True
    w_a_rm=False if n_a_rm==1 else True
    cc=0
    dd=0
    ee=0
    ff=0

    if atom_indices is None:
        if structure_indices is None:
            for ii in range(n_structures):
                for jj in range(n_atoms):
                    if w_s_rm:
                        cc=ii
                    if w_a_rm:
                        dd=jj
                    if w_s_cr:
                        ee=ii
                    if w_a_cr:
                        ff=jj
                    coordinates[ii,jj,:]=rotation_matrix_t[cc,dd,:,:]@(coordinates[ii,jj,:]-center_rotation[ee,ff,:])
        else:
            for aa,ii in enumerate(structure_indices):
                for jj in range(n_atoms):
                    if w_s_rm:
                        cc=aa
                    if w_a_rm:
                        dd=jj
                    if w_s_cr:
                        ee=aa
                    if w_a_cr:
                        ff=jj
                    coordinates[ii,jj,:]=rotation_matrix_t[cc,dd,:,:]@(coordinates[ii,jj,:]-center_rotation[ee,ff,:])


