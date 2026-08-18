from molsysmt._private.argdigest import arg_digest


@arg_digest(form='file:molsys_yaml')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form file:molsys_yaml supports a specific attribute.

    Parameters
    ----------
    molecular_system : object
        Argument molecular_system.
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
    from .to_molsysmt_MolSysDict import to_molsysmt_MolSysDict
    from molsysmt.form.molsysmt_MolSysDict.has_attribute import has_attribute as dict_has_attribute

    item = to_molsysmt_MolSysDict(molecular_system, skip_digestion=True)
    return dict_has_attribute(item, attribute=attribute, include_none=include_none, skip_digestion=True)
