import numpy as np
import numba as nb
from .math import dot_product
from .make_numba_signature import make_numba_signature

arguments=[
    nb.float64[:,:,:], # coordinates
    nb.float64[:,:,:], # coordinates_ref
]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments,output))
def get_least_rmsd(coordinates, reference_coordinates):

    n_atoms, n_structures = coordinates.shape[:-1]

    center_ref=np.empty((3), dtype=nb.float64)
    center_2=np.empty((3), dtype=nb.float64)

    x=np.zeros((n_atoms,3), dtype=nb.float64)
    y=np.zeros((n_atoms,3), dtype=nb.float64)

    output_rmsd=np.zeros((n_structures), dtype=nb.float64)

    R=np.zeros((3,3), dtype=nb.float64)
    F=np.zeros((4,4), dtype=nb.float64)

    # copy and weigth coordinates

    ##weights for atoms
    w=np.ones((n_atoms), dtype=nb.float64)

    for ii in range(n_atoms):
        x[ii,:]=w[ii]*coors_ref[0,ii,:]

    # calculo baricentros, centroides y normas:
    x_norm=0.0
    for ii in range(3):
        center_ref[ii]=np.sum(x[:,ii])/n_atoms
        x[:,ii]=x[:,ii]-center_ref[ii]
        x_norm=x_norm+dot_product(x[:,ii],x[:,ii])

    for ll in range(n_structures):

        msd=0.0
        y_norm=0.0
        center_2[:]=0.0
        y[:,:]=0.0
        R[:,:]=0.0
        F[:,:]=0.0

        # copy and weight coordinates
        for ii in range(n_atoms):
            y[ii,:]=w[ii]*coors[ll,ii,:]
        # baricentros, centroides y normas
        for ii in range(3):
            center_2[ii]=np.sum(y[:,ii])/n_atoms
            y[:,ii]=y[:,ii]-center_2[ii]
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
        output_rmsd[ll]=math.sqrt(msd)

    return output_rmsd

