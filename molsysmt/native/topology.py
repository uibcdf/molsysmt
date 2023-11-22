import pandas as pd
from molsysmt._private.variables import is_all


class Atoms_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['atom_id', 'atom_name', 'atom_type', 'group_index', 'chain_index']

        super().__init__(columns=columns)

        self['atom_id'] = self['atom_id'].astype('Int64')
        self['atom_name'] = self['atom_name'].astype(str)
        self['atom_type'] = self['atom_type'].astype(str)
        self['group_index'] = self['group_index'].astype('Int64')
        self['chain_index'] = self['chain_index'].astype('Int64')

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)


class Groups_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['group_id', 'group_name', 'group_type', 'component_index']

        super().__init__(columns=columns)

        self['group_id'] = self['group_id'].astype('Int64')
        self['group_name'] = self['group_name'].astype(str)
        self['group_type'] = self['group_type'].astype(str)
        self['component_index'] = self['component_index'].astype('Int64')

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)


class Components_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['component_id', 'component_name', 'component_type', 'molecule_index']

        super().__init__(columns=columns)

        self['component_id'] = self['component_id'].astype('Int64')
        self['component_name'] = self['component_name'].astype(str)
        self['component_type'] = self['component_type'].astype(str)
        self['molecule_index'] = self['molecule_index'].astype('Int64')

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)


class Molecules_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['molecule_name', 'molecule_id', 'molecule_type', 'entity_index']

        super().__init__(columns=columns)

        self['molecule_id'] = self['molecule_id'].astype('Int64')
        self['molecule_name'] = self['molecule_name'].astype(str)
        self['molecule_type'] = self['molecule_type'].astype(str)
        self['entity_index'] = self['entity_index'].astype('Int64')

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)


class Entities_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['entity_id', 'entity_name', 'entity_type']

        super().__init__(columns=columns)

        self['entity_id'] = self['entity_id'].astype('Int64')
        self['entity_name'] = self['entity_name'].astype(str)
        self['entity_type'] = self['entity_type'].astype(str)

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)


class Chains_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['chain_id', 'chain_name', 'chain_type']

        super().__init__(columns=columns)

        self['chain_id'] = self['chain_id'].astype('Int64')
        self['chain_name'] = self['chain_name'].astype(str)
        self['chain_type'] = self['chain_type'].astype(str)

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)


class Bonds_DataFrame(pd.DataFrame):

    def __init__(self):

        columns = ['atom1_index', 'atom2_index', 'order', 'type']

        super().__init__(columns=columns)

        self['atom1_index'] = self['atom1_index'].astype('Int64')
        self['atom2_index'] = self['atom2_index'].astype('Int64')
        self['order'] = self['order'].astype(str)
        self['type'] = self['type'].astype(str)

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)

    def _sort_bonds(self):

        self_mask = self['atom1_index'] > self['atom2_index']
        self.update(self.loc[self_mask].rename({'atom1_index': 'atom2_index', 'atom2_index': 'atom1_index'}, axis=1))
        self.sort_values(by=['atom1_index', 'atom2_index'], inplace=True)
        self.reset_index(drop=True, inplace=True)


class Topology():

    def __init__(self, n_atoms=0, n_groups=0, n_components=0, n_molecules=0, n_entities=0, n_chains=0, n_bonds=0):

        self.atoms = Atoms_DataFrame()
        self.groups = Groups_DataFrame()
        self.components = Components_DataFrame()
        self.molecules = Molecules_DataFrame()
        self.entities = Entities_DataFrame()
        self.chains = Chains_DataFrame()
        self.bonds = Bonds_DataFrame()

    def extract(self, atom_indices='all', copy_if_all=False):

        if is_all(atom_indices):

            if copy_if_all:

                return self.copy()

            else:

                return self

        else:

            raise NotImplementedError

    def add(self, item, selection='all'):

        raise NotImplementedError

    def copy(self):

        tmp_item = Topology()

        tmp_item.atoms = self.atoms.copy()
        tmp_item.groups = self.groups.copy()
        tmp_item.components = self.components.copy()
        tmp_item.molecules = self.molecules.copy()
        tmp_item.entities = self.entities.copy()
        tmp_item.chains = self.chains.copy()
        tmp_item.bonds = self.bonds.copy()

        return tmp_item

    def rebuild_components(self):

        raise NotImplementedError

    def rebuild_molecules(self):

        raise NotImplementedError

    def rebuild_entities(self):

        raise NotImplementedError

    def _join_molecules(self, indices=None):

        raise NotImplementedError

    def _fix_null_values(self):

        self.atoms._fix_null_values()
        self.groups._fix_null_values()
        self.components._fix_null_values()
        self.molecules._fix_null_values()
        self.entities._fix_null_values()
        self.chains._fix_null_values()
        self.bonds._fix_null_values()

    def _sort_bonds(self):

        self.bonds._sort_bonds()
