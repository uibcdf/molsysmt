from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import networkx as nx


@digest(form='molsysmt.Topology')
def to_networkx_Graph(item, atom_indices='all', skip_digestion=False):

    g = nx.Graph()

    if is_all(atom_indices):

        g.add_nodes_from(range(item.atoms.shape[0]))
        g.add_edges_from(item.bonds[['atom1_index', 'atom2_index']].to_numpy())

    else:

        raise NotImplementedError

    return g
