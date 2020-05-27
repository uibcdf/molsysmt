from .molecule import Molecule

class Protein(Molecule):

    def __init__(self, index=None, id=None, name=None, atoms=[],
                 groups=[], components=[]):

        super().__init__(index=index, id=id, name=name, type="protein",
                         atoms=[], groups=[], components=[])

