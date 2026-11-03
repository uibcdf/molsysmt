from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:topology_yaml")
def to_molsysmt_MolSys(item, atom_indices="all", skip_digestion=False):
    """Converting declared inventory and chemistry to independent native domains.

    Parameters
    ----------
    item : molecular system
        Source form supplying its declared atom inventory and connectivity.
    atom_indices : str or array-like of int, default='all'
        Source atom indices to retain together with their induced chemistry.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    molsysmt.MolSys
        Native domains preserving available source chemistry without coordinates.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_TopologyDict.to_molsysmt_MolSys import (
        to_molsysmt_MolSys as decode,
    )

    from .to_molsysmt_TopologyDict import to_molsysmt_TopologyDict

    return decode(
        to_molsysmt_TopologyDict(item, skip_digestion=True),
        atom_indices=atom_indices,
        skip_digestion=True,
    )
