import numba as nb
import numpy as np
import math
from ..make_numba_signature import make_numba_signature

arguments=[nb.float64[:,:], # lengths
           nb.float64[:,:]  # angles
          ]
output=nb.float64[:,:,:] # box
@nb.njit(make_numba_signature(arguments, output))
def get_box_from_lengths_and_angles(lengths, angles):

    n_structures = lengths.shape[0]

    box = np.zeros((n_structures,3,3), dtype=nb.float64)

    for ii in range(n_structures):

        alpha=angles[ii,0]
        beta=angles[ii,1]
        gamm=angles[ii,2]
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

