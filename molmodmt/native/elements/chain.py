
class Chain:

    def __init__(self):

        self.id = None
        self.index = None
        self.name = None
        self.type = None

        self.bioassembly_id = None
        self.bioassembly_index = None
        self.bioassembly_name = None
        self.bioassembly_type = None

        self.entity = []
        self.segment = []
        self.group = []
        self.atom = []
        self.bond = []

        self.num_entities = 0
        self.num_segments = 0
        self.num_groups = 0
        self.num_atoms = 0
        self.num_bonds = 0

