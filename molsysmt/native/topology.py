from pandas import DataFrame as PandasDataFrame

class Topology(PandasDataFrame):

    def __init__(self):

        topology_columns = ['atom.index', 'atom.name', 'atom.id', 'atom.type',
                               'atom.formal_charge', 'atom.bonded_atom_indices',
                               'group.index', 'group.name', 'group.id', 'group.type',
                               'component.index', 'component.name', 'component.id', 'component.type',
                               'chain.index', 'chain.name', 'chain.id', 'chain.type',
                               'molecule.index', 'molecule.name', 'molecule.id', 'molecule.type',
                               'entity.index', 'entity.name', 'entity.id', 'entity.type']


        super().__init__(columns=topology_columns)

    def extract(self, atom_indices='all', frame_indices='all'):

        if type(atom_indices)==str:

            if atom_indices in ['all', 'All', 'ALL']:
                return self.copy()

        else:

            from numpy import arange, empty
            from networkx import empty_graph, connected_components

            tmp_item = Topology()
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

        item = Topology()
        for column in self.columns:
            item[column]=self[column]

        return item

    def _nan_to_None(self):

        list_columns_where_nan = ['group.type', 'component.name', 'component.type',
                                 'chain.name', 'chain.type', 'molecule.name', 'molecule.type',
                                 'entity.name', 'entity.type']

        for column in list_columns_where_nan:
            self[column].where(self[column].notnull(), None, inplace=True)

    def _to_pdb_string(self, trajectory_item, frame_indices='all'):

        from molsysmt.native.io.dataframe.files import to_pdb as molsysmt_DataFrame_to_pdb

        return molsysmt_DataFrame_to_pdb(self, trajectory_item=trajectory_item, output_filepath='.pdb',
                                         atom_indices='all', frame_indices=frame_indices)

    def _build_components_type(self):

        from molsysmt.forms.classes.api_molsysmt_Topology import get_n_components_from_system
        from molsysmt.forms.classes.api_molsysmt_Topology import get_n_groups_from_component

        n_components = get_n_components_from_system(self)
        n_groups_per_component = get_n_groups_from_component(self, 'all')

        print(n_components)
        print(n_groups_per_component)

    #def _rebuild_auxiliary_lists(self):

    #    atom_index_array = self['atom.index'].to_numpy()
    #    group_index_array = self['group.index'].to_numpy()
    #    component_index_array = self['component.index'].to_numpy()
    #    molecule_index_array = self['molecule.index'].to_numpy()
    #    chain_index_array = self['chain.index'].to_numpy()
    #    entity_index_array = self['entity.index'].to_numpy()

    #    for atom_index, group_index, component_index, molecule_index, chain_index,
    #    entity_index in zip(atom_index_array, group_index_array, component_index_array,
    #                       molecule_index_array, chain_index_array)
    #    n_atoms = self['atom.index'][-1]

    #def _rebuild_components_molecules_entities(self):

    #    from numpy import unique, argwhere

    #    group_index_array = self['group.index'].to_numpy()
    #    group_type_array = self['group.type'].to_numpy()
    #    component_index_array = self['component.index'].to_numpy()

    #    n_components = component_index_array[-1]+1

    #    for component_index in range(n_components):
    #        atom_indices_in_component = argwhere(component_index_array == component_index)
    #        aux_group_type = group_type_array[atom_indices_in_component[0]]
    #        tmp_component_type = None
    #        if aux_group_type in ['water','ion','cosolute','small_molecule']:
    #            tmp_component_type=aux_group_type
    #        elif aux_group_type == 'nucleotide':
    #            if aux_group_type in rna_names:
    #                tmp_component_type = 'rna'
    #            elif aux_group_type in dna_names:
    #                tmp_component_type = 'dna'
    #        elif aux_group_type == 'aminoacid':
    #            aux_n_groups = unique(group_index_array[atom_indices_in_component]).shape[0]
    #            if aux_n_groups>=50:
    #                tmp_component_type = 'protein'
    #            else:
    #                tmp_component_type = 'peptide'
    #        component_type_array[aux_list]=tmp_component_type

    #    self['component.type']=component_type_array

    #    del(group_index_array, group_type_array, component_index_array)

    #    pass

