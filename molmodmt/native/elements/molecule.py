
class Molecule():

    def __init__(self, index=None, id=None, name=None, type=None):

        self.index = index
        self.id = id
        self.name = name
        self.type = type

        self.atom = []
        self.atoms = []
        self.n_atoms = 0

        self.group = []
        self.groups = []
        self.n_groups = 0

        self.component = []
        self.components = []
        self.n_components = 0

        self.chain = []
        self.chains = []
        self.n_chains = 0

        self.entity = None
        self.bioassembly = None

def molecule_class_initialization(molecule_type=None):

    from . import molecules

    if molecule_type is None:
        return Molecule()
    elif molecule_type is "ion":
        return molecules.Ion()
    elif molecule_type is "water":
        return molecules.Water()
    elif molecule_type is "cosolute":
        return molecules.Cosolute()
    elif molecule_type is "small_molecule":
        return molecules.SmallMolecule()
    elif molecule_type is "peptide":
        return molecules.Peptide()
    elif molecule_type is "dna":
        return molecules.DNA()
    elif molecule_type is "rna":
        return molecules.RNA()
    elif molecule_type is "protein":
        return molecules.Protein()
    else:
        raise ValueError("Entity type not recognized.")


