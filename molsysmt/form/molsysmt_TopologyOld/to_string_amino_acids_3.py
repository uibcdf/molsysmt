from molsysmt._private.digestion import digest
import numpy as np

@digest(form='molsysmt.TopologyOld')
def to_string_amino_acids_3(item, group_indices='all', skip_digestion=False):

    from . import get_group_name_from_group

    group_names = get_group_name_from_group(item, indices=group_indices)
    tmp_item = ''.join([ii.title() for ii in group_names])

    return tmp_item

