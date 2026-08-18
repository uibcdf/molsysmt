from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSys")
def to_molsysmt_MolSysBuilder(item, atom_indices="all", structure_indices="all", skip_digestion=False):
    """
    Converting from molsysmt.MolSys to molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSysBuilder
        Resulting object in molsysmt.MolSysBuilder form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native import MolSysBuilder

    molsys = item.extract(
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=True,
        skip_digestion=True,
    )

    return MolSysBuilder(molsys, skip_digestion=True)
