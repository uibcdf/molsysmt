import numpy as np
import numba as nb
from .math import dot_product

@nb.jit(nb.float64[:](nb.float64[:,:,:], nb.int64[:], nb.float64[:,:,:], nb.int64[:]), nopython=True)
def rmsd(coors, list_atoms, coors_ref, structure_indices):

    n_structure_indices = structure_indices.shape[0]
    n_list_atoms = list_atoms.shape[0]

    output = np.empty((n_structure_indices), dtype=float)

    counter=0
    for ll in structure_indices:
        val_aux=0.0
        for ii in list_atoms:
            vect_aux=coors_ref[0,ii,:]-coors[ll,list_atoms[ii],:]
            val_aux+=dot_product(vect_aux)
        output[counter]=val_aux
        counter+=1

    output=np.sqrt(output/n_list_atoms)

    return output


@nb.jit(nb.float64[:](nb.float64[:,:,:], nb.int64[:], nb.float64[:,:,:], nb.int64[:]), nopython=True)
def least_rmsd(coors, list_atoms, coors_ref, structure_indices):

    n_structure_indices = structure_indices.shape[0]
    n_list_atoms = list_atoms.shape[0]

    center_ref=np.empty((3), dtype=float)

    x=np.zeros((n_list_atoms,3), dtype=float)
    y=np.zeros((n_list_atoms,3), dtype=float)

    output=np.zeros((n_structure_indices), dtype=float)

    R=np.zeros((3,3), dtype=float)
    F=np.zeros((4,4), dtype=float)

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
        x_norm=x_norm+dot_product(x[:,ii])

    for ll in range(n_structure_indices):

        structure_index=structure_indices[ll]

        y=0.0
        rmsd=0.0
        msd=0.0
        center_2=0.0
        y_norm=0.0
        R=0.0
        F=0.0

        # copy and weight coordinates
        for ii in range(n_list_atoms):
            y[ii,:]=w[ii]*coors[structure_index, list_atoms[ii], :]

        # baricentros, centroides y normas
        for ii in range(3):
            center_2[ii]=np.sum(y[:,ii])/n_list_atoms
            y[:,ii]=y[:,ii]-center_2[ii]
            y_norm=y_norm+dot_product(y[:,ii])

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

        # Diagonalization
        values, vectors

def least_rmsd_fit(coors, list_atoms, coors_ref, structure_indices):

    raise NotImplementedError()


