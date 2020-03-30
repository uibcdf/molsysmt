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


    def _sanity_check (self, atoms=True, groups=True, components=True, molecules=True,
            chains=True, entities=True, bonds=True, children_elements=False):

        from molsysmt.utils.exceptions import IncompleteElementError

        if atoms:
            if len(self.atom)==0:
                raise IncompleteElementError("Bioassembly index {} has no atoms".format(self.index))
            elif children_elements:
                for atom in self.atom:
                    atom._sanity_check()

        if groups:
            if len(self.group)==0:
                raise IncompleteElementError("Bioassembly index {} has no groups".format(self.index))
            elif children_elements:
                for group in self.group:
                    group._sanity_check()

        if components:
            if len(self.component)==0:
                raise IncompleteElementError("Bioassembly index {} has no components".format(self.index))
            elif children_elements:
                for component in self.component:
                    component._sanity_check()

        if molecules:
            if len(self.molecule)==0:
                raise IncompleteElementError("Bioassembly index {} has no molecules".format(self.index))
            elif children_elements:
                for molecule in self.molecule:
                    molecule._sanity_check()

        if chains:
            if len(self.chain)==0:
                raise IncompleteElementError("Bioassembly index {} has no chains".format(self.index))
            elif children_elements:
                for chain in self.chain:
                    chain._sanity_check()

        if entities:
            if len(self.entity)==0:
                raise IncompleteElementError("Bioassembly index {} has no entities".format(self.index))
            elif children_elements:
                for entity in self.entity:
                    entity._sanity_check()

        if bonds:
            if len(self.bond)==0:
                raise IncompleteElementError("Bioassembly index {} has no bonds".format(self.index))
            elif children_elements:
                for bond in self.bond:
                    bond._sanity_check()

    def _update_atoms(self):

        self.n_atoms = len(self.atom)
        self.atom_indices = [atom.index for atom in self.atom]

    def _update_groups(self, children_elements=False):

        self.n_groups = len(self.group)
        self.group_indices = [group.index for group in self.group]
        if children_elements:
            for group in self.group:
                group._update_all()

    def _update_components(self, children_elements=False):

        self.n_components = len(self.component)
        self.component_indices = [component.index for component in self.component]
        if children_elements:
            for component in self.component:
                component._update_all()

    def _update_molecules(self, children_elements=False):

        self.n_molecules = len(self.molecule)
        self.molecule_indices = [molecule.index for molecule in self.molecule]
        if children_elements:
            for molecule in self.molecule:
                molecule._update_all()

    def _update_chains(self, children_elements=False):

        self.n_chains = len(self.chain)
        self.chain_indices = [chain.index for chain in self.chain]
        if children_elements:
            for chain in self.chain:
                chain._update_all()

    def _update_entities(self, children_elements=False):

        self.n_entities = len(self.entity)
        self.entity_indices = [entity.index for entity in self.entity]
        if children_elements:
            for entity in self.entity:
                entity._update_all()

    def _update_bonds(self):

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

    def _update_all(self, children_elements=False):

        self._update_atoms()
        self._update_groups(children_elements=children_elements)
        self._update_components(children_elements=children_elements)
        self._update_molecules(children_elements=children_elements)
        self._update_chains(children_elements=children_elements)
        self._update_entities(children_elements=children_elements)
        self._update_bonds()

class BioAssembly_Transformation():

    def __init__(self):

        self.chain_indices = []
        self.matrix = []

def bioassembly_init_wizard(index=None, id=None, name=None, type=None):

    return BioAssembly(index=index, id=id, name=name, type=type)

