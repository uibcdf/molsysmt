class Composition():

    def __init__(self):

        self.bioassembly = []
        self.entity = [] # naturalezas: HIF1, water, ion, etc.
        self.molecule = [] # unidad biológica o molécula
        self.chain = [] # cadena de proteina
        self.component = [] # algo unido covalentemente por similitud con las componentes de un grafo, (segmentos en una cadena, por ejemplo)
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

    def extract(self, atom_indices='all'):

        if atom_indices is 'all':
            return self
        else:
            raise NotImplementedError

    def duplicate(self):

        raise NotImplementedError

