import pandas as pd
import numpy as np


class Atoms_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['atom_index', 'atom_name', 'atom_id', 'atom_type',
                   'group_index', 'group_name', 'group_id', 'group_type',
                   'component_index', 'component_name', 'component_id', 'component_type',
                   'chain_index', 'chain_name', 'chain_id', 'chain_type',
                   'molecule_index', 'molecule_name', 'molecule_id', 'molecule_type',
                   'entity_index', 'entity_name', 'entity_id', 'entity_type',
                   'occupancy', 'alternate_location', 'b_factor', 'formal_charge', 'partial_charge']

        super().__init__(columns=columns)

    def _nan_to_UNK(self):

        for column in self:
            self[column].where(self[column].notnull(), 'UNK', inplace=True)


class Groups_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['group_name', 'group_id', 'group_type', 'component_index']

        super().__init__(columns=columns)

    def _nan_to_UNK(self):

        for column in self:
            self[column].where(self[column].notnull(), 'UNK', inplace=True)


class Components_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['component_name', 'component_id', 'component_type', 'molecule_index']

        super().__init__(columns=columns)

    def _nan_to_UNK(self):

        for column in self:
            self[column].where(self[column].notnull(), 'UNK', inplace=True)


class Molecules_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['molecule_name', 'molecule_id', 'molecule_type', 'entity_index']

        super().__init__(columns=columns)

    def _nan_to_UNK(self):

        for column in self:
            self[column].where(self[column].notnull(), 'UNK', inplace=True)


class Entities_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['entity_name', 'entity_id', 'entity_type']

        super().__init__(columns=columns)

    def _nan_to_UNK(self):

        for column in self:
            self[column].where(self[column].notnull(), 'UNK', inplace=True)


class Chains_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['chain_name', 'chain_id', 'chain_type']

        super().__init__(columns=columns)

    def _nan_to_UNK(self):

        for column in self:
            self[column].where(self[column].notnull(), 'UNK', inplace=True)


class Bonds_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['atom1_index', 'atom2_index', 'order', 'type']

        super().__init__(columns=columns)

    def _nan_to_UNK(self):

        for column in self:
            self[column].where(self[column].notnull(), 'UNK', inplace=True)

    def _sort_bonds(self):

        self_mask = self['atom1_index'] > self['atom2_index']
        self.update(self.loc[self_mask].rename({'atom1_index': 'atom2_index',
                                      'atom2_index': 'atom1_index'}, axis=1))
        self.sort_values(by=['atom1_index', 'atom2_index'], inplace=True)
        self.reset_index(drop=True, inplace=True)


class Topology2():

    def __init__(self, n_atoms=0, n_bonds=0):

        self.atoms = Atoms_DataFrame()
        self.groups = Groups_DataFrame()
        self.components = Components_DataFrame()
        self.molecules = Molecules_DataFrame()
        self.entities = Entities_DataFrame()
        self.chains = Chains_DataFrame()
        self.bonds = Bonds_DataFrame()

    def extract(self, atom_indices='all'):

        if type(atom_indices)==str:

            if atom_indices in ['all', 'All', 'ALL']:
                return self.copy()

        else:

            raise NotImplementedError

        return tmp_item


    def add(self, item, selection='all'):

        raise NotImplementedError


    def copy(self):

        tmp_item = Topology2()

        tmp_item.atoms = Atoms_DataFrame()
        tmp_item.groups = Groups_DataFrame()
        tmp_item.components = Components_DataFrame()
        tmp_item.molecules = Molecules_DataFrame()
        tmp_item.entities = Entities_DataFrame()
        tmp_item.chains = Chains_DataFrame()
        tmp_item.bonds = Bonds_DataFrame()

        for column in self.atoms.columns:
            tmp_item.atoms[column]=self.atoms[column].to_numpy()

        for column in self.groups.columns:
            tmp_item.groups[column]=self.groups[column].to_numpy()

        for column in self.groups.columns:
            tmp_item.groups[column]=self.groups[column].to_numpy()



        for column in self.bonds_dataframe.columns:
            tmp_item.bonds_dataframe[column]=self.bonds_dataframe[column].to_numpy()

        return tmp_item


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

