from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

@digest(form='mdtraj.Topology')
def to_string_amino_acids_3(item, atom_indices='all', skip_digestion=False):

    from . import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices, skip_digestion=True)
    group_indices = np.unique(group_indices)

    if is_all(group_indices):

        tmp_item = ''.join([ r.name.title() for r in item.residues ])

    else:

        tmp_item = ''

        for group_index in group_indices:
            r = item.residue(group_index)
            tmp_item += r.name.title()

    return tmp_item

