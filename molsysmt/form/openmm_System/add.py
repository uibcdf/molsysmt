from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.System', to_form='openmm.System')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form openmm.System.

    Parameters
    ----------
    to_item : openmm.System
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.System
        Target item with added elements.
    """

    raise NotImplementedMethodError()

