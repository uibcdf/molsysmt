class BioAssembly():

    def __init__(self, index=None, id=None, name=None, type=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.transformation = []

        self.atom = []
        self.n_atoms = 0

        self.group = []
        self.n_groups = 0

        self.component = []
        self.n_components = 0

        self.chain = []
        self.n_chains = 0

        self.molecule = []
        self.n_molecules = 0

        self.entity = []
        self.n_entities = 0

class BioAssembly_Transformation():

    def __init__(self):

        self.chain_indices = []
        self.matrix = []

