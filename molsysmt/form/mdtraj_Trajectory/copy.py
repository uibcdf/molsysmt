from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form mdtraj.Trajectory.

    Parameters
    ----------
    item : mdtraj.Trajectory
        Source item in mdtraj.Trajectory form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.

    .. versionadded:: 1.0.0
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

