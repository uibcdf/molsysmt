from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:h5 to mdtraj.Trajectory.

    Parameters
    ----------
    item : file:h5
        Source item in file:h5 form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.

    .. versionadded:: 1.0.0
    """

    import mdtraj as mdt
    from molsysmt._private.variables import is_all

    if is_all(atom_indices):
        atom_indices = None

    if is_all(structure_indices):
        tmp_item = mdt.load(item, atom_indices=atom_indices)
    else:
        tmp_item = mdt.load(item, atom_indices=atom_indices, frame=structure_indices)

    return tmp_item

