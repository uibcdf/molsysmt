from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Molecule')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form openff.Molecule supports a specific attribute.

    Parameters
    ----------
    attribute : str
        Attribute name to query.

    Returns
    -------
    bool
        True if attribute is supported, False otherwise.
    """

    from .attributes import attributes
    if attribute == 'partial_charge':
        return item.partial_charges is not None
    if attribute in {'coordinates', 'structure_id', 'structure_index'}:
        return item.n_conformers > 0
    return attributes.get(attribute, False)
