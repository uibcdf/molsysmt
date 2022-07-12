from molsysmt._private.digestion import digest_item, digest_group_indices
from molsysmt._private.variables import is_all

def to_string_aminoacids3(item, group_indices='all', check=True):

    if check:

        digest_item(item, 'mdtraj.Topology')
        group_indices = digest_group_indices(group_indices)

    if is_all(group_indices):

        tmp_item = ''.join([ r.name.title() for r in item.residues ])

    else:

        tmp_item = ''

        for group_index in group_indices:
            r = item.residue(group_index)
            tmp_item += r.name.title()

    return tmp_item

