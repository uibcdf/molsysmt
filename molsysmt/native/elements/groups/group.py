class Group:

    """Group element.

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

    chemical_type : str
        Description of chemical type.
    formal_charge : float
        Description of formal change.
    
    atom : obj 
        Description of atom.
    atom_indices : x
        Description of atom indices.
    n_atoms : x
        Description of n_atoms.

    component : obj
        Description of component.
    chain : obj
        Description of chain.
    molecule : obj
        Description of molecule.        
    entity : obj
        Description of molecule.
         
    """


    def __init__(self, index=None, id=None, name=None, type=None,
                 atoms=[]):

        """Init method for group.

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

        self.component = None
        self.chain = None
        self.molecule = None
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

    def copy(self):

        tmp_item = Group(index=self.index, id=self.id, name=self.name)
        return tmp_item

    def _sanity_check (self, atoms=True, component=True, chain=True, molecule=True,
            entity=True, bioassembly=True, children_elements=True):

        from molsysmt.utils.exceptions import IncompleteElementError

        if atoms:
            if len(self.atom)==0:
                raise IncompleteElementError("Group index {} has no atoms".format(self.index))
            elif children_elements:
                for atom in self.atom:
                    atom._sanity_check()

        if component and (self.component is None):
            raise IncompleteElementError("Group index {} has no component".format(self.index))

        if chain and (self.chain is None):
            raise IncompleteElementError("Group index {} has no chain".format(self.index))

        if molecule and (self.molecule is None):
            raise IncompleteElementError("Group index {} has no molecule".format(self.index))

        if entity and (self.entity is None):
            raise IncompleteElementError("Group index {} has no entity".format(self.index))


