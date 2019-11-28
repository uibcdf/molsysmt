
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


def entity_initialization_wizard(index=None, id=None, name=None, type=None):

    from . import entities

    if type is None:
        return Entity(index=index, id=id, name=name)
    elif type is "ion":
        return entities.Ion(index=index, id=id, name=name)
    elif type is "water":
        return entities.Water(index=index, id=id, name=name)
    elif type is "cosolute":
        return entities.Cosolute(index=index, id=id, name=name)
    elif type is "small_molecule":
        return entities.SmallMolecule(index=index, id=id, name=name)
    elif type is "peptide":
        return entities.Peptide(index=index, id=id, name=name)
    elif type is "dna":
        return entities.DNA(index=index, id=id, name=name)
    elif type is "rna":
        return entities.RNA(index=index, id=id, name=name)
    elif type is "protein":
        return entities.Protein(index=index, id=id, name=name)
    else:
        raise ValueError("Entity type not recognized.")

