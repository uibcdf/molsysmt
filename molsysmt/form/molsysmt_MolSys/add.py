from molsysmt._private.argdigest import arg_digest

@arg_digest(to_form='molsysmt.MolSys', from_form='molsysmt.MolSys')
def add(to_item, from_item, atom_indices='all', structure_indices='all', keep_ids=True,
        attribute_policy='intersection', skip_digestion=False):
    """
    Adding elements from another item into an item of form molsysmt.MolSys.

    Parameters
    ----------
    to_item : molsysmt.MolSys
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    keep_ids : bool, default=True
        Whether to preserve unique element IDs.
    attribute_policy : object
        Argument attribute_policy.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.

    .. versionadded:: 1.0.0
    """

    to_item.add(from_item, atom_indices=atom_indices, structure_indices=structure_indices,
                keep_ids=keep_ids, attribute_policy=attribute_policy, skip_digestion=True)
