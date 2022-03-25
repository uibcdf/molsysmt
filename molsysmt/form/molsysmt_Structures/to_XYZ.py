from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_Structures import is_molsysmt_Structures

def to_XYZ(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import get_coordinates_from_atom
    tmp_item = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

