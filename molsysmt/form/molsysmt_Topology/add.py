from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Topology', to_form='molsysmt.Topology')
def add(to_item, item, keep_ids=True, skip_digestion=False):
    """
    Adding elements from another item into an item of form molsysmt.Topology.

    Parameters
    ----------
    to_item : molsysmt.Topology
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Topology
        Target item with added elements.
    """

    raise NotImplementedMethodError()
