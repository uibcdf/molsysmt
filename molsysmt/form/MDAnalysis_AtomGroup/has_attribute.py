from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.AtomGroup')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form MDAnalysis.AtomGroup supports a specific attribute.

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

    if not attributes[attribute]:
        return False
    from molsysmt.basic import has_attribute as msm_has_attribute
    return msm_has_attribute(item.universe, attribute, include_none=include_none, skip_digestion=True)
