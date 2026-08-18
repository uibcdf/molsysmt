from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Molecule')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form openff.Molecule supports a specific attribute.


    Parameters
    ----------
    item : molecular system
        Argument item.
    attribute : object
        Argument attribute.
    include_none : object, default=False
        Argument include_none.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.


    .. versionadded:: 1.0.0
    """

    from .attributes import attributes
    if attribute == 'partial_charge':
        return item.partial_charges is not None
    if attribute in {'coordinates', 'structure_id', 'structure_index'}:
        return item.n_conformers > 0
    return attributes.get(attribute, False)
