from .is_string_aminoacids3 import is_string_aminoacids3
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.atom_indices import digest_atom_indices

def to_string_aminoacids1(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_string_aminoacids3(item)
        except:
            raise WrongFormError('string:aminoacids3')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    try:
        from Bio.SeqUtils import seq1
    except:
        raise LibraryNotFoundError()

    tmp_item = seq1(item)

    return tmp_item

