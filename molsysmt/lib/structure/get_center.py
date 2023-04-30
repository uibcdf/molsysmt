import numba as nb
import numpy as np
from .make_numba_signature import make_numba_signature
from ..itertools import infinite_sequence, repeat


arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    [nb.float64[:], None], # weights: [n_atoms] or None
    [nb.int64[:], None], # atom indices: [n_atoms] or None
]
output=nb.float64[:,:] # center: [0,3]
@nb.njit(make_numba_signature(arguments,output))
def get_center_single_structure(coordinates, weights=None, atom_indices=None):

    if atom_indices is None:
        n_atoms = coordinates.shape[0]
        iter_atoms = range(n_atoms)
    else:
        n_atoms = len(atom_indices)
        iter_atoms = atom_indices

    center=np.zeros((1, 3), dtype=nb.float64)
    aux=np.zeros((3), dtype=nb.float64)

    if weights is None:
        for ii in iter_atoms:
            aux[:]=aux[:]+coordinates[ii,jj,:]
        center[0,:]=aux/n_atoms
    else:
        weight=0.0
        for a_w, ii in enumerate(iter_atoms):
            aux[:]+=weights[a_w]*coordinates[ii,:]
            weight+=weights[a_w]
        center[0,:]=aux/weight

    return center


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    [nb.float64[:], None], # weights: [n_atoms] or None
    [nb.int64[:], None], # atom indices: [n_atoms] or None
    [nb.int64[:], None], # structure indices: [n_structures] or None
]
output=nb.float64[:,:,:]
@nb.njit(make_numba_signature(arguments,output))
def get_center(coordinates, weights=None, atom_indices=None, structure_indices=None):

    if structure_indices is None:
        n_structures = coordinates.shape[0]
        iter_structures = range(coordinates.shape[1])
    else:
        n_structures = len(structure_indices)
        iter_structures = structure_indices

    if atom_indices is None:
        n_atoms = coordinates.shape[0]
        iter_atoms = range(n_atoms)
    else:
        n_atoms = len(atom_indices)
        iter_atoms = atom_indices

    center=np.zeros((n_structures, 1, 3), dtype=nb.float64)
    aux=np.zeros((3), dtype=nb.float64)

    if weights is None:
        for s_c, ii in enumerate(iter_structures):
            aux[:]=0.0
            for jj in iter_atoms:
                aux[:]=aux[:]+coordinates[ii,jj,:]
            center[s_c,0,:]=aux/n_atoms
    else:
        for s_c, ii in enumerate(iter_structures):
            weight=0.0
            aux[:]=0.0
            for a_w, jj in enumerate(iter_atoms):
                aux[:]+=weights[a_w]*coordinates[ii,jj,:]
                weight+=weights[a_w]
            center[s_c,0,:]=aux/weight

    return center


arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    [nb.types.ListType(nb.types.ListType(nb.float64)), None], # weights: lists of lists of atom indices, None
    [nb.types.ListType(nb.types.ListType(nb.int64)), None], # groups_of_atoms: lists of lists of atom indices, None
]
output=nb.float64[:,:] # center: [n_groups,3]
@nb.njit(make_numba_signature(arguments,output))
def get_center_groups_of_atoms_single_structure(coordinates, weights=None, groups_of_atoms=None):

    if groups_of_atoms is None:
        n_atoms = [coordinates.shape[0]]
        n_groups = 1
        groups_of_atoms = [range(n_atoms[0])]
    else:
        n_atoms = [len(group) for group in groups_of_atoms]
        n_groups = len(groups_of_atoms)

    center=np.zeros((n_groups, 3), dtype=nb.float64)
    aux=np.zeros((3), dtype=nb.float64)

    if weights is None:
        for ii, atom_indices, nn in enumerate(groups_of_atoms, n_atoms):
            for jj in atom_indices:
                aux[:]=aux[:]+coordinates[jj,:]
            center[ii,:]=aux/nn
    else:
        for ii, atom_indices, atoms_weights in enumerate(groups_of_atoms, atoms_weights):
            weight=0.0
            for jj, ww in zip(atom_indices, atoms_weights):
                aux[:]=aux[:]+ww*coordinates[jj,:]
                weight+=ww
            center[ii,:]=aux/weight

    return center


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.types.ListType(nb.types.ListType(nb.int64)), # weights: lists of lists of atom indices, None
    [nb.types.ListType(nb.types.ListType(nb.float64)), None], # groups_of_atoms: lists of lists of atom indices, None
]
output=nb.float64[:,:,:] # center: [n_structures, n_groups, 3]
@nb.njit(make_numba_signature(arguments,output))
def get_center_groups_of_atoms(coordinates, groups_of_atoms, weights=None):

    if structure_indices is None:
        n_structures = coordinates.shape[0]
        iter_structures = range(coordinates.shape[1])
    else:
        n_structures = len(structure_indices)
        iter_structures = structure_indices

    if groups_of_atoms is None:
        n_atoms = [coordinates.shape[0]]
        n_groups = 1
        groups_of_atoms = [range(n_atoms[0])]
    else:
        n_atoms = [len(group) for group in groups_of_atoms]
        n_groups = len(groups_of_atoms)

    center=np.zeros((n_structures, n_groups, 3), dtype=nb.float64)
    aux=np.zeros((3), dtype=nb.float64)

    if weights is None:
        for s_c, ii in enumerate(iter_structures):
            for gg, atom_indices, nn in enumerate(groups_of_atoms, n_atoms):
                for jj in atom_indices:
                    aux[:]=aux[:]+coordinates[ii,jj,:]
                center[s_c,gg,:]=aux/nn
    else:
        for s_c, ii in enumerate(iter_structures):
            for gg, atom_indices, atoms_weights in enumerate(groups_of_atoms, atoms_weights):
                weight=0.0
                for jj, ww in zip(atom_indices, atoms_weights):
                    aux[:]=aux[:]+ww*coordinates[ii,jj,:]
                    weight+=ww
                center[s_c,gg,:]=aux/weight

    return center

