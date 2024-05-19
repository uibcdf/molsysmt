from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np
import pandas as pd

@digest()
def get_component_type(molecular_system, element='atom', selection='all', redefine_indices=False,
                       redefine_types=False, syntax='MolSysMT', skip_digestion=False):

    from molsysmt.basic import get

    if redefine_indices or redefine_types:

        from molsysmt.basic import select
        from .get_component_index import get_component_index

        if redefine_indices:

            component_indices = get_component_index(molecular_system, element='atom',
                                                    selection='all', redefine_indices=True,
                                                    skip_digestion=True)

            group_index_per_atom = get(molecular_system, element='atom', selection='all', group_index=True,
                                       skip_digestion=True)

            group_names, group_types = get(molecular_system, element='group', selection='all', group_name=True,
                                           group_type=True, skip_digestion=True)

            group_names = np.array(group_names)
            group_types = np.array(group_types)


            aux_df = pd.DataFrame({'component_indices':component_indices, 'group_indices':group_index_per_atom})
            aux_dict = aux_df.groupby('component_indices')['group_indices'].unique().to_dict()
            
            component_types={}

            for component_index, group_indices in aux_dict.items():

                component_type = _get_component_type_from_group_names_and_types(group_names[group_indices],
                                                                                group_types[group_indices])

                component_types[component_index]=component_type

            if element == 'atom':

                atom_indices = select(molecular_system, element='atom', selection=selection,
                                      syntax=syntax, skip_digestion=True)
                output = [component_types[component_indices[ii]] for ii in atom_indices]

            elif element == 'group':

                output = []
                group_indices = get(molecular_system, element='atom',
                                        selection=selection, group_indices=True, skip_digestion=True)
                former_index = -1
                for ii,jj,kk in zip(group_indices, atom_indices, component_indices):
                    if ii!=former_index:
                        output.append(component_types[kk])

                del(group_indices)

            elif element == 'component':

                if is_all(selection):
                    output = list(component_types.values())
                else:
                    raise NotImplementedError

            else:

                raise NotImplementedError

            del component_types, component_indices, group_index_per_atom, group_names, group_types

        else:

            pass

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     component_type=True, skip_digestion=True)

    return output


def _get_component_type_from_group_names_and_types(group_names, group_types):

    from molsysmt.config import min_length_protein

    n_groups = len(group_types)
    first_group_type = group_types[0]
    last_group_type = group_types[-1]
    first_group_name = group_names[0]

    if first_group_type in ['water', 'ion', 'small molecule', 'lipid']:
        tmp_type = first_group_type
    elif (first_group_type == 'amino acid') or (first_group_type == 'terminal capping'):
        if first_group_type == 'terminal capping':
            n_groups -= 1
        if last_group_type == 'terminal capping':
            n_groups -= 1
        if n_groups >= min_length_protein:
            tmp_type = 'protein'
        else:
            tmp_type = 'peptide'
    elif first_group_type == 'nucleotide':
        if first_group_name in rna_names:
            tmp_type = 'rna'
        elif first_group_name in dna_names:
            tmp_type = 'dna'
    else:
        tmp_type = 'unknown'

    return tmp_type

