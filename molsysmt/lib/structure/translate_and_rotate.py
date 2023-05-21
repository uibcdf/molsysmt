import numpy as np
import numba as nb
from ..math import transpmatmul
from ..make_numba_signature import make_numba_signature

arguments=[
    nb.float64[:,:], # coordinates [n_atoms,3]
    nb.float64[:,:], # translation [n_atoms, 3]
    nb.float64[:,:], # center_rotation  [n_atoms,3]
    nb.float64[:,:,:], # rotation_matrix [n_atoms, 3, 3]
    nb.int64[:], # atom_indices [n_atoms]
]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def translate_and_rotate_single_structure(coordinates, translation, center_rotation, rotation_matrix, atom_indices):

    new_coordinates=coordinates.copy()

    n_atoms_translation = translation.shape[0]
    n_atoms_rotation = rotation_matrix.shape[0]
    n_atoms_center = center_rotation.shape[0]

    single_atom_translation = (n_atoms_translation==1)
    single_atom_rotation = (n_atoms_rotation==1)
    single_atom_center = (n_atoms_center==1)

    a_t=0
    a_r=0
    a_c=0

    for ii in atom_indices:
        aux_vect=coordinates[ii,:]+translation[a_t,:]
        aux_vect=aux_vect-center_rotation[a_c,:]
        new_coordinates[ii,:]=transpmatmul(rotation_matrix[a_r,:,:],aux_vect)
        if not single_atom_translation:
            a_t+=1
        if not single_atom_rotation:
            a_r+=1
        if not single_atom_center:
            a_c+=1

    return new_coordinates


arguments=[
    nb.float64[:,:,:], # coordinates [n_structures, n_atoms,3]
    nb.float64[:,:,:], # translation [n_structures, n_atoms, 3]
    nb.float64[:,:,:], # center_rotation  [n_structures, n_atoms,3]
    nb.float64[:,:,:,:], # rotation_matrix [n_structures, n_atoms, 3, 3]
    nb.int64[:], # atom_indices [n_atoms]
    nb.int64[:], # atom_indices [n_structures]
]
output=None
@nb.njit(make_numba_signature(arguments,output), cache=True)
def translate_and_rotate(coordinates, translation, center_rotation, rotation_matrix, atom_indices, structure_indices):

    n_structures, n_atoms = coordinates.shape[:2]
    n_structures_translation, n_atoms_translation = translation.shape[:2]
    n_structures_center, n_atoms_center = center_rotation.shape[:2]
    n_structures_rotation, n_atoms_rotation = rotation_matrix.shape[:2]

    single_structure_translation = (n_structures_translation==1)
    single_structure_center = (n_structures_center==1)
    single_structure_rotation = (n_structures_rotation==1)
    single_atom_translation = (n_atoms_translation==1)
    single_atom_center = (n_atoms_center==1)
    single_atom_rotation = (n_atoms_rotation==1)

    s_t=0
    s_c=0
    s_r=0

    for ii in structure_indices:

        a_t=0
        a_c=0
        a_r=0

        for jj in atom_indices:
            aux_vect=coordinates[ii,jj,:]+translation[s_t,a_t,:]
            aux_vect=aux_vect-center_rotation[s_c,a_c,:]
            coordinates[ii,jj,:]=transpmatmul(rotation_matrix[s_r,a_r,:,:],aux_vect)
            if not single_atom_translation:
                a_t+=1
            if not single_atom_center:
                a_c+=1
            if not single_atom_rotation:
                a_r+=1
        if not single_structure_translation:
            s_t+=1
        if not single_structure_center:
            s_c+=1
        if not single_structure_rotation:
            s_r+=1

    pass

