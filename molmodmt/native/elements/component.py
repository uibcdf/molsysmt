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

    atom : x
        Description of atom.
    atom_indices : x
        Description of atom_indices.
    n_atoms : x
        Description of n_atoms.

    group : x
        Description of group.
    group_indices : x
        Description of group_indices.
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
        self.atom_indices = []
        self.n_atoms = 0

        self.group = []
        self.group_indices = []
        self.n_groups = 0

        self.molecule = None
        self.chain = None
        self.entity = None
        self.bioassembly = None

        self.bond = []
        self.bond_indices = []
        self.bonded_atom_indices = []
        self.n_bonds = 0

    def _sanity_check (self, atoms=True, groups=True, chain=True, molecule=True,
            entity=True, bioassembly=True, children_elements=False):

        from molmodmt.utils.exceptions import IncompleteElementError

        if atoms:
            if len(self.atom)==0:
                raise IncompleteElementError("Component index {} has no atoms".format(self.index))
            elif children_elements:
                for atom in self.atom:
                    atom._sanity_check()

        if groups: 
            if len(self.group)==0:
                raise IncompleteElementError("Component index {} has no groups".format(self.index))
            elif children_elements:
                for group in self.group:
                    group._sanity_check()

        if chain and (self.chain is None):
            raise IncompleteElementError("Component index {} has no chain".format(self.index))

        if molecule and (self.molecule is None):
            raise IncompleteElementError("Component index {} has no molecule".format(self.index))

        if entity and (self.entity is None):
            raise IncompleteElementError("Component index {} has no entity".format(self.index))

        if bioassembly and (self.bioassembly is None):
            raise IncompleteElementError("Component index {} has no bioassembly".format(self.index))

    def _update_atoms(self):

        self.n_atoms = len(self.atom)
        self.atom_indices = [atom.index for atom in self.atom]

    def _update_groups(self, children_elements=False):

        self.n_groups = len(self.group)
        self.group_indices = [group.index for group in self.group]
        if children_elements:
            for group in self.group:
                group._update_all()

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
        self._update_bonds()

def component_init_wizard(index=None, id=None, name=None, type=None):

    return Component(index=index, id=id, name=name, type=type)

