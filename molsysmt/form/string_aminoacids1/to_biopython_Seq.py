from .is_string_aminoacids1 import is_string_aminoacids1
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_biopython_Seq(item, atom_indices='all', structure_indices='all', check=True):

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
        from Bio.Seq import Seq as bio_Seq
        #from Bio.Alphabet.IUPAC import ExtendedIUPACProtein
    except:
        raise LibraryNotFoundError('biopython')

    #tmp_item = bio_Seq(item, ExtendedIUPACProtein())
    tmp_item = bio_Seq(item)

    return tmp_item

