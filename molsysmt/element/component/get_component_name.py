from molsysmt._private.digestion import digest
import numpy as np


@digest()
def get_component_name(molecular_system, element='atom', selection='all', redefine_components=False,
                       redefine_names=False, syntax='MolSysMT'):

    if redefine_components or redefine_names:

        from .get_component_index import get_component_index
        from .get_component_type import get_component_type

        component_index_from_atom = get_component_index(molecular_system, element='atom',
            selection='all', syntax='MolSysMT', redefine_indices=redefine_components)

        _, first_atom_per_component, n_atoms_per_component = np.unique(component_index_from_atom,
                                                                       return_index=True, return_counts=True)

        component_type_from_component = get_component_type(molecular_system, element='component',
                selection='all', syntax='MolSysMT', redefine_components=redefine_components,
                redefine_types=True)

        counter = {'peptide':0, 'protein':0, 'small molecule':0, 'unknown':0}

        component_name_from_component = []

        for component_type, first_atom, n_atoms in zip(component_type_from_component, first_atom_per_component,
                                                       n_atoms_per_component):

            if component_type in ['peptide', 'protein', 'small molecule']:

                name = component_type+' '+str(counter[component_type])
                counter[component_type]+=1

            elif component_type in ['ion', 'lipid']:

                name = get(molecular_system, element='atom', selection=first_atom, group_name=True)[0]

            elif component_type in ['water']:

                name = 'water'

            else:

                name = 'unknown '+str(counter['unknown'])
                counter['unknown']+=1

            component_name_from_component.append(name)

        if element == 'atom':

            component_index_from_atom = get_component_index(molecular_system, element='atom',
            selection=selection, syntax=syntax, redefine_indices=redefine_components)

            output = [component_name_from_component[ii] for ii in component_index_from_atom]

        elif element == 'group':

            component_index_from_group = get_component_index(molecular_system, element='group',
            selection=selection, syntax=syntax, redefine_indices=redefine_components)

            output = [component_name_from_component[ii] for ii in component_index_from_group]

        elif element == 'component':

            component_index_from_component = get_component_index(molecular_system, element='component',
            selection=selection, syntax=syntax, redefine_indices=redefine_components)

            output = [component_name_from_component[ii] for ii in component_index_from_component]

        elif element == 'molecule':

            component_index_from_component = get_component_index(molecular_system, element='component',
            selection=selection, syntax=syntax, redefine_indices=redefine_components)

            output = [component_name_from_component[ii] for ii in component_index_from_component]

        elif element == 'entity':

            component_indices_from_entity = get_component_index(molecular_system,
                    element='entity', selection=selection, redefine_indices=redefine_components,
                    syntax=syntax)

            output = []
            for aux in component_indices_from_entity:
                output.append([component_name_from_component[ii] for ii in aux])

        else:

            raise NotImplementedError

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     component_name=True)

    return output
