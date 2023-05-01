import numpy as np
import numba as nb
from .math import dot_product
from .make_numba_signature import make_numba_signature
from ..itertools import infinite_sequence, repeat

arguments=[
    nb.float64[:,:], # coordinates
    nb.float64[:,:], # coordinates_ref
    [nb.int64[:], None], # atom_indices [n_atoms] or None
    [nb.int64[:], None], # atom_indices [n_atoms] or None
]
output=nb.float64
@nb.njit(make_numba_signature(arguments,output))
def get_rmsd_single_structure(coordinates, reference_coordinates, atom_indices=None, reference_atom_indices=None):

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

    output = 0.0

    for ii, ii_ref in zip(iter_atoms, iter_ref_atoms):
        vect_aux=reference_coordinates[ii_ref,:]-coordinates[ii,:]
        output+=dot_product(vect_aux,vect_aux)

    output=np.sqrt(output/n_atoms)

    return output


arguments=[
    nb.float64[:,:,:], # coordinates: [n_structures, n_atoms, 3]
    [nb.float64[:,:,:], None], # coordinates_ref: [n_structures, n_atoms, 3]
    [nb.int64[:], None], # atom_indices [n_atoms] or None
    [nb.int64[:], None], # structure_indices [n_structures] or None
    [nb.int64[:], None], # reference_atom_indices [n_atoms] or None
    [nb.int64[:], None], # reference_structure_indices [n_structures] or None
]
output=nb.float64
@nb.njit(make_numba_signature(arguments,output))
def get_rmsd(coordinates, reference_coordinates=None, atom_indices=None, structure_indices=None,
             reference_atom_indices=None, reference_structure_indices=None):

    if structure_indices is None:
        n_structure_indices = coordinates.shape[0]
        iter_structure_indices = range(n_structure_indices)
    else:
        n_atoms = len(structure_indices)
        iter_structure_indices = structure_indices

    if atom_indices is None:
        n_atoms = coordinates.shape[0]
        iter_atoms = range(n_atoms)
    else:
        n_atoms = len(atom_indices)
        iter_atoms = atom_indices


    if reference_coordinates is None:
        reference_coordinates = coordinates


    if reference_structure_indices is None:
        n_ref_structure_indices = reference_coordinates.shape[0]
        iter_ref_structure_indices = range(n_ref_structure_indices)
    elif len(reference_structure_indices)==1:
        n_ref_structure_indices = 1
        iter_ref_structure_indices=repeat(reference_coordinates[0])
    else:
        n_ref_structure_indices = len(reference_structure_indices)
        iter_ref_structure_indices = reference_structure_indices

    if reference_atom_indices is None:
        n_atoms = coordinates.shape[0]
        iter_atoms = range(n_atoms)
    else:
        n_atoms = len(atom_indices)
        iter_atoms = atom_indices



    output = 0.0

    for ii, ii_ref in zip(iter_atoms, iter_ref_atoms):
        vect_aux=reference_coordinates[ii_ref,:]-coordinates[ii,:]
        output+=dot_product(vect_aux,vect_aux)

    output=np.sqrt(output/n_atoms)

    return output

