def MMTFDecoder_group_to_group_class_type(mmtf_group):

    from molsysmt import group_name_to_molecule_type

    molecule_type = group_name_to_molecule_type(mmtf_group['groupName'])
    if molecule_type == 'protein':
        return 'aminoacid'
    elif molecule_type == 'dna':
        return 'nucleotide'
    elif molecule_type == 'rna':
        return 'nucleotide'
    elif molecule_type == 'ion':
        return 'ion'
    elif molecule_type == 'water':
        return 'water'
    else:
        return None

    pass

def MMTFDecoder_entity_to_entity_class_type(mmtf_entity):

    from molsysmt import sequence_to_molecule_type

    if mmtf_entity['type']=='water':
        return 'water'
    elif mmtf_entity['type']=='polymer':
        from molsysmt import sequence_to_molecule_type
        molecule_type = sequence_to_molecule_type(mmtf_entity['sequence'])
        if molecule_type == 'protein':
            return 'protein'
        elif molecule_type == 'dna':
            return 'dNA'
        elif molecule_type == 'rna':
            return 'rNA'
        elif molecule_type == 'peptide':
            return 'peptide'
        else:
            return None
    else:
        return None

    pass

