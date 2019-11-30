
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
    bioassembly : obj
        Description of bioassembly.
         
    """


    def __init__(self, index=None, id=None, name=None, type=None):

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
        self.type = None

        self.chemical_type = None
        self.formal_charge = None #(sum of atoms formal charge)

        self.atom = []
        self.atom_indices = []
        self.n_atoms = 0

        self.component = None
        self.chain = None
        self.molecule = None
        self.entity = None
        self.bioassembly = None

    def __sanity_check (self, atom=False, component=False, chain=False, molecule=False,
            entity=False, bioassembly=False):

        from molmodmt.util.exceptions import IncompleteElementError

        if atom and (len(self.atom)>0):
            raise IncompleteElementError("Group index {} has no atoms".format(self.index))

        if component and (self.component is None):
            raise IncompleteElementError("Group index {} has no component".format(self.index))

        if chain and (self.chain is None):
            raise IncompleteElementError("Group index {} has no chain".format(self.index))

        if molecule and (self.molecule is None):
            raise IncompleteElementError("Group index {} has no molecule".format(self.index))

        if entity and (self.entity is None):
            raise IncompleteElementError("Group index {} has no entity".format(self.index))

        if bioassembly and (self.bioassembly is None):
            raise IncompleteElementError("Group index {} has no bioassembly".format(self.index))

    def __update_atoms(self):

        self.n_atoms = len(self.atom)
        self.atoms = [atom.index for atom in self.atom]

    def __update_all(self):

        self.__update_atoms()

def group_initialization_wizard(index=None, id=None, name=None, type=None):

    from . import groups

    if type is None:
        return Group(index=index, id=id, name=name)
    elif type == 'aminoacid':
        return groups.AminoAcid(index=index, id=id, name=name)
    elif type == 'nucleotide':
        return groups.Nucleotide(index=index, id=id, name=name)
    elif type == 'ion':
        return groups.Ion(index=index, id=id, name=name)
    elif type == 'water':
        return groups.Water(index=index, id=id, name=name)
    else:
        raise ValueError("Group type not recognized")

