import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature
from ..math import angle


arguments=[nb.float64[:,:], # coordinates
           nb.int64[:,:], # triplets [n_atoms,3]
          ]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_angles_single_structure(coordinates, triplets):

    n_angles = triplets.shape[0]

    angles = np.empty((n_angles), dtype=np.float64)

    for ii in range(n_angles):

        at0=triplets[ii,0]
        at1=triplets[ii,1]
        at2=triplets[ii,2]

        vect0=coordinates[at1]-coordinates[at0]
        vect1=coordinates[at2]-coordinates[at1]

        angles[ii]=angle(vect0,vect1)

    return angles

arguments=[nb.float64[:,:,:], # coordinates
           nb.int64[:,:], # triplets [n_atoms,3]
          ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_angles(coordinates, triplets):

    n_structures = coordinates.shape[0]
    n_angles = triplets.shape[0]

    angles = np.empty((n_structures, n_angles), dtype=np.float64)

    for ii in range(n_structures):

        for jj in range(n_angles):

            at0=triplets[jj,0]
            at1=triplets[jj,1]
            at2=triplets[jj,2]

            vect0=coordinates[ii,at1]-coordinates[ii,at0]
            vect1=coordinates[ii,at2]-coordinates[ii,at1]

            angles[ii,jj]=angle(vect0,vect1)

    return angles

