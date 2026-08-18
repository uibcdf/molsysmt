from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:gro')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:gro to mdtraj.Trajectory.

    Parameters
    ----------
    item : file:gro
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Trajectory
        Converted molecular system representation.
    """

    from mdtraj import load
    from ..mdtraj_Trajectory.extract import extract

    tmp_item = load(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)

    return tmp_item
