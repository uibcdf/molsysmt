from .group import Group

class AminoAcid(Group):

    def __init__(self, index=None, id=None, name=None):

        super().__init__(index=index, id=id, name=name, type='aminoacid')

        self.lettercode = None

    def copy(self):

        tmp_item = AminoAcid(index=self.index, id=self.id, name=self.name)
        tmp_item.lettercode = self.lettercode
        return tmp_item

