class Topology():

    def __init__(self):

        self.entity = []
        self.entity_indices = []
        self.n_entities = 0

        self.molecule = []
        self.molecule_indices = []
        self.n_molecules = 0

        self.chain = []
        self.chain_indices = []
        self.n_chains = 0

        self.component = []
        self.component_indices = []
        self.n_components = 0

        self.group = []
        self.group_indices = []
        self.n_groups = 0

        self.atom = []
        self.atom_indices = []
        self.n_atoms = 0

        self.bond = []
        self.bond_indices = []
        self.bonded_atom_indices = []
        self.n_bonds = 0

        self.dataframe = None

    def extract(self, atom_indices='all', structure_indices='all'):

        from .io.topology.classes import from_molsysmt_DataFrame

        if atom_indices is 'all':
            tmp_item = from_molsysmt_DataFrame(self.dataframe)
        else:
            tmp_item = from_molsysmt_DataFrame(self.dataframe.extract(atom_indices=atom_indices))

        return tmp_item

    def copy(self):

        return self.extract(atom_indices='all')

