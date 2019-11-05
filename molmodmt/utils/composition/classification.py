from molmodmt.utils.exceptions import *

def MMTFDecoder_group_to_group_class(mmtf_group):

    from molmodmt import group_name_to_molecule_type

    molecule_type = group_name_to_molecule_type(mmtf_group['groupName'])
    if molecule_type == 'protein':
        return 'AminoAcid'
    elif molecule_type == 'dna':
        return 'Nucleotide'
    elif molecule_type == 'rna':
        return 'Nucleotide'
    elif molecule_type == 'ion':
        return 'Ion'
    elif molecule_type == 'water':
        return 'Water'
    else:
        return None

    pass

def MMTFDecoder_entity_to_entity_class(mmtf_entity):

    if mmtf_entity['type']=='water':
        return 'Water'
    elif mmtf_entity['type']=='polymer':
        from molmodmt import sequence_to_molecule_type
        molecule_type = sequence_to_molecule_type(mmtf_entity['sequence'])
        if molecule_type == 'protein':
            return 'Protein'
        elif molecule_type == 'dna':
            return 'DNA'
        elif molecule_type == 'rna':
            return 'RNA'
        elif molecule_type == 'peptide':
            return 'Peptide'
        else:
            return None
    else:
        return None

    pass

