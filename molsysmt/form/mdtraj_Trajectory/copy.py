from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form mdtraj.Trajectory.

    Parameters
    ----------
    item : mdtraj.Trajectory
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Trajectory
        Copied item.
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

