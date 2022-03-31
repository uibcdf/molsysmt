
def get_entity_type_from_sequence(sequence):

    from molsysmt.elements.molecule.molecule import _get_type_from_sequence as molecule_type_from_sequence

    molecule_type = molecule_type_from_sequence(sequence)

    if molecule_type == 'protein':
        return 'protein'
    elif molecule_type == 'dna':
        return 'dna'
    elif molecule_type == 'rna':
        return 'rna'
    elif molecule_type == 'peptide':
        return 'peptide'
    else:
        return None

