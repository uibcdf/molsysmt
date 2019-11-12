
class Entity:

    def __init__(self, index=None, id=None, name=None, type=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.description = None
        self.mmtf_type = None

        self.atom = []
        self.n_atoms = 0

        self.group = []
        self.n_groups = 0

        self.component = []
        self.n_components = 0

        self.chain = []
        self.n_chains = 0

        self.molecule = []
        self.n_molecules = 0

        self.bioassembly = None


def entity_class_initialization(class_type=None):

    from . import entities

    if class_type is None:
        return Entity()
    else:
        return getattr(entities, class_type)()

