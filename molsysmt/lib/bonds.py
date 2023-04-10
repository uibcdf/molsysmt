import numpy as np
import numba as nb
import networkx as nx

def component_indices(atom_indices):

    g = nx.Graph(atom_indices)
    components = list(nx.connected_components(g)) 
    output = _sorted_component_indices(components, g.number_of_nodes)

    return output

@nb.jit(nb.types.Array(nb.int64, 1, "C")(nb.types.List(nb.types.Set(nb.int64)),nb.int64), nopython=True)
def _sorted_component_indices(components, n_atoms):

    output = np.empty([n_atoms], dtype=int)

    component_index=0
    for component in components:
        output[component]=component_index
        component_index+=1

    
    aux_dict=dict()
    component_index=0
    for ii in range(n_atoms):
        try:
            output[ii]=aux_dict[output[ii]]
        except:
            aux_dict[output[ii]]=component_index
            output[ii]=component_index
            component_index+1

    return output

