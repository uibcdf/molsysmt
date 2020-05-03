from .entity import Entity

class Cosolute(Entity):

    def __init__(self, id=None, index=None, name=None, atoms=[], groups=[],
                 components=[], chains=[], molecules=[]):

        super().__init__(id=id, index=index, name=name, type='cosolute', atoms=atoms,
                        groups=groups, components=components, chains=chains, molecule=molecule)

    def copy(self):

        tmp_item = Cosolute(index=self.index, id=self.id, name=self.name)
        return tmp_item

