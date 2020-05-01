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

    def extract(self, atom_indices='all', frame_indices='all'):

        if atom_indices is 'all':
            return self.copy()
        else:
            raise NotImplementedError

    pass

    def copy(self):

        tmp_item = Composition()

        for original_atom in self.atom:
            new_atom = original_atom.copy()
            tmp_item.atom.append(new_atom)

        for original_group in self.group:
            new_group = original_group.copy()
            for atom_index in original_group.atom_indices:
                atom=tmp_item.atom[atom_index]
                new_group.add_atom(atom)
                atom.group=new_group
            tmp_item.group.append(new_group)

        for original_component in self.component:
            new_component = original_component.copy()
            for atom_index in original_component.atom_indices:
                atom=tmp_item.atom[atom_index]
                new_component.add_atom(atom)
                atom.component=new_component
            for group_index in original_component.group_indices:
                group=tmp_item.group[group_index]
                new_component.add_group(group)
                group.component=new_component
            tmp_item.component.append(new_component)

        for original_molecule in self.molecule:
            new_molecule = original_molecule.copy()
            for atom_index in original_molecule.atom_indices:
                atom=tmp_item.atom[atom_index]
                new_molecule.add_atom(atom)
                atom.molecule=new_molecule
            for group_index in original_molecule.group_indices:
                group=tmp_item.group[group_index]
                new_molecule.add_group(group)
                group.molecule=new_molecule
            for component_index in original_molecule.component_indices:
                component=tmp_item.component[component_index]
                new_molecule.add_component(component)
                component.molecule=new_molecule
            tmp_item.molecule.append(new_molecule)

        for original_chain in self.chain:
            new_chain = original_chain.copy()
            for atom_index in original_chain.atom_indices:
                atom=tmp_item.atom[atom_index]
                new_chain.add_atom(atom)
                atom.chain=new_chain
            for group_index in original_chain.group_indices:
                group=tmp_item.group[group_index]
                new_chain.add_group(group)
                group.chain=new_chain
            for component_index in original_chain.component_indices:
                component=tmp_item.component[component_index]
                new_chain.add_component(component)
                component.chain=new_chain
            tmp_item.chain.append(new_chain)

        for original_entity in self.entity:
            new_entity = original_entity.copy()
            for atom_index in original_entity.atom_indices:
                atom=tmp_item.atom[atom_index]
                new_entity.add_atom(atom)
                atom.entity=new_entity
            for group_index in original_entity.group_indices:
                group=tmp_item.group[group_index]
                new_entity.add_group(group)
                group.entity=new_entity
            for component_index in original_entity.component_indices:
                component=tmp_item.component[component_index]
                new_entity.add_component(component)
                component.entity=new_entity
            for chain_index in original_entity.chain_indices:
                chain=tmp_item.chain[chain_index]
                new_entity.add_chain(chain)
                chain.entity=new_entity
            for molecule_index in original_entity.molecule_indices:
                molecule=tmp_item.molecule[molecule_index]
                new_entity.add_molecule(molecule)
                molecule.entity=new_entity
            tmp_item.entity.append(new_entity)

        tmp_item.dataframe = self.dataframe.copy()

        return tmp_item

