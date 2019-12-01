# covalent unit

class Component():

    """Component element.

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

    group : x
        Description of group.
    groups : x
        Description of groups.
    n_groups : x
        Description of n_groups.

    molecule : obj
        Description of molecule.
    chain : obj
        Description of chain.
    entity : obj
        Description of molecule.
    bioassembly : obj
        Description of bioassembly.

    bond : x
        Description of bond.
    bond_indices : x
        Description of bond_indices.
    bonded_atom_indices : x
        Description of bonded_atom_indices.
    n_bonds: x
        Description of n_bonds.

     """


    def __init__(self, index=None, id=None, name=None, type=None):

        """Init method for component.

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

        self.atom = []
        self.atoms = []
        self.n_atoms = 0

        self.group = []
        self.groups = []
        self.n_groups = 0

        self.molecule = None
        self.chain = None
        self.entity = None
        self.bioassembly = None

        self.bond = []
        self.bond_indices = []
        self.bonded_atom_indices = []
        self.n_bonds = 0

    def __sanity_check (self, atom=False, group=False, chain=False, molecule=False,
            entity=False, bioassembly=False):

        from molmodmt.util.exceptions import IncompleteElementError

        if atom and (len(self.atom)>0):
            raise IncompleteElementError("Component index {} has no atoms".format(self.index))

        if group and (len(self.group)>0):
            raise IncompleteElementError("Component index {} has no component".format(self.index))

        if chain and (self.chain is None):
            raise IncompleteElementError("Component index {} has no chain".format(self.index))

        if molecule and (self.molecule is None):
            raise IncompleteElementError("Component index {} has no molecule".format(self.index))

        if entity and (self.entity is None):
            raise IncompleteElementError("Component index {} has no entity".format(self.index))

        if bioassembly and (self.bioassembly is None):
            raise IncompleteElementError("Component index {} has no bioassembly".format(self.index))

    def __update_atoms(self):

        self.n_atoms = len(self.atom)
        self.atoms = [atom.index for atom in self.atom]

    def __update_groups(self):

        self.n_groups = len(self.group)
        self.groups = [group.index for group in self.group]

    def __update_bonds(self):

        from numpy import empty

        self.n_bonds = len(self.bond)

        if self.n_bonds>0:
            self.bond_indices = []
            self.bonded_atom_indices = empty([self.n_bonds, 2], dtype=int)
            count_bonds = 0
            for bond in self.bond:
                self.bond_indices.append(bond.index)
                self.bonded_atom_indices[count_bonds, :] = [bond.atom[0].index, bond.atom[1].index]
                count_bonds += 1

    def __update_all(self):

        self.__update_atoms()
        self.__update_groups()
        self.__update_bonds()

