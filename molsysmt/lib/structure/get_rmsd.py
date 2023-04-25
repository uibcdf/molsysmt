import numpy as np
import numba as nb
from .math import dot_product
from .make_numba_signature import make_numba_signature

arguments=[
    nb.float64[:,:,:], # coordinates
    nb.float64[:,:,:], # coordinates_ref
    [nb.int64[:], 'all'], # atom indices
    [nb.int64[:], 'all'], # structure_indices
]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments,output))
def rmsd(coordinates, coors_ref, atom_indices, structure_indices):

    n_structure_indices = structure_indices.shape[0]
    n_list_atoms = list_atoms.shape[0]

    output = np.empty((n_structure_indices), dtype=nb.float64)

    counter=0
    for ll in structure_indices:
        val_aux=0.0
        for ii in list_atoms:
            vect_aux=coors_ref[0,ii,:]-coors[ll,list_atoms[ii],:]
            val_aux+=dot_product(vect_aux,vect_aux)
        output[counter]=val_aux
        counter+=1

    output=np.sqrt(output/n_list_atoms)

    return output

