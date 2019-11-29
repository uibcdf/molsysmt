
class Bond():

    def __init__(self, index=None, atoms=None, order=None):

        self.index = index
        self.atom = atoms
        self.order = order

        self.component = None
        self.molecule = None
        self.entity = None
        self.bioassembly = None

    def __sanity_check (self, component=False, molecule=False, entity=False, bioassembly=False):

        from molmodmt.util.exceptions import IncompleteElementError

        if component and (self.component is None):
            raise IncompleteElementError("Bond index {} has no component".format(self.index))

        if molecule and (self.molecule is None):
            raise IncompleteElementError("Bond index {} has no molecule".format(self.index))

        if entity and (self.entity is None):
            raise IncompleteElementError("Bond index {} has no entity".format(self.index))

        if bioassembly and (self.bioassembly is None):
            raise IncompleteElementError("Bond index {} has no bioassembly".format(self.index))

