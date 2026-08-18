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
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolSys
        Target item with added elements.
    """

    to_item.add(from_item, atom_indices=atom_indices, structure_indices=structure_indices,
                keep_ids=keep_ids, attribute_policy=attribute_policy, skip_digestion=True)
