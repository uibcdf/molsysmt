from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Topology', to_form='molsysmt.Topology')
def add(to_item, item, keep_ids=True, skip_digestion=False):
    """
    Adding elements from another item into an item of form molsysmt.Topology.


    Parameters
    ----------
    to_item : object
        Argument to_item.
    item : molecular system
        Argument item.
    keep_ids : object, default=True
        Argument keep_ids.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()
