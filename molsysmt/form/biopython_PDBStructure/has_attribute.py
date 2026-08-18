from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.PDBStructure')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form biopython.PDBStructure supports a specific attribute.

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

    output = attributes.get(attribute, False)

    return output
