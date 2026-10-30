from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSys")
def to_networkx_Graph(item, atom_indices="all", skip_digestion=False):
    """
    Converting from molsysmt.MolSys to networkx.Graph.


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
    networkx.Graph
        Resulting object in networkx.Graph form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.networkx_Graph._from_native import export_native

    return export_native(
        item.topology,
        atom_indices=atom_indices,
        chemical_states=item.chemical_states,
        skip_digestion=True,
    )
