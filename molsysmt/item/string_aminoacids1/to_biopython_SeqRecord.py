from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_biopython_SeqRecord(item, group_indices='all', check=True):

    if check:

        digest_item(item, 'string:aminoacids1')
        group_indices = digest_group_indices(group_indices)

    from . import to_biopython_Seq
    from ..biopython_Seq import to_biopython_SeqRecord as biopython_Seq_to_biopython_SeqRecord

    tmp_item = to_biopython_Seq(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = biopython_Seq_to_biopython_SeqRecord(tmp_item, check=False)

    return tmp_item

