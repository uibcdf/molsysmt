from .cosolute.names import names as cosolute_names
from .ion.names import names as ion_names
from .lipid.names import names as lipid_names
from .peptide.names import names as peptide_names
from .protein.names import names as protein_names
from .rna.names import names as rna_names
from .dna.names import names as dna_names
from .small_molecule.names import names as small_molecule_names
from .water.names import names as water_names

def get_entity_type_from_entity_name(name):

    output = None

    if name in water_names:

        output = 'water'

    elif name in ion_names:

        output = 'ion'

    elif name in lipid_names:

        output = 'lipid'

    elif name in peptide_names:

        output = 'peptide'

    elif name in protein_names:

        output = 'protein'

    elif name in rna_names:

        output = 'rna'

    elif name in dna_names:

        output = 'dna'

    elif name in small_molecule_names:

        output = 'small molecule'

    return output

