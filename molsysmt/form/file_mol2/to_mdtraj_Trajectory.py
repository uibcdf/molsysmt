from molsysmt._private.digestion import digest

@digest(form='file:mol2')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', digest=True):

    from mdtraj import load_mol2
    from ..mdtraj_Trajectory import extract as extract_mdtraj_Trajectory

    tmp_item = load_mol2(item)
    tmp_item = extract_mdtraj_Trajectory(tmp_item, digest=False)

    return tmp_item

