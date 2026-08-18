from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.AtomGroup')
def has_attribute(item, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form MDAnalysis.AtomGroup supports a specific attribute.


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

    from . import attributes

    if not attributes[attribute]:
        return False
    from molsysmt.basic import has_attribute as msm_has_attribute
    return msm_has_attribute(item.universe, attribute, include_none=include_none, skip_digestion=True)
