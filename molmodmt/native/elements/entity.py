
class Entity:

    def __init__(self, index=None, id=None, name=None, type=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.description = None
        self.mmtf_type = None

        self.atom = []
        self.atoms = []
        self.n_atoms = 0

        self.group = []
        self.groups = []
        self.n_groups = 0

        self.component = []
        self.components = []
        self.n_components = 0

        self.molecule = []
        self.molecules = []
        self.n_molecules = 0

        self.chain = []
        self.chains = []
        self.n_chains = 0

        self.bioassembly = None


def entity_class_initialization(entity_type=None):

    from . import entities

    if entity_type is None:
        return Entity()
    elif entity_type is "ion":
        return entities.Ion()
    elif entity_type is "water":
        return entities.Water()
    elif entity_type is "cosolute":
        return entities.Cosolute()
    elif entity_type is "small_molecule":
        return entities.SmallMolecule()
    elif entity_type is "peptide":
        return entities.Peptide()
    elif entity_type is "dna":
        return entities.DNA()
    elif entity_type is "rna":
        return entities.RNA()
    elif entity_type is "protein":
        return entities.Protein()
    else:
        raise ValueError("Entity type not recognized.")

