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
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Structures
        Target item with added elements.
    """

    to_item.add(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        attribute_policy=attribute_policy,
        skip_digestion=True,
    )
