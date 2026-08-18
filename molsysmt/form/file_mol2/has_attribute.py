from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form file:mol2 supports a specific attribute.

    Parameters
    ----------
    attribute : str
        Attribute name to query.

    Returns
    -------
    bool
        True if attribute is supported, False otherwise.
    """

    from . import attributes

    if not attributes.get(attribute, False):
        return False
    if attribute in {'partial_charge', 'box'}:
        from ._reader import _source_metadata

        metadata = _source_metadata(molecular_system)
        if attribute == 'partial_charge':
            return metadata['charge_type'] != 'NO_CHARGES'
        return metadata['has_crysin']
    return True
