import numpy as np
import numba as nb
from .make_numba_signature import make_numba_signature

arguments=[
        nb.float64[:,:,:], # coordinates
        nb.int64[:], # group_indices
        nb.int64[:], # groups_atoms_indices
        nb.int64[:] # groups_starts
        ]
output=nb.float64[:,:,:]
@nb.njit(make_numba_signature(artuments,output))
def geometrical_center(coordinates, group_indices, groups_atoms_indices, groups_starts):


    n_structures=coordinates.shape[0]
    n_groups=group_indices.shape[0]

    center=np.zeros((n_structures, n_groups, 3), dtype=nb.float64)

    for ii in range(n_groups):
        n_atoms_in_group = groups_starts[ii+1]-groups_starts[ii]
        for jj in range(groups_starts[ii], groups_starts[ii+1]):
            atom_index = groups_atoms_indices[jj]
            for ll in range(n_structures):
                center[ll,ii,:]=center[ll,ii,:]+coordinates[ll,atom_index,:]/n_atoms_in_group

    return center


arguments=[
        nb.float64[:,:,:], # coordinates
        nb.int64[:], # group_indices
        nb.int64[:], # groups_atoms_indices
        nb.int64[:], # groups_starts
        nb.float64[:] # weights
        ]
output=nb.float64[:,:,:]
@nb.njit(make_numba_signature(artuments,output))
def center_of_mass(coordinates, group_indices, groups_atoms_indices, groups_starts, weights):

    n_structures=coordinates.shape[0]
    n_groups=group_indices.shape[0]

    center=np.zeros((n_structures, n_groups, 3), dtype=nb.float64)

    for ii in range(n_groups):
        total_weight=0.0
        for jj in range(groups_starts[ii], groups_starts[ii+1]):
            total_weight = total_weight+weights[jj]
        for jj in range(groups_starts[ii], groups_starts[ii+1]):
            atom_index = groups_atoms_indices[jj]
            for ll in range(n_structures):
                center[ll,ii,:]=center[ll,ii,:]+weights[jj]*coordinates[ll,atom_index,:]/total_weight

    return center

del(artuments, output, np, nb)

