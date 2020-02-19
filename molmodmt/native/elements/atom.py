
class Atom:

    """Atom element.

    Blablabla descripcion.

    Attributes
    ----------

    index : int
        Description of index.
    id : int or str
        Description of id.
    name : str
        Description of name.
    type : str
        Description of type.

    formal_charge : float
        Description of formal change.

    group : obj
        Description of group.
    component : obj
        Description of component.
    chain : obj
        Description of chain.
    molecule : obj
        Description of molecule.
    entity : obj
        Description of molecule.
    bioassembly : obj
        Description of bioassembly.

    bond : x
        Description of bond.
    bond_indices : x
        Description of bond_indices.
    bonded_atom_indices : x
        Description of bonded atom indices.
    n_bonds : x
        Description of n_bonds.
    """

    def __init__(self, index=None, id=None, name=None, type=None):


        """Init method for atom.

        Bla bla parrafo de inicialización.

        Parameters
        ----------
        index : int
            Description of index.
        id : int
            Description of index.
        name : int
            Description of index.
        type : int
            Description of index.
        """

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.formal_charge = None

        self.group = None
        self.component = None
        self.chain = None
        self.molecule = None
        self.entity = None
        self.bioassembly = None

        self.bond = []
        self.bond_indices = []
        self.bonded_atom_indices = []
        self.n_bonds = 0

    def _sanity_check (self, group=True, component=True, chain=True, molecule=True,
            entity=True, bioassembly=True):

        from molmodmt.utils.exceptions import IncompleteElementError

        if group and (self.group is None):
            raise IncompleteElementError("Atom index {} has no group".format(self.index))

        if component and (self.component is None):
            raise IncompleteElementError("Atom index {} has no component".format(self.index))

        if chain and (self.chain is None):
            raise IncompleteElementError("Atom index {} has no chain".format(self.index))

        if molecule and (self.molecule is None):
            raise IncompleteElementError("Atom index {} has no molecule".format(self.index))

        if entity and (self.entity is None):
            raise IncompleteElementError("Atom index {} has no entity".format(self.index))

        if bioassembly and (self.bioassembly is None):
            raise IncompleteElementError("Atom index {} has no bioassembly".format(self.index))

    def _update_bonds(self):

        from numpy import empty

        self.n_bonds = len(self.bond)

        if self.n_bonds>0:
            self.bond_indices = []
            self.bonded_atom_indices = []
            for bond in self.bond:
                self.bond_indices.append(bond.index)
                atom_0 = bond.atom[0]
                atom_1 = bond.atom[1]
                if atom_0.index != self.index:
                    self.bonded_atom.append(atom_1)
                    self.bonded_atom_indices.append(atom_1.indices)
                elif atom_1.index != self.index:
                    self.bonded_atom.append(atom_0)
                    self.bonded_atom_indices.append(atom_0.indices)
                else:
                    raise Exception("Atom index does not participate in one of its bonds")

    def _update_all(self):

        self._update_bonds()

def atom_init_wizard(index=None, id=None, name=None, type=None):

    return Atom(index=index, id=id, name=name, type=type)

