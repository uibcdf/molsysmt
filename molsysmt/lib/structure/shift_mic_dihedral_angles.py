import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature
from ..pbc.wrap_to_mic import wrap_to_mic_vector_single_structure
from ..pbc.box_is_orthogonal import box_is_orthogonal_single_structure
from ..math import inverse_matrix_3x3, normalize_vector, rodrigues_rotation


arguments=[nb.float64[:,:], # coordinates
           nb.float64[:,:], # box
           nb.float64[:], # angles [n_angs]
           nb.int64[:,:], # quartets [n_angs,4]
           nb.boolean[:,:], # blocks [n_angs,n_atoms]
          ]
output=None
@nb.njit(make_numba_signature(arguments, output), cache=True)
def shift_mic_dihedral_angles_single_structure(coordinates, box, angles, quartets, blocks):

    inv_box = inverse_matrix_3x3(box)
    orthogonal = box_is_orthogonal_single_structure(box)

    n_angles = angles.shape[0]
    n_atoms = coordinates.shape[0]

    for ii in range(n_angles):

        at1=quartets[ii,1]
        at2=quartets[ii,2]

        coordinates_at2=coordinates[at2]

        vect1=coordinates_at2-coordinates[at1]

        vect1=wrap_to_mic_vector_single_structure(vect1, box, inv_box, orthogonal)

        u_vect = normalize_vector(vect1)
        shift_ang=angles[ii]

        for jj in range(n_atoms):
            if blocks[ii,jj]:
                vect_aux = coordinates[jj,:]-coordinates_at2
                vect_aux = wrap_to_mic_vector_single_structure(vect_aux, box, inv_box, orthogonal)
                rodrigues_rotation(vect_aux, u_vect, shift_ang)
                vect_aux = wrap_to_mic_vector_single_structure(vect_aux, box, inv_box, orthogonal)
                coordinates[jj,:]=coordinates_at2+vect_aux

    pass


arguments=[nb.float64[:,:,:], # coordinates
           nb.float64[:,:,:], # box
           nb.float64[:,:], # angles [n_angs]
           nb.int64[:,:], # quartets [n_angs,4]
           nb.boolean[:,:], # blocks [n_angs,n_atoms]
           nb.int64[:], # structure_indices
          ]
output=None
@nb.njit(make_numba_signature(arguments, output), cache=True)
def shift_mic_dihedral_angles(coordinates, box, angles, quartets, blocks, structure_indices):

    n_angles = angles.shape[0]
    n_atoms = coordinates.shape[1]

    for ii in structure_indices:

        tmp_box = box[ii,:,:]
        inv_box = inverse_matrix_3x3(tmp_box)
        orthogonal = box_is_orthogonal_single_structure(tmp_box)

        for aa in range(n_angles):

            at1=quartets[aa,1]
            at2=quartets[aa,2]

            coordinates_at2=coordinates[ii,at2]

            vect1=coordinates_at2-coordinates[ii,at1]

            vect1=wrap_to_mic_vector_single_structure(vect1, tmp_box, inv_box, orthogonal)

            u_vect = normalize_vector(vect1)
            shift_ang=angles[ii,aa]

            for jj in range(n_atoms):
                if blocks[aa,jj]:
                    vect_aux = coordinates[ii,jj,:]-coordinates_at2
                    vect_aux = wrap_to_mic_vector_single_structure(vect_aux, tmp_box, inv_box, orthogonal)
                    rodrigues_rotation(vect_aux, u_vect, shift_ang)
                    vect_aux = wrap_to_mic_vector_single_structure(vect_aux, tmp_box, inv_box, orthogonal)
                    coordinates[ii,jj,:]=coordinates_at2+vect_aux

    pass

