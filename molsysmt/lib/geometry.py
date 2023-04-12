import numpy as np
import numba as nb
import math
from .pbc import mic
from .math import norm_vector, cross_product, dot_product


@nb.jit(nb.float64(nb.float64[:], nb.float64[:], nb.float64[:,:], nb.float64[:,:], nb.boolean, nb.boolean), nopython=True)
def distance_2_points(point1, point2, box, inv, ortho, mic_opt):

    vect_aux=point1-point2
    if mic_opt:
        mic(vect_aux, box, inv, ortho)

    dist=norm_vector(vect_aux)

    return dist


@nb.jit(nb.float64(nb.float64[:], nb.float64[:], nb.float64[:]), nopython=True)
def angle_3_vects(vec1, vec2, vec3):

    aux1 = cross_product(vec1, vec2)
    aux2 = cross_product(vec2, vec3)

    cosa = dot_product(aux1,aux2)/(norm_vector(aux1)*norm_vector(aux2))

    if cosa>=1.0:
        cosa=1.0
    if cosa<=-1.0:
        cosa=-1.0

    ang = math.degrees(math.acos(cosa))

    aux3 = cross_product(aux1,aux2)

    if dot_product(aux3,vec2)<=0:
        ang=-ang

    return ang


@nb.jit(nb.float64[:,:,:](nb.boolean,nb.float64[:,:,:], nb.float64[:,:,:], nb.float64[:,:,:],
    np.boolean, np.boolean), nopython=True)
def distance(diff_set, coors1, coors2, box, ortho, mic_opt):

    n_structures = coors1.shape[0]
    n1 = coors1.shape[1]
    if diff_set:
        n2 = coors2.shape[1]
    else:
        n2=n1

    matrix=np.zeros((n_structures,n1,n2), dtype=nb.float64)

    if diff_set:
        for kk in range(n_structures):
            tmp_box=box[kk,:,:]
            tmp_inv=inverse_matrix_3x3(tmp_box)
            for ii in range(n1):
                vect_aux1=coors1[kk,ii,:]
                for jj in range(n2):
                    vect_aux2=coors2[kk,jj,:]
                    matrix[kk,jj,ii]=distance_2_points(vect_aux1, vect_aux2, tmp_box, tmp_inv, ortho, mic_opt)
    else:
        for kk in range(n_structures):
            tmp_box=box[kk,:,:]
            tmp_inv=inverse_matrix_3x3(tmp_box)
            for ii in range(n1):
                vect_aux1=coors1[kk,ii,:]
                for jj in range(ii+1,n2):
                    vect_aux2=coors1[kk,jj,:]
                    val_aux=distance_2_points(vect_aux1, vect_aux2, tmp_box, tmp_inv, ortho, mic_opt)
                    matrix[kk,jj,ii]=val_aux
                    matrix[kk,ii,jj]=val_aux

    return matrix


@nb.jit(nb.float64[:,:](nb.boolean,nb.float64[:,:,:], nb.float64[:,:,:], nb.float64[:,:,:],
    np.boolean, np.boolean), nopython=True)
def distance_pairs(coors1, coors2, box, ortho, mic_opt):

    n_structures = coors1.shape[0]
    n1 = coors1.shape[1]

    matrix=np.zeros((n_structures,n1), dtype=nb.float64)

    for kk in range(n_structures):
        tmp_box=box[kk,:,:]
        tmp_inv=inverse_matrix_3x3(tmp_box)
        for ii in range(n1):
            matrix[kk,ii]=distance_2_points(coors1[kk,ii,:], coors2[kk,ii,:], tmp_box, tmp_inv, ortho, mic_opt)

    return matrix


@nb.jit(void(nb.boolean,nb.float64[:,:,:], nb.float64[:,:], nb.float64[:]), nopython=True)
def translate(coors, shifts, structure_indices):

    n_structures_indices=structure_indices.shape[0]

    for ii in range(n_structures_indices):
        kk=structure_indices[ii]
        for jj in range(n_atoms):
            coors[kk,jj,:]=coors[kk,jj,:]+shifts[ii,:]


@nb.jit(nb.float64[:,:](nb.float64[:,:,:], nb.float64[:,:,:], np.boolean, np.boolean, np.int64[:,:]), nopython=True)
def dihedral_angles(coors, box, ortho, mic_opt, quartets):

    n_structures=coors.shape[0]
    n_angs=quartets[0]

    for jj in range(n_structures):
        tmp_box=box[jj,:,:]
        tmp_inv=inverse_matrix_3x3[tmp_box]
        counter=0
        for at0, at1, at2, at3 in quartets:
            vect0=coors[jj,at1]-coors[jj,at0]
            vect1=coors[jj,at2]-coors[jj,at1]
            vect2=coors[jj,at3]-coors[jj,at2]
            if mic_opt:
                mic(vect0, tmp_box, tmp_inv, ortho)
                mic(vect1, tmp_box, tmp_inv, ortho)
                mic(vect2, tmp_box, tmp_inv, ortho)
            angs[jj,counter]=angle_3_vectors(vect0, vect1, vect2)
            counter+=1

    return angs


@nb.jit(void(nb.float64[:,:,:], nb.float64[:,:,:], np.boolean, np.boolean, np.int64[:,:],
    nb.float64[:,:], nb.int64[:], nb.int64[:]), nopython=True)
def set_dihedral_angles(coors, box, ortho, mic_opt, quartets, angs, blocks, atoms_per_block):

    n_structures=coors.shape[0]
    n_angs=angs.shape[0]

    aux_block = np.zeros((n_angs+1), dtype=int)

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
            if mic_opt:
                mic(vect0, tmp_box, tmp_inv, ortho)
                mic(vect1, tmp_box, tmp_inv, ortho)
                mic(vect2, tmp_box, tmp_inv, ortho)
            u_vect = normalize_vector(vect2)
            old_ang=angle_3_vectors(vect0, vect1, vect2)
            shift_ang=angs[jj,counter]-old_ang
            for kk in range(aux_block[ii], aux_block[ii+1]):
                vect_aux=coors[jj,kk,:]-coors[jj,at2,:]
                if mic_opt:
                    mic(vect_aux, tmp_box, tmp_inv, ortho)
                rogrigues_rotation(vect_aux, u_vect, shift_ang)
                if mic_opt:
                    mic(vect_aux, tmp_box, tmp_inv, ortho)
                coors[jj,ll,:]=coors[jj,at2,:]+vect_aux

    pass

