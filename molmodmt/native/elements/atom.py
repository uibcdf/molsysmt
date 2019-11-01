
class Atom:

    def __init__(self, id=None, index=None, name=None, type=None, element=None):

        self.id = id
        self.index = index
        self.name = name
        self.type = type
        self.element = element
        self.formal_charge = None

        self.bonded_atoms = []

        self.group = None
        self.component = None
        self.chain = None
        self.molecule = None
        self.entity = None
        self.bioassembly = None

