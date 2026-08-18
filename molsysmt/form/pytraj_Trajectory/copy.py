from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pytraj.Trajectory')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form pytraj.Trajectory.

    Parameters
    ----------
    item : pytraj.Trajectory
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    pytraj.Trajectory
        Copied item.
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

