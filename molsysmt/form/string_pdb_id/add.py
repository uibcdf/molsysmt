from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_id', to_form='string:pdb_id')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form string:pdb_id.

    Parameters
    ----------
    to_item : string:pdb_id
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string:pdb_id
        Target item with added elements.
    """

    raise NotImplementedMethodError()

