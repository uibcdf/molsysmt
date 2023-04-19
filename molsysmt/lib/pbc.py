import numba as nb
import numpy as np
import math
from .math import inverse_matrix_3x3, norm_vector, dot_product


@nb.njit(nb.void(nb.float64[:],
                 nb.float64[:,:],
                 nb.optional(nb.float64[:,:]),
                 nb.optional(nb.boolean),
                 )
        )
def pbc_vector(vector, box, inv_box, orthogonal):

    if orthogonal is None:
        orthogonal = box_is_orthogonal_single_structure(box)

    if orthogonal:

        vector[0]=vector[0]-box[0,0]*round(vector[0]/box[0,0])
        vector[1]=vector[1]-box[1,1]*round(vector[1]/box[1,1])
        vector[2]=vector[2]-box[2,2]*round(vector[2]/box[2,2])

    else:

        if inv_box is None:
            inv_box=inverse_matrix_3x3(box)

        vaux = np.empty((3), dtype=float)

        vaux[0]=inv_box[0,0]*vector[0]+inv_box[1,0]*vector[1]+inv_box[2,0]*vector[2]
        vaux[1]=                       inv_box[1,1]*vector[1]+inv_box[2,1]*vector[2]
        vaux[2]=                                              inv_box[2,2]*vector[2]
        vaux[0]=vaux[0]-round(vaux[0])
        vaux[1]=vaux[1]-round(vaux[1])
        vaux[2]=vaux[2]-round(vaux[2])
        vector[0]=box[0,0]*vaux[0]+box[1,0]*vaux[1]+box[2,0]*vaux[2]
        vector[1]=                 box[1,1]*vaux[1]+box[2,1]*vaux[2]
        vector[2]=                                  box[2,2]*vaux[2]

    pass

@nb.njit(nb.void(nb.float64[:],
                 nb.float64[:,:],
                 nb.optional(nb.float64[:,:]),
                 nb.optional(nb.boolean)
                 )
        )
def mic_vector(vector, box, inv_box, orthogonal):

    if orthogonal is None:
        orthogonal = box_is_orthogonal_single_structure(box)

    if orthogonal:

        vector[0]=vector[0]-box[0,0]*round(vector[0]/box[0,0])
        vector[1]=vector[1]-box[1,1]*round(vector[1]/box[1,1])
        vector[2]=vector[2]-box[2,2]*round(vector[2]/box[2,2])

    else:

        vaux = np.empty((3), dtype=float)

        if inv_box is None:
            inv_box=inverse_matrix_3x3(box)

        vaux[0]=inv_box[0,0]*vector[0]+inv_box[1,0]*vector[1]+inv_box[2,0]*vector[2]
        vaux[1]=                       inv_box[1,1]*vector[1]+inv_box[2,1]*vector[2]
        vaux[2]=                                              inv_box[2,2]*vector[2]
        vaux[0]=vaux[0]-round(vaux[0])
        vaux[1]=vaux[1]-round(vaux[1])
        vaux[2]=vaux[2]-round(vaux[2])
        vector[0]=box[0,0]*vaux[0]+box[1,0]*vaux[1]+box[2,0]*vaux[2]
        vector[1]=                 box[1,1]*vaux[1]+box[2,1]*vaux[2]
        vector[2]=                                  box[2,2]*vaux[2]

        vmin=vector
        dmin=(vmin[0]*vmin[0]+vmin[1]*vmin[1]+vmin[2]*vmin[2])

        for ii in [-1,0,1]:
            vaux=vector+ii*box[0,:]
            for jj in [-1,0,1]:
                vaux2=vaux+jj*box[1,:]
                for kk in [-1,0,1]:
                    vaux3=vaux2[:]+kk*box[2,:]
                    d=(vaux3[0]*vaux3[0]+vaux3[1]*vaux3[1]+vaux3[2]*vaux3[2])
                    if dmin>d:
                        vmin=vaux3
                        dmin=d

        vector=vmin

    pass

@nb.njit(nb.void(nb.float64[:,:,:],
                 nb.float64[:,:,:],
                 nb.float64[:,:,:],
                 )
        )
def wrap_pbc(coordinates, centers, box):

    orthogonal = box_is_orthogonal(box)

    n_frames=coordinates.shape[0]
    n_atoms=coordinates.shape[1]

    for ii in range(n_frames):
        tmp_inv=inverse_matrix_3x3(box[ii,:,:])
        center=centers[ii,0,:]
        for jj in range(n_atoms):
            aux=coorsdinates[ii,jj,:]-center
            pbc_single_structure(aux, box[ii,:,:], tmp_inv, orthogonal)
            coordinates[ii,jj,:]=center+aux

    pass

@nb.njit(nb.void(nb.float64[:,:,:],
                 nb.float64[:,:,:],
                 nb.float64[:,:,:],
                 )
        )
def wrap_mic(coordinates, centers, box):

    orthogonal = box_is_orthogonal(box)

    n_structures, n_atoms=coordinates.shape[:-1]

    for ii in range(n_structures):
        tmp_inv=inverse_matrix_3x3(box[ii,:,:])
        center=centers[ii,0,:]
        for jj in range(n_atoms):
            aux=coordinates[ii,jj,:]-center
            mic_single_structure(aux, box[ii,:,:], tmp_inv, orthogonal)
            coors[ii,jj,:]=center+aux

    pass


@nb.njit(nb.void(nb.float64[:,:,:],
                 nb.float64[:,:,:],
                )
        )
def unwrap(coordinates, box):

    orthogonal = box_is_orthogonal(box)

    n_structures, n_atoms=coordinates.shape[:-1]

    for ii in range(n_structures-1):
        tmp_inv=inverse_matrix_3x3(box[ii,:,:])
        for jj in range(n_atoms):
            delta = coordinates[ii+1,jj,:]-coordinates[ii,jj,:]
            mic_single_structure(delta, box[ii,:,:], tmp_inv, orthogonal)
            coordinates[ii+1,jj,:]=coordinates[ii,jj,:]+delta

    pass

