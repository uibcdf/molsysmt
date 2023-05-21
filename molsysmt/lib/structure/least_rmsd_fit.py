import numpy as np
import numba as nb
from ..math import dot_product, quaternion_to_rotation_matrix,\
        rotation_and_translation_single_structure
import math
from ..make_numba_signature import make_numba_signature


arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    nb.float64[:,:], # reference_coordinates: [n_atoms, 3]
    nb.int64[:], # atom_indices [n_atoms]
    nb.int64[:], # atom_indices [n_atoms]
    nb.int64[:], # atom_indices [n_atoms]
]
output=nb.float64[:,:]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def least_rmsd_fit_single_structure(coordinates, reference_coordinates, atom_indices,
                                    atom_indices_to_move, reference_atom_indices):

    n_atoms = atom_indices.shape[0]

    center_ref=np.empty((3), dtype=nb.float64)
    center=np.empty((3), dtype=nb.float64)

    x=np.zeros((n_atoms,3), dtype=nb.float64)
    y=np.zeros((n_atoms,3), dtype=nb.float64)

    R=np.zeros((3,3), dtype=nb.float64)
    F=np.zeros((4,4), dtype=nb.float64)

    w=np.ones((n_atoms), dtype=nb.float64) # without weights

    # reference coordinates

    aa=0
    for ii in reference_atom_indices:
        x[aa,:]=w[aa]*reference_coordinates[ii,:]
        aa+=1

    x_norm=0.0
    for ii in range(3):
        center_ref[ii]=np.sum(x[:,ii])/n_atoms
        x[:,ii]=x[:,ii]-center_ref[ii]
        x_norm=x_norm+dot_product(x[:,ii],x[:,ii])

    # coordinates

    aa=0
    for ii in atom_indices:
        y[aa,:]=w[aa]*coordinates[ii,:]
        aa+=1

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
    new_coordinates = rotate_and_translate_single_structure(coordinates, center, U, center_ref,
                                                            atom_indices=atom_indices_to_move)

    return new_coordinates


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

    w=np.ones((n_atoms), dtype=nb.float64)

    center_ref=np.empty((3), dtype=nb.float64)
    center=np.empty((3), dtype=nb.float64)

    x=np.zeros((n_atoms,3), dtype=nb.float64)
    y=np.zeros((n_atoms,3), dtype=nb.float64)

    R=np.zeros((3,3), dtype=nb.float64)
    F=np.zeros((4,4), dtype=nb.float64)

    flag=True
    for ll, mm in zip(iter_structures, iter_ref_structures):

        # reference coordinates
        if flag==True:

            if n_ref_structures==1:
                flag=False

            if reference_atom_indices is None:
                if atom_indices is None:
                    iter_ref_atoms = range(reference_coordinates.shape[1])
                else:
                    iter_ref_atoms = atom_indices
            else:
                iter_ref_atoms = reference_atom_indices

            x_norm=0.0
            x[:,:]=0.0

            for aa,jj in enumerate(iter_ref_atoms):
                x[aa,:]=w[aa]*reference_coordinates[mm,jj,:]

            for ii in range(3):
                center_ref[ii]=np.sum(x[:,ii])/n_atoms
                x[:,ii]=x[:,ii]-center_ref[ii]
                x_norm=x_norm+dot_product(x[:,ii],x[:,ii])

        # coordinates

        if atom_indices is None:
            n_atoms = coordinates.shape[0]
            iter_atoms = range(n_atoms)
        else:
            n_atoms = len(atom_indices)
            iter_atoms = atom_indices

        y_norm=0.0
        y[:,:]=0.0

        for aa,jj in enumerate(iter_atoms):
            y[aa,:]=w[aa]*coordinates[ll,jj,:]

        for ii in range(3):
            center[ii]=np.sum(x[:,ii])/n_atoms
            x[:,ii]=x[:,ii]-center[ii]
            x_norm=x_norm+dot_product(x[:,ii],x[:,ii])

        R[:,:]=0.0
        F[:,:]=0.0

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
        coordinates[ll,:,:] = rotate_and_translate_single_structure(coordinates[ll,:,:], center, U, center_ref,
                                                                    atom_indices=atom_indices_to_move)

    pass

