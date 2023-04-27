import numpy as np
import numba as nb
from .math import dot_product, quaternion_to_rotation_matrix,\
        rotation_and_translation_single_structure
import math
from .make_numba_signature import make_numba_signature
from itertools import repeat

arguments=[
    nb.float64[:,:,:], # coordinates
    nb.int64[:], # atom_indices
    nb.int64[:], # atom_indices_to_move
    nb.int64[:], # structure_indices
    [nb.float64[:,:,:], None], # reference_coordinates
    nb.int64[:], # reference_atom_indices
    nb.int64[:], # reference_structure_indices
]
output=None
@nb.njit(make_numba_signature(arguments,output))
def least_rmsd_fit(coordinates, atom_indices, atom_indices_to_move, structure_indices,
                   reference_coordinates, reference_atom_indices, reference_structure_indices):

    n_structures, n_atoms = coordinates.shape[:-1]

    if reference_coordinates is None:
        reference_coordinates = coordinates

    n_ref_structures, n_ref_atoms = coordinates.shape[:-1]
 

    center_ref=np.empty((3), dtype=nb.float64)
    center_2=np.empty((3), dtype=nb.float64)

    x=np.zeros((n_atoms,3), dtype=nb.float64)
    y=np.zeros((n_atoms,3), dtype=nb.float64)

    output=np.zeros((n_structure_indices), dtype=nb.float64)

    R=np.zeros((3,3), dtype=nb.float64)
    F=np.zeros((4,4), dtype=nb.float64)

    # copy and weigth coordinates

    ##weights for atoms
    w=np.ones((n_list_atoms), dtype=float)

    for ii in range(n_list_atoms):
        x[ii,:]=w[ii]*coors_ref[0,ii,:]

    # calculo baricentros, centroides y normas:
    x_norm=0.0
    for ii in range(3):
        center_ref[ii]=np.sum(x[:,ii])/n_list_atoms
        x[:,ii]=x[:,ii]-center_ref[ii]
        x_norm=x_norm+dot_product(x[:,ii],x[:,ii])

    for ll in range(n_structure_indices):

        structure_index=structure_indices[ll]

        msd=0.0
        y_norm=0.0
        center_2[:]=0.0
        y[:,:]=0.0
        R[:,:]=0.0
        F[:,:]=0.0

        # copy and weight coordinates
        for ii in range(n_list_atoms):
            mm=list_atoms[ii]
            y[ii,:]=w[ii]*coors[structure_index, mm, :]

        # baricentros, centroides y normas
        for ii in range(3):
            center_2[ii]=np.sum(y[:,ii])/n_list_atoms
            y[:,ii]=y[:,ii]-center_2[ii]
            y_norm=y_norm+dot_product(y[:,ii],y[:,ii])

        # R matrix
        for ii in range(3):
            for jj in range(3):
                R[ii,jj]=dot_product(x[:,ii], y[:,jj])

        # F matrix
        F[0,0]=R[0,0]+R[1,1]+R[2,2]
        F[1,0]=R[1,2]-R[2,1]
        F[2,0]=R[2,0]-R[0,2]
        F[3,0]=R[0,1]-R[1,0]
        F[0,1]=F[1,0]
        F[1,1]=R[0,0]-R[1,1]-R[2,2]
        F[2,1]=R[0,1]+R[1,0]
        F[3,1]=R[0,2]+R[2,0]
        F[0,2]=F[2,0]
        F[1,2]=F[2,1]
        F[2,2]=-R[0,0]+R[1,1]-R[2,2]
        F[3,2]=R[1,2]+R[2,1]
        F[0,3]=F[3,0]
        F[1,3]=F[3,1]
        F[2,3]=F[3,2]
        F[3,3]=-R[0,0]-R[1,1]+R[2,2]

        # Diagonalization with dsyevx (Lapack)
        eigvalues, eigvectors = np.linalg.eigh(F)

        # Rotation matrix
        U=quaternion_to_rotation_matrix(eigvectors[:,3])

        # New positions with translation and rotation
        rotation_and_translation_single_structure(coors[structure_index,:,:], center_2, U, center_ref)

    pass

