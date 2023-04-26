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
def get_rmsd(coordinates, reference_coordinates):

    n_structures, n_atoms = coordinates.shape[-1]

    output = np.empty((n_structures), dtype=nb.float64)

    counter=0
    for ll in range(n_structures):
        val_aux=0.0
        for ii in range(n_atoms):
            vect_aux=coors_ref[0,ii,:]-coors[ll,ii,:]
            val_aux+=dot_product(vect_aux,vect_aux)
        output[counter]=val_aux
        counter+=1

    output=np.sqrt(output/n_atoms)

    return output

