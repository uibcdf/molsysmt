from molsysmt._private.digestion import digest
import numpy as np

from .cosolute.get_name_from_mmtf_name import mmtf_translator as mmtf_translator_cosolute
from .ion.get_name_from_mmtf_name import mmtf_translator as mmtf_translator_ion
from .lipid.get_name_from_mmtf_name import mmtf_translator as mmtf_translator_lipid
from .peptide.get_name_from_mmtf_name import mmtf_translator as mmtf_translator_peptide
from .protein.get_name_from_mmtf_name import mmtf_translator as mmtf_translator_protein
from .dna.get_name_from_mmtf_name import mmtf_translator as mmtf_translator_dna
from .rna.get_name_from_mmtf_name import mmtf_translator as mmtf_translator_rna
from .small_molecule.get_name_from_mmtf_name import mmtf_translator as mmtf_translator_small_molecule
from .water.get_name_from_mmtf_name import mmtf_translator as mmtf_translator_water

mmtf_translator={}

mmtf_translator.update(mmtf_translator_cosolute)
mmtf_translator.update(mmtf_translator_ion)
mmtf_translator.update(mmtf_translator_lipid)
mmtf_translator.update(mmtf_translator_peptide)
mmtf_translator.update(mmtf_translator_protein)
mmtf_translator.update(mmtf_translator_rna)
mmtf_translator.update(mmtf_translator_dna)
mmtf_translator.update(mmtf_translator_small_molecule)
mmtf_translator.update(mmtf_translator_water)

@digest()
def get_entity_type_from_MMTFDecoder_entity(mmtf_entity):

    from . import get_entity_type_from_entity_name
    from . import get_entity_type_from_sequence

    output = None

    if mmtf_entity['type']=='water':
        return 'water'
    elif mmtf_entity['type']=='polymer':
        return get_entity_type_from_sequence(mmtf_entity['sequence'])
    elif mmtf_entity['type']=='non-polymer':
        try:
            entity_name = mmtf_translator[mmtf_entity['description']]
            output = get_entity_type_from_entity_name(entity_name)
        except:
            if 'ION' in mmtf_entity['description']:
                return 'ion'
            else:
                return 'small molecule'
                #raise NotImplementedError("The mmtf entity type {} is not implemented.".format(mmtf_entity))

    return output

