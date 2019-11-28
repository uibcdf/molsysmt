# covalent unit

class Component():

    def __init__(self, index=None, id=None, name=None, type=None):

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
        self.bonds = []
        self.n_bonds = 0

        self.bonded_atoms = []
        self.n_bonded_atoms = 0

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
        self.n_bonded_atoms = self.n_bonds

        if self.n_bonds>0:
            self.bonded_atoms = empty([self.n_bonds, 2], dtype=int)
            self.bonds = []
            count_bonds = 0
            for bond in self.bond:
                self.bonds.append(bond.index)
                atom_0 = bond.atom[0]
                atom_1 = bond.atom[1]
                self.bonded_atoms[count_bonds, :] = [atom_0.index, atom_1.index]

    def __update_all(self):

        self.__update_atoms()
        self.__update_groups()
        self.__update_bonds()

