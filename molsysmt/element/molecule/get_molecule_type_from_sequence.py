def get_molecule_type_from_sequence(sequence):

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

