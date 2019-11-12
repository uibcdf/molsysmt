# covalent unit

class Component():

    def __init__(self, index=None, id=None, name=None, type=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.bonds = None
        self.n_bonds = 0

        self.atom = []
        self.n_atoms = 0

        self.group = []
        self.n_groups = 0

        self.chain = None
        self.molecule = None
        self.entity = None
        self.bioassembly = None

