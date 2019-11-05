class BioAssembly:

    def __init__(self, id=None, index=None, name=None, type=None):

        self.id = id
        self.index = index
        self.name = name
        self.type = type

        self.mmtf_transform_list = None

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

