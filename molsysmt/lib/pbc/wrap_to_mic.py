import numba as nb
import numpy as np
from .box_is_orthogonal import box_is_orthogonal_single_structure
from ..math import inverse_matrix_3x3, dot_product
from ..make_numba_signature import make_numba_signature

arguments=[nb.float64[:], # vector [3]
           nb.float64[:,:], # box [3,3]
           [nb.float64[:,:], None], # inv_box [3,3]
           [nb.boolean, None], # orthogonal
          ]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments, output), cache=True)
def wrap_to_mic_vector_single_structure(vector, box, inv_box, orthogonal):

    output = np.empty((3), dtype=np.float)

    if inv_box is None:
        inv_box = inverse_matrix_3x3(box)

    if orthogonal is None:
        orthogonal = box_is_orthogonal_single_structure(box)

    if orthogonal:

        output[0]=vector[0]-box[0,0]*round(vector[0]/box[0,0])
        output[1]=vector[1]-box[1,1]*round(vector[1]/box[1,1])
        output[2]=vector[2]-box[2,2]*round(vector[2]/box[2,2])

    else:

        vaux = np.empty((3), dtype=float)

        vaux[0]=inv_box[0,0]*vector[0]+inv_box[1,0]*vector[1]+inv_box[2,0]*vector[2]
        vaux[1]=                       inv_box[1,1]*vector[1]+inv_box[2,1]*vector[2]
        vaux[2]=                                              inv_box[2,2]*vector[2]
        vaux[0]=vaux[0]-round(vaux[0])
        vaux[1]=vaux[1]-round(vaux[1])
        vaux[2]=vaux[2]-round(vaux[2])
        output[0]=box[0,0]*vaux[0]+box[1,0]*vaux[1]+box[2,0]*vaux[2]
        output[1]=                 box[1,1]*vaux[1]+box[2,1]*vaux[2]
        output[2]=                                  box[2,2]*vaux[2]
        dmin=dot_product(output,output)
        for ii in [-1,0,1]:
            vaux=vector+ii*box[0,:]
            for jj in [-1,0,1]:
                vaux2=vaux+jj*box[1,:]
                for kk in [-1,0,1]:
                    vaux3=vaux2[:]+kk*box[2,:]
                    dd=dot_product(vaux3,vaux3)
                    if dmin>dd:
                        output=vaux3
                        dmin=dd

    return output


arguments=[nb.float64[:,:], # coordinates
           nb.float64[:,:], # box
           [nb.float64[:], None], # center
           nb.boolean, # center_at_origin
          ]
output=None
@nb.njit(make_numba_signature(arguments, output), cache=True)
def wrap_to_mic_single_structure(coordinates, box, center, center_at_origin):

    n_atoms = coordinates.shape[0]

    orthogonal = box_is_orthogonal_single_structure(box[:,:])
    inv_box = inverse_matrix_3x3(box)

    if center is None:

        for ii in range(n_atoms):
            coordinates[ii,:] = wrap_to_mic_vector_single_structure(coordinates[ii,:], box, inv_box,
                    orthogonal)

    else:

        for ii in range(n_atoms):
            tmp_vect = coordinates[ii,:]-center
            tmp_vect = wrap_to_mic_vector_single_structure(tmp_vect, box, inv_box,
                    orthogonal)
            if not center_at_origin:
                tmp_vect=tmp_vect+center
            coordinates[ii,:]=tmp_vect

    pass


arguments=[nb.float64[:,:,:], # coordinates
           nb.float64[:,:,:], # box
           [nb.float64[:,:], None], # center
           nb.boolean, # center_at_origin
          ]
output=None
@nb.njit(make_numba_signature(arguments, output), cache=True)
def wrap_to_mic(coordinates, box, center, center_at_origin):

    n_structures, n_atoms = coordinates.shape[:2]


    if center is None:

        for ii in range(n_structures):
            tmp_box = box[ii,:,:]
            orthogonal = box_is_orthogonal_single_structure(tmp_box)
            inv_box = inverse_matrix_3x3(tmp_box)
            for jj in range(n_atoms):
                coordinates[ii,jj,:] = wrap_to_mic_vector_single_structure(coordinates[ii,jj,:],
                        tmp_box, inv_box, orthogonal)

    else:

        single_structure_center = (center.shape[0]==1)

        aa=0
        for ii in range(n_structures):
            tmp_box = box[ii,:,:]
            orthogonal = box_is_orthogonal_single_structure(tmp_box)
            inv_box = inverse_matrix_3x3(tmp_box)
            tmp_center = center[aa,:]
            for jj in range(n_atoms):
                tmp_vect = coordinates[ii,jj,:]-tmp_center
                tmp_vect = wrap_to_mic_vector_single_structure(tmp_vect, tmp_box, inv_box, orthogonal)
                if not center_at_origin:
                    tmp_vect=tmp_vect+tmp_center
                coordinates[ii,jj,:]=tmp_vect
            if not single_structure_center:
                aa+=1
    pass



