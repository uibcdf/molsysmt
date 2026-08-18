from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Structures', to_form='molsysmt.Structures')
def add(to_item, item, atom_indices='all', structure_indices='all',
        attribute_policy='intersection', skip_digestion=False):
    """
    Adding elements from another item into an item of form molsysmt.Structures.

    Parameters
    ----------
    to_item : molsysmt.Structures
        Target item to modify or add elements to.
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    attribute_policy : object
        Argument attribute_policy.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.

    .. versionadded:: 1.0.0
    """

    to_item.add(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        attribute_policy=attribute_policy,
        skip_digestion=True,
    )
