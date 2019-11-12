
class Atom:

    def __init__(self, index=None, id=None, name=None, type=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.element = None
        self.formal_charge = None
        self.bonded_atoms = []

        self.group = None
        self.component = None
        self.chain = None
        self.molecule = None
        self.entity = None
        self.bioassembly = None

