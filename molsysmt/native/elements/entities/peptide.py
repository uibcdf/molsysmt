from molsysmt.native.elements import Entity

class Peptide(Entity):

    def __init__(self, id=None, index=None, name=None):

        super().__init__(id=id, index=index, name=name, type='peptide')

    def copy(self):

        tmp_item = Peptide(index=self.index, id=self.id, name=self.name)
        return tmp_item

