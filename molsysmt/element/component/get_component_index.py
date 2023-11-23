from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import networkx as nx
from molsysmt import lib as msmlib
import numpy as np


@digest()
def get_component_index(molecular_system, element='atom', selection='all', redefine_indices=False,
                        syntax='MolSysMT'):

    from molsysmt import get

    if redefine_indices:

        from molsysmt import convert

        component_index_of_atoms = None

        if is_all(selection):

            g = convert(molecular_system, to_form='networkx.Graph')

            components = list(nx.connected_components(g))

            aux_n_components = len(components)

            component_index_of_atoms = np.empty((g.number_of_nodes()), dtype=int)

            for component_index, component in enumerate(components):
                component_index_of_atoms[list(component)] = component_index

            component_index_of_atoms = msmlib.series.occurrence_order(component_index_of_atoms)

        else:

            raise NotImplementedError

        if element == 'atom':

            output = component_index_of_atoms.tolist()

        elif element == 'group':

            group_index_of_atoms = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                                       group_index=True)
            group_index, first_atom_indices = np.unique(group_index_of_atoms, return_index=True)
            output = component_index_of_atoms[first_atom_indices].tolist()
            del group_index, group_index_of_atoms

        elif element == 'component':

            if is_all(selection):

                output = list(np.arange(aux_n_components, dtype=int))
                del component_index_of_atoms

            else:

                raise NotImplementedError

        else:

            raise NotImplementedError

    else:

        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     component_index=True)

    return output
