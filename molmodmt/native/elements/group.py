
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

def group_class_initialization(class_type=None):

    from . import groups

    if class_type is None:
        return Group()
    else:
        return getattr(groups, class_type)()

