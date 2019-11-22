
class Group:

    def __init__(self, index=None, id=None, name=None, type=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.chemical_type = None
        self.formal_charge = None #(sum of atoms formal charge)

        self.atom = []
        self.n_atoms = 0

        self.component = None
        self.chain = None
        self.molecule = None
        self.entity = None
        self.bioassembly = None

def group_class_initialization(group_type=None):

    from . import groups

    if group_type is None:
        return Group()
    elif group_type == 'aminoacid':
        return groups.AminoAcid()
    elif group_type == 'nucleotide':
        return groups.Nucleotide()
    elif group_type == 'ion':
        return groups.Ion()
    elif group_type == 'water':
        return groups.Water()
    else:
        raise ValueError("Group type not recognized")

