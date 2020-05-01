from molsysmt.native.elements import Entity

class RNA(Entity):

    def __init__(self, id=None, index=None, name=None):

        super().__init__(id=id, index=index, name=name, type='rna')

    def copy(self):

        tmp_item = RNA(index=self.index, id=self.id, name=self.name)
        return tmp_item

