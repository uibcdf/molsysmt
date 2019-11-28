
class Chain:

    def __init__(self, index=None, id=None, name=None):

        self.index = index
        self.id = id
        self.name = name

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

        self.entity = []
        self.entities = []
        self.n_entities = 0

        self.bioassembly = None

    def __sanity_check (self, atom=False, group=False, component=False, molecule=False,
            entity=False, bioassembly=False):

        from molmodmt.util.exceptions import IncompleteElementError

        if atom and (len(self.atom)>0):
            raise IncompleteElementError("Chain index {} has no atoms".format(self.index))

        if group and (len(self.group)>0):
            raise IncompleteElementError("Chain index {} has no groups".format(self.index))

        if component and (len(self.component)>0):
            raise IncompleteElementError("Chain index {} has no components".format(self.index))

        if molecule and (len(self.molecule)>0):
            raise IncompleteElementError("Chain index {} has no molecules".format(self.index))

        if entity and (len(self.entity)>0):
            raise IncompleteElementError("Chain index {} has no entities".format(self.index))

        if bioassembly and (self.bioassembly is None):
            raise IncompleteElementError("Chain index {} has no bioassembly".format(self.index))

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

    def __update_entities(self):

        self.n_entities = len(self.entity)
        self.entities = [entity.index for entity in self.entity]

    def __update_all(self):

        self.__update_atoms()
        self.__update_groups()
        self.__update_components()
        self.__update_molecules()
        self.__update_entities()

