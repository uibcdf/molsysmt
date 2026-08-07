from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    import mdtraj as mdt
    from molsysmt._private.variables import is_all

    if is_all(atom_indices):
        atom_indices = None

    if is_all(structure_indices):
        tmp_item = mdt.load(item, atom_indices=atom_indices)
    else:
        tmp_item = mdt.load(item, atom_indices=atom_indices, frame=structure_indices)

    return tmp_item

