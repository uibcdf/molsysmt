import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature
from ..math import norm_vector


arguments=[nb.float64[:], # point1 [3]
           nb.float64[:], # point2 [3]
          ]
output=nb.float64
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_distance_two_points_single_structure(point1, point2):

    tmp_vect=point2-point1
    distance = norm_vector(tmp_vect)

    return distance


arguments=[nb.float64[:,:,:], # coordinates
          ]
output=nb.float64[:,:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_distances_single_system(coordinates):

    n_structures, n_atoms = coordinates.shape[0:2]

    distances = np.zeros((n_structures, n_atoms, n_atoms), dtype=np.float64)

    for ii in range(n_structures):
        for jj in range(n_atoms):
            point1 = coordinates[ii,jj,:]
            for kk in range(jj+1, n_atoms):
                point2 = coordinates[ii,kk,:]
                aux = get_distance_two_points_single_structure(point1, point2)
                distances[ii,jj,kk]=aux
                distances[ii,kk,jj]=aux

    return distances


arguments=[nb.float64[:,:,:], # coordinates1
           nb.float64[:,:,:], # coordinates2
          ]
output=nb.float64[:,:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_distances(coordinates1, coordinates2):

    n_structures1, n_atoms1 = coordinates1.shape[0:2]
    n_structures2, n_atoms2 = coordinates2.shape[0:2]

    distances = np.zeros((n_structures1, n_atoms1, n_atoms2), dtype=np.float64)

    for ii in range(n_structures1):
        for jj in range(n_atoms1):
            point1 = coordinates1[ii,jj,:]
            for kk in range(n_atoms2):
                point2 = coordinates2[ii,kk,:]
                aux = get_distance_two_points_single_structure(point1, point2)
                distances[ii,jj,kk]=aux

    return distances


arguments=[nb.float64[:,:,:], # coordinates1
           nb.float64[:,:,:], # coordinates2
          ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_distances_pairs(coordinates1, coordinates2):

    n_structures, n_atoms = coordinates1.shape[0:2]

    distances = np.zeros((n_structures, n_atoms), dtype=np.float64)

    for ii in range(n_structures):
        for jj in range(n_atoms):
            point1 = coordinates1[ii,jj,:]
            point2 = coordinates2[ii,jj,:]
            aux = get_distance_two_points_single_structure(point1, point2)
            distances[ii,jj]=aux

    return distances


arguments=[nb.float64[:,:], # coordinates
          ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_distances_single_system_single_structure(coordinates):

    n_atoms = coordinates.shape[0]

    distances = np.zeros((n_atoms, n_atoms), dtype=np.float64)

    for ii in range(n_atoms):
        point1 = coordinates[ii,:]
        for jj in range(ii+1, n_atoms):
            point2 = coordinates[jj,:]
            aux = get_distance_two_points_single_structure(point1, point2)
            distances[ii,jj]=aux
            distances[jj,ii]=aux

    return distances


arguments=[nb.float64[:,:], # coordinates1
           nb.float64[:,:], # coordinates2
          ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_distances_single_structure(coordinates1, coordinates2):

    n_atoms1 = coordinates1.shape[0]
    n_atoms2 = coordinates2.shape[0]

    distances = np.zeros((n_atoms1, n_atoms2), dtype=np.float64)

    for ii in range(n_atoms1):
        point1 = coordinates1[ii,:]
        for jj in range(n_atoms2):
            point2 = coordinates2[jj,:]
            aux = get_distance_two_points_single_structure(point1, point2)
            distances[ii,jj]=aux

    return distances


arguments=[nb.float64[:,:], # coordinates1
           nb.float64[:,:], # coordinates2
          ]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_distances_pairs_single_structure(coordinates1, coordinates2):

    n_atoms = coordinates1.shape[0]

    distances = np.zeros((n_atoms), dtype=np.float64)

    for ii in range(n_atoms):
        point1 = coordinates1[ii,:]
        point2 = coordinates2[ii,:]
        aux = get_distance_two_points_single_structure(point1, point2)
        distances[ii]=aux

    return distances

