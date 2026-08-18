from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSysBuilder")
def to_molsysmt_MolSysBuilder(item, skip_digestion=False):
    """
    Converting from molsysmt.MolSysBuilder to molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolSysBuilder
        Converted molecular system representation.
    """
    return item.copy()
