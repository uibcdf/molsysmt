from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSysBuilder")
def to_molsysmt_MolSys(item, atom_indices="all", structure_indices="all", copy_if_all=True, skip_digestion=False):
    """
    Converting from molsysmt.MolSysBuilder to molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.


    .. versionadded:: 1.0.0
    """

    if atom_indices != "all" or structure_indices != "all":
        return item.build(skip_digestion=True).extract(
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            copy_if_all=copy_if_all,
            skip_digestion=True,
        )

    return item.build(skip_digestion=True)
