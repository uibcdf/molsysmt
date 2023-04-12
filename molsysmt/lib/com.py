import numpy as np
import numba as nb

@nb.jit(nb.float64[:,:,:](nb.float64[:,:,:],nb.int64[:],nb.int64[:],nb.int64[:]), nopython=True)
def geometrical_center(coors, group_indices, groups_atoms_indices, groups_starts):


    n_groups_atoms=groups_atoms_indices.shape[0]

    weights=np.ones((n_groups_atoms), dtype=nb.float64)

    center=center_of_mass(coors, group_indices, groups_atoms_indices, groups_starts, weights)

    return center

@nb.jit(nb.float64[:,:,:](nb.float64[:,:,:],nb.int64[:],nb.int64[:],nb.int64[:],nb.float64[:]), nopython=True)
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
