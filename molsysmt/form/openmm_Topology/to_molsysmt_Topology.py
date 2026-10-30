from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openmm.Topology")
def to_molsysmt_Topology(
    item, atom_indices="all", get_missing_bonds=True, skip_digestion=False
):
    """
    Converting from openmm.Topology to molsysmt.Topology.


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

    return read_native(item, atom_indices=atom_indices, skip_digestion=True).topology
