from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', digest=True):

    from mdtraj import load
    from ..mdtraj_Trajectory import extract

    tmp_item = load(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, digest=False)

    return tmp_item

