
class Atom:

    def __init__(self, atoms=None, order=None):

        self.atom = atoms
        self.group = None
        self.order = order

        if self.atom is not None:
            self.group = [atom.group for atom in self.atom]

        self.component = None
        self.chain = None
        self.molecule = None
        self.entity = None
        self.bioassembly = None

