from molsysmt.native.elements import Entity

class Protein(Entity):

    def __init__(self, id=None, index=None, name=None):

        super().__init__(id=id, index=index, name=name, type='protein')

    def copy(self):

        tmp_item = Protein(index=self.index, id=self.id, name=self.name)
        return tmp_item

