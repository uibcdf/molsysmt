from molsysmt._private.digestion import digest
import numpy as np


@digest()
def get_component_type(molecular_system, element='atom', selection='all', redefine_components=False,
                       redefine_types=False, syntax='MolSysMT'):

    from molsysmt.basic import get
    from .get_component_index import get_component_index

    if redefine_components:

        component_indices = get_component_index(molecular_system, element='group',
                                                selection=selection, redefine_indices=True,
                                                syntax=syntax)

        group_names, group_types = get(molecular_system, element='group', selection=selection,
                                       syntax=syntax, group_name=True, group_type=True)

        counts = np.unique(component_indices, return_counts=True)

        component_types_from_component = []

        kk=0
        for count in counts:
            ll=kk+count
            component_type = _get_component_type_from_group_names_and_types(group_names[kk:ll], group_types[kk:ll])
            component_types_from_component.append(component_type)
            kk=ll

        del group_names, group_types, counts

        if element == 'atom':
            aux = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                    component_index=True)
            output = np.array(component_types_from_component, dtype=object)[aux].tolist()
        elif element == 'group':
            aux = get(molecular_system, element='group', selection=selection, syntax=syntax,
                    component_index=True)
            output = np.array(component_types_from_component, dtype=object)[aux].tolist()
        elif element == 'component':
            output = component_types_from_component
        else:
            raise NotImplementedError

    elif redefine_types:

        group_names, group_types = get(molecular_system, element='component', selection=selection,
                                       syntax=syntax, group_name=True, group_type=True)

        component_types_from_component =  [_get_component_type_from_group_names_and_types(ii, jj)
                for ii,jj in zip(group_names, group_types)]

        if element == 'atom':
            aux = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                    component_index=True)
            output = np.array(component_types_from_component, dtype=object)[aux].tolist()
        elif element == 'group':
            aux = get(molecular_system, element='group', selection=selection, syntax=syntax,
                    component_index=True)
            output = np.array(component_types_from_component, dtype=object)[aux].tolist()
        elif element == 'component':
            output = component_types_from_component
        else:
            raise NotImplementedError

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     component_type=True)

    return output


def _get_component_type_from_group_names_and_types(group_names, group_types):

    from molsysmt.config import min_length_protein

    n_groups = len(group_types)
    first_type = group_types[0]
    last_type = group_types[-1]

    if first_type in ['water', 'ion', 'small molecule', 'lipid']:
        tmp_type = first_type
    elif (first_type == 'amino acid') or (first_type == 'terminal capping'):
        if first_type == 'terminal capping':
            n_groups -= 1
        if last_type == 'terminal capping':
            n_groups -= 1
        if n_groups >= min_length_protein:
            tmp_type = 'protein'
        else:
            tmp_type = 'peptide'
    elif first_type == 'nucleotide':
        if group_names[0] in rna_names:
            tmp_type = 'rna'
        elif group_names[0] in dna_names:
            tmp_type = 'dna'
    else:
        tmp_type = 'unknown'

    return tmp_type
