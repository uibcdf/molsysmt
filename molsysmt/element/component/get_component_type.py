from molsysmt._private.digestion import digest
import numpy as np


@digest()
def get_component_type(molecular_system, element='atom', selection='all', redefine_components=False,
                       redefine_types=False, syntax='MolSysMT'):

    if redefine_components:

        from .get_component_index import get_component_index
        from molsysmt.basic import get

        component_indices = get_component_index(molecular_system, element='group',
                                                selection=selection, redefine_components=True,
                                                syntax=syntax)

        group_types = get(molecular_system, element='group', selection=selection,
                          syntax=syntax, group_name=True, group_type=True)



        if element == 'atom':
            from molsysmt.basic import get
            n_atoms = get(molecular_system, element='atom', selection=selection, syntax=syntax)
            output = np.full(n_atoms, None, dtype=object).to_list()
        elif element == 'group':
            from molsysmt.basic import get
            n_groups = get(molecular_system, element='group', selection=selection, syntax=syntax)
            output = np.full(n_groups, None, dtype=object).to_list()
        elif element == 'component':
            from .get_n_components import get_n_components
            n_components = get_n_components(molecular_system, selection=selection, redefine_components=True,
                                            syntax=syntax)
            output = np.full(n_components, None, dtype=object).to_list()
        else:
            raise NotImplementedError

    elif redefine_types:

        if element == 'atom':
            from molsysmt.basic import get
            n_atoms = get(molecular_system, element='atom', selection=selection, syntax=syntax)
            output = np.full(n_atoms, None, dtype=object).to_list()
        elif element == 'group':
            from molsysmt.basic import get
            n_groups = get(molecular_system, element='group', selection=selection, syntax=syntax)
            output = np.full(n_groups, None, dtype=object).to_list()
        elif element == 'component':
            from .get_n_components import get_n_components
            n_components = get_n_components(molecular_system, selection=selection, redefine_components=False,
                                            syntax=syntax)
            output = np.full(n_components, None, dtype=object).to_list()
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
