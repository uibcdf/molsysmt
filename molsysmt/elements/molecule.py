from molsysmt.utils.exceptions import *

types=['water', 'ion', 'cosolute', 'small_molecule', 'peptide', 'protein', 'rna', 'dna', 'lipid']

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

