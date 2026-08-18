from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Topology')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form molsysmt.Topology.

    Parameters
    ----------
    item : molsysmt.Topology
        Source item in molsysmt.Topology form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.

    .. versionadded:: 1.0.0
    """

    return item.copy()

