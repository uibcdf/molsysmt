
class Chain:

    def __init__(self, id=None, index=None, name=None):

        self.id = id
        self.index = index
        self.name = name

        self.atom = []
        self.n_atoms = 0

        self.group = []
        self.n_groups = 0

        self.component = []
        self.n_components = 0

        self.molecule = None
        self.entity = None
        self.bioassembly = None

