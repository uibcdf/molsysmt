from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Topology')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form openff.Topology supports a specific attribute.

    Parameters
    ----------
    item : openff.Topology
        Source item in openff.Topology form.
    attribute : str
        Attribute name to query.
    include_none : object
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
        molecules = list(item.molecules)
        return bool(molecules) and all(
            molecule.partial_charges is not None for molecule in molecules
        )
    return attributes.get(attribute, False)
