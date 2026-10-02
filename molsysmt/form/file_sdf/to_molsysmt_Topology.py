from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:sdf")
def to_molsysmt_Topology(
    item, atom_indices="all", discard_properties=False, skip_digestion=False
):
    """Converting a single SDF record into topology and explicit chemistry.

    Parameters
    ----------
    item : str or pathlib.Path
        Single-record SDF input file.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    discard_properties : bool, default=False
        Explicitly authorize discarding SD property blocks without native storage.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Topology with the explicit source graph and chemical-state facade.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    return to_molsysmt_MolSys(
        item,
        atom_indices=atom_indices,
        discard_properties=discard_properties,
        skip_digestion=True,
    ).topology
