from molsysmt._private.digestion import digest
import numpy as np

@digest(form='molsysmt.MolSys')
def to_biopython_Seq(item, group_indices='all'):

    from . import to_string_aminoacids1
    from ..string_aminoacids1 import to_biopython_Seq as string_aminoacids1_to_biopython_Seq

    tmp_item = to_string_aminoacids1(item, group_indices=group_indices)
    tmp_item = string_aminoacids1_to_biopython_Seq(tmp_item)

    return tmp_item

def _to_biopython_Seq(item, molecular_system, atom_indices='all', structure_indices='all'):

    from . import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)

    return to_biopython_Seq(item, group_indices=group_indices)

