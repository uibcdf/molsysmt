import math
import numpy as np
import numba as nb
from .math import inverse_matrix_3x3, norm_vector, dot_product
from .pbc import pbc, mic

@nb.jit(nb.float64[:,:](nb.float64[:,:,:]), nopython=True)
def length_edges_box(box):

    n_frames = box.shape[0]

    lengths = np.zeros((n_frames,3), dtype=nb.float64)

    for ii in range(n_frames):
        lengths[:,0] = norm_vector(box[ii,0,:])
        lengths[:,1] = norm_vector(box[ii,1,:])
        lengths[:,2] = norm_vector(box[ii,2,:])

    return lengths

@nb.jit(nb.float64[:,:](nb.float64[:,:,:]), nopython=True)
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

@nb.jit(nb.float64[:,:,:](nb.float64[:,:], nb.float64[:,:]), nopython=True)
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

@nb.jit(void(nb.float64[:,:,:], nb.float64[:,:,:], nb.float64[:,:,:], nb.boolean), nopython=True)
def wrap_pbc(coors, centers, box, ortho):

    n_frames=coors.shape[0]
    n_atoms=coors.shape[1]

    for ii in range(n_frames):
        tmp_inv=inverse_matrix_3x3(box[ii,:,:]):
            for jj in range(n_atoms):
                aux=coors[ii,jj,:]-center[ii,:]
                pbc(aux, box[ii,:,:], tmp_inv, ortho)
                coors[ii,jj,:]=center+aux

    pass

@nb.jit(void(nb.float64[:,:,:], nb.float64[:,:,:], nb.float64[:,:,:], nb.boolean), nopython=True)
def wrap_mic(coors, centers, box, ortho):

    n_frames=coors.shape[0]
    n_atoms=coors.shape[1]

    for ii in range(n_frames):
        tmp_inv=inverse_matrix_3x3(box[ii,:,:]):
            for jj in range(n_atoms):
                aux=coors[ii,jj,:]-center[ii,:]
                mic(aux, box[ii,:,:], tmp_inv, ortho)
                coors[ii,jj,:]=center+aux

    pass

@nb.jit(void(nb.float64[:,:,:], nb.float64[:,:,:], nb.boolean), nopython=True)
def unwrap(coors, box, ortho):

    n_frames=coors.shape[0]
    n_atoms=coors.shape[1]

    for ii in range(n_frames-1):
        tmp_inv=inverse_matrix_3x3(box[ii,:,:]):
            for jj in range(n_atoms):
                delta = coors[ii+1,jj,:]-coors[ii,jj,:]
                mic(delta, box[ii,:,:], tmp_inv, ortho)
                coors[ii+1,jj,:]=coors[ii,jj,:]+delta

    pass

