import numba as nb
import numpy as np
import math
from ..math import inverse_matrix_3x3
from ..make_numba_signature import make_numba_signature
from .box_is_orthogonal import box_is_orthogonal_single_structure

arguments=[nb.float64[:,:,:], # coordinates
           nb.float64[:,:,:], # box
           [nb.float64[:,:,:], None], # center
           [nb.boolean, None], # center_at_origin
           [nb.float64[:,:,:], None], # inv_box
           [nb.boolean, None], # orthogonal
          ]
output=None
@nb.njit(make_numba_signature(arguments, output), cache=True)
def wrap_to_pbc(coordinates, box, center=None, center_at_origin=None, inv_box=None, orthogonal=None):

    n_structures, n_atoms = coordinates.shape[:-1]

    if center is not None:
        with_center = True
        if center_at_origin is None:
            center_at_origin = False

    with_inv_box = False

    if inv_box is not None:
        with_inv_box = True

    if orthogonal is None:
        orthogonal = box_is_orthogonal_single_structure(box[0,:,:])

    if orthogonal:

        if center is not None:

            for ii in range(n_structures):
                tmp_box=np.diag(box[ii,:,:])
                tmp_center=center[ii,0,:]
                for jj in range(n_atoms):
                    tmp_coors=coordinates[ii,jj,:]-tmp_center[:]
                    tmp_coors[0]=tmp_coors[0]-tmp_box[0]*round(tmp_coors[0]/tmp_box[0])
                    tmp_coors[1]=tmp_coors[1]-tmp_box[1]*round(tmp_coors[1]/tmp_box[1])
                    tmp_coors[2]=tmp_coors[2]-tmp_box[2]*round(tmp_coors[2]/tmp_box[2])
                    if not center_at_origin:
                        tmp_coors=tmp_coors+tmp_center
                    coordinates[ii,jj,:]=tmp_coors[:]

        else:

            for ii in range(n_structures):
                tmp_box=np.diag(box[ii,:,:])
                for jj in range(n_atoms):
                    tmp_coors=coordinates[ii,jj,:]
                    tmp_coors[0]=tmp_coors[0]-tmp_box[0]*round(tmp_coors[0]/tmp_box[0])
                    tmp_coors[1]=tmp_coors[1]-tmp_box[1]*round(tmp_coors[1]/tmp_box[1])
                    tmp_coors[2]=tmp_coors[2]-tmp_box[2]*round(tmp_coors[2]/tmp_box[2])
                    coordinates[ii,jj,:]=tmp_coors[:]
    else:

        vaux = np.empty((3), dtype=float)

        if center is not None:

            for ii in range(n_structures):
                tmp_box=box[ii,:,:]
                tmp_center=center[ii,0,:]
                if inv_box is None:
                    tmp_inv_box=inverse_matrix_3x3(tmp_box)
                else:
                    tmp_inv_box=inv_box[ii,:,:]
                for jj in range(n_atoms):
                    tmp_coors=coordinates[ii,jj,:]-tmp_center[:]
                    vaux[0]=tmp_inv_box[0,0]*tmp_coors[0]+tmp_inv_box[1,0]*tmp_coors[1]+tmp_inv_box[2,0]*tmp_coors[2]
                    vaux[1]=                              tmp_inv_box[1,1]*tmp_coors[1]+tmp_inv_box[2,1]*tmp_coors[2]
                    vaux[2]=                                                            tmp_inv_box[2,2]*tmp_coors[2]
                    vaux[0]=vaux[0]-round(vaux[0])
                    vaux[1]=vaux[1]-round(vaux[1])
                    vaux[2]=vaux[2]-round(vaux[2])
                    tmp_coors[0]=tmp_box[0,0]*vaux[0]+tmp_box[1,0]*vaux[1]+tmp_box[2,0]*vaux[2]
                    tmp_coors[1]=                     tmp_box[1,1]*vaux[1]+tmp_box[2,1]*vaux[2]
                    tmp_coors[2]=                                          tmp_box[2,2]*vaux[2]
                    if not center_at_origin:
                        tmp_coors=tmp_coors+tmp_center
                    coordinates[ii,jj,:]=tmp_coors[:]

        else:

            for ii in range(n_structures):
                tmp_box=box[ii,:,:]
                if inv_box is None:
                    tmp_inv_box=inverse_matrix_3x3(tmp_box)
                else:
                    tmp_inv_box=inv_box[ii,:,:]
                for jj in range(n_atoms):
                    tmp_coors=coordinates[ii,jj,:]
                    vaux[0]=tmp_inv_box[0,0]*tmp_coors[0]+tmp_inv_box[1,0]*tmp_coors[1]+tmp_inv_box[2,0]*tmp_coors[2]
                    vaux[1]=                              tmp_inv_box[1,1]*tmp_coors[1]+tmp_inv_box[2,1]*tmp_coors[2]
                    vaux[2]=                                                            tmp_inv_box[2,2]*tmp_coors[2]
                    vaux[0]=vaux[0]-round(vaux[0])
                    vaux[1]=vaux[1]-round(vaux[1])
                    vaux[2]=vaux[2]-round(vaux[2])
                    tmp_coors[0]=tmp_box[0,0]*vaux[0]+tmp_box[1,0]*vaux[1]+tmp_box[2,0]*vaux[2]
                    tmp_coors[1]=                     tmp_box[1,1]*vaux[1]+tmp_box[2,1]*vaux[2]
                    tmp_coors[2]=                                          tmp_box[2,2]*vaux[2]
                    coordinates[ii,jj,:]=tmp_coors[:]

    pass

