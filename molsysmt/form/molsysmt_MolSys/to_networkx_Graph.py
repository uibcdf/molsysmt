from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_networkx_Graph(item, atom_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to networkx.Graph.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    networkx.Graph
        Resulting object in networkx.Graph form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_Topology.to_networkx_Graph import to_networkx_Graph as molsysmt_Topology_to_networkx_Graph

    return molsysmt_Topology_to_networkx_Graph(item.topology, atom_indices=atom_indices, skip_digestion=True)
