from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:bcif.gz', to_form='file:bcif.gz')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form file:bcif.gz.

    Parameters
    ----------
    to_item : file:bcif.gz
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:bcif.gz
        Target item with added elements.
    """

    raise NotImplementedMethodError()

