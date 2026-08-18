from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.Universe', to_form='MDAnalysis.Universe')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form MDAnalysis.Universe.

    Parameters
    ----------
    to_item : MDAnalysis.Universe
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    MDAnalysis.Universe
        Target item with added elements.
    """

    raise NotImplementedMethodError()

