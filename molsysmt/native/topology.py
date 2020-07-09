from pandas import DataFrame as PandasDataFrame

class ElementsDF(PandasDataFrame):

    def __init__(self):

        topology_columns = ['atom_index', 'atom_name', 'atom_id', 'atom_type',
                            'group_index', 'group_name', 'group_id', 'group_type',
                            'component_index', 'component_name', 'component_id', 'component_type',
                            'chain_index', 'chain_name', 'chain_id', 'chain_type',
                            'molecule_index', 'molecule_name', 'molecule_id', 'molecule_type',
                            'entity_index', 'entity_name', 'entity_id', 'entity_type']


        super().__init__(columns=topology_columns)

    def _nan_to_None(self):

        list_columns_where_nan = ['group_type', 'component_name', 'component_type',
                                 'chain_name', 'chain_type', 'molecule_name', 'molecule_type',
                                 'entity_name', 'entity_type']

        for column in list_columns_where_nan:
            self[column].where(self[column].notnull(), None, inplace=True)


class BondsDF(PandasDataFrame):

    def __init__(self):

        topology_columns = ['atom1_index', 'atom2_index', 'order', 'type']


        super().__init__(columns=topology_columns)

    def _nan_to_None(self):

        list_columns_where_nan = ['order','type']

        for column in list_columns_where_nan:
            self[column].where(self[column].notnull(), None, inplace=True)

class Topology():

    def __init__(self):

        self.elements=ElementsDF()
        self.bonds=BondsDF()

    def extract(self, atom_indices='all', frame_indices='all'):

        if type(atom_indices)==str:

            if atom_indices in ['all', 'All', 'ALL']:
                return self.copy()

        else:

            from numpy import arange, empty, vectorize, in1d

            tmp_item = Topology()
            tmp_item.elements = self.elements.iloc[atom_indices].copy()

            bond_atom1 = self.bonds['atom1_index'].to_numpy()
            bond_atom2 = self.bonds['atom2_index'].to_numpy()
            mask_atom1 = in1d(bond_atom1, atom_indices)
            mask_atom2 = in1d(bond_atom2, atom_indices)
            mask = mask_atom1*mask_atom2
            tmp_item.bonds = self.bonds[mask].copy()
            del(bond_atom1, bond_atom2, mask_atom1, mask_atom2)

            n_atoms=tmp_item.elements.shape[0]
            n_bonds=tmp_item.bonds.shape[0]

            tmp_item.elements['atom_index']=arange(n_atoms)
            aux_dict=tmp_item.elements['atom_index'].to_dict()
            tmp_item.elements.index=arange(n_atoms)
            vaux_dict = vectorize(aux_dict.__getitem__)

            tmp_item.bonds['atom1_index']=vaux_dict(tmp_item.bonds['atom1_index'].to_numpy())
            tmp_item.bonds['atom2_index']=vaux_dict(tmp_item.bonds['atom2_index'].to_numpy())
            tmp_item.elements.index=tmp_item.elements['atom_index'].to_numpy()

            tmp_item._build_components()

            for column in ['group_index', 'molecule_index', 'chain_index', 'entity_index']:
                aux_array=tmp_item.elements[column].to_numpy()
                old_index=-1
                count=-1
                for ii in range(n_atoms):
                    if old_index!=aux_array[ii]:
                        old_index=aux_array[ii]
                        count+=1
                    aux_array[ii]=count
                tmp_item.elements[column]=aux_array

        return tmp_item

    def copy(self):

        tmp_item = Topology()

        tmp_item.elements = ElementsDF()
        tmp_item.bonds = BondsDF()

        for column in self.elements.columns:
            tmp_item.elements[column]=self.elements[column].to_numpy()

        for column in self.bonds.columns:
            tmp_item.bonds[column]=self.bonds[column].to_numpy()

        return tmp_item

    def _to_pdb_string(self, trajectory_item, frame_indices='all'):

        from molsysmt.native.io.topology.files import to_pdb as molsysmt_Topology_to_pdb

        return molsysmt_Topology_to_pdb(self, trajectory_item=trajectory_item, output_filepath='.pdb',
                                         atom_indices='all', frame_indices=frame_indices)

    def _build_components(self):

        from numpy import empty, stack
        from networkx import empty_graph, connected_components
        from molsysmt.forms.classes.api_molsysmt_Topology import get_n_atoms_from_system
        from molsysmt.forms.classes.api_molsysmt_Topology import get_n_groups_from_atom
        from molsysmt.forms.classes.api_molsysmt_Topology import get_group_type_from_atom
        from molsysmt.elements.group import type_to_component_type as group_type_to_component_type

        n_atoms = get_n_atoms_from_system(self)

        component_index_array = empty(n_atoms, dtype=int)
        component_type_array = empty(n_atoms, dtype=object)

        G = empty_graph(n_atoms)

        G.add_edges_from(stack([self.bonds['atom1_index'].to_numpy(),
                                self.bonds['atom2_index'].to_numpy()], axis=1))

        component_index = 0

        for atom_indices_of_component in connected_components(G):
            aux_list = list(atom_indices_of_component)
            group_type = get_group_type_from_atom(self, indices=[aux_list[0]])[0]
            component_type = group_type_to_component_type(group_type)
            if component_type == 'peptide':
                n_groups = get_n_groups_from_atom(self, indices=aux_list)
                component_type = group_type_to_component_type(group_type, n_groups)
            component_index_array[aux_list] = component_index
            component_type_array[aux_list] = component_type
            component_index += 1

        self.elements["component_index"] = component_index_array
        self.elements["component_type"] = component_type_array

        del(G)
        del(component_index_array, component_type_array)

    def _build_molecules(self):

        self.elements["molecule_index"] = self.elements["component_index"].to_numpy()
        self.elements["molecule_type"] = self.elements["component_type"].to_numpy()

    def _build_entities(self):

        from numpy import empty, stack
        from molsysmt.forms.classes.api_molsysmt_Topology import get_n_atoms_from_system
        from molsysmt.forms.classes.api_molsysmt_Topology import get_atom_index_from_molecule
        from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_index_from_molecule
        from molsysmt.forms.classes.api_molsysmt_Topology import get_molecule_type_from_molecule
        from molsysmt.forms.classes.api_molsysmt_Topology import get_group_name_from_atom

        entities = {}
        n_entities = 0
        n_atoms = get_n_atoms_from_system(self)

        n_peptides = 0
        n_proteins = 0

        entity_index_array = empty(n_atoms, dtype=int)
        entity_type_array = empty(n_atoms, dtype=object)
        entity_name_array = empty(n_atoms, dtype=object)

        molecule_index = get_molecule_index_from_molecule(self)
        atom_indices_in_molecule = get_atom_index_from_molecule(self)
        molecule_type = get_molecule_type_from_molecule(self)

        for m_index, m_type, m_atoms in zip(molecule_index, molecule_type, atom_indices_in_molecule):

            if m_type == 'water':
                name = 'water'
                type = 'water'
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'ion':
                group_name = get_group_name_from_atom(self, m_atoms)[0]
                name = group_name
                type = 'ion'
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'peptide':
                name = 'Peptide'+str(n_peptides)
                type = 'peptide'
                n_peptides+=1
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'protein':
                name = 'Protein'+str(n_proteins)
                type = 'protein'
                n_proteins+=1
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1

            entity_index_array[m_atoms]=index
            entity_type_array[m_atoms]=type
            entity_name_array[m_atoms]=name

        self.elements['entity_index']=entity_index_array
        self.elements['entity_type']=entity_type_array
        self.elements['entity_name']=entity_name_array

        del(entity_index_array, entity_type_array, entity_name_array)
        del(molecule_index, molecule_type, atom_indices_in_molecule)

        pass


    def _join_molecules(self, indices=None):

        pass


    def _nan_to_None(self):

        self.elements._nan_to_None()
        self.bonds._nan_to_None()

