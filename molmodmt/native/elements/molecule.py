
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

    def __sanity_check (self, atom=False, group=False, component=False, chain=False,
            entity=False, bioassembly=False):

        from molmodmt.util.exceptions import IncompleteElementError

        if atom and (len(self.atom)>0):
            raise IncompleteElementError("Molecules index {} has no atoms".format(self.index))

        if group and (len(self.group)>0):
            raise IncompleteElementError("Molecules index {} has no groups".format(self.index))

        if component and (len(self.component)>0):
            raise IncompleteElementError("Molecules index {} has no components".format(self.index))

        if chain and (len(self.chain)>0):
            raise IncompleteElementError("Molecules index {} has no chains".format(self.index))

        if entity and (self.entity is None):
            raise IncompleteElementError("Molecules index {} has no entity".format(self.index))

        if bioassembly and (self.bioassembly is None):
            raise IncompleteElementError("Molecules index {} has no bioassembly".format(self.index))

    def __update_atoms(self):

        self.n_atoms = len(self.atom)
        self.atoms = [atom.index for atom in self.atom]

    def __update_groups(self):

        self.n_groups = len(self.group)
        self.groups = [group.index for group in self.group]

    def __update_components(self):

        self.n_components = len(self.component)
        self.components = [component.index for component in self.component]

    def __update_chains(self):

        self.n_chains = len(self.chain)
        self.chains = [chain.index for chain in self.chain]


def molecule_initialization_wizard(index=None, id=None, name=None, type=None):

    from . import molecules

    if molecule_type is None:
        return Molecule(intex=index, id=id, name=name)
    elif molecule_type is "ion":
        return molecules.Ion(intex=index, id=id, name=name)
    elif molecule_type is "water":
        return molecules.Water(intex=index, id=id, name=name)
    elif molecule_type is "cosolute":
        return molecules.Cosolute(intex=index, id=id, name=name)
    elif molecule_type is "small_molecule":
        return molecules.SmallMolecule(intex=index, id=id, name=name)
    elif molecule_type is "peptide":
        return molecules.Peptide(intex=index, id=id, name=name)
    elif molecule_type is "dna":
        return molecules.DNA(intex=index, id=id, name=name)
    elif molecule_type is "rna":
        return molecules.RNA(intex=index, id=id, name=name)
    elif molecule_type is "protein":
        return molecules.Protein(intex=index, id=id, name=name)
    else:
        raise ValueError("Entity type not recognized.")

