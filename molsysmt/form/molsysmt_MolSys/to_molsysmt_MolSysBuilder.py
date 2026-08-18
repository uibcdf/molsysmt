from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSys")
def to_molsysmt_MolSysBuilder(item, atom_indices="all", structure_indices="all", skip_digestion=False):
    """
    Converting from molsysmt.MolSys to molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolSysBuilder
        Converted molecular system representation.
    """

    from molsysmt.native import MolSysBuilder

    molsys = item.extract(
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=True,
        skip_digestion=True,
    )

    return MolSysBuilder(molsys, skip_digestion=True)
