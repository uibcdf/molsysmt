
class Bond():

    """Entity element.

    Blablabla descripcion.

    Attributes
    ----------

    index : int
        Description of index.
    atom : obj atom
        Description of atom.
    order : str
        Description of order.

    component : obj
        Description of component.
    molecule : obj
        Description of molecule.
    entity : obj
        Description of entity.
    bioassembly : obj
        Description of bioassembly.
    """

    def __init__(self, index=None, atoms=None, order=None):

        """Init method for entity.

        Bla bla parrafo de inicialización.

        Parameters
        ----------
        index : int
            Description of index.
        atoms : list of objs
            Description of atoms.
        order : int
            Description of order.
        """

        self.index = index
        self.atom = atoms
        self.atom_indices = None
        self.order = order

        self.component = None
        self.molecule = None
        self.entity = None
        self.bioassembly = None

        if self.atom is not None:
            self.atom_indices = [self.atom[0].index, self.atom[1].index]

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

