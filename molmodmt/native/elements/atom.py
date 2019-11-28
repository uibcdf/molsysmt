
class Atom:

    def __init__(self, index=None, id=None, name=None, type=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.formal_charge = None

        self.group = None
        self.component = None
        self.chain = None
        self.molecule = None
        self.entity = None
        self.bioassembly = None

        self.bonded_atom = []
        self.bonded_atoms = []
        self.n_bonded_atoms = 0

        self.bond = []
        self.bonds = []
        self.n_bonds = 0

