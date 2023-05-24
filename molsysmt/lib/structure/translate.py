import numpy as np
import numba as nb
from ..make_numba_signature import make_numba_signature

arguments=[
    nb.float64[:,:], # coordinates [n_atoms,3]
    nb.float64[:,:], # translation [n_atoms, 3]
    nb.int64[:], # atom_indices [n_atoms]
]
output=None
@nb.njit(make_numba_signature(arguments,output), cache=True)
def translate_single_structure(coordinates, translation, atom_indices):

    n_atoms = coordinates.shape[0]
    n_atoms_translation = translation.shape[0]
    single_atom_translation = (n_atoms_translation==1)

    a_t=0
    for ii in atom_indices:
        coordinates[ii,:]=coordinates[ii,:]+translation[a_t,:]
        if not single_atom_translation:
            a_t+=1

    pass

arguments=[
    nb.float64[:,:,:], # coordinates
    nb.float64[:,:,:], # translation
    nb.int64[:], # atom_indices
    nb.int64[:], # structure_indices
]
output=None
@nb.njit(make_numba_signature(arguments,output), cache=True)
def translate(coordinates, translation, atom_indices, structure_indices):

    n_structures, n_atoms = coordinates.shape[:2]
    n_structures_translation, n_atoms_translation = translation.shape[:2]
    single_structure_translation = (n_structures_translation==1)
    single_atom_translation = (n_atoms_translation==1)

    s_t=0
    for ii in structure_indices:
        a_t=0
        for jj in atom_indices:
            coordinates[ii,jj,:]+=translation[s_t,a_t,:]
            if not single_atom_translation:
                a_t+=1
        if not single_structure_translation:
            s_t+=1

    pass

