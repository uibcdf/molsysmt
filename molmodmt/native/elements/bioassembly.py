class BioAssembly:

    def __init__(self):

        self.id = None
        self.index = None
        self.name = None
        self.type = None

        self.chain = []
        self.entity = []
        self.segment = []
        self.group = []
        self.atom = []
        self.bond = []

        self.num_chains = 0
        self.num_entities = 0
        self.num_segments = 0
        self.num_groups = 0
        self.num_atoms = 0
        self.num_bonds = 0

        self.ion = []
        self.water = []
        self.small_molecule = []
        self.protein = []
        self.peptide = []
        self.dna = []
        self.rna = []

        self.num_ions = 0
        self.num_waters = 0
        self.num_small_molecules = 0
        self.num_proteins = 0
        self.num_peptides = 0
        self.num_dnas = 0
        self.num_rnas = 0

