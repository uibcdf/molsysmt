import numpy as np
import numba as nb

@nb.njit(nb.float64[:,:,:](nb.float64[:,:,:],nb.int64[:],nb.int64[:],nb.int64[:]))
def geometrical_center(coors, group_indices, groups_atoms_indices, groups_starts):


    n_structures=coors.shape[0]
    n_groups=group_indices.shape[0]

    center=np.zeros((n_structures, n_groups, 3), dtype=nb.float64)

    for ii in range(n_groups):
        n_atoms_in_group = groups_starts[ii+1]-groups_starts[ii]
        for jj in range(groups_starts[ii], groups_starts[ii+1]):
            atom_index = groups_atoms_indices[jj]
            for ll in range(n_structures):
                center[ll,ii,:]=center[ll,ii,:]+coors[ll,atom_index,:]/n_atoms_in_group

    return center

@nb.njit(nb.float64[:,:,:](nb.float64[:,:,:],nb.int64[:],nb.int64[:],nb.int64[:],nb.float64[:]))
def center_of_mass(coors, group_indices, groups_atoms_indices, groups_starts, weights):

    n_structures=coors.shape[0]
    n_groups=group_indices.shape[0]

    center=np.zeros((n_structures, n_groups, 3), dtype=nb.float64)

    for ii in range(n_groups):
        total_weight=0.0
        for jj in range(groups_starts[ii], groups_starts[ii+1]):
            total_weight = total_weight+weights[jj]
        for jj in range(groups_starts[ii], groups_starts[ii+1]):
            atom_index = groups_atoms_indices[jj]
            for ll in range(n_structures):
                center[ll,ii,:]=center[ll,ii,:]+weights[jj]*coors[ll,atom_index,:]/total_weight

    return center
