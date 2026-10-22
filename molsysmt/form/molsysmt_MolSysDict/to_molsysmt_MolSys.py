from molsysmt._private.argdigest import arg_digest

from ._builder import build_molsys_builder_from_molsys_dict


@arg_digest(form="molsysmt.MolSysDict")
def to_molsysmt_MolSys(
    item, skip_digestion=False, *, atom_indices="all", structure_indices="all"
):
    """
    Converting from molsysmt.MolSysDict to molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    atom_indices : str or array-like of int, default='all'
        Atom indices to retain, in sorted source order through dictionary extraction.
    structure_indices : str or array-like of int, default='all'
        Structure indices to retain, preserving their supplied order and repetitions.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.native import MolSys
    >>> data = msm.convert(MolSys(n_atoms=2), to_form='molsysmt.MolSysDict')
    >>> to_molsysmt_MolSys(data, atom_indices=[1]).topology.n_atoms
    1


    .. versionadded:: 1.0.0
    """

    from .extract import extract

    item = extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=False,
        skip_digestion=True,
    )
    return build_molsys_builder_from_molsys_dict(item).build(skip_digestion=True)
