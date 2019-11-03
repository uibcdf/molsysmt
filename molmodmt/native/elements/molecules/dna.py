from molmodmt.native.elements import Molecule

class DNA(Molecule):

    def __init__(self, id=None, index=None, name=None, type=None):

        super().__init__(id=id, index=index, name=name, type=type)

