from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_networkx_Graph(item, atom_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to networkx.Graph.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    networkx.Graph
        Converted molecular system representation.
    """

    from molsysmt.form.molsysmt_Topology.to_networkx_Graph import to_networkx_Graph as molsysmt_Topology_to_networkx_Graph

    return molsysmt_Topology_to_networkx_Graph(item.topology, atom_indices=atom_indices, skip_digestion=True)
