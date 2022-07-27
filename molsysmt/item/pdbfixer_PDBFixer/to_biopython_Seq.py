from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer

def to_biopython_Seq(item, atom_indices='all'):

    if check:

        try:
            is_pdbfixer_PDBFixer(item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from . import to_string_aminoacids1
    from ..string_aminoacids1 import to_biopython_Seq as string_aminoacids1_to_biopython_Seq

    tmp_item = to_string_aminoacids1(item, atom_indices=atom_indices)
    tmp_item = string_aminoacids1_to_biopython_Seq(tmp_item)

    return tmp_item

