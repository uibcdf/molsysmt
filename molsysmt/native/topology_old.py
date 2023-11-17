import pandas as pd
import numpy as np

class Atoms_DataFrame(pd.DataFrame):

    def __init__(self, n_atoms=0):

        columns = ['atom_index', 'atom_name', 'atom_id', 'atom_type',
                   'group_index', 'group_name', 'group_id', 'group_type',
                   'component_index', 'component_name', 'component_id', 'component_type',
                   'chain_index', 'chain_name', 'chain_id', 'chain_type',
                   'molecule_index', 'molecule_name', 'molecule_id', 'molecule_type',
                   'entity_index', 'entity_name', 'entity_id', 'entity_type',
                   'occupancy', 'alternate_location', 'b_factor', 'formal_charge', 'partial_charge']

        # columns with dimensionality:
        #
        # 'b_factor' = {'[L]': 2}
        # 'formal_charge' = {'[T]': 1, '[A]:1'}
        # 'partial_charge' = {'[T]': 1, '[A]:1'}

        super().__init__(columns=columns)

        if n_atoms:
            self["atom_index"] = np.arange(0, n_atoms, dtype=int)
            self._nan_to_None()

    def _nan_to_None(self):

        for column in self:
            self[column].where(self[column].notnull(), None, inplace=True)


class Bonds_DataFrame(pd.DataFrame):

    def __init__(self, n_bonds=0):

        columns = ['atom1_index', 'atom2_index', 'order', 'type']

        super().__init__(columns=columns)

        if n_bonds:
            self["atom_index"] = np.arange(0, n_atoms, dtype=int)
            self._nan_to_None()

    def all_nan_to_None(self):

        list_columns_where_nan = ['atom1_index','atom2_index','order','type']

        for column in self:
            self[column].where(self[column].notnull(), None, inplace=True)

    def _nan_to_None(self):

        list_columns_where_nan = ['order','type']

        for column in self:
            self[column].where(self[column].notnull(), None, inplace=True)

    def _sort_bonds(self):

        self_mask = self['atom1_index'] > self['atom2_index']
        self.update(self.loc[self_mask].rename({'atom1_index': 'atom2_index',
                                      'atom2_index': 'atom1_index'}, axis=1))
        self.sort_values(by=['atom1_index', 'atom2_index'], inplace=True)
        self.reset_index(drop=True, inplace=True)

class TopologyOld():

    def __init__(self, n_atoms=0, n_bonds=0):

        self.atoms_dataframe=Atoms_DataFrame(n_atoms=n_atoms)
        self.bonds_dataframe=Bonds_DataFrame(n_bonds=n_bonds)

    def extract(self, atom_indices='all', structure_indices='all'):

        if type(atom_indices)==str:

            if is_all(atom_indices):
                return self.copy()

        else:

            tmp_item = TopologyOld()
            tmp_item.atoms_dataframe = self.atoms_dataframe.iloc[atom_indices].copy()

            bond_atom1 = self.bonds_dataframe['atom1_index'].to_numpy()
            bond_atom2 = self.bonds_dataframe['atom2_index'].to_numpy()
            mask_atom1 = np.in1d(bond_atom1, atom_indices)
            mask_atom2 = np.in1d(bond_atom2, atom_indices)
            mask = mask_atom1*mask_atom2
            tmp_item.bonds_dataframe = self.bonds_dataframe[mask].copy()
            tmp_item.bonds_dataframe.reset_index(drop=True, inplace=True)
            del(bond_atom1, bond_atom2, mask_atom1, mask_atom2)

            n_atoms=tmp_item.atoms_dataframe.shape[0]
            n_bonds=tmp_item.bonds_dataframe.shape[0]

            tmp_item.atoms_dataframe['atom_index']=np.arange(n_atoms)
            aux_dict=tmp_item.atoms_dataframe['atom_index'].to_dict()
            tmp_item.atoms_dataframe.index=np.arange(n_atoms)

            vaux_dict = np.vectorize(aux_dict.__getitem__)

            if n_bonds>0:
                tmp_item.bonds_dataframe['atom1_index']=vaux_dict(tmp_item.bonds_dataframe['atom1_index'].to_numpy())
                tmp_item.bonds_dataframe['atom2_index']=vaux_dict(tmp_item.bonds_dataframe['atom2_index'].to_numpy())

            tmp_item.atoms_dataframe.index=tmp_item.atoms_dataframe['atom_index'].to_numpy()

            #tmp_item._build_components()

            for column in ['group_index', 'component_index', 'molecule_index', 'chain_index', 'entity_index']:
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

    def add(self, item, selection='all', structure_indices='all'):

        from molsysmt import convert, get

        tmp_item = convert(item, to_form='molsysmt.TopologyOld', selection=selection, structure_indices=structure_indices)

        n_atoms, n_groups, n_components, n_chains, n_molecules = get(self, element='system', n_atoms=True,
                                                                     n_groups=True, n_components=True, n_chains=True,
                                                                     n_molecules=True)

        tmp_item.atoms_dataframe['atom_index'] += n_atoms
        tmp_item.atoms_dataframe['group_index'] += n_groups
        tmp_item.atoms_dataframe['component_index'] += n_components
        tmp_item.atoms_dataframe['chain_index'] += n_chains
        tmp_item.atoms_dataframe['molecule_index'] += n_molecules
        tmp_item.bonds_dataframe['atom1_index'] += n_atoms
        tmp_item.bonds_dataframe['atom2_index'] += n_atoms


        self.atoms_dataframe = pd.concat([self.atoms_dataframe, tmp_item.atoms_dataframe],
                ignore_index=True, copy=False)
        self.bonds_dataframe = pd.concat([self.bonds_dataframe, tmp_item.bonds_dataframe],
                ignore_index=True, copy=False)
        self._build_entities()

    def copy(self):

        tmp_item = TopologyOld()

        tmp_item.atoms_dataframe = Atoms_DataFrame()
        tmp_item.bonds_dataframe = Bonds_DataFrame()

        for column in self.atoms_dataframe.columns:
            tmp_item.atoms_dataframe[column]=self.atoms_dataframe[column].to_numpy()

        for column in self.bonds_dataframe.columns:
            tmp_item.bonds_dataframe[column]=self.bonds_dataframe[column].to_numpy()

        return tmp_item

    #def _to_pdb_string(self, trajectory_item, structure_indices='all'):

    #    from molsysmt.native.io.topology import to_pdb as molsysmt_Topology_to_pdb

    #    return molsysmt_Topology_to_pdb(self, trajectory_item=trajectory_item, output_filepath='.pdb',
    #                                     atom_indices='all', structure_indices=structure_indices)

    def _build_components(self):

        from molsysmt.element.component import get_component_type_from_group_names
        from molsysmt.element.component import get_component_index_from_bonded_atoms

        n_atoms = self.atoms_dataframe.shape[0]
        n_bonds = self.bonds_dataframe.shape[0]

        group_index_from_atom = self.atoms_dataframe['group_index'].to_numpy()
        group_name_from_atom = self.atoms_dataframe['group_name'].to_numpy()
        atom_index_from_bond = self.bonds_dataframe[['atom1_index','atom2_index']].to_numpy(dtype=int, copy=True)

        if n_bonds==0:

            index_array = np.full(n_atoms, None, dtype=object)
            id_array = np.full(n_atoms, None, dtype=object)
            name_array = np.full(n_atoms, None, dtype=object)
            type_array = np.full(n_atoms, None, dtype=object)

        else:

            index_array = get_component_index_from_bonded_atoms(atom_index_from_bond, n_atoms)
            component_indices = np.unique(index_array)
            n_components = component_indices.shape[0]

            type_array = np.full(n_atoms, None, dtype=object)

            for ii in component_indices:

                mask = (index_array==ii)
                group_indices=np.unique(group_index_from_atom[mask])
                group_names=[]
                for group_index in group_indices:
                    first_occurrence = np.where(group_index_from_atom==group_index)[0][0]
                    group_names.append(group_name_from_atom[first_occurrence])

                type_array[mask]=get_component_type_from_group_names(group_names)

        self.atoms_dataframe["component_index"] = index_array
        self.atoms_dataframe["component_id"] = index_array
        self.atoms_dataframe["component_name"] = index_array
        self.atoms_dataframe["component_type"] = type_array

        del(group_index_from_atom, group_name_from_atom, atom_index_from_bond, index_array, type_array)

    def _build_molecules(self):

        component_index_from_atom = self.atoms_dataframe['component_index'].to_numpy()
        component_type_from_atom = self.atoms_dataframe['component_type'].to_numpy()

        n_atoms=component_index_from_atom.shape[0]
        index_array = component_index_from_atom.copy()
        id_array = np.full(n_atoms, None, dtype=object)
        name_array = np.full(n_atoms, None, dtype=object)
        type_array = component_type_from_atom.copy()

        self.atoms_dataframe["molecule_index"] = index_array
        self.atoms_dataframe["molecule_id"] = id_array
        self.atoms_dataframe["molecule_name"] = name_array
        self.atoms_dataframe["molecule_type"] = type_array

        del(component_index_from_atom, component_type_from_atom, index_array, id_array, name_array,
                type_array)

    def _build_entities(self):

        n_atoms=self.atoms_dataframe.shape[0]

        entity_index = np.empty(n_atoms, dtype=int)
        entity_name = np.empty(n_atoms, dtype=object)
        entity_id = np.empty(n_atoms, dtype=object)
        entity_type = np.empty(n_atoms, dtype=object)

        entities= {}
        n_entities = 0

        current_molecule_name = '@'

        ii=0
        for molecule_name, molecule_type in zip(self.atoms_dataframe['molecule_name'],
                self.atoms_dataframe['molecule_type']):

            if molecule_name!=current_molecule_name:

                current_molecule_name=molecule_name
                current_molecule_type=molecule_type

                if current_molecule_name in entities:

                    current_entity_index = entities[current_molecule_name]['entity_index']
                    current_entity_id = entities[current_molecule_name]['entity_id']
                    current_entity_name = entities[current_molecule_name]['entity_name']
                    current_entity_type = entities[current_molecule_name]['entity_type']

                else:

                    current_entity_index = n_entities
                    current_entity_id = n_entities
                    current_entity_name = current_molecule_name
                    current_entity_type = current_molecule_type

                    entities[current_entity_name]={}
                    entities[current_entity_name]['entity_index'] = current_entity_index
                    entities[current_entity_name]['entity_id'] = current_entity_id
                    entities[current_entity_name]['entity_name'] = current_entity_name
                    entities[current_entity_name]['entity_type'] = current_entity_type

                    n_entities +=1

            entity_index[ii]=current_entity_index
            entity_id[ii]=current_entity_id
            entity_name[ii]=current_entity_name
            entity_type[ii]=current_entity_type

            ii+=1

        self.atoms_dataframe["entity_index"] = entity_index
        self.atoms_dataframe["entity_name"] = entity_name
        self.atoms_dataframe["entity_type"] = entity_type
        self.atoms_dataframe["entity_id"] = entity_id

        del(entity_name, entity_type, entity_id)
        del(entities)

    def _join_molecules(self, indices=None):

        pass

    def _nan_to_None(self):

        self.atoms_dataframe._nan_to_None()
        self.bonds_dataframe._nan_to_None()

