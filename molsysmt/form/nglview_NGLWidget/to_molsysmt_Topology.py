from molsysmt._private.argdigest import arg_digest


@arg_digest(form="nglview.NGLWidget")
def to_molsysmt_Topology(
    item, atom_indices="all", get_missing_bonds=True, skip_digestion=False
):
    """
    Converting from nglview.NGLWidget to molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    get_missing_bonds : object, default=True
        Argument get_missing_bonds.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.


    .. versionadded:: 1.0.0
    """

    from ._read_native import read_native
    from ._topology_sidecar import get_topology_sidecar

    inventory = get_topology_sidecar(item)
    if inventory is not None:
        return inventory.extract(
            atom_indices=atom_indices, copy_if_all=True, skip_digestion=True
        )

    return read_native(
        item,
        atom_indices=atom_indices,
        get_missing_bonds=get_missing_bonds,
        skip_digestion=True,
    ).topology
