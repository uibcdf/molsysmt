from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_pytraj_Topology(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'pytraj.Trajectory')
        atom_indices = digest_atom_indices(atom_indices)

    from ..pytraj_Topology import extract as extract_pytraj_Topology

    tmp_item = item.topology
    tmp_item = extract_pytraj_Topology(item, atom_indices=atom_indices, copy_if_all=False,
                                       check=False)

    return tmp_item

