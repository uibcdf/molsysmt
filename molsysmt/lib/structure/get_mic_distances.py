import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature
from ..pbc.wrap_to_mic import wrap_to_mic_vector_single_structure
from ..pbc.box_is_orthogonal import box_is_orthogonal_single_structure
from ..math import norm_vector, inverse_matrix_3x3

arguments=[nb.float64[:], # point1 [3]
           nb.float64[:], # point2 [3]
           nb.float64[:,:], # box [3,3]
           [nb.float64[:,:], None], # inv_box [3,3]
           [nb.boolean, None], # orthogonal
          ]
output=nb.float64
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_distance_two_points_single_structure(point1, point2, box, inv_box, orthogonal):

    tmp_vect=point2-point1

    if inv_box is None:
        inv_box = inverse_matrix_3x3(box)

    if orthogonal is None:
        orthogonal = box_is_orthogonal_single_structure(box)

    tmp_vect = wrap_to_mic_vector_single_structure(tmp_vect, box, inv_box, orthogonal)

    distance = norm_vector(tmp_vect)

    return distance


arguments=[nb.float64[:,:,:], # coordinates
           nb.float64[:,:,:], # box
           nb.int64[:], # atom_indices1 [n_atoms]
           nb.int64[:], # structure_indices1 [n_structures]
           [nb.int64[:],None], # atom_indices2 [n_atoms]
           [nb.int64[:],None], # structure_indices2 [n_structures]
          ]
output=nb.float64[:,:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_distances_single_system(coordinates, box, atom_indices1, structure_indices1,
        atom_indices2, structure_indices2):

    if atom_indices2 is None:

        if structure_indices2 is None:

            n_atoms=atom_indices1.shape[0]
            n_structures=structure_indices1.shape[0]

            distances = np.zeros((n_structures, n_atoms, n_atoms), dtype=np.float64)

            for aa in range(n_structures):
                ii = structure_indices1[aa]
                tmp_box = box[ii,:,:]
                inv_box = inverse_matrix_3x3(tmp_box)
                orthogonal = box_is_orthogonal_single_structure(tmp_box)
                for bb in range(n_atoms):
                    jj=atom_indices1[bb]
                    point1 = coordinates[ii,jj,:]
                    for cc in range(bb+1, n_atoms):
                        kk=atom_indices1[cc]
                        point2 = coordinates[ii,kk,:]
                        aux = get_mic_distance_two_points_single_structure(point1, point2, tmp_box,
                                inv_box, orthogonal)
                        distances[aa,bb,cc]=aux
                        distances[aa,cc,bb]=aux

        else:

            n_atoms=atom_indices1.shape[0]
            n_structures=structure_indices1.shape[0]

            distances = np.zeros((n_structures, n_atoms, n_atoms), dtype=np.float64)

            for aa in range(n_structures):
                ii = structure_indices1[aa]
                jj = structure_indices2[aa]
                tmp_box = box[ii,:,:]
                inv_box = inverse_matrix_3x3(tmp_box)
                orthogonal = box_is_orthogonal_single_structure(tmp_box)

                for bb in range(n_atoms):
                    kk=atom_indices1[bb]
                    point1 = coordinates[ii,kk,:]
                    for cc in range(n_atoms):
                        ll=atom_indices1[cc]
                        point2 = coordinates[jj,ll,:]
                        aux = get_mic_distance_two_points_single_structure(point1, point2, tmp_box,
                                inv_box, orthogonal)
                        distances[aa,bb,cc]=aux

    else:

        if structure_indices2 is None:

            n_atoms1=atom_indices1.shape[0]
            n_atoms2=atom_indices2.shape[0]
            n_structures=structure_indices1.shape[0]

            distances = np.zeros((n_structures, n_atoms1, n_atoms2), dtype=np.float64)

            for aa in range(n_structures):
                ii = structure_indices1[aa]
                tmp_box = box[ii,:,:]
                inv_box = inverse_matrix_3x3(tmp_box)
                orthogonal = box_is_orthogonal_single_structure(tmp_box)

                for bb in range(n_atoms1):
                    jj=atom_indices1[bb]
                    point1 = coordinates[ii,jj,:]
                    for cc in range(n_atoms2):
                        kk=atom_indices2[cc]
                        point2 = coordinates[ii,kk,:]
                        aux = get_mic_distance_two_points_single_structure(point1, point2, tmp_box,
                                inv_box, orthogonal)
                        distances[aa,bb,cc]=aux

        else:

            n_atoms1=atom_indices1.shape[0]
            n_atoms2=atom_indices2.shape[0]
            n_structures=structure_indices1.shape[0]

            distances = np.zeros((n_structures, n_atoms1, n_atoms2), dtype=np.float64)

            for aa in range(n_structures):
                ii = structure_indices1[aa]
                jj = structure_indices2[aa]
                tmp_box = box[ii,:,:]
                inv_box = inverse_matrix_3x3(tmp_box)
                orthogonal = box_is_orthogonal_single_structure(tmp_box)

                for bb in range(n_atoms1):
                    kk=atom_indices1[bb]
                    point1 = coordinates[ii,kk,:]
                    for cc in range(n_atoms2):
                        ll=atom_indices2[cc]
                        point2 = coordinates[jj,ll,:]
                        aux = get_mic_distance_two_points_single_structure(point1, point2, tmp_box,
                                inv_box, orthogonal)
                        distances[aa,bb,cc]=aux

    return distances


arguments=[nb.float64[:,:,:], # coordinates1
           nb.float64[:,:,:], # coordinates2
           nb.float64[:,:,:], # box
           nb.int64[:], # atom_indices1 [n_atoms]
           nb.int64[:], # structure_indices1 [n_structures]
           nb.int64[:], # atom_indices2 [n_atoms]
           nb.int64[:], # structure_indices2 [n_structures]
          ]
output=nb.float64[:,:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_distances_two_systems(coordinates1, coordinates2, box, atom_indices1, structure_indices1,
        atom_indices2, structure_indices2):

    n_atoms1=atom_indices1.shape[0]
    n_atoms2=atom_indices2.shape[0]
    n_structures=structure_indices1.shape[0]

    distances = np.zeros((n_structures, n_atoms1, n_atoms2), dtype=np.float64)

    for aa in range(n_structures):
        ii = structure_indices1[aa]
        jj = structure_indices2[aa]
        tmp_box = box[ii,:,:]
        inv_box = inverse_matrix_3x3(tmp_box)
        orthogonal = box_is_orthogonal_single_structure(tmp_box)

        for bb in range(n_atoms1):
            kk=atom_indices1[bb]
            point1 = coordinates1[ii,kk,:]
            for cc in range(n_atoms2):
                ll=atom_indices2[cc]
                point2 = coordinates2[jj,ll,:]
                aux = get_mic_distance_two_points_single_structure(point1, point2, tmp_box,
                        inv_box, orthogonal)
                distances[aa,bb,cc]=aux

    return distances


arguments=[nb.float64[:,:,:], # coordinates
           nb.float64[:,:,:], # box
           nb.int64[:], # atom_indices1 [n_atoms]
           nb.int64[:], # structure_indices1 [n_structures]
           nb.int64[:], # atom_indices2 [n_atoms]
           [nb.int64[:],None], # structure_indices2 [n_structures]
          ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_distances_pairs_single_system(coordinates, box, atom_indices1, structure_indices1,
        atom_indices2, structure_indices2):

    n_atoms=atom_indices1.shape[0]
    n_structures=structure_indices1.shape[0]

    distances = np.zeros((n_structures, n_atoms), dtype=np.float64)

    if structure_indices2 is None:

        for aa in range(n_structures):
            ii = structure_indices1[aa]
            tmp_box = box[ii,:,:]
            inv_box = inverse_matrix_3x3(tmp_box)
            orthogonal = box_is_orthogonal_single_structure(tmp_box)

            for bb in range(n_atoms):
                jj=atom_indices1[bb]
                kk=atom_indices2[bb]
                point1 = coordinates[ii,jj,:]
                point2 = coordinates[ii,kk,:]
                aux = get_mic_distance_two_points_single_structure(point1, point2, tmp_box,
                            inv_box, orthogonal)
                distances[aa,bb]=aux

    else:

        for aa in range(n_structures):
            ii = structure_indices1[aa]
            jj = structure_indices2[aa]
            tmp_box = box[ii,:,:]
            inv_box = inverse_matrix_3x3(tmp_box)
            orthogonal = box_is_orthogonal_single_structure(tmp_box)

            for bb in range(n_atoms):
                kk=atom_indices1[bb]
                ll=atom_indices2[bb]
                point1 = coordinates[ii,kk,:]
                point2 = coordinates[jj,ll,:]
                aux = get_mic_distance_two_points_single_structure(point1, point2, tmp_box,
                            inv_box, orthogonal)
                distances[aa,bb]=aux

    return distances


arguments=[nb.float64[:,:,:], # coordinates1
           nb.float64[:,:,:], # coordinates2
           nb.float64[:,:,:], # box
           nb.int64[:], # atom_indices1 [n_atoms]
           nb.int64[:], # structure_indices1 [n_structures]
           nb.int64[:], # atom_indices2 [n_atoms]
           nb.int64[:], # structure_indices2 [n_structures]
          ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_distances_pairs_two_systems(coordinates1, coordinates2, box, atom_indices1, structure_indices1,
        atom_indices2, structure_indices2):

    n_atoms=atom_indices1.shape[0]
    n_structures=structure_indices1.shape[0]

    distances = np.zeros((n_structures, n_atoms), dtype=np.float64)

    for aa in range(n_structures):
        ii = structure_indices1[aa]
        jj = structure_indices2[aa]
        tmp_box = box[ii,:,:]
        inv_box = inverse_matrix_3x3(tmp_box)
        orthogonal = box_is_orthogonal_single_structure(tmp_box)

        for bb in range(n_atoms):
            kk=atom_indices1[bb]
            ll=atom_indices2[bb]
            point1 = coordinates1[ii,kk,:]
            point2 = coordinates2[jj,ll,:]
            aux = get_mic_distance_two_points_single_structure(point1, point2, tmp_box,
                        inv_box, orthogonal)
            distances[aa,bb]=aux

    return distances


arguments=[nb.float64[:,:], # coordinates
           nb.float64[:,:], # box
           nb.int64[:], # atom_indices1 [n_atoms]
           [nb.int64[:],None], # atom_indices2 [n_atoms]
          ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_distances_single_system_single_structure(coordinates, box, atom_indices1, atom_indices2):

    inv_box = inverse_matrix_3x3(box)
    orthogonal = box_is_orthogonal_single_structure(box)

    if atom_indices2 is None:

        n_atoms=atom_indices1.shape[0]

        distances = np.zeros((n_atoms, n_atoms), dtype=np.float64)

        for bb in range(n_atoms):
            jj=atom_indices1[bb]
            point1 = coordinates[jj,:]
            for cc in range(bb+1, n_atoms):
                kk=atom_indices1[cc]
                point2 = coordinates[kk,:]
                aux = get_mic_distance_two_points_single_structure(point1, point2, box,
                                inv_box, orthogonal)
                distances[bb,cc]=aux
                distances[cc,bb]=aux

    else:

        n_atoms1=atom_indices1.shape[0]
        n_atoms2=atom_indices2.shape[0]

        distances = np.zeros((n_atoms1, n_atoms2), dtype=np.float64)

        for bb in range(n_atoms1):
            jj=atom_indices1[bb]
            point1 = coordinates[jj,:]
            for cc in range(n_atoms2):
                kk=atom_indices2[cc]
                point2 = coordinates[kk,:]
                aux = get_mic_distance_two_points_single_structure(point1, point2, tmp_box,
                        inv_box, orthogonal)
                distances[bb,cc]=aux

    return distances


arguments=[nb.float64[:,:], # coordinates1
           nb.float64[:,:], # coordinates2
           nb.float64[:,:], # box
           nb.int64[:], # atom_indices1 [n_atoms]
           nb.int64[:], # atom_indices2 [n_atoms]
          ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_distances_two_systems_single_structure(coordinates1, coordinates2, box, atom_indices1, atom_indices2):

    inv_box = inverse_matrix_3x3(box)
    orthogonal = box_is_orthogonal_single_structure(box)

    n_atoms1=atom_indices1.shape[0]
    n_atoms2=atom_indices2.shape[0]

    distances = np.zeros((n_atoms1, n_atoms2), dtype=np.float64)

    for bb in range(n_atoms1):
        kk=atom_indices1[bb]
        point1 = coordinates1[kk,:]
        for cc in range(n_atoms2):
            ll=atom_indices2[cc]
            point2 = coordinates2[ll,:]
            aux = get_mic_distance_two_points_single_structure(point1, point2, tmp_box,
                        inv_box, orthogonal)
            distances[bb,cc]=aux

    return distances


arguments=[nb.float64[:,:], # coordinates
           nb.float64[:,:], # box
           nb.int64[:], # atom_indices1 [n_atoms]
           nb.int64[:], # atom_indices2 [n_atoms]
          ]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_distances_pairs_single_system_single_structure(coordinates, box, atom_indices1, atom_indices2):

    inv_box = inverse_matrix_3x3(box)
    orthogonal = box_is_orthogonal_single_structure(box)

    n_atoms=atom_indices1.shape[0]

    distances = np.zeros((n_atoms), dtype=np.float64)

    for bb in range(n_atoms):
        jj=atom_indices1[bb]
        kk=atom_indices2[bb]
        point1 = coordinates[jj,:]
        point2 = coordinates[kk,:]
        aux = get_mic_distance_two_points_single_structure(point1, point2, tmp_box,
                            inv_box, orthogonal)
        distances[bb]=aux

    return distances


arguments=[nb.float64[:,:], # coordinates1
           nb.float64[:,:], # coordinates2
           nb.float64[:,:], # box
           nb.int64[:], # atom_indices1 [n_atoms]
           nb.int64[:], # atom_indices2 [n_atoms]
          ]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_distances_pairs_two_systems_single_structure(coordinates1, coordinates2, box, atom_indices1, atom_indices2):

    n_atoms=atom_indices1.shape[0]

    distances = np.zeros((n_atoms), dtype=np.float64)

    for bb in range(n_atoms):
        kk=atom_indices1[bb]
        ll=atom_indices2[bb]
        point1 = coordinates1[kk,:]
        point2 = coordinates2[ll,:]
        aux = get_mic_distance_two_points_single_structure(point1, point2, tmp_box,
                        inv_box, orthogonal)
        distances[bb]=aux

    return distances

