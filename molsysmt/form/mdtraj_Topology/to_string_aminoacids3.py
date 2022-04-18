from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_string_aminoacids3(item, group_indices='all', check=True):

    if check:

        digest_item(item, 'mdtraj.Topology')
        atom_indices = digest_atom_indices(atom_indices)

    from . import extract

    tmp_item = extract(item, group_indices=group_indices, copy_if_all=False, check=False)
    tmp_item = ''.join([ r.name.title() for r in item.residues ])

    return tmp_item

