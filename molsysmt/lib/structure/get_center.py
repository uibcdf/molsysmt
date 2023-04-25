import numba as nb
import numpy as np
from .make_numba_signature import make_numba_signature

arguments=[
    nb.float64[:,:,:], # coordinates
    [nb.int64[:], 'all'], # lists of lists of atom indices
    [nb.float64[:], None], # lists of lists of atom indices
]
output=nb.float64[:,:,:]
@nb.njit(make_numba_signature(arguments,output))
def get_center(coordinates, atom_indices='all', weights=None):

    n_structures=coordinates.shape[0]

    center=np.zeros((n_structures, 1, 3), dtype=nb.float64)
    aux=np.zeros((3), dtype=nb.float64)

    if isinstance(atom_indices, str):
        if atom_indices=='all':
            n_atoms = coordinates.shape[1]
            if weights is None:
                for ii in range(n_structures):
                    aux[:]=0.0
                    for jj in range(n_atoms):
                        aux[:]=aux[:]+coordinates[ii,jj,:]
                    center[ii,0,:]=aux/n_atoms
            else:
                for ii in range(n_structures):
                    aux[:]=0.0
                    weight=0.0
                    for jj in range(n_atoms):
                        aux[:]+=weights[jj]*coordinates[ii,jj,:]
                        weight+=weights[jj]
                    center[ii,0,:]=aux/n_atoms
    else:
        if weights is None:
            for ii in range(n_structures):
                aux[:]=0.0
                for jj in atom_indices:
                    aux[:]=aux[:]+coordinates[ii,jj,:]
                center[ii,0,:]=aux/n_atoms
        else:
            for ii in range(n_structures):
                aux[:]=0.0
                weight=0.0
                for kk,jj in enumerate(atom_indices):
                    aux[:]+=weights[kk]*coordinates[ii,jj,:]
                    weight+=weights[kk]
                center[ii,0,:]=aux/n_atoms

    return center

arguments=[
    nb.float64[:,:,:], # coordinates
    nb.types.ListType(nb.types.ListType(nb.int64)), # lists of lists of atom indices
    [nb.types.ListType(nb.types.ListType(nb.float64)), None], # lists of lists of atom indices
]
output=nb.float64[:,:,:]
@nb.njit(make_numba_signature(arguments,output))
def get_center_groups_of_atoms(coordinates, groups_of_atoms, weights=None):

    n_structures=coordinates.shape[0]

    center=np.zeros((n_structures, 1, 3), dtype=nb.float64)
    aux=np.zeros((3), dtype=nb.float64)

    if isinstance(atom_indices, str):
        if atom_indices=='all':
            n_atoms = coordinates.shape[1]
            if weights is None:
                for ii in range(n_structures):
                    aux[:]=0.0
                    for jj in range(n_atoms):
                        aux[:]=aux[:]+coordinates[ii,jj,:]
                    center[ii,0,:]=aux/n_atoms
            else:
                for ii in range(n_structures):
                    aux[:]=0.0
                    weight=0.0
                    for jj in range(n_atoms):
                        aux[:]+=weights[jj]*coordinates[ii,jj,:]
                        weight+=weights[jj]
                    center[ii,0,:]=aux/n_atoms
    else:
        if weights is None:
            for ii in range(n_structures):
                aux[:]=0.0
                for jj in atom_indices:
                    aux[:]=aux[:]+coordinates[ii,jj,:]
                center[ii,0,:]=aux/n_atoms
        else:
            for ii in range(n_structures):
                aux[:]=0.0
                weight=0.0
                for kk,jj in enumerate(atom_indices):
                    aux[:]+=weights[kk]*coordinates[ii,jj,:]
                    weight+=weights[kk]
                center[ii,0,:]=aux/n_atoms

    return center

