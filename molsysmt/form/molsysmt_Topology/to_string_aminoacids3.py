from molsysmt._private.digestion import digest
import numpy as np

@digest(form='molsysmt.Topology')
def to_string_aminoacids3(item, group_indices='all'):

    from . import get_group_name_from_group

    group_names = get_group_name_from_group(item, indices=group_indices)
    tmp_item = ''.join([ii.title() for ii in group_names])

    return tmp_item

def _to_string_aminoacids3(item, atom_indices='all', structure_indices='all'):

    from . import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    group_indices = np.unique(group_indices)

    return to_string_aminoacids3(item, group_indices=group_indices)
