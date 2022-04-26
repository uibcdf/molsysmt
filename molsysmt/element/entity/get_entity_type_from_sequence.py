
def get_entity_type_from_sequence(sequence):

    from molsysmt.element.molecule import get_molecule_type_from_sequence

    molecule_type = get_molecule_type_from_sequence(sequence)

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

