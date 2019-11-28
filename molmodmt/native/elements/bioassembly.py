class BioAssembly():

    def __init__(self, index=None, id=None, name=None, type=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.transformation = []

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

        self.chain = []
        self.chains = []
        self.n_chains = 0

        self.entity = []
        self.entities = []
        self.n_entities = 0

class BioAssembly_Transformation():

    def __init__(self):

        self.chain_indices = []
        self.matrix = []

