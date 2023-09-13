import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature


arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    nb.float64[:], # vector: [3]
    nb.float64[:], # point: [3]
]
output=nb.float64[:,:] # coordinates: [n_atoms, 3]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def flip_single_structure(coordinates, vector, point):

    n_atoms = coordinates.shape[0]

    output = np.zeros((n_atoms,3), dtype=nb.float64)

    for ii in range(n_atoms):

        position = coordinates[ii,:]
        aux_vector = position-point
        dist = aux_vector[0]*vector[0]+aux_vector[1]*vector[1]+aux_vector[2]*vector[2]
        output[ii,:]=position-2*dist*vector

    return output


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.float64[:], # vector: [3]
    nb.float64[:], # point: [3]
]
output=nb.float64[:,:,:] # coordinates: [n_structures, n_atoms, 3]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def flip(coordinates, vector, point):

    n_structures, n_atoms = coordinates.shape[0:2]
    output = np.zeros((n_structures,n_atoms,3), dtype=nb.float64)

    for jj in range(n_structures):
        for ii in range(n_atoms):

            position = coordinates[jj,ii,:]
            aux_vector = position-point
            dist = aux_vector[0]*vector[0]+aux_vector[1]*vector[1]+aux_vector[2]*vector[2]
            output[jj,ii,:]=position-2*dist*vector

    return output


