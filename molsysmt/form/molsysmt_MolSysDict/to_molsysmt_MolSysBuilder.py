from molsysmt._private.argdigest import arg_digest

from ._builder import build_molsys_builder_from_molsys_dict


@arg_digest(form="molsysmt.MolSysDict")
def to_molsysmt_MolSysBuilder(item, skip_digestion=False):
    """
    Converting from molsysmt.MolSysDict to molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysDict
        Source item in molsysmt.MolSysDict form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSysBuilder
        Resulting object in molsysmt.MolSysBuilder form.

    .. versionadded:: 1.0.0
    """

    return build_molsys_builder_from_molsys_dict(item)
