from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_networkx_Graph(item, atom_indices='all', skip_digestion=False):

    from ..molsysmt_Topology import to_networkx_Graph as molsysmt_Topology_to_networkx_Graph

    return molsysmt_Topology_to_networkx_Graph(item.topology, atom_indices=atom_indices, skip_digestion=True)
