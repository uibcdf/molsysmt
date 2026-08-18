from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Topology')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form mdtraj.Topology.

    Parameters
    ----------
    item : mdtraj.Topology
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Topology
        Copied item.
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

