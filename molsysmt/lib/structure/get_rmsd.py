import numpy as np
import numba as nb
from ..math import dot_product
from ..make_numba_signature import make_numba_signature

arguments=[
    nb.float64[:,:], # coordinates: [n_atoms, 3]
    nb.float64[:,:], # reference_coordinates: [n_atoms, 3]
    nb.int64[:], # atom_indices [n_atoms]
    nb.int64[:], # atom_indices [n_atoms]
]
output=nb.float64
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_rmsd_single_structure(coordinates, reference_coordinates, atom_indices, reference_atom_indices):

    n_atoms = atom_indices.shape[0]

    output = 0.0

    for ii, ii_ref in zip(atom_indices, reference_atom_indices):
        vect_aux=reference_coordinates[ii_ref,:]-coordinates[ii,:]
        output+=dot_product(vect_aux,vect_aux)

    output=np.sqrt(output/n_atoms)

    return output


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    nb.float64[:,:,:], # coordinates_ref: [n_structures, n_atoms, 3]
    nb.int64[:], # atom_indices [n_atoms]
    nb.int64[:], # structure_indices [n_structures]
    nb.int64[:], # reference_atom_indices [n_atoms]
    nb.int64[:], # reference_structure_indices [n_structures]
]
output=nb.float64[:]
@nb.njit(make_numba_signature(arguments,output), cache=True)
def get_rmsd(coordinates, reference_coordinates, atom_indices, structure_indices,
             reference_atom_indices, reference_structure_indices):

    n_atoms = atom_indices.shape[0]
    n_structures = structure_indices.shape[0]

    n_reference_structures = reference_structure_indices.shape[0]

    single_reference_structure = (reference_structure_indices==1)

    output = np.zeros((n_structures), dtype=nb.float64)

    oo = 0
    ii_ref = 0
    for ii in structure_indices:
        val_aux = 0.0
        for jj, jj_ref in zip(atom_indices, reference_atom_indices):
            vect_aux=reference_coordinates[ii_ref,jj_ref,:]-coordinates[ii,jj,:]
        output[oo]=np.sqrt(val_aux/n_atoms)
        oo+=1
        if not single_reference_structure:
            ii_ref+=1

    return output

