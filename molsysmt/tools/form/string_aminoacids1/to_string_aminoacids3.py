from molsysmt.tools.string_aminoacids1.is_string_aminoacids1 import is_string_aminoacids1
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError
from molsysmt._private_tools.exceptions import NotImplementedMethodError
from molsysmt._private_tools.atom_indices import digest_atom_indices

def to_string_aminoacids3(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_string_aminoacids1(item)
        except:
            raise WrongFormError('string:aminoacids1')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    try:
        from Bio.SeqUtils import seq3
    except:
        raise LibraryNotFoundError('biopython')

    tmp_item=seq3(item)

    return tmp_item

