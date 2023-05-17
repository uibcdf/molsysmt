import numpy as np
import numba as nb
from ..make_numba_signature import make_numba_signature
from ..itertools import infinite_sequence

arguments=[
    nb.float64[:,:], # coordinates [n_atoms,3]
    nb.float64[:,:], # translation [n_atoms, 3]
    nb.int64[:], # atom_indices [n_atoms]
]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments,output))
def translate_single_structure(coordinates, translation, atom_indices=None):

    new_coordinates=coordinates.copy()

    if translation.shape[0]==1:
        iter_atoms_t=infinite_sequence(0,0)
    else:
        iter_atoms_t=infinite_sequence(0,1)

    if atom_indices is None:

        iter_atoms = range(coordinates.shape[0])
        for ii, a_t in zip(iter_atoms, iter_atoms_t):
            new_coordinates[ii,:]=coordinates[ii,:]+translation[a_t,:]

    else:

        iter_atoms = atom_indices
        for ii, a_t in zip(iter_atoms, iter_atoms_t):
            new_coordinates[ii,:]=coordinates[ii,:]+translation[a_t,:]

    return new_coordinates

arguments=[
    nb.float64[:,:,:], # coordinates
    nb.float64[:,:,:], # translation
    [nb.int64[:], None], # atom_indices
    [nb.int64[:], None], # structure_indices
]
output=None
@nb.njit(make_numba_signature(arguments,output))
def translate(coordinates, translation, atom_indices=None, structure_indices=None):

    new_coordinates=coordinates.copy()

    if structure_indices is None:
        iter_structures = range(coordinates.shape[0])
    else:
        iter_structures = structure_indices

    if atom_indices is None:
        iter_atoms = range(coordinates.shape[1])
    else:
        iter_atoms = atom_indices

    if translation.shape[0]==1:
        iter_structures_t=repeat(0)
    else:
        iter_structures_t=infinite_sequence(0,1)

    for ii, s_t in zip(iter_structures, iter_structures_t):

        if translation.shape[0]==1:
            iter_atoms_t=repeat(0)
        else:
            iter_atoms_t=infinite_sequence(0,1)

        for jj, a_t in zip(iter_atoms, iter_atoms_t):

            coordinates[ii,jj,:]+=translation[s_t,a_t,:]

    pass

