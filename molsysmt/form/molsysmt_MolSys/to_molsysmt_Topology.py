from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSys")
def to_molsysmt_Topology(item, atom_indices="all", skip_digestion=False):
    """
    Converting from molsysmt.MolSys to molsysmt.Topology.


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
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.

    Raises
    ------
    ValueError
        If the source MolSys has no topology domain.


    .. versionadded:: 1.0.0
    """

    if item.topology is None:
        raise ValueError("This MolSys has no topology domain to convert.")
    return item.topology.extract(atom_indices=atom_indices, skip_digestion=True)
