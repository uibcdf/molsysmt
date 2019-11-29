
class Atom:

    def __init__(self, index=None, id=None, name=None, type=None):

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

        self.bonded_atom = []
        self.bonded_atoms = []
        self.n_bonded_atoms = 0

        self.bond = []
        self.bonds = []
        = 0

    def __sanity_check (self, group=False, component=False, chain=False, molecule=False,
            entity=False, bioassembly=False):

        from molmodmt.util.exceptions import IncompleteElementError

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
                if atom_0.index != self.index:
                    self.bonded_atom.append(atom_1)
                elif atom_1.index != self.index:
                    self.bonded_atom.append(atom_0)
                else:
                    raise Exception("Atom index does not participate in one of its bonds")

    def __update_all(self):

        self.__update_bonds()

