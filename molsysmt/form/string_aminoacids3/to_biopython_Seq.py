from .is_string_aminoacids3 import is_string_aminoacids3
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_biopython_Seq(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_string_aminoacids3(item)
        except:
            raise WrongFormError('string:aminoacids3')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from . import to_string_aminoacids1
    from ..string_aminoacids1 import to_biopython_Seq

    tmp_item = to_string_aminoacids1(item, atom_indices=atom_indices, check=False)
    tmp_item = string_aminoacids1_to_biopython_Seq(tmp_item, check=False)

    return tmp_item

