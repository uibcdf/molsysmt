
class Molecule():

    def __init__(self):

        self.id = None
        self.index = None
        self.name = None
        self.type = None

        self.atom = []
        self.n_atoms = 0

        self.group = []
        self.n_groups = 0

        self.component = []
        self.n_components = 0

        self.chain = []
        self.n_chains = 0

        self.entity = None
        self.bioassembly = None

