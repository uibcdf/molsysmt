from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import networkx as nx
import numpy as np

@digest(form='openmm.Topology')
def to_networkx_Graph(item, atom_indices='all'):

    g = nx.Graph()

    if is_all(atom_indices):

        g.add_nodes_from(range(item.getNumAtoms()))

        output=[[bond.atom1.index, bond.atom2.index] for bond in item.bonds()]
        g.add_edges_from(np.array(output))
        del output

    else:

        raise NotImplementedError

    return g
