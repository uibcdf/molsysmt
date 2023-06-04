import numpy as np
import numba as nb
from ..math import dot_product
from ..make_numba_signature import make_numba_signature
import math

arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    nb.float64[:,:], # reference_coordinates: [n_atoms, 3]
]
output=nb.float64
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_rmsd_single_structure(coordinates, reference_coordinates):

    n_atoms = coordinates.shape[0]

    output = 0.0

    for ii in range(n_atoms):
        vect_aux=reference_coordinates[ii,:]-coordinates[ii,:]
        output+=dot_product(vect_aux,vect_aux)

    output=math.sqrt(output/n_atoms)

    return output


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.float64[:,:,:], # coordinates_ref: [n_structures, n_atoms, 3]
]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_rmsd(coordinates, reference_coordinates):

    n_structures, n_atoms = coordinates.shape[0:2]

    output = np.zeros((n_structures), dtype=nb.float64)

    for ii in range(n_structures):
        val_aux = 0.0
        for jj in range(n_atoms):
            vect_aux=reference_coordinates[ii,jj,:]-coordinates[ii,jj,:]
            val_aux+=dot_product(vect_aux,vect_aux)
        output[ii]=math.sqrt(val_aux/n_atoms)

    return output

arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.float64[:,:], # coordinates_ref: [n_structures, n_atoms, 3]
]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_rmsd_with_single_reference_structure(coordinates, reference_coordinates):

    n_structures, n_atoms = coordinates.shape[0:2]

    output = np.zeros((n_structures), dtype=nb.float64)

    for ii in range(n_structures):
        val_aux = 0.0
        for jj in range(n_atoms):
            vect_aux=reference_coordinates[jj,:]-coordinates[ii,jj,:]
            val_aux+=dot_product(vect_aux,vect_aux)
        output[ii]=math.sqrt(val_aux/n_atoms)

    return output

