from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all'):

    from mdtraj import load_pdb
    from ..mdtraj_Trajectory import extract as extract_mdtraj_Trajectory

    tmp_item = load_pdb(item)
    tmp_item = extract_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

