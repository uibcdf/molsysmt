class BioAssembly():

    """BioAssembly element.

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

    transformation : str
        Description of transformation.

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

    chain : list of objects
        Description of chain
    chain_indices : list of ints
        Description of chain_indices
    n_chains : list of ints
        Description of n_chains

    entity : list of objects
        Description of entity
    entity_indices : list of ints
        Description of entity_indices
    n_entities : list of ints
        Description of n_entities

    bond : list of objects
        Description of bond
    bond_indices : list of ints
        Description of bond_indices
    bonded_atom_indices : list of ints
        Description of bonded_atom_indices
    n_bonds : list of ints
        Description of n_bonds

    """


    def __init__(self, index=None, id=None, name=None, type=None):

        """Init method for entity.

        Bla bla parrafo de inicialización.

        Parameters
        ----------
        index : int
            Description of index.
        id : int
            Description of id.
        name : int
            Description of name.
        type : int
            Description of type.
        """


        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.transformation = []

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

        self.chain = []
        self.chain_indices = []
        self.n_chains = 0

        self.entity = []
        self.entity_indices = []
        self.n_entities = 0

        self.bond = []
        self.bond_indices = []
        self.bonded_atoms_indices = []
        self.n_bonds = 0


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
        self.atom_indices = [atom.index for atom in self.atom]

    def __update_groups(self):

        self.n_groups = len(self.group)
        self.group_indices = [group.index for group in self.group]

    def __update_components(self):

        self.n_components = len(self.component)
        self.component_indices = [component.index for component in self.component]

    def __update_molecules(self):

        self.n_molecules = len(self.molecule)
        self.molecule_indices = [molecule.index for molecule in self.molecule]

    def __update_chains(self):

        self.n_chains = len(self.chain)
        self.chain_indices = [chain.index for chain in self.chain]

    def __update_entities(self):

        self.n_entities = len(self.entity)
        self.entity_indices = [entity.index for entity in self.entity]

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
        self.__update_components()
        self.__update_molecules()
        self.__update_bonds()

class BioAssembly_Transformation():

    def __init__(self):

        self.chain_indices = []
        self.matrix = []

