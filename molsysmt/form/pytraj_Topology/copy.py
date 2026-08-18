from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pytraj.Topology')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form pytraj.Topology.

    Parameters
    ----------
    item : pytraj.Topology
        Source item in pytraj.Topology form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    pytraj.Topology
        Resulting object in pytraj.Topology form.

    .. versionadded:: 1.0.0
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

