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

        self._dataframe = None

    def _update_dataframe(self):

        from molmodmt.forms.classes.api_molmodmt_Composition import to_pandas_DataFrame
        self._dataframe = to_pandas_DataFrame(self)

    def extract(self, atom_indices='all'):

        if atom_indices is 'all':
            return self
        else:
            raise NotImplementedError

    def duplicate(self):

        raise NotImplementedError

