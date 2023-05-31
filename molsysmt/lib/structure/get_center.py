import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature


arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    nb.float64[:], # weights: [n_atoms]
]
output=nb.float64[:] # center: [0,3]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_center_single_structure(coordinates, weights):

    n_atoms = coordinates.shape[0]

    center=np.zeros((3), dtype=nb.float64)
    aux_coors=np.zeros((3), dtype=nb.float64)

    aux_weight=0.0
    for ii in range(n_atoms):
        aux_coors[:]+=weights[ii]*coordinates[ii,:]
        aux_weight+=weights[ii]
    center[:]=aux_coors/aux_weight

    return center


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.float64[:], # weights: [n_atoms]
]
output=nb.float64[:,:,:]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_center(coordinates, weights):

    n_structures, n_atoms = coordinates.shape[0:2]
    center=np.zeros((n_structures, 1, 3), dtype=nb.float64)
    aux_coors=np.zeros((3), dtype=nb.float64)

    for ii in range(n_structures):
        aux_weight=0.0
        aux_coors[:]=0.0
        for jj in range(n_atoms):
            aux_coors[:]+=weights[jj]*coordinates[ii,jj,:]
            aux_weight+=weights[jj]
        center[ii,0,:]=aux_coors/aux_weight

    return center


arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    nb.int64[:], # atoms_per_group [n_groups]
    nb.float64[:], # weights: [n_atoms]
]
output=nb.float64[:,:] # center: [n_groups,3]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_center_groups_of_atoms_single_structure(coordinates, atoms_per_group, weights):

    n_groups = atoms_per_group.shape[0]

    center=np.zeros((n_groups, 3), dtype=nb.float64)
    aux_coors=np.zeros((3), dtype=nb.float64)

    ii=0 
    for kk in range(n_groups):
        aux_weight=0.0
        aux_coors[:]=0.0
        for ll in range(atoms_per_group[kk]):
            aux_coors[:]+=weights[ii]*coordinates[ii,:]
            aux_weight+=weights[ii]
            ii+=1
        center[kk,:]=aux_coors/aux_weight

    return center


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.int64[:], # atoms_per_group [n_groups]
    nb.float64[:], # weights [n_atoms]
]
output=nb.float64[:,:,:] # center: [n_structures, n_groups, 3]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_center_groups_of_atoms(coordinates, atoms_per_group, weights):

    n_structures, n_atoms = coordinates.shape[0:2]

    n_groups = atoms_per_group.shape[0]

    center=np.zeros((n_structures, n_groups, 3), dtype=nb.float64)
    aux_coors=np.zeros((3), dtype=nb.float64)

    for ii in range(n_structures):
        jj=0 
        for kk in range(n_groups):
            aux_weight=0.0
            aux_coors[:]=0.0
            for ll in range(atoms_per_group[kk]):
                aux_coors[:]+=weights[jj]*coordinates[ii,jj,:]
                aux_weight+=weights[jj]
                jj+=1
            center[ii,kk,:]=aux_coors/aux_weight

    return center

