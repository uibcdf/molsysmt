from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSysBuilder")
def to_molsysmt_MolSysBuilder(item, skip_digestion=False):
    """
    Converting from molsysmt.MolSysBuilder to molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSysBuilder
        Resulting object in molsysmt.MolSysBuilder form.

    .. versionadded:: 1.0.0
    """
    return item.copy()
