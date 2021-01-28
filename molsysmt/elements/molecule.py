from molsysmt._private_tools.exceptions import *
import numpy as np
from .group import rna_names as rna_group_names, dna_names as dna_group_names

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

    from molsysmt.multitool import get

    group_types_from_molecule = get(item, target='molecule', indices=indices, group_type=True)

    output = []

    for group_types in group_types_from_molecule:
        molecule_type = _type_from_group_type(group_types)
        output.append(molecule_type)

    output = np.array(output, dtype=object)

    return output

def n_molecules_from_system(item, indices='all'):

    from molsysmt import get

    molecule_index_from_atom = get(item, target='atom', indices='all', molecule_index=True)
    if molecule_index_from_atom[0] is None:
        n_molecules = 0
    else:
        output = np.unique(molecule_index_from_atom)
        n_molecules = output.shape[0]
    return n_molecules


def _type_from_group_type(group_types):

    n_groups = len(group_types)
    first_type = group_types[0]

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


def _shortpath_to_build_molecules(component_index_from_atom, component_type_from_atom):

    n_atoms=component_index_from_atom.shape[0]
    index_array = component_index_from_atom.copy()
    id_array = np.full(n_atoms, None, dtype=object)
    name_array = np.full(n_atoms, None, dtype=object)
    type_array = component_type_from_atom.copy()

    return index_array, id_array, name_array, type_array



