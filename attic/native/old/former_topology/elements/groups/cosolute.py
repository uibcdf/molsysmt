from .group import Group

class Cosolute(Group):

    def __init__(self, index=None, id=None, name=None, atoms=[]):

        super().__init__(index=None, id=id, name=name, type="cosolute", atoms=atoms)

    def copy(self):

        tmp_item = Cosolute(index=self.index, id=self.id, name=self.name)
        return tmp_item

