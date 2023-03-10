from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='mdtraj.Topology')
def to_string_aminoacids3(item, atom_indices='all'):

    if is_all(group_indices):

        tmp_item = ''.join([ r.name.title() for r in item.residues ])

    else:

        tmp_item = ''

        for group_index in group_indices:
            r = item.residue(group_index)
            tmp_item += r.name.title()

    return tmp_item

