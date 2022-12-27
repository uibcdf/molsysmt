from molsysmt._private.digestion import digest
from .ion.names import names as ion_names
from .lipid.names import names as lipid_names
from .peptide.names import names as peptide_names
from .protein.names import names as protein_names
from .rna.names import names as rna_names
from .dna.names import names as dna_names
from .small_molecule.names import names as small_molecule_names
from .water.names import names as water_names

@digest()
def get_entity_type_from_entity_name(entity_name, digest=True):

    output = None

    if entity_name in water_names:

        output = 'water'

    elif entity_name in ion_names:

        output = 'ion'

    elif entity_name in lipid_names:

        output = 'lipid'

    elif entity_name in peptide_names:

        output = 'peptide'

    elif entity_name in protein_names:

        output = 'protein'

    elif entity_name in rna_names:

        output = 'rna'

    elif entity_name in dna_names:

        output = 'dna'

    elif entity_name in small_molecule_names:

        output = 'small molecule'

    return output

