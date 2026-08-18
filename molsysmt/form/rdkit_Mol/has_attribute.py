from molsysmt._private.argdigest import arg_digest

@arg_digest(form='rdkit.Mol')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form rdkit.Mol supports a specific attribute.

    Parameters
    ----------
    item : rdkit.Mol
        Source item in rdkit.Mol form.
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

    output = attributes.get(attribute, False)
    if output and not include_none:
        if attribute == 'isotope':
            output = any(atom.GetIsotope() != 0 for atom in item.GetAtoms())
        elif attribute == 'partial_charge':
            from .get_mechanical_attributes import _get_partial_charges

            output = _get_partial_charges(item) is not None
        elif attribute in {'coordinates', 'structure_id'}:
            output = item.GetNumConformers() > 0
    return output
