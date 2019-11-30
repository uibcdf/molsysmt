
class Chain:

    """Chain element.

    Blablabla descripcion.

    Attributes
    ----------

    index : int
        Description of index.
    id : int or str
        Description of id.
    name : str
        Description of name.
    type : int
        Description of type.

    atom : list of objects
        Description of atom
    atom_indices : list of ints
        Description of atom
    n_atoms : list of ints
        Description of n_atoms

    group : list of objects
        Description of group
    group_indices : list of ints
        Description of group_indices
    n_groups : list of ints
        Description of n_groups

    component : list of objects
        Description of component
    component_indices : list of ints
        Description of component_indices
    n_components : list of ints
        Description of n_components

    molecule : list of objects
        Description of molecule
    molecule_indices : list of ints
        Description of molecule_indices
    n_molecules : list of ints
        Description of n_molecules

    entity : list of objects
        Description of entity
    entity_indices : list of ints
        Description of entity_indices
    n_entities : list of ints
        Description of n_entities

    bioassembly : object
        Description of bioassembly

    """

    def __init__(self, index=None, id=None, name=None, type=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.atom = []
        self.atom_indices = []
        self.n_atoms = 0

        self.group = []
        self.group_indices = []
        self.n_groups = 0

        self.component = []
        self.component_indices = []
        self.n_components = 0

        self.molecule = []
        self.molecule_indices = []
        self.n_molecules = 0

        self.entity = []
        self.entity_indices = []
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

