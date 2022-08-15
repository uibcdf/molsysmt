from .molecule import Molecule

class DNA(Molecule):

    def __init__(self, index=None, id=None, name=None, atoms=[],
                 groups=[], components=[]):

        super().__init__(id=id, index=index, name=name, type="dna",
                         atoms=[], groups=[], components=[])

    def copy(self):

        tmp_item = DNA(index=self.index, id=self.id, name=self.name)
        return tmp_item

