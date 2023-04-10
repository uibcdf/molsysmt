import numpy as np
import numba as nb
import networkx as nx

def component_indices(atom_indices):

    g = nx.from_edgelist(atom_indices)
    components = list(nx.connected_components(g))

    output = np.empty((g.number_of_nodes()), dtype=int)

    component_index=0
    for component in components:
        output[list(component)]=component_index
        component_index+=1

    _jit_reindexing_sorted(output, component_index)

    return output

@nb.jit(nb.void(nb.int64[:],nb.int64), nopython=True)
def _jit_reindexing_sorted(component_indices, n_components):

    aux = np.zeros((n_components), dtype=nb.int64)
    mask = np.zeros((n_components), dtype=nb.boolean)

    new_index = 0
    for ii in component_indices:
        if not mask[ii]:
            mask[ii]=True
            aux[ii]=new_index
            new_index+=1

    for ii in range(component_indices.shape[0]):
        component_indices[ii]=aux[component_indices[ii]]

    pass

