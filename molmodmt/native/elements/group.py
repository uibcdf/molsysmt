
class Group:

    def __init__(self, index=None, id=None, name=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = None

        self.chemical_type = None
        self.formal_charge = None #(sum of atoms formal charge)

        self.atom = []
        self.atoms = []
        self.n_atoms = 0

        self.component = None
        self.chain = None
        self.molecule = None
        self.entity = None
        self.bioassembly = None

def group_initialization_wizard(index=None, id=None, name=None, type=None):

    from . import groups

    if type is None:
        return Group()
    elif type == 'aminoacid':
        return groups.AminoAcid(index=None, id=None, name=None)
    elif type == 'nucleotide':
        return groups.Nucleotide(index=None, id=None, name=None)
    elif type == 'ion':
        return groups.Ion(index=None, id=None, name=None)
    elif type == 'water':
        return groups.Water(index=None, id=None, name=None)
    else:
        raise ValueError("Group type not recognized")

