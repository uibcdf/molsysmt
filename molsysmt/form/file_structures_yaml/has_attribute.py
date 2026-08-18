from molsysmt._private.argdigest import arg_digest
from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict


@arg_digest(form='file:structures_yaml')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form file:structures_yaml supports a specific attribute.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
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
    from molsysmt.form.molsysmt_StructuresDict.has_attribute import has_attribute as _has_attribute
    tmp_item = to_molsysmt_StructuresDict(molecular_system, skip_digestion=True)
    return _has_attribute(tmp_item, attribute=attribute, include_none=include_none, skip_digestion=True)
