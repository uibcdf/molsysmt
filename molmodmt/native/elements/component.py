# polymer segment

class Segment:

    def __init__(self):

        self.index = None
        self.id = None
        self.name = None
        self.type = None

        self.index_start = 0
        self.index_end = 0
        self.pdb_start = 0
        self.pdb_end = 0
        self.uniprot_start = 0
        self.uniprot_end = 0
        self.length = 0

        self.sequence = None
        self.secondary_structure_dssp = None
        self.secondary_structure_abc = None

        self.bioassembly_index = None
        self.bioassembly_id = None
        self.bioassembly_name = None
        self.bioassembly_type = None

        self.entity_index = None
        self.entity_id = None
        self.entity_name = None
        self.entity_type = None

        self.chain_index = None
        self.chain_id = None
        self.chain_name = None
        self.chain_type = None

        self.group = []
        self.atom = []
        self.bond = []

        self.num_groups = 0
        self.num_atoms = 0
        self.num_bonds = 0

