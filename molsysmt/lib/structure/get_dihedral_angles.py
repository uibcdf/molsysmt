import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature
from ..math import dihedral_angle


arguments=[nb.float64[:,:], # coordinates
           nb.int64[:,:], # quartets [n_atoms,4]
          ]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_dihedral_angles_single_structure(coordinates, quartets):

    n_angles = quartets.shape[0]

    angles = np.empty((n_angles), dtype=np.float64)

    for ii in range(n_angles):

        at0=quartets[ii,0]
        at1=quartets[ii,1]
        at2=quartets[ii,2]
        at3=quartets[ii,3]

        vect0=coordinates[at1]-coordinates[at0]
        vect1=coordinates[at2]-coordinates[at1]
        vect2=coordinates[at3]-coordinates[at2]

        angles[ii]=dihedral_angle(vect0,vect1,vect2)

    return angles

arguments=[nb.float64[:,:,:], # coordinates
           nb.int64[:,:], # quartets [n_atoms,4]
          ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_dihedral_angles(coordinates, quartets):

    n_structures = coordinates.shape[0]
    n_angles = quartets.shape[0]

    angles = np.empty((n_structures, n_angles), dtype=np.float64)

    for ii in range(n_structures):

        for jj in range(n_angles):

            at0=quartets[jj,0]
            at1=quartets[jj,1]
            at2=quartets[jj,2]
            at3=quartets[jj,3]

            vect0=coordinates[ii,at1]-coordinates[ii,at0]
            vect1=coordinates[ii,at2]-coordinates[ii,at1]
            vect2=coordinates[ii,at3]-coordinates[ii,at2]

            angles[ii,jj]=dihedral_angle(vect0,vect1,vect2)

    return angles

