from molsysmt._private.argdigest import arg_digest


@arg_digest(form='file:molsys_yaml')
def to_molsysmt_MolSys(item, skip_digestion=False):
    """
    Converting from file:molsys_yaml to molsysmt.MolSys.

    Parameters
    ----------
    item : file:molsys_yaml
        Source item in file:molsys_yaml form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.

    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_MolSysDict import to_molsysmt_MolSysDict
    from molsysmt.form.molsysmt_MolSysDict.to_molsysmt_MolSys import to_molsysmt_MolSys as dict_to_molsys

    tmp_item = to_molsysmt_MolSysDict(item, skip_digestion=True)
    return dict_to_molsys(tmp_item, skip_digestion=True)
