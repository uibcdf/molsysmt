from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Topology', to_form='openff.Topology')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form openff.Topology.

    Parameters
    ----------
    to_item : openff.Topology
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openff.Topology
        Target item with added elements.
    """

    raise NotImplementedMethodError()
