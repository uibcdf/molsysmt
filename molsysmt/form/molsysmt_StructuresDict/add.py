from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.StructuresDict', to_form='molsysmt.StructuresDict')
def add(to_item, item, atom_indices='all', structure_indices='all'):
    """
    Adding elements from another item into an item of form molsysmt.StructuresDict.

    Parameters
    ----------
    to_item : molsysmt.StructuresDict
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.StructuresDict
        Target item with added elements.
    """

    raise NotImplementedMethodError()

