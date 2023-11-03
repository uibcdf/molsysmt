import pandas as pd
import numpy as np


class Atoms_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['atom_name', 'atom_id', 'atom_type',
                   'group_index', 'chain_index',
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


class TopologyNEW():

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

        for column in self.components.columns:
            tmp_item.components[column]=self.components[column].to_numpy()

        for column in self.molecules.columns:
            tmp_item.molecules[column]=self.molecules[column].to_numpy()

        for column in self.entities.columns:
            tmp_item.entities[column]=self.entities[column].to_numpy()

        for column in self.chains.columns:
            tmp_item.chains[column]=self.chains[column].to_numpy()

        for column in self.bonds_dataframe.columns:
            tmp_item.bonds_dataframe[column]=self.bonds_dataframe[column].to_numpy()

        return tmp_item


    def _build_components(self):

        raise NotImplementedError

    def _build_molecules(self):

        raise NotImplementedError

    def _build_entities(self):

        raise NotImplementedError

    def _join_molecules(self, indices=None):

        raise NotImplementedError

    def _nan_to_None(self):

        self.atoms._nan_to_None()
        self.groups._nan_to_None()
        self.components._nan_to_None()
        self.molecules._nan_to_None()
        self.entities._nan_to_None()
        self.chains._nan_to_None()
        self.bonds._nan_to_None()

