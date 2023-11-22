import networkx as nx
from molsysmt import lib as msmlib
import numpy as np


def get_component_index(molecular_system):

    from molsysmt import convert

    g = convert(molecular_system, to_form='networkx.Graph')

    components = list(nx.connected_components(g))

    aux_n_components = len(components)

    component_index_of_atoms = np.empty((g.number_of_nodes()), dtype=int)

    for component_index, component in enumerate(components):
        component_index_of_atoms[list(component)]=component_index

    component_index_of_atoms=msmlib.series.occurrence_order(component_index_of_atoms)

    return component_index_of_atoms.tolist()

