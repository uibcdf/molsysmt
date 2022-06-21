from .indices import digest_indices
from ..lists_and_tuples import is_list_or_tuple


def digest_structure_indices(structure_indices):
    """ Checks if structure indices are of the expected type and value. """
    return digest_indices(structure_indices)


def digest_multiple_structure_indices(structure_indices):

    if is_list_or_tuple(structure_indices):
        return [digest_structure_indices(ii) for ii in structure_indices]
    else:

        return digest_structure_indices(structure_indices)
