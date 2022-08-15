from .entity import Entity

class SmallMolecule(Entity):

    def __init__(self, id=None, index=None, name=None, atoms=[], groups=[],
                 components=[], chains=[], molecules=[]):

        super().__init__(id=id, index=index, name=name, type='small_molecule', atoms=[],
                         groups=[], components=[], chains=[], molecules=[])

    def copy(self):

        tmp_item = SmallMolecule(index=self.index, id=self.id, name=self.name)
        return tmp_item

