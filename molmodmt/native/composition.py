class Composition():

    def __init__(self):

        self.bioassembly = []
        self.entity = []
        self.molecule = []
        self.chain = []
        self.component = []
        self.group = []
        self.atom = []

        self.n_bioassemblies = 0
        self.n_entities = 0
        self.n_molecules = 0
        self.n_chains = 0
        self.n_components = 0
        self.n_groups = 0
        self.n_atoms = 0

        self.ion = []
        self.water = []
        self.cosolute = []
        self.small_molecule = []
        self.protein = []
        self.peptide = []
        self.dna = []
        self.rna = []

        self.n_ions = 0
        self.n_waters = 0
        self.n_cosolutes = 0
        self.n_small_molecules = 0
        self.n_proteins = 0
        self.n_peptides = 0
        self.n_dnas = 0
        self.n_rnas = 0

        self.bond = []
        self.n_bonds = 0

        self.dataframe = None

    def update_dataframe(self):

        from molmodmt.native import DataFrame
        from pandas import Series

        tmp_item = DataFrame()

        tmp_item['atom.index'] = Series(atom.index for atom in item.atom).values
        tmp_item['atom.name'] = Series(atom.name for atom in item.atom).values
        tmp_item['atom.id'] = Series(atom.id for atom in item.atom).values
        tmp_item['atom.type'] = Series(atom.type for atom in item.atom).values
        tmp_item['atom.element'] = Series(atom.element for atom in item.atom).values

        tmp_item['group.index'] = Series(atom.group.index for atom in item.atom).values
        tmp_item['group.name'] = Series(atom.group.name for atom in item.atom).values
        tmp_item['group.id'] = Series(atom.group.id for atom in item.atom).values
        tmp_item['group.type'] = Series(atom.group.type for atom in item.atom).values

        tmp_item['component.index'] = Series(atom.component.index for atom in item.atom).values
        tmp_item['component.name'] = Series(atom.component.name for atom in item.atom).values
        tmp_item['component.id'] = Series(atom.component.id for atom in item.atom).values
        tmp_item['component.type'] = Series(atom.component.type for atom in item.atom).values

        tmp_item['chain.index'] = Series(atom.chain.index for atom in item.atom).values
        tmp_item['chain.name'] = Series(atom.chain.name for atom in item.atom).values
        tmp_item['chain.id'] = Series(atom.chain.id for atom in item.atom).values
        tmp_item['chain.type'] = Series(atom.chain.type for atom in item.atom).values

        tmp_item['molecule.index'] = Series(atom.molecule.index for atom in item.atom).values
        tmp_item['molecule.name'] = Series(atom.molecule.name for atom in item.atom).values
        tmp_item['molecule.id'] = Series(atom.molecule.id for atom in item.atom).values
        tmp_item['molecule.type'] = Series(atom.molecule.type for atom in item.atom).values

        tmp_item['entity.index'] = Series(atom.entity.index for atom in item.atom).values
        tmp_item['entity.name'] = Series(atom.entity.name for atom in item.atom).values
        tmp_item['entity.id'] = Series(atom.entity.id for atom in item.atom).values
        tmp_item['entity.type'] = Series(atom.entity.type for atom in item.atom).values

        tmp_item['bioassembly.index'] = Series(atom.bioassembly.index for atom in item.atom).values
        tmp_item['bioassembly.name'] = Series(atom.bioassembly.name for atom in item.atom).values
        tmp_item['bioassembly.id'] = Series(atom.bioassembly.id for atom in item.atom).values
        tmp_item['bioassembly.type'] = Series(atom.bioassembly.type for atom in item.atom).values

        tmp_item.set_index(tmp_item['atom.index'].values)

        self.dataframe = tmp_item

    def extract(self, atom_indices='all'):

        if atom_indices is 'all':
            return self
        else:
            raise NotImplementedError

    def duplicate(self):

        raise NotImplementedError

