
class Chain:

    def __init__(self, index=None, id=None, name=None):

        self.index = index
        self.id = id
        self.name = name

        self.atom = []
        self.atoms = []
        self.n_atoms = 0

        self.group = []
        self.groups = []
        self.n_groups = 0

        self.component = []
        self.components = []
        self.n_components = 0

        self.molecule = []
        self.molecules = []
        self.n_molecules = 0

        self.entity = []
        self.entities = []
        self.n_entities = 0

        self.bioassembly = None

