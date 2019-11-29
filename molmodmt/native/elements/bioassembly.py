class BioAssembly():

    def __init__(self, index=None, id=None, name=None, type=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.transformation = []

        self.atom = []
        self.atoms = []
        self.n_atoms = 0

        self.group = []
        self.groups = []
        self.n_groups = 0

        self.component = []
        self.components = []
        self.n_components = 0

        self.molecule = []
        self.molecules = []
        self.n_molecules = 0

        self.chain = []
        self.chains = []
        self.n_chains = 0

        self.entity = []
        self.entities = []
        self.n_entities = 0

        self.bond = []
        self.bonds = []
        self.n_bonds = 0

        self.bonded_atoms = []
        self.n_bonded_atoms = 0


    def __sanity_check (self, atom=False, group=False, component=False, molecule=False,
            chain=False, entity=False):

        from molmodmt.util.exceptions import IncompleteElementError

        if atom and (len(self.atom)>0):
            raise IncompleteElementError("Bioassembly index {} has no atoms".format(self.index))

        if group and (len(self.group)>0):
            raise IncompleteElementError("Bioassembly index {} has no groups".format(self.index))

        if component and (len(self.component)>0):
            raise IncompleteElementError("Bioassembly index {} has no components".format(self.index))

        if molecule and (len(self.molecule)>0):
            raise IncompleteElementError("Bioassembly index {} has no molecules".format(self.index))

        if chain and (len(self.chain)>0):
            raise IncompleteElementError("Bioassembly index {} has no chains".format(self.index))

        if entity and (len(self.entity)>0):
            raise IncompleteElementError("Bioassembly index {} has no entities".format(self.index))

    def __update_atoms(self):

        self.n_atoms = len(self.atom)
        self.atoms = [atom.index for atom in self.atom]

    def __update_groups(self):

        self.n_groups = len(self.group)
        self.groups = [group.index for group in self.group]

    def __update_components(self):

        self.n_components = len(self.component)
        self.components = [component.index for component in self.component]

    def __update_molecules(self):

        self.n_molecules = len(self.molecule)
        self.molecules = [molecule.index for molecule in self.molecule]

    def __update_chains(self):

        self.n_chains = len(self.chain)
        self.chains = [chain.index for chain in self.chain]

    def __update_entities(self):

        self.n_entities = len(self.entity)
        self.entities = [entity.index for entity in self.entity]

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
        self.__update_components()
        self.__update_molecules()
        self.__update_bonds()

class BioAssembly_Transformation():

    def __init__(self):

        self.chain_indices = []
        self.matrix = []

