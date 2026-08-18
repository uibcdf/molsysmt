from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Topology')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openff.Topology.

    Parameters
    ----------
    item : openff.Topology
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openff.Topology
        Copied item.
    """

    from copy import deepcopy
    return deepcopy(item)
