import networkx as nx
from molsysmt import lib as msmlib
import numpy as np


def get_component_name(molecular_system, selection='all', component_index_of_atoms=None,
        syntax='MolSysMT'):

    from molsysmt import convert

    g = convert(molecular_system, to_form='networkx.Graph')

    components = list(nx.connected_components(g))

    aux_n_components = len(components)

    component_index_of_atoms = np.empty((g.number_of_nodes()), dtype=int)

    for component_index, component in enumerate(components):
        component_index_of_atoms[list(component)]=component_index

    component_index_of_atoms=msmlib.series.occurrence_order(component_index_of_atoms)

    output = [component_index_of_atoms.tolist()]

    if component_id:

        output.append(list(np.arange(aux_n_components)))

    if component_name:

        output.append(np.full(aux_n_components, None, dtype=object).tolist())

    if component_type:

        output.append(np.full(aux_n_components, None, dtype=object).tolist())

    if n_components:

        output.append(aux_n_components)

    if len(output)==1:

        output = output[0]

    return output
