import math
import numpy as np
import numba as nb

@nb.jit(nb.float64[:,:](nb.float64[:,:]), nopython=True)
def invbox2d(box):

    invbox = np.zeros(box.shape, dtype=nb.float64)

    invbox[0,0]=1.0/box[0,0]
    invbox[1,1]=1.0/box[1,1]
    invbox[2,2]=1.0/box[2,2]

    invbox[1,0]=-box[1,0]/(box[0,0]*box[1,1])
    invbox[2,0]=(box[1,0]*box[2,1]-box[2,0]*box[1,1])/(box[0,0]*box[1,1]*box[2,2])
    invbox[2,1]=-box[2,1]/(box[1,1]*box[2,2])

    return invbox

@nb.jit(nb.float64[:,:](nb.float64[:,:,:]), nopython=True)
def length_edges_box(box):

    lengths = np.zeros((box.shape[0],3), dtype=nb.float64)
    lengths[:,0] = np.sqrt(box[:,0,0]**2 + box[:,0,1]**2 + box[:,0,2]**2)
    lengths[:,1] = np.sqrt(box[:,1,0]**2 + box[:,1,1]**2 + box[:,1,2]**2)
    lengths[:,2] = np.sqrt(box[:,2,0]**2 + box[:,2,1]**2 + box[:,2,2]**2)

    return lengths

@nb.jit(nb.float64[:,:](nb.float64[:,:,:]), nopython=True)
def angles_box(box):

    n_frames = box.shape[0]
    angles = np.zeros((n_frames,3), dtype=nb.float64)

    for ii in range(n_frames):

        v0 = box[ii,0,:]
        v1 = box[ii,1,:]
        v2 = box[ii,2,:]
        x = np.linalg.norm(v0)
        y = np.linalg.norm(v1)
        z = np.linalg.norm(v2)
        a=math.acos(np.dot(v1,v2)/(y*z)) # alpha: v2 and v3
        b=math.acos(np.dot(v2,v0)/(x*z)) # beta: v1 and v3
        c=math.acos(np.dot(v1,v0)/(x*y)) # gamma: v1 and v2
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

def wrap_pbc(coors, centers, box, ortho):

    raise NotImplementedError()

def wrap_mic(coors, centers, box, ortho):

    raise NotImplementedError()

def unwrap(coors, box, ortho):

    raise NotImplementedError()

