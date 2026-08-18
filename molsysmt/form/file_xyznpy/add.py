from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:xyznpy', to_form='file:xyznpy')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form file:xyznpy.

    Parameters
    ----------
    to_item : file:xyznpy
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:xyznpy
        Target item with added elements.
    """

    raise NotImplementedMethodError()

