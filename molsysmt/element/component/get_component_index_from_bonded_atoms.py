import numpy as np
import networkx as nx
from molsysmt import lib as msmlib

def get_component_index_from_bonded_atoms(bonded_atoms, n_atoms):

    g = nx.Graph() 
    g.add_nodes_from(range(n_atoms))
    g.add_edges_from(bonded_atoms)
    components = list(nx.connected_components(g))

    output = np.empty((g.number_of_nodes()), dtype=int)

    component_index=0
    for component in components:
        output[list(component)]=component_index
        component_index+=1

    output=msmlib.series.occurrence_order(output)

    return output

