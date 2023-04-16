import numpy as np
import numba as nb
import math
from .make_numba_signature import make_numba_signature
from .pbc import mic_single_structure
from .math import norm_vector, cross_product, dot_product, inverse_matrix_3x3, normalize_vector,\
        rodrigues_rotation

arguments=[
        nb.float64[:],
        nb.float64[:],
        [nb.float64[:,:], None],
        [nb.float64[:,:], None],
        [nb.boolean, None],
        [nb.boolean, True]
        ]
output=nb.float64
@nb.njit(make_numba_signature(arguments,output))
def distance_2_points_single_structure(point1, point2, box=None, inv_box=None, orthogonal=None, pbc=True):

    if pbc and (box is None):
        pbc=False

    vect_aux=point1-point2

    if pbc:

        mic_single_structure(vect_aux, box, inv_box, orthogonal)

    dist=norm_vector(vect_aux)

    return dist


arguments=[
        nb.float64[:],
        nb.float64[:],
        nb.float64[:],
        [nb.float64[:,:], None],
        [nb.float64[:,:], None],
        [nb.boolean, None],
        [nb.boolean, True]
        ]
output=nb.float64
@nb.njit(make_numba_signature(arguments,output))
def dihedral_angle_single_structure(vect0, vect1, vect2, box=None, inv_box=None, orthogonal=None, pbc=True):

    if pbc and (box is None):
        pbc=False

    if pbc:
        minimum_image_convention(vect0, box, inv_box, ortho)
        minimum_image_convention(vect1, box, inv_box, ortho)
        minimum_image_convention(vect2, box, inv_box, ortho)

    dist=norm_vector(vect_aux)
    aux0 = cross_product(vect0, vect1)
    aux1 = cross_product(vect1, vect2)

    cosa = dot_product(aux0,aux1)/(norm_vector(aux0)*norm_vector(aux1))

    if cosa>=1.0:
        cosa=1.0
    if cosa<=-1.0:
        cosa=-1.0

    ang = math.degrees(math.acos(cosa))

    aux3 = cross_product(aux0,aux1)

    if dot_product(aux3,vect1)<=0:
        ang=-ang

    return ang


arguments=[
        nb.float64[:,:,:],
        nb.float64[:,:,:],
        [nb.float64[:,:,:], None],
        [nb.boolean, True]
        ]
output=nb.float64[:,:,:]
@nb.njit(make_numba_signature(arguments,output))
def distance(coors1, coors2, box=None,  pbc=True):

    if pbc and (box is None):
        pbc=False

    n_structures = coors1.shape[0]
    n1 = coors1.shape[1]

    if pbc:

        orthogonal=box_is_orthogonal(box)

        if coors2 is None:
            n2 = coors2.shape[1]
            matrix=np.zeros((n_structures,n1,n2), dtype=nb.float64)
            for kk in range(n_structures):
                tmp_box=box[kk,:,:]
                tmp_inv=inverse_matrix_3x3(tmp_box)
                for ii in range(n1):
                    point1=coors1[kk,ii,:]
                    for jj in range(n2):
                        point2=coors2[kk,jj,:]
                        matrix[kk,jj,ii]=distance_2_points_single_structure(point1, point2, tmp_box, tmp_inv,
                                orthogonal, pbc)
        else:
            matrix=np.zeros((n_structures,n1,n1), dtype=nb.float64)
            for kk in range(n_structures):
                tmp_box=box[kk,:,:]
                tmp_inv=inverse_matrix_3x3(tmp_box)
                for ii in range(n1):
                    point1=coors1[kk,ii,:]
                    for jj in range(ii+1,n1):
                        point2=coors1[kk,jj,:]
                        val_aux=distance_2_points(point1, point2, tmp_box, tmp_inv, orthogonal, pbc)
                        matrix[kk,jj,ii]=val_aux
                        matrix[kk,ii,jj]=val_aux

    else:

        if coors2 is None:
            n2 = coors2.shape[1]
            matrix=np.zeros((n_structures,n1,n2), dtype=nb.float64)
            for kk in range(n_structures):
                for ii in range(n1):
                    point1=coors1[kk,ii,:]
                    for jj in range(n2):
                        point2=coors2[kk,jj,:]
                        matrix[kk,jj,ii]=distance_2_points_single_structure(point1, point2, None,
                                None, None, False)
        else:
            matrix=np.zeros((n_structures,n1,n1), dtype=nb.float64)
            for kk in range(n_structures):
                for ii in range(n1):
                    point1=coors1[kk,ii,:]
                    for jj in range(ii+1,n1):
                        point2=coors1[kk,jj,:]
                        val_aux=distance_2_points(point1, point2, None, None, None, False)
                        matrix[kk,jj,ii]=val_aux
                        matrix[kk,ii,jj]=val_aux

    return matrix


@nb.njit([nb.float64[:,:,:](nb.boolean,
                            nb.float64[:,:,:],
                            nb.optional(nb.float64[:,:,:]),
                            nb.optional(nb.float64[:,:,:]),
                            nb.types.Omitted(True),
                            ),
          nb.float64[:,:,:](nb.boolean,
                            nb.float64[:,:,:],
                            nb.optional(nb.float64[:,:,:]),
                            nb.optional(nb.float64[:,:,:]),
                            nb.boolean,
                           )
         ])
def distance_pairs(coors1, coors2, box, pbc=True):

    if pbc and (box is None):
        pbc=False

    n_structures = coors1.shape[0]
    n1 = coors1.shape[1]

    matrix=np.zeros((n_structures,n1), dtype=nb.float64)

    if pbc:

        orthogonal=box_is_orthogonal(box)

        for kk in range(n_structures):
            tmp_box=box[kk,:,:]
            tmp_inv=inverse_matrix_3x3(tmp_box)
            for ii in range(n1):
                matrix[kk,ii]=distance_2_points(coors1[kk,ii,:], coors2[kk,ii,:], tmp_box, tmp_inv,
                        orthogonal, pbc)

    else:

        for kk in range(n_structures):
            for ii in range(n1):
                matrix[kk,ii]=distance_2_points(coors1[kk,ii,:], coors2[kk,ii,:], None, None, None,
                        False)

    return matrix


@nb.njit([nb.float64[:,:,:](nb.float64[:,:,:],
                            nb.float64[:,:,:],
                            nb.optional(nb.float64[:,:,:]),
                            nb.types.Omitted(True),
                            ),
          nb.float64[:,:,:](nb.boolean,
                            nb.float64[:,:,:],
                            nb.optional(nb.float64[:,:,:]),
                            nb.optional(nb.float64[:,:,:]),
                            nb.boolean,
                           )
         ])
@nb.njit(nb.void(nb.float64[:,:,:], nb.float64[:,:], nb.int64[:]))
def translate(coordinates, translation, atom_indices, structure_indices):

    n_structures_indices=structure_indices.shape[0]
    n_atoms=coors.shape[1]

    for ii in range(n_structures_indices):
        kk=structure_indices[ii]
        for jj in range(n_atoms):
            coors[kk,jj,:]=coors[kk,jj,:]+shifts[ii,:]

    pass

@nb.njit(nb.float64[:,:](nb.float64[:,:,:], nb.float64[:,:,:], nb.boolean, nb.boolean, nb.int64[:,:]))
def dihedral_angles(coors, box, ortho, pbc, quartets):

    n_structures=coors.shape[0]
    n_angs=quartets.shape[0]

    angs=np.empty((n_structures,n_angs), dtype=nb.float64)

    for jj in range(n_structures):
        tmp_box=box[jj,:,:]
        tmp_inv=inverse_matrix_3x3(tmp_box)
        counter=0
        for at0, at1, at2, at3 in quartets:
            vect0=coors[jj,at1]-coors[jj,at0]
            vect1=coors[jj,at2]-coors[jj,at1]
            vect2=coors[jj,at3]-coors[jj,at2]
            if pbc:
                minimum_image_convention(vect0, tmp_box, tmp_inv, ortho)
                minimum_image_convention(vect1, tmp_box, tmp_inv, ortho)
                minimum_image_convention(vect2, tmp_box, tmp_inv, ortho)
            angs[jj,counter]=angle_3_vectors(vect0, vect1, vect2)
            counter+=1

    return angs


@nb.njit(nb.void(nb.float64[:,:,:], nb.float64[:,:,:], nb.boolean, nb.boolean, nb.int64[:,:],
    nb.float64[:,:], nb.int64[:], nb.int64[:]))
def set_dihedral_angles(coors, box, ortho, pbc, quartets, angs, blocks, atoms_per_block):

    n_structures=coors.shape[0]
    n_angs=angs.shape[0]

    aux_block = np.zeros((n_angs+1), dtype=nb.int64)

    for ii in range(n_angs):
        aux_block[ii+1:]=aux_block[ii+1:]+atoms_per_block[ii]

    for jj in range(n_structures):
        tmp_box=box[jj,:,:]
        tmp_inv=inverse_matrix_3x3(tmp_box)
        counter=0
        for at0, at1, at2, at3 in quartets:
            vect0=coors[jj,at1]-coors[jj,at0]
            vect1=coors[jj,at2]-coors[jj,at1]
            vect2=coors[jj,at3]-coors[jj,at2]
            if pbc:
                minimum_image_convention(vect0, tmp_box, tmp_inv, ortho)
                minimum_image_convention(vect1, tmp_box, tmp_inv, ortho)
                minimum_image_convention(vect2, tmp_box, tmp_inv, ortho)
            u_vect = normalize_vector(vect2)
            old_ang=angle_3_vectors(vect0, vect1, vect2)
            shift_ang=angs[jj,counter]-old_ang
            for kk in range(aux_block[ii], aux_block[ii+1]):
                ll=blocks[kk]
                vect_aux=coors[jj,ll,:]-coors[jj,at2,:]
                if pbc:
                    minimum_image_convention(vect_aux, tmp_box, tmp_inv, ortho)
                rodrigues_rotation(vect_aux, u_vect, shift_ang)
                if pbc:
                    minimum_image_convention(vect_aux, tmp_box, tmp_inv, ortho)
                coors[jj,ll,:]=coors[jj,at2,:]+vect_aux

    pass

