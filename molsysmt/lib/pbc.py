import numba as nb
import numpy as np
import math
from .math import inverse_matrix_3x3, norm_vector, dot_product


@nb.njit(nb.float64[:,:](nb.float64[:,:,:]))
def length_edges_box(box):

    n_frames = box.shape[0]

    lengths = np.zeros((n_frames,3), dtype=nb.float64)

    for ii in range(n_frames):
        lengths[:,0] = norm_vector(box[ii,0,:])
        lengths[:,1] = norm_vector(box[ii,1,:])
        lengths[:,2] = norm_vector(box[ii,2,:])

    return lengths


@nb.njit(nb.float64[:,:](nb.float64[:,:,:]))
def angles_box(box):

    n_frames = box.shape[0]
    angles = np.zeros((n_frames,3), dtype=nb.float64)

    for ii in range(n_frames):

        v0 = box[ii,0,:]
        v1 = box[ii,1,:]
        v2 = box[ii,2,:]
        x = norm_vector(v0)
        y = norm_vector(v1)
        z = norm_vector(v2)
        a=math.acos(dot_product(v1,v2)/(y*z)) # alpha: v2 and v3
        b=math.acos(dot_product(v2,v0)/(x*z)) # beta: v1 and v3
        c=math.acos(dot_product(v1,v0)/(x*y)) # gamma: v1 and v2
        angles[ii,0] = math.degrees(a)
        angles[ii,1] = math.degrees(b)
        angles[ii,2] = math.degrees(c)

    return angles


@nb.njit(nb.float64[:,:,:](nb.float64[:,:],
                           nb.float64[:,:],
                           )
        )
def lengths_and_angles_to_box(lengths, angles):

    n_frames = lengths.shape[0]

    box = np.zeros((n_frames,3,3), dtype=nb.float64)

    for ii in range(n_frames):

        alpha=math.radians(angles[ii,0])
        beta=math.radians(angles[ii,1])
        gamm=math.radians(angles[ii,2])
        x=lengths[ii,0]
        y=lengths[ii,1]
        z=lengths[ii,2]
        box[ii,0,0]=x
        box[ii,1,0]=y*math.cos(gamm)
        box[ii,1,1]=y*math.sin(gamm)
        box[ii,2,0]=z*math.cos(beta)
        box[ii,2,1]=z*(math.cos(alpha)-math.cos(beta)*math.cos(gamm))/math.sin(gamm)
        box[ii,2,2]=math.sqrt(z*z-box[ii,2,0]**2-box[ii,2,1]**2)

    return box


@nb.njit(nb.boolean(nb.float64[:,:,:]))
def box_is_orthogonal(box):

    p01=dot_product(box[0,0,:], box[0,1,:])
    p02=dot_product(box[0,0,:], box[0,2,:])
    p12=dot_product(box[0,1,:], box[0,2,:])

    orthogonal = np.allclose([p01,p02,12],[0.0,0.0,0.0])

    return orthogonal

@nb.njit(nb.boolean(nb.float64[:,:]))
def box_is_orthogonal_single_structure(box):

    p01=dot_product(box[0,:], box[1,:])
    p02=dot_product(box[0,:], box[2,:])
    p12=dot_product(box[1,:], box[2,:])

    orthogonal = np.allclose([p01,p02,12],[0.0,0.0,0.0])

    return orthogonal

@nb.njit(nb.void(nb.float64[:],
                 nb.float64[:,:],
                 nb.optional(nb.float64[:,:]),
                 nb.optional(nb.boolean),
                 )
        )
def pbc_single_structure(vector, box, inv_box, orthogonal):

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
def mic_single_structure(vector, box, inv_box, orthogonal):

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

