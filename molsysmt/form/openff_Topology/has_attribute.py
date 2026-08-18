from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Topology')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form openff.Topology supports a specific attribute.

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
        molecules = list(item.molecules)
        return bool(molecules) and all(
            molecule.partial_charges is not None for molecule in molecules
        )
    return attributes.get(attribute, False)
