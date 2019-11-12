from molmodmt.native.elements import Group

class Water(Group):

    def __init__(self, index=None, id=None, name=None, type=None):

        super().__init__(index=None, id=id, name=name, type=type)

        self.model = None

