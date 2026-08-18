from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:smiles', to_form='string:smiles')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form string:smiles.

    Parameters
    ----------
    to_item : string:smiles
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string:smiles
        Target item with added elements.
    """

    raise NotImplementedMethodError()
