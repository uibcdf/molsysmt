import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature


arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    nb.float64[:], # weights: [n_atoms]
]
output=[nb.float64[:], # [3]
        nb.float64[:,:], # [3, 3]
]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_principal_inertia_axis_single_structure(coordinates, weights):

    n_atoms = coordinates.shape[0]

    eigenvectors=np.zeros((3, 3), dtype=nb.float64)
    eigenvalues=np.zeros((3), dtype=nb.float64)
    matrix=np.zeros((3,3), dtype=nb.float64)
    center=np.zeros((3), dtype=nb.float64)
    aux_coors=np.zeros((3), dtype=nb.float64)

    aux_weight=0.0
    for ii in range(n_atoms):
        aux_coors[:]+=weights[ii]*coordinates[ii,:]
        aux_weight+=weights[ii]
    center[:]=aux_coors/aux_weight

    for ii in range(n_atoms):
        aux_coors[:]=coordinates[ii,:]-center[:]
        matrix[0,0]+=weights[ii]*(aux_coors[1]**2+aux_coors[2]**2)
        matrix[1,1]+=weights[ii]*(aux_coors[0]**2+aux_coors[2]**2)
        matrix[2,2]+=weights[ii]*(aux_coors[0]**2+aux_coors[1]**2)
        matrix[0,1]-=weights[ii]*(aux_coors[0]*aux_coors[1])
        matrix[0,2]-=weights[ii]*(aux_coors[0]*aux_coors[2])
        matrix[1,2]-=weights[ii]*(aux_coors[1]*aux_coors[2])

    matrix[1,0]=matrix[0,1]
    matrix[2,0]=matrix[0,2]
    matrix[2,1]=matrix[1,2]

    eigenvalues[:], eigenvectors[:,:] = np.linalg.eigh(matrix)
    eigenvectors[:,:] = eigenvectors[:,:].transpose()

    return eigenvalues, eigenvectors


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.float64[:], # weights: [n_atoms]
]
output=[nb.float64[:,:], # [n_structures, 3]
        nb.float64[:,:,:], # [n_structures, 3, 3]
]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_principal_inertia_axis(coordinates, weights):

    n_structures, n_atoms = coordinates.shape[0:2]

    eigenvectors=np.zeros((n_structures, 3, 3), dtype=nb.float64)
    eigenvalues=np.zeros((n_structures, 3), dtype=nb.float64)
    matrix=np.zeros((3,3), dtype=nb.float64)
    center=np.zeros((3), dtype=nb.float64)
    aux_coors=np.zeros((3), dtype=nb.float64)

    for jj in range(n_structures):

        aux_weight=0.0
        aux_coors[:]=0.0
        matrix[:,:]=0.0

        for ii in range(n_atoms):

            aux_coors[:]+=weights[ii]*coordinates[jj,ii,:]
            aux_weight+=weights[ii]

        center[:]=aux_coors/aux_weight

        for ii in range(n_atoms):

            aux_coors[:]=coordinates[jj,ii,:]-center[:]
            matrix[0,0]+=weights[ii]*(aux_coors[1]**2+aux_coors[2]**2)
            matrix[1,1]+=weights[ii]*(aux_coors[0]**2+aux_coors[2]**2)
            matrix[2,2]+=weights[ii]*(aux_coors[0]**2+aux_coors[1]**2)
            matrix[0,1]-=weights[ii]*(aux_coors[0]*aux_coors[1])
            matrix[0,2]-=weights[ii]*(aux_coors[0]*aux_coors[2])
            matrix[1,2]-=weights[ii]*(aux_coors[1]*aux_coors[2])

        matrix[1,0]=matrix[0,1]
        matrix[2,0]=matrix[0,2]
        matrix[2,1]=matrix[1,2]

        eigenvalues[jj,:], eigenvectors[jj,:,:] = np.linalg.eigh(matrix)
        eigenvectors[jj,:,:] = eigenvectors[jj,:,:].transpose()

    return eigenvalues, eigenvectors

