from molmodmt.native.elements import Atom

class Ion(Atom):

    def __init__(self, id=None, index=None, name=None, type=None):

        super().__init__(id=id, index=index, name=name, type=type)

        self.model = None

