
class Entity:

    """Entity element.

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

    description : str
        Description of description.
    mmtf_type : str
        Description of mmtf_type.

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

    """

    def __init__(self, index=None, id=None, name=None, type=None,
                atoms=[], groups=[], components=[], chains=[], molecules=[]):

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

        self.atom = atoms
        self.atom_indices = [atom.index for atom in atoms]
        self.n_atoms = len(atoms)

        self.group = groups
        self.group_indices = [group.index for group in groups]
        self.n_groups = len(groups)

        self.component = components
        self.component_indices = [component.index for component in components]
        self.n_components = len(components)

        self.molecule = molecules
        self.molecule_indices = [molecule.index for molecule in molecules]
        self.n_molecules = len(molecules)

        self.chain = chains
        self.chain_indices = [chain.index for chain in chains]
        self.n_chains = len(chains)

    def add_atom (self, atom):

        self.atom.append(atom)
        self.atom_indices.append(atom.index)
        self.n_atoms+=1

    def add_group (self, group):

        self.group.append(group)
        self.group_indices.append(group.index)
        self.n_groups+=1

    def add_component (self, component):

        self.component.append(component)
        self.component_indices.append(component.index)
        self.n_components+=1

    def add_molecule (self, molecule):

        self.molecule.append(molecule)
        self.molecule_indices.append(molecule.index)
        self.n_molecules+=1

    def add_chain (self, chain):

        self.chain.append(chain)
        self.chain.append(chain.index)
        self.n_chains+=1

    def copy(self):

        tmp_item = Entity(index=self.index, id=self.id, name=self.name)
        return tmp_item

    def _sanity_check(self, atoms=True, groups=True, components=True, chains=True, molecules=True,
           bioassembly=True, children_elements=False):

        from molsysmt.utils.exceptions import IncompleteElementError

        if atoms:
            if len(self.atom)==0:
                raise IncompleteElementError("Entity index {} has no atoms".format(self.index))
            elif children_elements:
                for atom in self.atom:
                    atom._sanity_check()

        if groups:
            if len(self.group)==0:
                raise IncompleteElementError("Entity index {} has no groups".format(self.index))
            elif children_elements:
                for group in self.group:
                    group._sanity_check()

        if components:
            if len(self.component)==0:
                raise IncompleteElementError("Entity index {} has no components".format(self.index))
            elif children_elements:
                for component in self.component:
                    component._sanity_check()

        if molecules:
            if len(self.molecule)==0:
                raise IncompleteElementError("Entity index {} has no molecules".format(self.index))
            elif children_elements:
                for molecule in self.molecule:
                    molecule._sanity_check()

        if chains:
            if len(self.chain)==0:
                raise IncompleteElementError("Entity index {} has no chains".format(self.index))
            elif children_elements:
                for chain in self.chain:
                    chain._sanity_check()

