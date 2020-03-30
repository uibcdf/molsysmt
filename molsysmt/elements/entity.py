from molsysmt.utils.exceptions import *

types = ["water", "ion", "cosolute", "protein", "peptide", "rna", "dna"]

def type_from_MMTFDecoder_entity (mmtf_entity):

    if mmtf_entity['type']=='water':
        return 'water'
    elif mmtf_entity['type']=='polymer':
        return type_from_sequence(mmtf_entity['sequence'])
    else:
        return None

    pass

def type_from_sequence(sequence):

    from .molecule import type_from_sequence as molecule_type_from_sequence

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

