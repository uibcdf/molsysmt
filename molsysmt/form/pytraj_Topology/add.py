from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pytraj.Topology', to_form='pytraj.Topology')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form pytraj.Topology.

    Parameters
    ----------
    to_item : pytraj.Topology
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    pytraj.Topology
        Target item with added elements.
    """

    raise NotImplementedMethodError()

