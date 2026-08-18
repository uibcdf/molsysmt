from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:amino_acids_3', to_form='string:amino_acids_3')
def add(to_item, item, group_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form string:amino_acids_3.

    Parameters
    ----------
    to_item : string:amino_acids_3
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string:amino_acids_3
        Target item with added elements.
    """

    raise NotImplementedMethodError()

