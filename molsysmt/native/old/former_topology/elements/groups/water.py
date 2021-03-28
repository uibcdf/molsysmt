from .group import Group

class Water(Group):

    def __init__(self, index=None, id=None, name=None, type=None, atoms=[]):

        super().__init__(index=index, id=id, name=name, type="water", atoms=[])

    def copy(self):

        tmp_item = Water(index=self.index, id=self.id, name=self.name)
        return tmp_item

