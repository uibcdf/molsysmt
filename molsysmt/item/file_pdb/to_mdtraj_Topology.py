from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_mdtraj_Topology(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'file:pdb')
        atom_indices = digest_atom_indices(atom_indices)

    from mdtraj import load_topology
    from ..mdtraj_Topology import extract as extract_mdtraj_Topology

    tmp_item = load_topology(item)
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, check=False)

    return tmp_item

