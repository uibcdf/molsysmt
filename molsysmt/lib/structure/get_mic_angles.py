import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature
from ..pbc.wrap_to_mic import wrap_to_mic_vector_single_structure
from ..pbc.box_is_orthogonal import box_is_orthogonal_single_structure
from ..math import inverse_matrix_3x3, angle


arguments=[nb.float64[:,:], # coordinates
           nb.float64[:,:], # box
           nb.int64[:,:], # triplets [n_atoms,3]
          ]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_angles_single_structure(coordinates, box, triplets):

    inv_box = inverse_matrix_3x3(box)
    orthogonal = box_is_orthogonal_single_structure(box)

    n_angles = triplets.shape[0]

    angles = np.empty((n_angles), dtype=np.float64)

    for ii in range(n_angles):

        at0=triplets[ii,0]
        at1=triplets[ii,1]
        at2=triplets[ii,2]

        vect0=coordinates[at1]-coordinates[at0]
        vect1=coordinates[at2]-coordinates[at1]

        vect0=wrap_to_mic_vector_single_structure(vect0, box, inv_box, orthogonal)
        vect1=wrap_to_mic_vector_single_structure(vect1, box, inv_box, orthogonal)

        angles[ii]=angle(vect0,vect1)

    return angles

arguments=[nb.float64[:,:,:], # coordinates
           nb.float64[:,:,:], # box
           nb.int64[:,:], # triplets [n_atoms,3]
          ]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def get_mic_angles(coordinates, box, triplets):

    n_structures = coordinates.shape[0]
    n_angles = triplets.shape[0]

    angles = np.empty((n_structures, n_angles), dtype=np.float64)

    for ii in range(n_structures):

        tmp_box = box[ii,:,:]
        inv_box = inverse_matrix_3x3(tmp_box)
        orthogonal = box_is_orthogonal_single_structure(tmp_box)

        for jj in range(n_angles):

            at0=triplets[jj,0]
            at1=triplets[jj,1]
            at2=triplets[jj,2]

            vect0=coordinates[ii,at1]-coordinates[ii,at0]
            vect1=coordinates[ii,at2]-coordinates[ii,at1]

            vect0=wrap_to_mic_vector_single_structure(vect0, tmp_box, inv_box, orthogonal)
            vect1=wrap_to_mic_vector_single_structure(vect1, tmp_box, inv_box, orthogonal)

            angles[ii,jj]=angle(vect0,vect1)

    return angles

