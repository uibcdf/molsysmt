import numba as nb
from molsysmt._private.jit import lazy_njit
import numpy as np
from ..make_numba_signature import make_numba_signature
import math


arguments = [
    nb.float64[:, :],  # coordinates: (n_atoms, 3)
    nb.float64[:],     # weights: (n_atoms,)
]
output = nb.float64
@lazy_njit(make_numba_signature(arguments, output), cache=True)
def get_radius_of_gyration_single_structure(coordinates, weights):

    n_atoms = coordinates.shape[0]

    total_weight = 0.0
    cx = 0.0
    cy = 0.0
    cz = 0.0
    for ii in range(n_atoms):
        cx += weights[ii] * coordinates[ii, 0]
        cy += weights[ii] * coordinates[ii, 1]
        cz += weights[ii] * coordinates[ii, 2]
        total_weight += weights[ii]
    cx /= total_weight
    cy /= total_weight
    cz /= total_weight

    sum_sq = 0.0
    for ii in range(n_atoms):
        dx = coordinates[ii, 0] - cx
        dy = coordinates[ii, 1] - cy
        dz = coordinates[ii, 2] - cz
        sum_sq += weights[ii] * (dx * dx + dy * dy + dz * dz)

    return math.sqrt(sum_sq / total_weight)


arguments = [
    nb.float64[:, :, :],  # coordinates: (n_structures, n_atoms, 3)
    nb.float64[:],         # weights: (n_atoms,)
]
output = nb.float64[:]
@lazy_njit(make_numba_signature(arguments, output), cache=True)
def get_radius_of_gyration(coordinates, weights):

    n_structures = coordinates.shape[0]
    n_atoms = coordinates.shape[1]

    rg = np.zeros(n_structures, dtype=nb.float64)

    for ii in range(n_structures):
        total_weight = 0.0
        cx = 0.0
        cy = 0.0
        cz = 0.0
        for jj in range(n_atoms):
            cx += weights[jj] * coordinates[ii, jj, 0]
            cy += weights[jj] * coordinates[ii, jj, 1]
            cz += weights[jj] * coordinates[ii, jj, 2]
            total_weight += weights[jj]
        cx /= total_weight
        cy /= total_weight
        cz /= total_weight

        sum_sq = 0.0
        for jj in range(n_atoms):
            dx = coordinates[ii, jj, 0] - cx
            dy = coordinates[ii, jj, 1] - cy
            dz = coordinates[ii, jj, 2] - cz
            sum_sq += weights[jj] * (dx * dx + dy * dy + dz * dz)

        rg[ii] = math.sqrt(sum_sq / total_weight)

    return rg
