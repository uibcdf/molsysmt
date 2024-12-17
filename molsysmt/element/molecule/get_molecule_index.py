from molsysmt._private.digestion import digest


@digest()
def get_molecule_index(molecular_system, element='atom', selection='all',
        redefine_components=False, redefine_indices=False, syntax='MolSysMT', skip_digestion=False):

    if redefine_indices:

        from ..component import get_component_index

        component_indices_from_component = get_component_index(molecular_system, element='component',
                            selection='all', redefine_indices=redefine_components, syntax='MolSysMT')

        molecule_indices_from_component = component_indices_from_component

        if element == 'atom':

            component_indices_from_atom = get_component_index(molecular_system, element='atom',
                    selection=selection, redefine_indices=redefine_components, syntax=syntax)

            output = [molecule_indices_from_component[ii] for ii in component_indices_from_atom]

        elif element == 'group':

            component_indices_from_group = get_component_index(molecular_system, element='group',
                    selection=selection, redefine_indices=redefine_components, syntax=syntax)

            output = [molecule_indices_from_component[ii] for ii in component_indices_from_group]

        elif element == 'component':

            component_indices_from_component = get_component_index(molecular_system,
                    element='component', selection=selection, redefine_indices=redefine_components,
                    syntax=syntax)

            output = [molecule_indices_from_component[ii] for ii in component_indices_from_component]

        elif element == 'molecule':

            component_indices_from_component = get_component_index(molecular_system,
                    element='component', selection=selection, redefine_indices=redefine_components,
                    syntax=syntax)

            output = [molecule_indices_from_component[ii] for ii in component_indices_from_component]

        elif element == 'entity':

            component_indices_from_entity = get_component_index(molecular_system,
                    element='entity', selection=selection, redefine_indices=redefine_components,
                    syntax=syntax)

            output = []
            for aux in component_indices_from_entity:
                output.append([molecule_indices_from_component[ii] for ii in aux])

        else:

            raise NotImplementedError

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_index=True)

    return output

