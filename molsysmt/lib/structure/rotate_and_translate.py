import numpy as np
import numba as nb
from .math import dot_product
from .make_numba_signature import make_numba_signature

arguments=[
    nb.float64[:,:], # coordinates [n_atoms,3]
    nb.float64[:,:], # center_rotation  [n_atoms,3]
    nb.float64[:,:,:], # rotation_matrix [n_atoms, 3, 3]
    nb.float64[:,:], # translation [n_atoms, 3]
    [nb.int64[:], None], # atom_indices [n_atoms] or None
]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments,output))
def rotate_and_translate_single_structure(coordinates, center_rotation, rotation_matrix, translation, atom_indices=None):

    new_coordinates=coordinates.copy()

    if atom_indices is None:
        iter_atoms = range(coordinates.shape[0])
    else:
        iter_atoms = atom_indices

    if center_rotation.shape[0]==1:
        iter_atoms_cr=repeat(0)
    else:
        iter_atoms_cr=infinite_sequence(0,1)

    if rotation_matrix.shape[0]==1:
        iter_atoms_rm=repeat(0)
    else:
        iter_atoms_rm=infinite_sequence(0,1)

    if translation.shape[0]==1:
        iter_atoms_t=repeat(0)
    else:
        iter_atoms_t=infinite_sequence(0,1)

    for ii, a_cr, a_rm, a_t in zip(iter_atoms, iter_atoms_cr, iter_atoms_rm, iter_atoms_t):
        aux_vect=coordinates[ii,:]-center_rotation[a_cr,:]
        aux_vect=transpmatmul(rotation_matrix[a_rm,:,:],aux_vect)
        new_coordinates[ii,:]=aux_vect+translation[a_t,:]

    return new_coordinates


arguments=[
    nb.float64[:,:,:], # coordinates [n_structures, n_atoms,3]
    nb.float64[:,:,:], # center_rotation  [n_structures, n_atoms,3]
    nb.float64[:,:,:,:], # rotation_matrix [n_structures, n_atoms, 3, 3]
    nb.float64[:,:,:], # translation [n_structures, n_atoms, 3]
    [nb.int64[:], None], # atom_indices [n_atoms] or None
    [nb.int64[:], None], # atom_indices [n_structures] or None
]
output=None
@nb.njit(make_numba_signature(arguments,output))
def rotate_and_translate(coordinates, center_rotation, rotation_matrix, translation, atom_indices=None, structure_indices=None):

    new_coordinates=coordinates.copy()

    if structure_indices is None:
        iter_structures = range(coordinates.shape[0])
    else:
        iter_structures = structure_indices

    if atom_indices is None:
        iter_atoms = range(coordinates.shape[1])
    else:
        iter_atoms = atom_indices

    if center_rotation.shape[0]==1:
        iter_structures_cr=repeat(0)
    else:
        iter_structures_cr=infinite_sequence(0,1)

    if rotation_matrix.shape[0]==1:
        iter_structures_rm=repeat(0)
    else:
        iter_structures_rm=infinite_sequence(0,1)

    if translation.shape[0]==1:
        iter_structures_t=repeat(0)
    else:
        iter_structures_t=infinite_sequence(0,1)


    for ii, s_cr, s_rm, s_t in zip(iter_structures, iter_structures_cr, iter_structures_rm, iter_structures_t):

        if center_rotation.shape[1]==1:
            iter_atoms_cr=repeat(0)
        else:
            iter_atoms_cr=infinite_sequence(0,1)

        if rotation_matrix.shape[1]==1:
            iter_atoms_rm=repeat(0)
        else:
            iter_atoms_rm=infinite_sequence(0,1)

        if translation.shape[1]==1:
            iter_atoms_t=repeat(0)
        else:
            iter_atoms_t=infinite_sequence(0,1)

        for jj, a_cr, a_rm, a_t in zip(iter_atoms, iter_atoms_cr, iter_atoms_rm, iter_atoms_t):
            aux_vect=coordinates[ii,jj,:]-center_rotation[s_cr,a_cr,:]
            aux_vect=transpmatmul(rotation_matrix[s_rm,a_rm,:,:],aux_vect)
            new_coordinates[ii,jj,:]=aux_vect+translation[a_s,a_t,:]

    pass
