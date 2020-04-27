class Composition():

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

    #def _update_from_bioassembly(self):

    #    if self.bioassembly is not None:

    #        self.entity = self.bioassembly.entity
    #        self.entity_indices = self.bioassembly.entity_indices
    #        self.n_entities = self.bioassembly.n_entities

    #        self.molecule = self.bioassembly.molecule
    #        self.molecule_indices = self.bioassembly.molecule_indices
    #        self.n_molecules = self.bioassembly.n_molecules

    #        self.chain = self.bioassembly.chain
    #        self.chain_indices = self.bioassembly.chain_indices
    #        self.n_chains = self.bioassembly.n_chains

    #        self.component = self.bioassembly.component
    #        self.component_indices = self.bioassembly.component_indices
    #        self.n_components = self.bioassembly.n_components

    #        self.group = self.bioassembly.group
    #        self.groups = self.bioassembly.group_indices
    #        self.n_groups = self.bioassembly.n_groups

    #        self.atom = self.bioassembly.atom
    #        self.atom_indices = self.bioassembly.atom_indices
    #        self.n_atoms = self.bioassembly.n_atoms

    #        self.bond = self.bioassembly.bond
    #        self.bond_indices = self.bioassembly.bond_indices
    #        self.bonded_atom_indices = self.bioassembly.bonded_atom_indices
    #        self.n_bonds = self.bioassembly.n_bonds

    def _update_dataframe(self):

        from molsysmt.native import DataFrame
        from pandas import Series

        tmp_item = DataFrame()

        tmp_item['atom.index'] = Series(atom.index for atom in self.atom).values
        tmp_item['atom.name'] = Series(atom.name for atom in self.atom).values
        tmp_item['atom.id'] = Series(atom.id for atom in self.atom).values
        tmp_item['atom.type'] = Series(atom.type for atom in self.atom).values

        tmp_item['group.index'] = Series(atom.group.index for atom in self.atom).values
        tmp_item['group.name'] = Series(atom.group.name for atom in self.atom).values
        tmp_item['group.id'] = Series(atom.group.id for atom in self.atom).values
        tmp_item['group.type'] = Series(atom.group.type for atom in self.atom).values

        tmp_item['component.index'] = Series(atom.component.index for atom in self.atom).values
        tmp_item['component.name'] = Series(atom.component.name for atom in self.atom).values
        tmp_item['component.id'] = Series(atom.component.id for atom in self.atom).values
        tmp_item['component.type'] = Series(atom.component.type for atom in self.atom).values

        tmp_item['chain.index'] = Series(atom.chain.index for atom in self.atom).values
        tmp_item['chain.name'] = Series(atom.chain.name for atom in self.atom).values
        tmp_item['chain.id'] = Series(atom.chain.id for atom in self.atom).values
        tmp_item['chain.type'] = Series(atom.chain.type for atom in self.atom).values

        tmp_item['molecule.index'] = Series(atom.molecule.index for atom in self.atom).values
        tmp_item['molecule.name'] = Series(atom.molecule.name for atom in self.atom).values
        tmp_item['molecule.id'] = Series(atom.molecule.id for atom in self.atom).values
        tmp_item['molecule.type'] = Series(atom.molecule.type for atom in self.atom).values

        tmp_item['entity.index'] = Series(atom.entity.index for atom in self.atom).values
        tmp_item['entity.name'] = Series(atom.entity.name for atom in self.atom).values
        tmp_item['entity.id'] = Series(atom.entity.id for atom in self.atom).values
        tmp_item['entity.type'] = Series(atom.entity.type for atom in self.atom).values

        tmp_item.set_index(tmp_item['atom.index'].values)

        self.dataframe = tmp_item

    def extract(self, atom_indices='all'):

        if atom_indices is 'all':
            return self
        else:
            raise NotImplementedError

    def duplicate(self):

        raise NotImplementedError

    def select(self, selection, output_indices='atom'):

        from molsysmt.native.selector import dataframe_select
        indices = dataframe_select(self.dataframe, selection, output_indices=output_indices)
        return indices

