from molsysmt._private.argdigest import arg_digest

form = 'molsysviewer.MolSysView'


@arg_digest(form=form)
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form molsysviewer.MolSysView supports a specific attribute.


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

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from ..molsysmt_MolSys.has_attribute import has_attribute as molsys_has_attribute

    tmp_item = to_molsysmt_MolSys(molecular_system, skip_digestion=True)
    if tmp_item is None:
        return False

    return molsys_has_attribute(tmp_item, attribute, include_none=include_none, skip_digestion=True)
