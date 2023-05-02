import numpy as np
import numba as nb
from ..math import dot_product
from ..make_numba_signature import make_numba_signature
from ..itertools import infinite_sequence, repeat


arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    nb.float64[:,:], # reference_coordinates: [n_atoms, 3]
    [nb.int64[:], None], # atom_indices [n_atoms] or None
    [nb.int64[:], None], # atom_indices [n_atoms] or None
]
output=nb.float64
@nb.njit(make_numba_signature(arguments,output))
def get_least_rmsd_single_structure(coordinates, reference_coordinates, atom_indices=None, reference_atom_indices=None):

    if atom_indices is None:
        n_atoms = coordinates.shape[0]
        iter_atoms = range(n_atoms)
    else:
        n_atoms = len(atom_indices)
        iter_atoms = atom_indices

    if reference_atom_indices is None:
        iter_ref_atoms = range(reference_coordinates.shape[0])
    else:
        iter_ref_atoms = reference_atom_indices

    center_ref=np.empty((3), dtype=nb.float64)
    center=np.empty((3), dtype=nb.float64)

    x=np.zeros((n_atoms,3), dtype=nb.float64)
    y=np.zeros((n_atoms,3), dtype=nb.float64)

    R=np.zeros((3,3), dtype=nb.float64)
    F=np.zeros((4,4), dtype=nb.float64)

    w=np.ones((n_atoms), dtype=nb.float64) # without weights

    # reference coordinates

    for aa,ii in enumerate(iter_ref_atoms):
        x[aa,:]=w[aa]*reference_coordinates[ii,:]

    x_norm=0.0
    for ii in range(3):
        center_ref[ii]=np.sum(x[:,ii])/n_atoms
        x[:,ii]=x[:,ii]-center_ref[ii]
        x_norm=x_norm+dot_product(x[:,ii],x[:,ii])

    # coordinates

    for aa,ii in enumerate(iter_atoms):
        y[aa,:]=w[aa]*coordinates[ii,:]

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
    eigvalues = np.linalg.eigvalsh(F)

    # rmsd
    msd=max(0.0,((x_norm+y_norm)-2.0*eigvalues[3]))/n_atoms
    output_rmsd=math.sqrt(msd)

    return output_rmsd


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    [nb.float64[:,:,:], None], # coordinates_ref: [n_structures, n_atoms, 3]
    [nb.int64[:], None], # atom_indices [n_atoms] or None
    [nb.int64[:], None], # structure_indices [n_structures] or None
    [nb.int64[:], None], # reference_atom_indices [n_atoms] or None
    [nb.int64[:], None], # reference_structure_indices [n_structures] or None
]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments,output))
def get_least_rmsd(coordinates, reference_coordinates=None, atom_indices=None, structure_indices=None,
             reference_atom_indices=None, reference_structure_indices=None):

    if structure_indices is None:
        n_structure_indices = coordinates.shape[0]
        iter_structure_indices = range(n_structure_indices)
    else:
        n_atoms = len(structure_indices)
        iter_structure_indices = structure_indices

    if reference_coordinates is None:
        reference_coordinates = coordinates
        if reference_structure_indices is None:
            raise ValueError('reference_structure_indices needed.')
        elif len(reference_structure_indices)==1:
            n_ref_structure_indices = 1
            iter_ref_structure_indices=repeat(reference_structure_indices[0])
        else:
            n_ref_structure_indices = len(reference_structure_indices)
            iter_ref_structure_indices = reference_structure_indices
    else:
        if reference_structure_indices is None:
            n_ref_structure_indices = reference_coordinates.shape[0]
            iter_ref_structure_indices = range(n_ref_structure_indices)
        elif len(reference_structure_indices)==1:
            n_ref_structure_indices = 1
            iter_ref_structure_indices=repeat(reference_coordinates[0])
        else:
            n_ref_structure_indices = len(reference_structure_indices)
            iter_ref_structure_indices = reference_structure_indices


    output_rmsd = np.zeros((n_structures), dtype=nb.float64)

    w=np.ones((n_atoms), dtype=nb.float64)

    center_ref=np.empty((3), dtype=nb.float64)
    center=np.empty((3), dtype=nb.float64)

    x=np.zeros((n_atoms,3), dtype=nb.float64)
    y=np.zeros((n_atoms,3), dtype=nb.float64)

    R=np.zeros((3,3), dtype=nb.float64)
    F=np.zeros((4,4), dtype=nb.float64)

    iter_out_structures = infinite_sequence(0)
    flag=True
    for bb, ll, mm in zip(iter_out_structures, iter_structures, iter_ref_structures):

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

        msd=0.0
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
        eigvalues = np.linalg.eigvalsh(F)

        # rmsd
        msd=max(0.0,((x_norm+y_norm)-2.0*eigvalues[3]))/n_atoms
        output_rmsd[bb]=math.sqrt(msd)

    return output_rmsd

