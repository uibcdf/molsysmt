from pandas import DataFrame as Pandas_DataFrame

class Atoms_DataFrame(Pandas_DataFrame):

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


class Bonds_DataFrame(Pandas_DataFrame):

    def __init__(self):

        topology_columns = ['atom1_index', 'atom2_index', 'order', 'type']


        super().__init__(columns=topology_columns)

    def _nan_to_None(self):

        list_columns_where_nan = ['order','type']

        for column in list_columns_where_nan:
            self[column].where(self[column].notnull(), None, inplace=True)

class Topology():

    def __init__(self):

        self.atoms_dataframe=Atoms_DataFrame()
        self.bonds_dataframe=Bonds_DataFrame()

    def extract(self, atom_indices='all', frame_indices='all'):

        if type(atom_indices)==str:

            if atom_indices in ['all', 'All', 'ALL']:
                return self.copy()

        else:

            from numpy import arange, empty, vectorize, in1d

            tmp_item = Topology()
            tmp_item.atoms_dataframe = self.atoms_dataframe.iloc[atom_indices].copy()

            bond_atom1 = self.bonds['atom1_index'].to_numpy()
            bond_atom2 = self.bonds['atom2_index'].to_numpy()
            mask_atom1 = in1d(bond_atom1, atom_indices)
            mask_atom2 = in1d(bond_atom2, atom_indices)
            mask = mask_atom1*mask_atom2
            tmp_item.bonds_dataframe = self.bonds_dataframe[mask].copy()
            del(bond_atom1, bond_atom2, mask_atom1, mask_atom2)

            n_atoms=tmp_item.atoms_dataframe.shape[0]
            n_bonds=tmp_item.bonds_dataframe.shape[0]

            tmp_item.atoms_dataframe['atom_index']=arange(n_atoms)
            aux_dict=tmp_item.atoms_dataframe['atom_index'].to_dict()
            tmp_item.atoms_dataframe.index=arange(n_atoms)
            vaux_dict = vectorize(aux_dict.__getitem__)

            tmp_item.bonds_dataframe['atom1_index']=vaux_dict(tmp_item.bonds_dataframe['atom1_index'].to_numpy())
            tmp_item.bonds_dataframe['atom2_index']=vaux_dict(tmp_item.bonds_dataframe['atom2_index'].to_numpy())
            tmp_item.atoms_dataframe.index=tmp_item.atoms_dataframe['atom_index'].to_numpy()

            tmp_item._build_components()

            for column in ['group_index', 'molecule_index', 'chain_index', 'entity_index']:
                aux_array=tmp_item.atoms_dataframe[column].to_numpy()
                old_index=-1
                count=-1
                for ii in range(n_atoms):
                    if old_index!=aux_array[ii]:
                        old_index=aux_array[ii]
                        count+=1
                    aux_array[ii]=count
                tmp_item.atoms_dataframe[column]=aux_array

        return tmp_item

    def copy(self):

        tmp_item = Topology()

        tmp_item.atoms_dataframe = Atoms_DataFrame()
        tmp_item.bonds_dataframe = Bonds_DataFrame()

        for column in self.atoms_dataframe.columns:
            tmp_item.atoms_dataframe[column]=self.atoms_dataframe[column].to_numpy()

        for column in self.bonds_dataframe.columns:
            tmp_item.bonds_dataframe[column]=self.bonds_dataframe[column].to_numpy()

        return tmp_item

    def _to_pdb_string(self, trajectory_item, frame_indices='all'):

        from molsysmt.native.io.topology.files import to_pdb as molsysmt_Topology_to_pdb

        return molsysmt_Topology_to_pdb(self, trajectory_item=trajectory_item, output_filepath='.pdb',
                                         atom_indices='all', frame_indices=frame_indices)

    def _build_components(self):

        from molsysmt.elements.component import get_elements

        index_array, id_array, name_array, type_array = get_elements(self)

        self.atoms_dataframe["component_index"] = index_array
        self.atoms_dataframe["component_id"] = id_array
        self.atoms_dataframe["component_name"] = name_array
        self.atoms_dataframe["component_type"] = type_array

    def _build_molecules(self):

        from molsysmt.elements.molecule import get_elements

        index_array, id_array, name_array, type_array = get_elements(self)

        self.atoms_dataframe["molecule_index"] = index_array
        self.atoms_dataframe["molecule_id"] = id_array
        self.atoms_dataframe["molecule_name"] = name_array
        self.atoms_dataframe["molecule_type"] = type_array

    def _build_entities(self):

        from molsysmt.elements.entity import get_elements

        index_array, id_array, name_array, type_array = get_elements(self)

        self.atoms_dataframe["entity_index"] = index_array
        self.atoms_dataframe["entity_id"] = id_array
        self.atoms_dataframe["entity_name"] = name_array
        self.atoms_dataframe["entity_type"] = type_array

    def _join_molecules(self, indices=None):

        pass


    def _nan_to_None(self):

        self.atoms_dataframe._nan_to_None()
        self.bonds_dataframe._nan_to_None()

