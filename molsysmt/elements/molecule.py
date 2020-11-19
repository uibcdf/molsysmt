from molsysmt.utils.exceptions import *
import numpy as np

types=['water', 'ion', 'cosolute', 'small_molecule', 'peptide', 'protein', 'rna', 'dna', 'lipid']

def molecule_index_from_atom(item, indices='all'):

    from molsysmt.multitool import get
    return get(item, target='atom', indices=indices, component_index=True)

def molecule_id_from_molecule(item, indices='all'):

    if indices is 'all':
        n_molecules = get_n_molecules_from_system(item)
        output = np.full(n_molecules, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

def molecule_name_from_molecule(item, indices='all'):

    if indices is 'all':
        n_molecules = get_n_molecules_from_system(item)
        output = np.full(n_molecules, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

def molecule_type_from_molecule(item, indices='all'):

    atom_indices_from_molecule = get_atom_index_from_molecule(item, indices=indices)

    output = []

    for atom_indices in atom_indices_from_molecule:
        molecule_type = _get_type_from_atoms(item, atom_indices)
        output.append(molecule_type)

    output = np.array(output, dtype=object)

    return output

def n_molecules_from_system(item, indices='all'):

    output = get_molecule_index_from_atom(item, indices='all')
    if output[0] is None:
        n_molecules = 0
    else:
        output = np.unique(output)
        n_molecules = output.shape[0]
    return n_molecules

def _get_type_from_atoms(item, indices):

    from molsysmt import get
    group_indices = get(item, target='atom', indices=indices, group_index=True)
    group_indices = np.unique(group_indices)
    return _get_type_from_groups(item, group_indices)

def _get_type_from_groups(item, indices):

    from molsysmt import get
    group_names = get(item, target='group', indices=indices, name=True)
    return _get_type_from_group_names(group_names)

def _get_type_from_group_names(group_names):

    from .group import name_to_type as group_name_to_group_type
    from .group import dna_names as dna_group_names
    from .group import rna_names as rna_group_names

    tmp_type = None

    group_types = [group_name_to_group_type(ii) for ii in group_names]

    n_groups = len(group_types)
    first_type = group_types[0]
    first_name = group_names[0]

    if not (np.array(group_types) == first_type).all():
        raise ValueError("Groups have different type")

    if first_type in ['water', 'ion', 'cosolute', 'small molecule', 'lipid']:
        tmp_type = first_type
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

def _get_type_from_sequence(sequence):

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

    index_array = get_molecule_index_from_atom(item, indices='all')
    id_array = get_molecule_id_from_atom(item, indices='all')
    name_array = get_molecule_name_from_atom(item, indices='all')
    type_array = get_molecule_type_from_atom(item, indices='all')

    return index_array, id_array, name_array, type_array

