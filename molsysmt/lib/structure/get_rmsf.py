import numba as nb
from molsysmt._private.jit import lazy_njit
import numpy as np
from ..make_numba_signature import make_numba_signature
import math


arguments = [
    nb.float64[:, :, :],  # coordinates: (n_structures, n_atoms, 3)
]
output = nb.float64[:]
@lazy_njit(make_numba_signature(arguments, output), cache=True)
def get_rmsf(coordinates):
    """Root-mean-square fluctuation per atom over all structures."""

    n_structures = coordinates.shape[0]
    n_atoms = coordinates.shape[1]

    mean = np.zeros((n_atoms, 3), dtype=nb.float64)
    for ii in range(n_structures):
        for jj in range(n_atoms):
            mean[jj, 0] += coordinates[ii, jj, 0]
            mean[jj, 1] += coordinates[ii, jj, 1]
            mean[jj, 2] += coordinates[ii, jj, 2]
    for jj in range(n_atoms):
        mean[jj, 0] /= n_structures
        mean[jj, 1] /= n_structures
        mean[jj, 2] /= n_structures

    rmsf = np.zeros(n_atoms, dtype=nb.float64)
    for ii in range(n_structures):
        for jj in range(n_atoms):
            dx = coordinates[ii, jj, 0] - mean[jj, 0]
            dy = coordinates[ii, jj, 1] - mean[jj, 1]
            dz = coordinates[ii, jj, 2] - mean[jj, 2]
            rmsf[jj] += dx * dx + dy * dy + dz * dz
    for jj in range(n_atoms):
        rmsf[jj] = math.sqrt(rmsf[jj] / n_structures)

    return rmsf
