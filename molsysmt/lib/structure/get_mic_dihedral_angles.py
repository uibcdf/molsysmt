import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature
from ..pbc.wrap_to_mic import wrap_to_mic_vector_single_structure
from ..pbc.box_is_orthogonal import box_is_orthogonal_single_structure
from ..math import inverse_matrix_3x3, dihedral_angle


arguments=[nb.float64[:,:], # coordinates
           nb.float64[:,:], # box
           nb.int64[:,:], # quartets [n_atoms,4]
          ]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_dihedral_angles_single_structure(coordinates, box, quartets):

    inv_box = inverse_matrix_3x3(box)
    orthogonal = box_is_orthogonal_single_structure(box)

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

        vect0=wrap_to_mic_vector_single_structure(vect0, box, inv_box, orthogonal)
        vect1=wrap_to_mic_vector_single_structure(vect1, box, inv_box, orthogonal)
        vect2=wrap_to_mic_vector_single_structure(vect2, box, inv_box, orthogonal)

        angles[ii]=dihedral_angle(vect0,vect1,vect2)

    return angles

arguments=[nb.float64[:,:,:], # coordinates
           nb.float64[:,:,:], # box
           nb.int64[:,:], # quartets [n_atoms,4]
          ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_dihedral_angles(coordinates, box, quartets):

    n_structures = coordinates.shape[0]
    n_angles = quartets.shape[0]

    angles = np.empty((n_structures, n_angles), dtype=np.float64)

    for ii in range(n_structures):

        tmp_box = box[ii,:,:]
        inv_box = inverse_matrix_3x3(tmp_box)
        orthogonal = box_is_orthogonal_single_structure(tmp_box)

        for jj in range(n_angles):

            at0=quartets[jj,0]
            at1=quartets[jj,1]
            at2=quartets[jj,2]
            at3=quartets[jj,3]

            vect0=coordinates[ii,at1]-coordinates[ii,at0]
            vect1=coordinates[ii,at2]-coordinates[ii,at1]
            vect2=coordinates[ii,at3]-coordinates[ii,at2]

            vect0=wrap_to_mic_vector_single_structure(vect0, tmp_box, inv_box, orthogonal)
            vect1=wrap_to_mic_vector_single_structure(vect1, tmp_box, inv_box, orthogonal)
            vect2=wrap_to_mic_vector_single_structure(vect2, tmp_box, inv_box, orthogonal)

            angles[ii,jj]=dihedral_angle(vect0,vect1,vect2)

    return angles

