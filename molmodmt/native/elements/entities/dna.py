from molmodmt.native.elements import Entity

class DNA(Entity):

    def __init__(self, id=None, index=None, name=None):

        super().__init__(id=id, index=index, name=name)

        self.type = 'dna'

