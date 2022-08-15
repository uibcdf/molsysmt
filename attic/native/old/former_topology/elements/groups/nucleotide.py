from .group import Group

class Nucleotide(Group):

    def __init__(self, index=None, id=None, name=None, atoms=[]):

        super().__init__(index=index, id=id, name=name, type='nucleotide', atoms=atoms)

        self.lettercode = None

    def copy(self):

        tmp_item =Nucleotide(index=self.index, id=self.id, name=self.name)
        tmp_item.lettercode = self.lettercode
        return tmp_item

