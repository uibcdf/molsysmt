from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Topology')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form molsysmt.Topology.

    Parameters
    ----------
    item : molsysmt.Topology
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Topology
        Copied item.
    """

    return item.copy()

