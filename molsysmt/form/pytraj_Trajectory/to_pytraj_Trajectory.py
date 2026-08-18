from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pytraj.Trajectory')
def to_pytraj_Trajectory(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from pytraj.Trajectory to pytraj.Trajectory.

    Parameters
    ----------
    item : pytraj.Trajectory
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    pytraj.Trajectory
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

