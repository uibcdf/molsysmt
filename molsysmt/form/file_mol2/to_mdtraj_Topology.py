from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_mdtraj_Topology(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'file:mol2')
        atom_indices = digest_atom_indices(atom_indices)


    from mdtraj import load_mol2
    from ..mdtraj_Topology import extract as extract_mdtraj_Topology

    tmp_item = load_mol2(item).topology
    tmp_item = extract_mdtraj_Topology(tmp_item)

    return tmp_item

