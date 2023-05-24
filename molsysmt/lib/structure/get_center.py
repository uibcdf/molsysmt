import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature


arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    nb.float64[:], # weights: [n_atoms]
    nb.int64[:], # atom indices: [n_atoms]
]
output=nb.float64[:] # center: [0,3]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_center_single_structure(coordinates, weights, atom_indices):

    center=np.zeros((3), dtype=nb.float64)
    aux=np.zeros((3), dtype=nb.float64)

    weight=0.0
    a_w=0
    for ii in atom_indices:
        aux[:]+=weights[a_w]*coordinates[ii,:]
        weight+=weights[a_w]
        a_w+=1
    center[:]=aux/weight

    return center


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.float64[:], # weights: [n_atoms]
    nb.int64[:], # atom indices: [n_atoms]
    nb.int64[:], # structure indices: [n_structures]
]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_center(coordinates, weights, atom_indices, structure_indices):

    n_structures = coordinates.shape[0]

    center=np.zeros((n_structures, 3), dtype=nb.float64)
    aux=np.zeros((3), dtype=nb.float64)

    ss=0
    for ii in structure_indices:
        weight=0.0
        aux[:]=0.0
        a_w=0
        for jj in atom_indices:
            aux[:]+=weights[a_w]*coordinates[ii,jj,:]
            weight+=weights[a_w]
            a_w+=1
        center[ss,:]=aux/weight
        ss+=1

    return center


arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    nb.types.ListType(nb.types.ListType(nb.float64)), # weights: lists of lists of atom indices
    nb.types.ListType(nb.types.ListType(nb.int64)), # groups_of_atoms: lists of lists of atom indices
]
output=nb.float64[:,:] # center: [n_groups,3]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_center_groups_of_atoms_single_structure(coordinates, weights, groups_of_atoms):

    n_atoms = [len(ii) for ii in groups_of_atoms]
    n_groups = len(groups_of_atoms)

    center=np.zeros((n_groups, 3), dtype=nb.float64)
    aux=np.zeros((3), dtype=nb.float64)

    for ii in range(n_groups):
        atom_indices=groups_of_atoms[ii]
        atoms_weights=weights[ii]
        weight=0.0
        for ll in range(n_atoms[ii]):
            jj=atom_indices[ll]
            ww=atoms_weights[ll]
            aux[:]=aux[:]+ww*coordinates[jj,:]
            weight+=ww
        center[ii,:]=aux/weight

    return center


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.types.ListType(nb.types.ListType(nb.float64)), # weights: lists of lists of atom indices, None
    nb.types.ListType(nb.types.ListType(nb.int64)), # groups_of_atoms: lists of lists of atom indices, None
    nb.int64[:], # structure_indices [n_structures]
]
output=nb.float64[:,:,:] # center: [n_structures, n_groups, 3]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_center_groups_of_atoms(coordinates, weights, groups_of_atoms, structure_indices):

    n_structures = structure_indices.shape[0]
    n_atoms = [len(ii) for ii in groups_of_atoms]
    n_groups = len(groups_of_atoms)

    center=np.zeros((n_structures, n_groups, 3), dtype=nb.float64)
    aux=np.zeros((3), dtype=nb.float64)

    ss=0
    for ii in structure_indices:
        for gg in range(n_groups):
            atom_indices=groups_of_atoms[gg]
            atoms_weights=weights[gg]
            weight=0.0
            for ll in range(n_atoms[gg]):
                jj=atom_indices[ll]
                ww=atoms_weights[ll]
                aux[:]=aux[:]+ww*coordinates[ii,jj,:]
                weight+=ww
            center[ss,gg,:]=aux/weight
        ss+=1

    return center

