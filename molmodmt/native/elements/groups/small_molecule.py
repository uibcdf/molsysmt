from molmodmt.native.elements import Group

class SmallMolecule(Group):

    def __init__(self, index=None, id=None, name=None, type="small_molecule"):

        super().__init__(index=None, id=id, name=name, type=type)

