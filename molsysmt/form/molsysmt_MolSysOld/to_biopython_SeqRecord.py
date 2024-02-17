from molsysmt._private.digestion import *
import numpy as np

@digest(form='molsysmt.MolSysOld')
def to_biopython_SeqRecord(item, atom_indices='all', skip_digestion=False):

    from . import to_string_aminoacids1
    from ..string_aminoacids1 import to_biopython_SeqRecord as string_aminoacids1_to_biopython_SeqRecord
    from . import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    tmp_item = to_string_aminoacids1(item, group_indices=group_indices, skip_digestion=True)
    tmp_item = string_aminoacids1_to_biopython_SeqRecord(tmp_item, skip_digestion=True)

    return tmp_item

