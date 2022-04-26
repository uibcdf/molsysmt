from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:mol2')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)


    from mdtraj import load_mol2
    from ..mdtraj_Trajectory import extract as extract_mdtraj_Trajectory

    tmp_item = load_mol2(item)
    tmp_item = extract_mdtraj_Trajectory(tmp_item)

    return tmp_item

