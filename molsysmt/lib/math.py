import numpy as np
import numba as nb
from molsysmt._private.jit import lazy_njit
import math


@lazy_njit(nb.float64[:,:](nb.float64[:,:]), cache=True)
def inverse_matrix_3x3(m):

    inv = np.zeros(m.shape, dtype=nb.float64)

    inv[0,0]=1.0/m[0,0]
    inv[1,1]=1.0/m[1,1]
    inv[2,2]=1.0/m[2,2]

    inv[1,0]=-m[1,0]/(m[0,0]*m[1,1])
    inv[2,0]=(m[1,0]*m[2,1]-m[2,0]*m[1,1])/(m[0,0]*m[1,1]*m[2,2])
    inv[2,1]=-m[2,1]/(m[1,1]*m[2,2])

    return inv

@lazy_njit(nb.float64[:](nb.float64[:,:],nb.float64[:]), cache=True)
def matmul(m,v):
    o = np.zeros(m.shape[0], nb.float64)
    for ii in range(m.shape[0]):
        for jj in range(m.shape[1]):
            o[ii]+=m[ii,jj]*v[jj]
    return o

@lazy_njit(nb.float64[:](nb.float64[:,:],nb.float64[:]), cache=True)
def transpmatmul(m,v):
    o = np.zeros(m.shape[1], nb.float64)
    for jj in range(m.shape[0]):
        for ii in range(m.shape[1]):
            o[ii]+=m[jj,ii]*v[jj]
    return o

@lazy_njit(nb.float64(nb.float64[:], nb.float64[:]), cache=True)
def dot_product(a, b):

    aux = 0.0
    for ii in range(a.shape[0]):
        aux += a[ii]*b[ii]
    return aux


@lazy_njit(nb.float64(nb.float64[:,:], nb.uint8[:], nb.uint8[:,:]), cache=True)
def minimum_distance_masked_not_bonded(coordinates, include_mask, bonded_matrix):

    n_atoms = coordinates.shape[0]
    min_distance_sq = 1.0e300
    found = False

    for atom_index_1 in range(n_atoms - 1):
        if include_mask[atom_index_1] == 0:
            continue

        x_1 = coordinates[atom_index_1, 0]
        y_1 = coordinates[atom_index_1, 1]
        z_1 = coordinates[atom_index_1, 2]

        for atom_index_2 in range(atom_index_1 + 1, n_atoms):
            if include_mask[atom_index_2] == 0:
                continue
            if bonded_matrix[atom_index_1, atom_index_2] != 0:
                continue

            dx = x_1 - coordinates[atom_index_2, 0]
            dy = y_1 - coordinates[atom_index_2, 1]
            dz = z_1 - coordinates[atom_index_2, 2]
            distance_sq = dx*dx + dy*dy + dz*dz

            if distance_sq < min_distance_sq:
                min_distance_sq = distance_sq
                found = True

    if not found:
        return np.inf

    return math.sqrt(min_distance_sq)


@lazy_njit(
    nb.float64(
        nb.float64[:, :],
        nb.uint8[:],
        nb.float64[:, :],
        nb.uint8[:],
        nb.int64,
        nb.uint8[:, :],
    ),
    cache=True,
)
def minimum_distance_between_coordinate_sets(existing_coordinates, existing_mask,
                                             candidate_coordinates, candidate_mask,
                                             candidate_start_index, bonded_matrix):

    n_existing = existing_coordinates.shape[0]
    n_candidate = candidate_coordinates.shape[0]
    min_distance_sq = 1.0e300
    found = False

    for existing_index in range(n_existing):
        if existing_mask[existing_index] == 0:
            continue

        x_1 = existing_coordinates[existing_index, 0]
        y_1 = existing_coordinates[existing_index, 1]
        z_1 = existing_coordinates[existing_index, 2]

        for candidate_local_index in range(n_candidate):
            if candidate_mask[candidate_local_index] == 0:
                continue

            candidate_global_index = candidate_start_index + candidate_local_index
            if bonded_matrix[existing_index, candidate_global_index] != 0:
                continue

            dx = x_1 - candidate_coordinates[candidate_local_index, 0]
            dy = y_1 - candidate_coordinates[candidate_local_index, 1]
            dz = z_1 - candidate_coordinates[candidate_local_index, 2]
            distance_sq = dx*dx + dy*dy + dz*dz

            if distance_sq < min_distance_sq:
                min_distance_sq = distance_sq
                found = True

    if not found:
        return np.inf

    return math.sqrt(min_distance_sq)


@lazy_njit(nb.float64[:](nb.float64[:], nb.float64[:]), cache=True)
def cross_product(a, b):

    output=np.empty((3), dtype=nb.float64)

    output[0]=a[1]*b[2]-a[2]*b[1]
    output[1]=-a[0]*b[2]+a[2]*b[0]
    output[2]=a[0]*b[1]-a[1]*b[0]

    return output

@lazy_njit(nb.float64(nb.float64[:]), cache=True)
def norm_vector(a):

    aux = 0.0
    for ii in range(a.shape[0]):
        aux += a[ii]*a[ii]
    return math.sqrt(aux)


@lazy_njit(nb.float64[:](nb.float64[:]), cache=True)
def normalize_vector(a):

    aux = norm_vector(a)

    return a/aux


@lazy_njit(nb.float64(nb.float64[:],
                     nb.float64[:],
                     ),
        cache=True)
def angle(vect0, vect1):

    cosa = dot_product(vect0,vect1)/(norm_vector(vect0)*norm_vector(vect1))

    if cosa>=1.0:
        cosa=1.0
    if cosa<=-1.0:
        cosa=-1.0

    ang = math.acos(cosa)

    return ang


@lazy_njit(nb.float64(nb.float64[:],
                     nb.float64[:],
                     nb.float64[:],
                     ),
        cache=True)
def dihedral_angle(vect0, vect1, vect2):

    aux0 = cross_product(vect0, vect1)
    aux1 = cross_product(vect1, vect2)

    cosa = dot_product(aux0,aux1)/(norm_vector(aux0)*norm_vector(aux1))

    if cosa>=1.0:
        cosa=1.0
    if cosa<=-1.0:
        cosa=-1.0

    ang = math.acos(cosa)

    aux2 = cross_product(aux0,aux1)

    if dot_product(aux2,vect1)<=0:
        ang=-ang

    return ang


@lazy_njit(nb.void(nb.float64[:], nb.float64[:], nb.float64), cache=True)
def rodrigues_rotation(vector, unit_vector, angle):

    cosa = math.cos(angle)
    sina = math.sin(angle)

    aux1 = vector*cosa
    aux2 = cross_product(unit_vector, vector)*sina
    aux3 = dot_product(unit_vector, vector)*(1.0-cosa)*unit_vector

    vector[:] = aux1[:]+aux2[:]+aux3[:]

    pass

@lazy_njit(nb.float64[:,:](nb.float64[:]), cache=True)
def quaternion_to_rotation_matrix(q):

    q0, q1, q2, q3 = q

    U=np.empty((3,3), dtype=float)

    q00=2*q0*q0
    q11=2*q1*q1
    q22=2*q2*q2
    q33=2*q3*q3

    q01=2*q0*q1
    q02=2*q0*q2
    q03=2*q0*q3
    q12=2*q1*q2
    q13=2*q1*q3
    q23=2*q2*q3

    U[0,0]=q00+q11-1.0
    U[1,1]=q00+q22-1.0
    U[2,2]=q00+q33-1.0

    U[0,1]=q12-q03
    U[1,0]=q12+q03

    U[0,2]=q13+q02
    U[2,0]=q13-q02

    U[1,2]=q23-q01
    U[2,1]=q23+q01

    return U
