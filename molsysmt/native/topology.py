import pandas as pd
import numpy as np
from molsysmt._private.variables import is_all


class Atoms_DataFrame(pd.DataFrame):

    def __init__(self, n_atoms=0):

        columns = ['atom_id', 'atom_name', 'atom_type', 'group_index', 'chain_index']

        super().__init__(index=range(n_atoms), columns=columns)

        self['atom_id'] = self['atom_id'].astype('Int64')
        self['atom_name'] = self['atom_name'].astype(str)
        self['atom_type'] = self['atom_type'].astype(str)
        self['group_index'] = self['group_index'].astype('Int64')
        self['chain_index'] = self['chain_index'].astype('Int64')

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)


class Groups_DataFrame(pd.DataFrame):

    def __init__(self, n_groups=0):

        columns = ['group_id', 'group_name', 'group_type', 'component_index']

        super().__init__(index=range(n_groups), columns=columns)

        self['group_id'] = self['group_id'].astype('Int64')
        self['group_name'] = self['group_name'].astype(str)
        self['group_type'] = self['group_type'].astype(str)
        self['component_index'] = self['component_index'].astype('Int64')

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)


class Components_DataFrame(pd.DataFrame):

    def __init__(self, n_components=0):

        columns = ['component_id', 'component_name', 'component_type', 'molecule_index']

        super().__init__(index=range(n_components), columns=columns)

        self['component_id'] = self['component_id'].astype('Int64')
        self['component_name'] = self['component_name'].astype(str)
        self['component_type'] = self['component_type'].astype(str)
        self['molecule_index'] = self['molecule_index'].astype('Int64')

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)


class Molecules_DataFrame(pd.DataFrame):

    def __init__(self, n_molecules=0):

        columns = ['molecule_name', 'molecule_id', 'molecule_type', 'entity_index']

        super().__init__(index=range(n_molecules), columns=columns)

        self['molecule_id'] = self['molecule_id'].astype('Int64')
        self['molecule_name'] = self['molecule_name'].astype(str)
        self['molecule_type'] = self['molecule_type'].astype(str)
        self['entity_index'] = self['entity_index'].astype('Int64')

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)


class Entities_DataFrame(pd.DataFrame):

    def __init__(self, n_entities=0):

        columns = ['entity_id', 'entity_name', 'entity_type']

        super().__init__(index=range(n_entities), columns=columns)

        self['entity_id'] = self['entity_id'].astype('Int64')
        self['entity_name'] = self['entity_name'].astype(str)
        self['entity_type'] = self['entity_type'].astype(str)

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)


class Chains_DataFrame(pd.DataFrame):

    def __init__(self, n_chains=0):

        columns = ['chain_id', 'chain_name', 'chain_type']

        super().__init__(index=range(n_chains), columns=columns)

        self['chain_id'] = self['chain_id'].astype('Int64')
        self['chain_name'] = self['chain_name'].astype(str)
        self['chain_type'] = self['chain_type'].astype(str)

    def _fix_null_values(self):

        for column in self:
            self[column].fillna(pd.NA, inplace=True)


class Bonds_DataFrame(pd.DataFrame):

    def __init__(self, n_bonds=0):

        columns = ['atom1_index', 'atom2_index', 'order', 'type']

        super().__init__(index=range(n_bonds), columns=columns)

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

        self.atoms = Atoms_DataFrame(n_atoms=n_atoms)
        self.groups = Groups_DataFrame(n_groups=n_groups)
        self.components = Components_DataFrame(n_components=n_components)
        self.molecules = Molecules_DataFrame(n_molecules=n_molecules)
        self.entities = Entities_DataFrame(n_entities=n_entities)
        self.chains = Chains_DataFrame(n_chains=n_chains)
        self.bonds = Bonds_DataFrame(n_bonds=n_bonds)

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

    def rebuild_groups(self):

        from molsysmt.element.group import get_group_type

        group_types_from_groups = get_group_type(self, element='group', redefine_types=True)
        self.groups["group_type"] = np.array(group_types_from_groups, dtype=object)

    def rebuild_components(self):

        from molsysmt.element.component import get_component_index, get_component_id,\
        get_component_name, get_component_type

        component_indices_from_groups = get_component_index(self, element='group', redefine_indices=True)
        self.groups["component_index"] = np.array(component_indices_from_groups, dtype=object)
        n_components = component_indices_from_groups[-1]+1
        del component_indices_from_groups

        self.components = Components_DataFrame(n_components=n_components)

        component_id = get_component_id(self, element='component', redefine_ids=True)
        self.components["component_id"] = np.array(component_id, dtype=int)
        del component_id

        component_name = get_component_name(self, element='component', redefine_names=True)
        self.components["component_name"] = np.array(component_name, dtype=object)
        del component_name

        component_type = get_component_type(self, element='component', redefine_types=True)
        self.components["component_type"] = np.array(component_type, dtype=object)
        del component_type
        del n_components

    def rebuild_molecules(self):

        from molsysmt.element.molecule import get_molecule_index, get_molecule_id,\
        get_molecule_name, get_molecule_type

        molecule_indices_from_components = get_molecule_index(self, element='component',
                redefine_components=False, redefine_indices=True)
        self.components["molecule_index"] = np.array(molecule_indices_from_components, dtype=object)
        n_molecules = molecule_indices_from_components[-1]+1
        del molecule_indices_from_components

        self.molecules = Molecules_DataFrame(n_molecules=n_molecules)

        molecule_id = get_molecule_id(self, element='molecule', redefine_ids=True)
        self.molecules["molecule_id"] = np.array(molecule_id, dtype=int)
        del molecule_id

        molecule_name = get_molecule_name(self, element='molecule', redefine_names=True)
        self.molecules["molecule_name"] = np.array(molecule_name, dtype=object)
        del molecule_name

        molecule_type = get_molecule_type(self, element='molecule', redefine_types=True)
        self.molecules["molecule_type"] = np.array(molecule_type, dtype=object)
        del molecule_type
        del n_molecules

    def rebuild_entities(self):

        from molsysmt.element.entity import get_entity_index, get_entity_id,\
        get_entity_name, get_entity_type

        entity_indices_from_molecules = get_entity_index(self, element='molecule',
                redefine_molecules=False, redefine_indices=True)
        self.molecules["entity_index"] = np.array(entity_indices_from_molecules, dtype=object)
        n_entities = entity_indices_from_molecules[-1]+1
        del entity_indices_from_molecules

        self.entities = Entities_DataFrame(n_entities=n_entities)

        entity_id = get_entity_id(self, element='entity', redefine_ids=True)
        self.entities["entity_id"] = np.array(entity_id, dtype=int)
        del entity_id

        entity_name = get_entity_name(self, element='entity', redefine_names=True)
        self.entities["entity_name"] = np.array(entity_name, dtype=object)
        del entity_name

        entity_type = get_entity_type(self, element='entity', redefine_types=True)
        self.entities["entity_type"] = np.array(entity_type, dtype=object)
        del entity_type
        del n_entities

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
