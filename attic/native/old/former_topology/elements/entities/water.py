from .entity import Entity

class Water(Entity):

    def __init__(self, id=None, index=None, name=None, atoms=[], groups=[],
                 components=[], chains=[], molecules=[]):

        super().__init__(id=id, index=index, name=name, type='water', atoms=[],
                         groups=[], components=[], chains=[], molecules=[])

    def copy(self):

        tmp_item = Water(index=self.index, id=self.id, name=self.name)
        return tmp_item

