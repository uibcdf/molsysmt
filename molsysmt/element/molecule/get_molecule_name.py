from molsysmt._private.digestion import arg_digest
import numpy as np


@arg_digest()
def get_molecule_name(molecular_system, element='molecule', selection='all', redefine_indices=False,
                       redefine_names=False, syntax='MolSysMT', skip_digestion=False):

    if redefine_indices or redefine_names:

        from ..component import get_component_name, get_component_index

        component_names_from_component = get_component_name(molecular_system, element='component',
                            selection='all', redefine_names=True, syntax='MolSysMT')

        molecule_names_from_component = component_names_from_component

        if element == 'atom':

            component_indices_from_atom = get_component_index(molecular_system, element='atom',
                    selection=selection, redefine_indices=redefine_indices, syntax=syntax)

            output = [molecule_names_from_component[ii] for ii in component_indices_from_atom]

        elif element == 'group':

            component_indices_from_group = get_component_index(molecular_system, element='group',
                    selection=selection, redefine_indices=redefine_indices, syntax=syntax)

            output = [molecule_names_from_component[ii] for ii in component_indices_from_group]

        elif element == 'component':

            component_indices_from_component = get_component_index(molecular_system,
                    element='component', selection=selection, redefine_indices=redefine_indices,
                    syntax=syntax)

            output = [molecule_names_from_component[ii] for ii in component_indices_from_component]

        elif element == 'molecule':

            component_indices_from_component = get_component_index(molecular_system,
                    element='component', selection=selection, redefine_indices=redefine_indices,
                    syntax=syntax)

            output = [molecule_names_from_component[ii] for ii in component_indices_from_component]

        elif element == 'entity':

            component_indices_from_entity = get_component_index(molecular_system,
                    element='entity', selection=selection, redefine_indices=redefine_indices,
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


#from molsysmt.element.group.small_molecule import group_names as small_molecule_names
#from molsysmt.element.group.saccharide import group_names as saccharide_names

#aux_df = self.groups.groupby('component_index').agg(group_name=('group_name', list),
#                                                    group_type=('group_type', list))

#component_types = self.components['component_type'].to_numpy()

#counter = {'peptide':0, 'protein':0, 'small molecule':0, 'saccharide':0, 'unknown':0}

#peptides = {}
#proteins = {}
#small_molecules = {}
#saccharides = {}

#for component_type, row in zip(component_types, aux_df.itertuples(index=True)):
#
#    if component_type == 'peptide':

#        string_peptide = ','.join(row.group_name)

#        if string_peptide in peptides:
#            component_name = peptides[string_peptide]
#        else:
#            component_name = component_type+' '+str(counter[component_type])
#            peptides[string_peptide] = component_name
#            counter[component_type] += 1

#    elif component_type == 'protein':

#        string_protein = ','.join(row.group_name)

#        if string_protein in proteins:
#            component_name = proteins[string_protein]
#        else:
#            component_name = component_type+' '+str(counter[component_type])
#            proteins[string_protein] = component_name
#            counter[component_type] += 1

#    elif component_type == 'small molecule':

#        group_name = row.group_name[0]

#        if group_name in small_molecules:
#            component_name = small_molecules[group_name]
#        else:
#            if group_name in small_molecule_names:
#                component_name = group_name
#            else:
#                component_name = group_name
#            small_molecules[component_name] = component_name

#    elif component_type == 'saccharide':

#        group_name = row.group_name[0]

#        if group_name in saccharides:
#            component_name = saccharides[group_name]
#        else:
#            if group_name in saccharide_names:
#                component_name = group_name
#            else:
#                component_name = group_name
#            saccharides[component_name] = component_name

#    elif component_type in ['ion', 'lipid']:

#        component_name = row.group_name[0]

#    elif component_type in ['water']:

#        component_name = 'water'

#    else:

#        component_name = 'unknown '+str(counter['unknown'])
#        counter['unknown']+=1

#    self.components.iloc[row.Index,1] = component_name
 
