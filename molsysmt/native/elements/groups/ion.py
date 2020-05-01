from molsysmt.native.elements import Group

class Ion(Group):

    def __init__(self, index=None, id=None, name=None):

        super().__init__(index=index, id=id, name=name, type='ion')

    def copy(self):

        tmp_item = Ion(index=self.index, id=self.id, name=self.name)
        return tmp_item

