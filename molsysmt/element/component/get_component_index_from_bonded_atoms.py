import numpy as np
import networkx as nx
from molsysmt.lib.math import occurrence_order

def get_component_index_from_bonded_atoms(bonded_atoms):

    g = nx.from_edgelist(bonded_atoms)
    components = list(nx.connected_components(g))

    output = np.empty((g.number_of_nodes()), dtype=int)

    component_index=0
    for component in components:
        output[list(component)]=component_index
        component_index+=1

    output=occurrence_order(output)

    return output

