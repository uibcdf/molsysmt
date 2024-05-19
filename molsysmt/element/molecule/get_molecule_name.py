from molsysmt._private.digestion import digest
import numpy as np


@digest()
def get_molecule_name(molecular_system, element='atom', selection='all', redefine_molecules=False,
                       redefine_names=False, syntax='MolSysMT', skip_digestion=False):

    if redefine_molecules or redefine_names:

        from ..component import get_component_name, get_component_index

        component_names_from_component = get_component_name(molecular_system, element='component',
                            selection='all', redefine_names=True, syntax='MolSysMT')

        molecule_names_from_component = component_names_from_component

        if element == 'atom':

            component_indices_from_atom = get_component_index(molecular_system, element='atom',
                    selection=selection, redefine_indices=redefine_molecules, syntax=syntax)

            output = [molecule_names_from_component[ii] for ii in component_indices_from_atom]

        elif element == 'group':

            component_indices_from_group = get_component_index(molecular_system, element='group',
                    selection=selection, redefine_indices=redefine_molecules, syntax=syntax)

            output = [molecule_names_from_component[ii] for ii in component_indices_from_group]

        elif element == 'component':

            component_indices_from_component = get_component_index(molecular_system,
                    element='component', selection=selection, redefine_indices=redefine_molecules,
                    syntax=syntax)

            output = [molecule_names_from_component[ii] for ii in component_indices_from_component]

        elif element == 'molecule':

            component_indices_from_component = get_component_index(molecular_system,
                    element='component', selection=selection, redefine_indices=redefine_molecules,
                    syntax=syntax)

            output = [molecule_names_from_component[ii] for ii in component_indices_from_component]

        elif element == 'entity':

            component_indices_from_entity = get_component_index(molecular_system,
                    element='entity', selection=selection, redefine_indices=redefine_molecules,
                    syntax=syntax)

            output = []
            for aux in component_indices_from_entity:
                output.append([molecule_names_from_component[ii] for ii in aux])

        else:

            raise NotImplementedError

    else:

        from molsysmt.basic import get

        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_name=True)

    return output

