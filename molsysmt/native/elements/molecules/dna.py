from molsysmt.native.elements import Molecule

class DNA(Molecule):

    def __init__(self, index=None, id=None, name=None):

        super().__init__(id=id, index=index, name=name, type="dna")

