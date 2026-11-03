from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:smi")
@dep_digest("rdkit")
def to_molsysmt_MolSys(item, atom_indices="all", skip_digestion=False):
    """
    Converting from file:smi to molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.rdkit_Mol.to_molsysmt_MolSys import (
        to_molsysmt_MolSys as rdkit_to_molsys,
    )

    from .to_rdkit_Mol import to_rdkit_Mol

    tmp_item = to_rdkit_Mol(item, skip_digestion=True)

    return rdkit_to_molsys(
        tmp_item,
        atom_indices=atom_indices,
        skip_digestion=True,
    )
