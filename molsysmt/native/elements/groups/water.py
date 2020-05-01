from molsysmt.native.elements import Group

class Water(Group):

    def __init__(self, index=None, id=None, name=None, type=None):

        super().__init__(index=index, id=id, name=name, type="water")

    def copy(self):

        tmp_item = Water(index=self.index, id=self.id, name=self.name)
        return tmp_item

