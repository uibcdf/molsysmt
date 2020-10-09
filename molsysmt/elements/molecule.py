from molsysmt.utils.exceptions import *
import numpy as np

types=['water', 'ion', 'cosolute', 'small_molecule', 'peptide', 'protein', 'rna', 'dna', 'lipid']

def type_from_atoms(item, indices):

    from molsysmt import get
    group_indices = get(item, target='atom', indices=indices, group_index=True)
    group_indices = np.unique(group_indices)
    return type_from_groups(item, group_indices)

def type_from_groups(item, indices):

    from molsysmt import get
    group_names = get(item, target='group', indices=indices, name=True)
    return type_from_group_names(group_names)

def type_from_components(item, indices):

    from molsysmt import get
    group_indices = get(item, target='component', indices=indices, group_index=True)
    group_indices = np.ravel(group_indices)
    return type_from_groups(item, group_indices)

def type_from_group_names(group_names):

    from .groups import name_to_type as group_name_to_group_type
    from .groups import dna_names as dna_group_names
    from .groups import rna_names as rna_group_names

    tmp_type = None

    group_types = [group_name_to_group_type(ii) for ii in group_names]

    n_groups = len(group_types)
    first_type = group_types[0]
    first_name = group_names[0]

    if not (np.array(group_types) == first_type):
        raise ValueError("Groups have different type")

    if first_type in ['water', 'ion', 'cosolute', 'small molecule', 'lipid']:
        tmp_type = group_type
    elif first_type == 'aminoacid':
        if n_groups>=50:
            tmp_type='protein'
        else:
            tmp_type='peptide'
    elif first_type == 'nucleotide':
        if first_name in rna_group_names:
            tmp_type = 'rna'
        elif first_name in dna_group_names:
            tmp_type = 'dna'

    return tmp_type

def type_from_sequence(sequence):

    tmp_type='unknown'

    n_Gs = sequence.count('G')
    n_As = sequence.count('A')
    n_Ts = sequence.count('T')
    n_Cs = sequence.count('C')
    n_Us = sequence.count('U')

    n_letters = len(sequence)

    if n_Gs+n_As+n_Ts+n_Cs == n_letters:
        return 'dna'
    elif n_Gs+n_As+n_Us+n_Cs == n_letters:
        return 'rna'
    else:
        return 'protein'

    return tmp_type

def get_elements(item):

    from molsysmt import get

    component_index, component_id, component_name, component_type = get(item, target='atom',
                                                                        component_index=True,
                                                                        component_id=True,
                                                                        component_name=True,
                                                                        component_type=True)

    molecule_index = component_index
    molecule_id = component_id
    molecule_name = component_name
    molecule_type = component_type

    return molecule_index, molecule_id, component_name, component_type

