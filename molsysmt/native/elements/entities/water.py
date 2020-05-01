from molsysmt.native.elements import Entity

class Water(Entity):

    def __init__(self, id=None, index=None, name=None):

        super().__init__(id=id, index=index, name=name, type='water')

    def copy(self):

        tmp_item = Water(index=self.index, id=self.id, name=self.name)
        return tmp_item

