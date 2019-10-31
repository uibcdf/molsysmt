
class Atom:

    def __init__(self, atoms=[], order=None):

        self.atom_ids = []
        self.atom = atoms
        self.order = order

        for atom in atoms:
            self.atom_ids.append(atom.id)

        self.atom_ids = set(self.atom_ids)

        self.component = None
        self.chain = None
        self.molecule = None
        self.entity = None
        self.bioassembly = None

