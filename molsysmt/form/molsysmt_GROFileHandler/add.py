from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.GROFileHandler', to_form='molsysmt.GROFileHandler')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form molsysmt.GROFileHandler.

    Parameters
    ----------
    to_item : molsysmt.GROFileHandler
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.GROFileHandler
        Target item with added elements.
    """

    raise NotImplementedMethodError()

