import numba as nb
import numpy as np
from ..make_numba_signature import make_numba_signature
from math import sqrt

arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.float64[:], # weights: [n_atoms]
]
output=[nb.float64[:,:], # [n_atoms]
        nb.float64[:,:,:], # [n_atoms, n_atoms]
]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def principal_component_analysis(coordinates, weights):

    n_structures, n_atoms = coordinates.shape[0:2]

    eigenvectors=np.zeros((n_atoms*3, n_atoms*3), dtype=nb.float64)
    eigenvalues=np.zeros((n_atoms*3), dtype=nb.float64)
    C=np.zeros((n_atoms*3, n_atoms*3), dtype=nb.float64)
    mean=np.zeros((n_atoms, 3), dtype=nb.float64)
    aux_ind=np.zeros((n_atoms,3), dtype=np.int64)

    gg=0
    for jj in range(3):
        for ii in range(n_atoms):
            aux_ind[ii,jj]=gg
            gg+=1

    for ll in range(n_structures):
        for ii in range(n_atoms):
            for jj in range(3):

                xx=aux_ind[ii,jj]
                aux_coor=coordinates[ll,ii,jj]
                mean[xx]+=aux_coor

            for ii2 in range(ii, n_atoms):
                for jj2 in range(jj, 3):

                   yy=aux_ind[ii2,jj2]

                   C[xx,yy]+=coordinates[ll,ii2,jj2]

    mean = mean/n_structures

    for jj in range(3):
        for ii in range(n_atoms):
            xx=aux_ind[ii,jj]
            aux_mean=mean[xx]
            aux_weight=sqrt(weight[ii])
            for ii2 in range(ii,n_atoms):
                aux_weight2=sqrt(weight[ii2])
                for jj2 in range(jj,3):
                    yy=aux_ind[ii2,jj2]
                    C[xx,yy]=aux_weight*aux_weight2(C[xx,yy]/n_structures-aux_mean*mean[yy])
                    C[yy,xx]=C[xx,yy]

    eigenvalues[:], eigenvectors[:,:] = np.linalg.eigh(matrix)
    eigenvectors[:,:] = eigenvectors[:,:].transpose()

    return eigenvalues, eigenvectors

