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

    """


    def __init__(self, index=None, id=None, name=None, type=None,
                atoms=[], groups=[]):

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

        self.atom = atoms
        self.atom_indices = [atom.index for atom in atoms]
        self.n_atoms = len(atoms)

        self.group = groups
        self.group_indices = [group.index for group in groups]
        self.n_groups = len(groups)

        self.molecule = None
        self.chain = None
        self.entity = None

    def formal_charge(self):

        value=0
        for atom in self.atom:
            value+=atom.formal_charge

        return value

    def add_atom (self, atom):

        self.atom.append(atom)
        self.atom_indices.append(atom.index)
        self.n_atoms+=1

    def add_group (self, group):

        self.group.append(group)
        self.group_indices.append(group.index)
        self.n_groups+=1

    def copy(self):

        tmp_item = Component(index=self.index, id=self.id, name=self.name, type=self.type)
        tmp_item.formal_charge = self.formal_charge
        return tmp_item

    def _sanity_check (self, atoms=True, groups=True, chain=True, molecule=True,
            entity=True, bioassembly=True, children_elements=False):

        from molsysmt.utils.exceptions import IncompleteElementError

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

