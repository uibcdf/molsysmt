from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_string_pdb_text import is_string_pdb_text

def set_box_to_system(item, structure_indices='all', value=None, check=True):

    if check:

        try:
            is_string_pdb_text(item)
        except:
            raise WrongFormError('string:pdb_text')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()


    raise NotImplementedMethodError()

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None, check=True):

    if check:

        try:
            is_string_pdb_text(item)
        except:
            raise WrongFormError('string:pdb_text')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    raise NotImplementedMethodError()

