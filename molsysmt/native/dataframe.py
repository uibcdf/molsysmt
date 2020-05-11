from pandas import DataFrame as PandasDataFrame

class DataFrame(PandasDataFrame):

    def __init__(self):

        topology_columns = ['atom.index', 'atom.name', 'atom.id', 'atom.type',
                               'atom.formal_charge', 'atom.bonded_atom_indices',
                               'group.index', 'group.name', 'group.id', 'group.type',
                               'component.index', 'component.name', 'component.id', 'component.type',
                               'chain.index', 'chain.name', 'chain.id', 'chain.type',
                               'molecule.index', 'molecule.name', 'molecule.id', 'molecule.type',
                               'entity.index', 'entity.name', 'entity.id', 'entity.type']


        super().__init__(columns=topology_columns)

    def extract(self, atom_indices='all'):

        if type(atom_indices)==str:

            if atom_indices in ['all', 'All', 'ALL']:
                return self.copy()

        else:

            from numpy import arange, empty
            from networkx import empty_graph, connected_components

            tmp_item = DataFrame()
            for column in self.columns:
                tmp_item[column]=self[column][atom_indices]

            n_atoms=tmp_item.shape[0]
            G = empty_graph(n_atoms)

            tmp_item['atom.index']=arange(n_atoms)
            aux_dict=tmp_item['atom.index'].to_dict()
            array_bonded_atom_indices=tmp_item['atom.bonded_atom_indices'].to_numpy()
            for ii in range(n_atoms):
                bonded_atom_indices=[]
                for old_atom_index in array_bonded_atom_indices[ii]:
                    if old_atom_index in aux_dict:
                        new_atom_index=aux_dict[old_atom_index]
                        bonded_atom_indices.append(new_atom_index)
                        if ii<new_atom_index:
                            G.add_edge(ii,new_atom_index)
                array_bonded_atom_indices[ii]=bonded_atom_indices.copy()
            tmp_item['atom.bonded_atom_indices']=array_bonded_atom_indices
            tmp_item.index=arange(n_atoms)

            atom_indices_per_component = list(connected_components(G))
            del(G)

            component_index_array = empty(n_atoms, dtype=int)
            component_index = 0
            for atom_indices_of_component in atom_indices_per_component:
                for atom_index in atom_indices_of_component:
                    component_index_array[atom_index] = component_index
                component_index += 1
            tmp_item["component.index"] = component_index_array


            for column in ['group.index', 'molecule.index', 'chain.index', 'entity.index']:
                aux_array=tmp_item[column].to_numpy()
                old_index=-1
                count=-1
                for ii in range(n_atoms):
                    if old_index!=aux_array[ii]:
                        old_index=aux_array[ii]
                        count+=1
                    aux_array[ii]=count
                tmp_item[column]=aux_array

            return tmp_item

    def copy(self):

        item = DataFrame()
        for column in self.columns:
            item[column]=self[column]

        return item

    def _nan_to_None(self):

        list_columns_where_nan = ['group.type', 'component.name', 'component.type',
                                 'chain.name', 'chain.type', 'molecule.name', 'molecule.type',
                                 'entity.name', 'entity.type']

        for column in list_columns_where_nan:
            self[column].where(self[column].notnull(), None, inplace=True)

    def _to_pdb_string(self, trajectory_item, frame_indices='all', engine='OpenMM'):

        from molsysmt.native.io.dataframe.files import to_pdb as molsysmt_DataFrame_to_pdb

        pdb_string=molsysmt_DataFrame_to_pdb(self, output_file_path='.pdb', atom_indices='all',
                                             frame_indices=frame_indices, engine=engine)

        return pdb_string

