import numpy as np
import numba as nb
from ..math import dot_product, quaternion_to_rotation_matrix
from .rotate_and_translate import rotate_and_translate_single_structure
import math
from ..make_numba_signature import make_numba_signature


arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    nb.float64[:,:], # reference_coordinates: [n_atoms, 3]
]
output=None
@nb.njit(make_numba_signature(arguments,output), cache=True)
def least_rmsd_fit_single_structure(coordinates, reference_coordinates):

    n_atoms = coordinates.shape[0]

    center_ref=np.empty((3), dtype=nb.float64)
    center=np.empty((3), dtype=nb.float64)

    x=np.zeros((n_atoms,3), dtype=nb.float64)
    y=np.zeros((n_atoms,3), dtype=nb.float64)

    R=np.zeros((3,3), dtype=nb.float64)
    F=np.zeros((4,4), dtype=nb.float64)

    w=np.ones((n_atoms), dtype=nb.float64) # without weights

    # reference coordinates

    for ii in range(n_atoms):
        x[ii,:]=w[ii]*reference_coordinates[ii,:]

    x_norm=0.0
    for ii in range(3):
        center_ref[ii]=np.sum(x[:,ii])/n_atoms
        x[:,ii]=x[:,ii]-center_ref[ii]
        x_norm=x_norm+dot_product(x[:,ii],x[:,ii])

    # coordinates

    for ii in range(n_atoms):
        y[ii,:]=w[ii]*coordinates[ii,:]

    y_norm=0.0
    for ii in range(3):
        center[ii]=np.sum(y[:,ii])/n_atoms
        y[:,ii]=y[:,ii]-center[ii]
        y_norm=y_norm+dot_product(y[:,ii], y[:,ii])

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
    center = np.expand_dims(center,0)
    U = np.expand_dims(U,0)
    center_ref = np.expand_dims(center_ref,0)
    #rotate_and_translate_single_structure(coordinates, center, U, center_ref, atom_indices_to_move)

    pass


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.float64[:,:,:], # reference_coordinates: [n_ref_structures, n_ref_atoms, 3]
    nb.int64[:], # atom_indices: [n_atoms]
    nb.int64[:], # atom_indices_to_move: [n_atoms]
    nb.int64[:], # structure_indices: [n_structures]
    nb.int64[:], # reference_atom_indices: [n_atoms]
    nb.int64[:], # reference_structure_indices: [n_structures]
]
output=None
@nb.njit(make_numba_signature(arguments,output), cache=True)
def least_rmsd_fit(coordinates, reference_coordinates,
                   atom_indices, atom_indices_to_move, structure_indices,
                   reference_atom_indices, reference_structure_indices):

    n_structures = structure_indices.shape[0]
    n_atoms = atom_indices.shape[0]

    n_reference_structures = reference_structure_indices.shape[0]

    single_reference_structure = (reference_structure_indices==1)

    w=np.ones((n_atoms), dtype=nb.float64)

    center_ref=np.empty((3), dtype=nb.float64)
    center=np.empty((3), dtype=nb.float64)

    x=np.zeros((n_atoms,3), dtype=nb.float64)
    y=np.zeros((n_atoms,3), dtype=nb.float64)

    R=np.zeros((3,3), dtype=nb.float64)
    F=np.zeros((4,4), dtype=nb.float64)

    bb = 0
    ii_ref = 0
    flag=True
    for ii in structure_indices:

        # reference coordinates
        if flag==True:

            x_norm=0.0
            x[:,:]=0.0

            aa=0
            for jj in reference_atom_indices:
                x[aa,:]=w[aa]*reference_coordinates[ii_ref,jj,:]
                aa+=1

            for jj in range(3):
                center_ref[jj]=np.sum(x[:,jj])/n_atoms
                x[:,jj]=x[:,jj]-center_ref[jj]
                x_norm=x_norm+dot_product(x[:,jj],x[:,jj])

            if single_reference_structure==1:
                flag=False
            else:
                ii_ref+=1

        # coordinates

        y_norm=0.0
        y[:,:]=0.0

        aa=0
        for jj in atom_indices:
            y[aa,:]=w[aa]*coordinates[ii,jj,:]
            aa+=1

        for jj in range(3):
            center[jj]=np.sum(x[:,jj])/n_atoms
            x[:,jj]=x[:,jj]-center[jj]
            x_norm=x_norm+dot_product(x[:,jj],x[:,jj])

        R[:,:]=0.0
        F[:,:]=0.0

        # R matrix
        for ll in range(3):
            for mm in range(3):
                R[ll,mm]=dot_product(x[:,ll], y[:,mm])

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
        rotate_and_translate_single_structure(coordinates[ii,:,:],
                                              np.expand_dims(center,0),
                                              np.expand_dims(U,0),
                                              np.expand_dims(center_ref,0),
                                              atom_indices_to_move)

    pass

