from molsysmt.native.elements import Molecule

class Peptide(Molecule):

    def __init__(self, index=None, id=None, name=None):

        super().__init__(index=index, id=id, name=name, type="peptide")

    def copy(self):

        tmp_item = Peptide(index=self.index, id=self.id, name=self.name)
        return tmp_item

