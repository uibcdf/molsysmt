from molsysmt.native.elements import Entity

class Ion(Entity):

    def __init__(self, id=None, index=None, name=None):

        super().__init__(id=id, index=index, name=name, type='ion')

    def copy(self):

        tmp_item = Ion(index=self.index, id=self.id, name=self.name)
        return tmp_item

