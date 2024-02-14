from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_component_name(molecular_system, element='atom', selection='all', redefine_indices=False,
                       redefine_names=False, syntax='MolSysMT', skip_digestion=False):

    if redefine_indices or redefine_names:

        from .get_component_index import get_component_index
        from .get_component_type import get_component_type
        from molsysmt import get

        if redefine_indices:
            redefine_names=True
            redefine_types=True
        else:
            redefine_types=False

        import time
        start=time.time()

        component_index_from_atom = get_component_index(molecular_system, element='atom',
            selection='all', syntax='MolSysMT', redefine_indices=redefine_indices, skip_digestion=True)

        _, first_atom_per_component, n_atoms_per_component = np.unique(component_index_from_atom,
                                                                       return_index=True, return_counts=True)

        component_type_from_component = get_component_type(molecular_system, element='component',
                selection='all', syntax='MolSysMT', redefine_indices=False,
                redefine_types=redefine_types, skip_digestion=True)

        counter = {'peptide':0, 'protein':0, 'small molecule':0, 'unknown':0}

        peptides = {}

        component_name_from_component = []
        
        end = time.time()
        print('<<<', end-start)

        start=time.time()

        for component_type, first_atom, n_atoms in zip(component_type_from_component, first_atom_per_component,
                                                       n_atoms_per_component):
            
            if component_type in ['peptide']:

                atom_indices_peptide = np.arange(n_atoms) + first_atom
                selection_peptide = 'atom_index in @atom_indices_peptide'
                group_names = get(molecular_system, element='group', selection=selection_peptide,
                                  group_name=True, skip_digestion=True)
                string_peptide = ','.join(group_names)

                if string_peptide in peptides:
                    name = peptides[string_peptide]
                else:
                    name = component_type+' '+str(counter[component_type])
                    peptides[string_peptide] = name
                    counter[component_type] += 1

            elif component_type in ['protein', 'small molecule']:

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
            selection=selection, syntax=syntax, redefine_indices=redefine_indices)

            output = [component_name_from_component[ii] for ii in component_index_from_atom]

        elif element == 'group':

            component_index_from_group = get_component_index(molecular_system, element='group',
            selection=selection, syntax=syntax, redefine_indices=redefine_indices)

            output = [component_name_from_component[ii] for ii in component_index_from_group]

        elif element == 'component':

            component_index_from_component = get_component_index(molecular_system, element='component',
            selection=selection, syntax=syntax, redefine_indices=False, skip_digestion=True)

            output = [component_name_from_component[ii] for ii in component_index_from_component]

        elif element == 'molecule':

            component_index_from_component = get_component_index(molecular_system, element='component',
            selection=selection, syntax=syntax, redefine_indices=redefine_indices)

            output = [component_name_from_component[ii] for ii in component_index_from_component]

        elif element == 'entity':

            component_indices_from_entity = get_component_index(molecular_system,
                    element='entity', selection=selection, redefine_indices=redefine_indices,
                    syntax=syntax)

            output = []
            for aux in component_indices_from_entity:
                output.append([component_name_from_component[ii] for ii in aux])

        else:

            raise NotImplementedError

        end = time.time()
        print('>>>', end-start)

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     component_name=True)

    return output
