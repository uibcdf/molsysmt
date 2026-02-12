import numba as nb
from molsysmt._private.jit import lazy_njit
import numpy as np
from ..make_numba_signature import make_numba_signature
from math import sqrt

arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.float64[:], # weights: [n_atoms]
]
output=[nb.float64[:], # [n_atoms*3]
        nb.float64[:,:], # [n_atoms*3, n_atoms*3]
]
@lazy_njit(make_numba_signature(arguments,output), cache=True)
def principal_component_analysis(coordinates, weights):

    n_structures, n_atoms = coordinates.shape[0:2]
    n_features = n_atoms * 3

    eigenvectors = np.zeros((n_features, n_features), dtype=nb.float64)
    eigenvalues = np.zeros((n_features), dtype=nb.float64)
    cov = np.zeros((n_features, n_features), dtype=nb.float64)
    mean = np.zeros((n_features), dtype=nb.float64)
    aux_ind = np.zeros((n_atoms, 3), dtype=np.int64)
    weight_per_feature = np.zeros((n_features), dtype=nb.float64)
    flat = np.zeros((n_structures, n_features), dtype=nb.float64)

    gg = 0
    for jj in range(3):
        for ii in range(n_atoms):
            aux_ind[ii, jj] = gg
            gg += 1

    for ll in range(n_structures):
        for ii in range(n_atoms):
            for jj in range(3):
                xx = aux_ind[ii, jj]
                aux_coor = coordinates[ll, ii, jj]
                flat[ll, xx] = aux_coor
                mean[xx] += aux_coor

    mean = mean / n_structures

    for jj in range(3):
        for ii in range(n_atoms):
            xx = aux_ind[ii, jj]
            weight_per_feature[xx] = sqrt(weights[ii])

    for ll in range(n_structures):
        for ii in range(n_features):
            xi = (flat[ll, ii] - mean[ii]) * weight_per_feature[ii]
            for jj in range(ii, n_features):
                xj = (flat[ll, jj] - mean[jj]) * weight_per_feature[jj]
                cov[ii, jj] += xi * xj

    for ii in range(n_features):
        for jj in range(ii, n_features):
            cov[ii, jj] = cov[ii, jj] / n_structures
            cov[jj, ii] = cov[ii, jj]

    eigenvalues[:], eigenvectors[:, :] = np.linalg.eigh(cov)
    eigenvectors[:, :] = eigenvectors[:, :].transpose()

    return eigenvalues, eigenvectors
