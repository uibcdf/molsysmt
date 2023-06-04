import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature
from ..math import normalize_vector, rodrigues_rotation


arguments=[nb.float64[:,:], # coordinates
           nb.float64[:], # angles [n_angs]
           nb.int64[:,:], # quartets [n_angs,4]
           nb.boolean[:,:], # blocks [n_angs,n_atoms]
          ]
output=None
@nb.njit(make_numba_signature(arguments, output), cache=True)
def shift_dihedral_angles_single_structure(coordinates, angles, quartets, blocks):

    n_angles = angles.shape[0]
    n_atoms = coordinates.shape[0]

    for ii in range(n_angles):

        at1=quartets[ii,1]
        at2=quartets[ii,2]

        coordinates_at2=coordinates[at2]

        vect1=coordinates_at2-coordinates[at1]

        u_vect = normalize_vector(vect1)
        shift_ang=angles[ii]

        for jj in range(n_atoms):
            if blocks[ii,jj]:
                vect_aux = coordinates[jj,:]-coordinates_at2
                rodrigues_rotation(vect_aux, u_vect, shift_ang)
                coordinates[jj,:]=coordinates_at2+vect_aux

    pass


arguments=[nb.float64[:,:,:], # coordinates
           nb.float64[:,:], # angles [n_angs]
           nb.int64[:,:], # quartets [n_angs,4]
           nb.boolean[:,:], # blocks [n_angs,n_atoms]
           nb.int64[:], # structure_indices
          ]
output=None
@nb.njit(make_numba_signature(arguments, output), cache=True)
def shift_dihedral_angles(coordinates, angles, quartets, blocks, structure_indices):

    n_angles = angles.shape[0]
    n_atoms = coordinates.shape[1]

    for ii in structure_indices:

        for aa in range(n_angles):

            at1=quartets[aa,1]
            at2=quartets[aa,2]

            coordinates_at2=coordinates[ii,at2]

            vect1=coordinates_at2-coordinates[ii,at1]

            u_vect = normalize_vector(vect1)
            shift_ang=angles[ii,aa]

            for jj in range(n_atoms):
                if blocks[aa,jj]:
                    vect_aux = coordinates[ii,jj,:]-coordinates_at2
                    rodrigues_rotation(vect_aux, u_vect, shift_ang)
                    coordinates[ii,jj,:]=coordinates_at2+vect_aux

    pass

