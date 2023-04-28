import numpy as np
import numba as nb
from .math import dot_product
from .make_numba_signature import make_numba_signature

arguments=[
    nb.float64[:,:], # coordinates [n_atoms,3]
    nb.float64[:,:] # translation [n_atoms, 3]
    [nb.int64[:], None], # atom_indices [n_atoms] or None
]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments,output))
def translate_single_structure(coordinates, translation, atom_indices=None):

    n_atoms = coordinates.shape[0]

    if atom_indices is None:

        new_coordinates=np.empty(coordinates.shape, dtype=nb.float64)

        if translation.shape[0]==1:
            for ii in range(n_atoms):
                new_coordinates[ii,:]=coordinates[ii,:]+translation[0,:]
        else:
            for ii in range(n_atoms):
                new_coordinates[ii,:]=coordinates[ii,:]+translation[ii,:]

    else:

        new_coordinates=coordinates.copy()

        if translation.shape[0]==1:
            for ii in atom_indices:
                new_coordinates[ii,:]+=translation[0,:]
        else:
            for aa,ii in enumerate(atom_indices):
                new_coordinates[ii,:]+=translation[aa,:]

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

    n_structures, n_atoms = coordinates.shape[:-1]

    if atom_indices is None:
        if structure_indices is None:
            if translation.shape[0]==1:
                if translation.shape[1]==1:
                    for ii in range(n_structures):
                        for jj in range(n_atoms):
                            coordinates[ii,jj,:]+=translation[0,0,:]
                else:
                    for ii in range(n_structures):
                        for jj in range(n_atoms):
                            coordinates[ii,jj,:]+=translation[0,jj,:]
            else:
                if translation.shape[1]==1:
                    for ii in range(n_structures):
                        for jj in range(n_atoms):
                            coordinates[ii,jj,:]+=translation[ii,0,:]
                else:
                    for ii in range(n_structures):
                        for jj in range(n_atoms):
                            coordinates[ii,jj,:]+=translation[ii,jj,:]
        else:
            if translation.shape[0]==1:
                if translation.shape[1]==1:
                    for ii in structure_indices:
                        for jj in range(n_atoms):
                            coordinates[ii,jj,:]+=translation[0,0,:]
                else:
                    for ii in structure_indices:
                        for jj in range(n_atoms):
                            coordinates[ii,jj,:]+=translation[0,jj,:]
            else:
                if translation.shape[1]==1:
                    for aa,ii in enumerate(structure_indices):
                        for jj in range(n_atoms):
                            coordinates[ii,jj,:]+=translation[aa,0,:]
                else:
                    for aa,ii in enumerate(structure_indices):
                        for jj in range(n_atoms):
                            coordinates[ii,jj,:]+=translation[aa,jj,:]
    else: 
        if structure_indices is None:
            if translation.shape[0]==1:
                if translation.shape[1]==1:
                    for ii in range(n_structures):
                        for jj in atom_indices:
                            coordinates[ii,jj,:]+=translation[0,0,:]
                else:
                    for ii in range(n_structures):
                        for bb,jj in enumerate(atom_indices):
                            coordinates[ii,jj,:]+=translation[0,bb,:]
            else:
                if translation.shape[1]==1:
                    for ii in range(n_structures):
                        for jj in atom_indices:
                            coordinates[ii,jj,:]+=translation[ii,0,:]
                else:
                    for ii in range(n_structures):
                        for bb,jj in enumerate(atom_indices):
                            coordinates[ii,jj,:]+=translation[ii,bb,:]
        else:
            if translation.shape[0]==1:
                if translation.shape[1]==1:
                    for ii in structure_indices:
                        for jj in atom_indices:
                            coordinates[ii,jj,:]+=translation[0,0,:]
                else:
                    for ii in structure_indices:
                        for bb,jj in enumerate(atom_indices):
                            coordinates[ii,jj,:]+=translation[0,bb,:]
            else:
                if translation.shape[1]==1:
                    for aa,ii in enumerate(structure_indices):
                        for jj in atom_indices:
                            coordinates[ii,jj,:]+=translation[aa,0,:]
                else:
                    for aa,ii in enumerate(structure_indices):
                        for bb,jj in enumerate(atom_indices):
                            coordinates[ii,jj,:]+=translation[aa,bb,:]

    pass

