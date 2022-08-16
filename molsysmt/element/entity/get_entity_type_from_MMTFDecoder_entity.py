from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_entity_type_from_MMTFDecoder_entity(mmtf_entity):

    from . import get_entity_type_from_sequence

    if mmtf_entity['type']=='water':
        return 'water'
    elif mmtf_entity['type']=='polymer':
        return get_entity_type_from_sequence(mmtf_entity['sequence'])
    elif mmtf_entity['type']=='non-polymer':
        if 'ION' in mmtf_entity['description'].split(' '):
            return 'ion'
        else:
            return 'small molecule'
    elif mmtf_entity['type']=='branched':
        return 'oligosaccharide'

    raise NotImplementedError("The mmtf entity type {} is not implemented.".format(mmtf_entity))

