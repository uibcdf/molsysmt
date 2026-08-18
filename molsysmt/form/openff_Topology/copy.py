from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Topology')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openff.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openff.Topology
        Resulting object in openff.Topology form.


    .. versionadded:: 1.0.0
    """

    from copy import deepcopy
    return deepcopy(item)
