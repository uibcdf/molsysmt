from .group import Group

class SmallMolecule(Group):

    def __init__(self, index=None, id=None, name=None, atoms=[]):

        super().__init__(index=index, id=id, name=name, type="small_molecule", atoms=atoms)

    def copy(self):

        tmp_item = SmallMolecule(index=self.index, id=self.id, name=self.name)
        return tmp_item

