from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form file:h5 supports a specific attribute.

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

    output = attributes[attribute]

    if not include_none:
        pass

    return output

