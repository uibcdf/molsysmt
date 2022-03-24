from .is_string_aminoacids1 import is_string_aminoacids1
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.atom_indices import digest_atom_indices

def to_biopython_SeqRecord(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_string_aminoacids1(item)
        except:
            raise WrongFormError('string:aminoacids1')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from . import to_biopython_Seq
    from ..biopython_Seq import to_biopython_SeqRecord as biopython_Seq_to_biopython_SeqRecord

    tmp_item = to_biopython_Seq(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = biopython_Seq_to_biopython_SeqRecord(tmp_item, check=False)

    return tmp_item

