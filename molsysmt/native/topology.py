import pandas as pd
import numpy as np
from molsysmt._private.variables import is_all
from molsysmt._private.arg_digestion import arg_digest
from molsysmt.lib.series import occurrence_order
import string
from smonitor import signal

class Atoms_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing atom-level topology fields."""

    def __init__(self, n_atoms=0):
        """Initialize an atoms table with the expected columns and dtypes."""

        columns = ['atom_id', 'atom_name', 'atom_type', 'group_index', 'component_index', 'chain_index']

        super().__init__(index=range(n_atoms), columns=columns)

        self['atom_id'] = self['atom_id'].astype('string')
        self['atom_name'] = self['atom_name'].astype(str)
        self['atom_type'] = self['atom_type'].astype(str)
        self['group_index'] = self['group_index'].astype('Int64')
        self['component_index'] = self['component_index'].astype('Int64')
        self['chain_index'] = self['chain_index'].astype('Int64')

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""

        for column in self:
            self[column]=self[column].fillna(pd.NA)
        self['atom_id'] = self['atom_id'].astype('string')


class Groups_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing group-level fields."""

    def __init__(self, n_groups=0):
        """Initialize a groups table with default types."""

        columns = ['group_id', 'group_name', 'group_type', 'molecule_index']

        super().__init__(index=range(n_groups), columns=columns)

        self['group_id'] = self['group_id'].astype('string')
        self['group_name'] = self['group_name'].astype(str)
        self['group_type'] = self['group_type'].astype(str)
        self['molecule_index'] = self['molecule_index'].astype('Int64')

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""

        for column in self:
            self[column]=self[column].fillna(pd.NA)
        self['group_id'] = self['group_id'].astype('string')


class Molecules_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing molecule-level fields."""

    def __init__(self, n_molecules=0):
        """Initialize a molecules table with default types."""

        columns = ['molecule_id', 'molecule_name', 'molecule_type', 'entity_index']

        super().__init__(index=range(n_molecules), columns=columns)


        self['molecule_id'] = self['molecule_id'].astype('string')
        self['molecule_name'] = self['molecule_name'].astype(str)
        self['molecule_type'] = self['molecule_type'].astype(str)
        self['entity_index'] = self['entity_index'].astype('Int64')

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""

        for column in self:
            self[column]=self[column].fillna(pd.NA)
        self['molecule_id'] = self['molecule_id'].astype('string')


class Entities_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing entity-level fields."""

    def __init__(self, n_entities=0):
        """Initialize an entities table with default types."""

        columns = ['entity_id', 'entity_name', 'entity_type']

        super().__init__(index=range(n_entities), columns=columns)

        self['entity_id'] = self['entity_id'].astype('string')
        self['entity_name'] = self['entity_name'].astype(str)
        self['entity_type'] = self['entity_type'].astype(str)

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""


        for column in self:
            self[column]=self[column].fillna(pd.NA)
        self['entity_id'] = self['entity_id'].astype('string')


class Components_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing component-level fields."""

    def __init__(self, n_components=0):
        """Initialize a components table with default types."""

        columns = ['component_id', 'component_name', 'component_type']

        super().__init__(index=range(n_components), columns=columns)

        self['component_id'] = self['component_id'].astype('string')
        self['component_name'] = self['component_name'].astype(str)
        self['component_type'] = self['component_type'].astype(str)

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""

        for column in self:
            self[column]=self[column].fillna(pd.NA)
        self['component_id'] = self['component_id'].astype('string')


class Chains_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing chain-level fields."""

    def __init__(self, n_chains=0):
        """Initialize a chains table with default types."""

        columns = ['chain_id', 'chain_name', 'chain_type']

        super().__init__(index=range(n_chains), columns=columns)

        self['chain_id'] = self['chain_id'].astype('string')
        self['chain_name'] = self['chain_name'].astype(str)
        self['chain_type'] = self['chain_type'].astype(str)

    def _fix_null_values(self):
        """Normalize missing values and enforce string ids."""

        for column in self:
            self[column]=self[column].fillna(pd.NA)
        self['chain_id'] = self['chain_id'].astype('string')


class Bonds_DataFrame(pd.DataFrame):
    """Pandas DataFrame wrapper storing bond connectivity."""

    def __init__(self, n_bonds=0):
        """Initialize a bonds table with default types."""

        columns = ['atom1_index', 'atom2_index']
        columns += ['order', 'type'] # extra columns -not necessary-

        super().__init__(index=range(n_bonds), columns=columns)

        self['atom1_index'] = self['atom1_index'].astype('Int64')
        self['atom2_index'] = self['atom2_index'].astype('Int64')
        self['order'] = self['order'].astype(str)
        self['type'] = self['type'].astype(str)

    def _reset(self, n_bonds=0):
        """Rebuild the bonds table to a clean state with the given size."""

        columns = ['atom1_index', 'atom2_index']
        columns += ['order', 'type'] # extra columns -not necessary-

        super().__init__(index=range(n_bonds), columns=columns)

        self['atom1_index'] = self['atom1_index'].astype('Int64')
        self['atom2_index'] = self['atom2_index'].astype('Int64')
        self['order'] = self['order'].astype(str)
        self['type'] = self['type'].astype(str)

    def _fix_null_values(self):
        """Normalize missing values in optional bond columns."""

        for column in self:
            self[column]=self[column].fillna(pd.NA)

    def _sort_bonds(self):
        """Sort bonds so `atom1_index` is always <= `atom2_index`."""

        mask = self['atom1_index'] > self['atom2_index']
        self.loc[mask, ['atom1_index', 'atom2_index']] = self.loc[mask, ['atom2_index', 'atom1_index']].values
        self.sort_values(by=['atom1_index', 'atom2_index'], inplace=True)
        self.reset_index(drop=True, inplace=True)

    def _remove_empty_columns(self):
        """Drop optional columns when they only contain NaN placeholders."""

        if (self['order']=='nan').all():
            del self['order']

        if (self['type']=='nan').all():
            del self['type']

class Topology():
    """Native topology container including atoms, groups, chains, and bonds."""

    @arg_digest()
    def __init__(self, n_atoms=0, n_groups=0, n_components=0, n_molecules=0, n_entities=0, n_chains=0, n_bonds=0,
                skip_digestion=False):
        """Initialize empty topology tables with the requested sizes."""

        self.reset_atoms(n_atoms=n_atoms)
        self.reset_groups(n_groups=n_groups)
        self.reset_components(n_components=n_components)
        self.reset_molecules(n_molecules=n_molecules)
        self.reset_entities(n_entities=n_entities)
        self.reset_chains(n_chains=n_chains)
        self.reset_bonds(n_bonds=n_bonds)
        self._coerce_id_columns_to_string()

    def get_n_atoms(self):
        return self.atoms.shape[0]

    def get_n_groups(self):
        return self.groups.shape[0]

    def get_n_components(self):
        return self.components.shape[0]

    def get_n_molecules(self):
        return self.molecules.shape[0]

    def get_n_entities(self):
        return self.entities.shape[0]

    def get_n_chains(self):
        return self.chains.shape[0]

    def get_n_bonds(self):
        return self.bonds.shape[0]

    def reset_atoms(self, n_atoms=0):
        """Reset atoms table to a new size."""

        self.atoms = Atoms_DataFrame(n_atoms=n_atoms)

    def reset_groups(self, n_groups=0):
        """Reset groups table to a new size."""

        self.groups = Groups_DataFrame(n_groups=n_groups)

    def reset_components(self, n_components=0):
        """Reset components table to a new size."""

        self.components = Components_DataFrame(n_components=n_components)

    def reset_molecules(self, n_molecules=0):
        """Reset molecules table to a new size."""

        self.molecules = Molecules_DataFrame(n_molecules=n_molecules)

    def reset_entities(self, n_entities=0):
        """Reset entities table to a new size."""

        self.entities = Entities_DataFrame(n_entities=n_entities)

    def reset_chains(self, n_chains=0):
        """Reset chains table to a new size."""

        self.chains = Chains_DataFrame(n_chains=n_chains)

    def reset_bonds(self, n_bonds=0):
        """Reset bonds table to a new size."""

        self.bonds = Bonds_DataFrame(n_bonds=n_bonds)

    def _coerce_id_columns_to_string(self):
        """Ensure all *_id columns use pandas string dtype."""

        self.atoms['atom_id'] = self.atoms['atom_id'].astype('string')
        self.groups['group_id'] = self.groups['group_id'].astype('string')
        self.components['component_id'] = self.components['component_id'].astype('string')
        self.molecules['molecule_id'] = self.molecules['molecule_id'].astype('string')
        self.entities['entity_id'] = self.entities['entity_id'].astype('string')
        self.chains['chain_id'] = self.chains['chain_id'].astype('string')

    @property
    def n_atoms(self):
        return self.atoms.shape[0]

    @property
    def n_groups(self):
        return self.groups.shape[0]

    @property
    def n_components(self):
        return self.components.shape[0]

    @property
    def n_molecules(self):
        return self.molecules.shape[0]

    @property
    def n_entities(self):
        return self.entities.shape[0]

    @property
    def n_chains(self):
        return self.chains.shape[0]

    @property
    def n_bonds(self):
        return self.bonds.shape[0]

    @signal(tags=['native'])
    @arg_digest()
    def extract(self, atom_indices='all', copy_if_all=False, skip_digestion=False):
        """Return a subset topology with the selected atoms and associated hierarchy."""

        if is_all(atom_indices):

            if copy_if_all:
                return self.copy()
            else:
                return self

        elif len(atom_indices) == self.atoms.shape[0]:

            if copy_if_all:
                return self.copy()
            else:
                return self

        else:

            atom_indices = np.sort(atom_indices)

            tmp_item = Topology(skip_digestion=True)
            tmp_item.atoms = self.atoms.iloc[atom_indices].copy()
            tmp_item.atoms.reset_index(drop=True, inplace=True)

            old_group_indices = tmp_item.atoms['group_index'].unique()
            tmp_item.groups = self.groups.iloc[old_group_indices].copy()
            tmp_item.groups.reset_index(drop=True, inplace=True)

            old_molecule_indices = tmp_item.groups['molecule_index'].dropna().unique().tolist()
            tmp_item.molecules = self.molecules.iloc[old_molecule_indices].copy()
            tmp_item.molecules.reset_index(drop=True, inplace=True)

            old_entity_indices = tmp_item.molecules['entity_index'].dropna().unique().tolist()
            tmp_item.entities = self.entities.iloc[old_entity_indices].copy()
            tmp_item.entities.reset_index(drop=True, inplace=True)

            old_component_indices = tmp_item.atoms['component_index'].dropna().unique().tolist()
            tmp_item.components = self.components.iloc[old_component_indices].copy()
            tmp_item.components.reset_index(drop=True, inplace=True)

            old_chain_indices = tmp_item.atoms['chain_index'].dropna().unique().tolist()
            tmp_item.chains = self.chains.iloc[old_chain_indices].copy()
            tmp_item.chains.reset_index(drop=True, inplace=True)

            tmp_item.atoms['group_index'] = tmp_item.atoms['group_index'].map({old: new for new, old in enumerate(old_group_indices)}).astype('Int64')
            tmp_item.groups['molecule_index'] = tmp_item.groups['molecule_index'].map({old: new for new, old in enumerate(old_molecule_indices)}).astype('Int64')
            tmp_item.molecules['entity_index'] = tmp_item.molecules['entity_index'].map({old: new for new, old in enumerate(old_entity_indices)}).astype('Int64')
            tmp_item.atoms['component_index'] = tmp_item.atoms['component_index'].map({old: new for new, old in enumerate(old_component_indices)}).astype('Int64')
            tmp_item.atoms['chain_index'] = tmp_item.atoms['chain_index'].map({old: new for new, old in enumerate(old_chain_indices)}).astype('Int64')

            del old_group_indices, old_molecule_indices, old_entity_indices, old_component_indices, old_chain_indices

            if self.bonds.shape[0]:

                mask_atom1 = np.isin(self.bonds['atom1_index'], atom_indices)
                mask_atom2 = np.isin(self.bonds['atom2_index'], atom_indices)
                mask = mask_atom1*mask_atom2
                tmp_item.bonds = self.bonds[mask].copy()
                tmp_item.bonds.reset_index(drop=True, inplace=True)
                del(mask_atom1, mask_atom2)

                if tmp_item.bonds.shape[0]:
                    aux_dict = {jj: ii for ii, jj in enumerate(atom_indices)}
                    vaux_dict = np.vectorize(aux_dict.__getitem__)
                    tmp_item.bonds['atom1_index']=vaux_dict(tmp_item.bonds['atom1_index'].to_numpy())
                    tmp_item.bonds['atom2_index']=vaux_dict(tmp_item.bonds['atom2_index'].to_numpy())
                    del aux_dict, vaux_dict

            tmp_item.rebuild_components(redefine_indices=False, redefine_ids=False,
                                        redefine_names=False, redefine_types=True)
            tmp_item.rebuild_chains(redefine_indices=False, redefine_ids=False,
                                    redefine_names=False, redefine_types=True)
            tmp_item.rebuild_molecules(redefine_indices=False, redefine_ids=False,
                                       redefine_names=False, redefine_types=True)
            tmp_item.rebuild_entities(redefine_indices=False, redefine_ids=False,
                                      redefine_names=False, redefine_types=True)
            tmp_item._coerce_id_columns_to_string()
            return tmp_item

    @signal(tags=['native'])
    @arg_digest()
    def remove(self, atom_indices=None, copy_if_None=False, skip_digestion=False):
        """Remove atoms by index and return the resulting topology."""

        if atom_indices is None:

            if copy_if_None:
                return self.copy()
            else:
                return self

        else:

            atom_indices_to_be_kept = np.setdiff1d(np.arange(self.n_atoms), atom_indices)

            tmp_item = self.extract(atom_indices=atom_indices_to_be_kept, skip_digestion=True)

            return tmp_item


    @signal(tags=['native'])
    @arg_digest(form='molsysmt.Topology')
    def add(self, item, atom_indices='all', keep_ids=True, skip_digestion=False):
        """Append another topology, offsetting indices as needed."""

        if is_all(atom_indices):
            tmp_item = item.copy()
        else:
            tmp_item = item.extract(atom_indices=atom_indices, skip_digestion=True)

        n_atoms = self.atoms.shape[0]
        n_groups = self.groups.shape[0]
        n_components = self.components.shape[0]
        n_molecules = self.molecules.shape[0]
        n_chains = self.chains.shape[0]

        tmp_item.atoms['group_index'] += n_groups
        tmp_item.atoms['component_index'] += n_components
        tmp_item.atoms['chain_index'] += n_chains
        tmp_item.groups['molecule_index'] += n_molecules
        tmp_item.bonds['atom1_index'] += n_atoms
        tmp_item.bonds['atom2_index'] += n_atoms

        self.atoms = pd.concat([self.atoms, tmp_item.atoms], ignore_index=True, copy=False)
        self.groups = pd.concat([self.groups, tmp_item.groups], ignore_index=True, copy=False)
        self.molecules = pd.concat([self.molecules, tmp_item.molecules], ignore_index=True, copy=False)
        self.components = pd.concat([self.components, tmp_item.components], ignore_index=True, copy=False)
        self.chains = pd.concat([self.chains, tmp_item.chains], ignore_index=True, copy=False)
        self.bonds = pd.concat([self.bonds, tmp_item.bonds], ignore_index=True, copy=False)

        if not keep_ids:
            self.rebuild_atoms(redefine_ids=True, redefine_types=False)
            self.rebuild_groups(redefine_ids=True, redefine_types=False)

        self.rebuild_components(redefine_indices=False, redefine_ids=(not keep_ids), redefine_names=True,
                                redefine_types=False)
        self.rebuild_chains(redefine_ids=(not keep_ids), redefine_types=True, redefine_names=False)

        self.rebuild_molecules(redefine_indices=False, redefine_ids=(not keep_ids), redefine_types=False,
                               redefine_names=True)
        self.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)
        self._coerce_id_columns_to_string()
        del tmp_item

    @signal(tags=['native'])
    def copy(self):
        """Return a deep copy of the topology tables."""

        tmp_item = Topology()

        tmp_item.atoms = self.atoms.copy()
        tmp_item.groups = self.groups.copy()
        tmp_item.molecules = self.molecules.copy()
        tmp_item.entities = self.entities.copy()
        tmp_item.components = self.components.copy()
        tmp_item.chains = self.chains.copy()
        tmp_item.bonds = self.bonds.copy()

        return tmp_item

    @signal(tags=['native'])
    def add_bonds(self, bonded_atom_pairs, skip_digestion=False):
        """Append new bonds given atom index pairs."""

        bonded_atom_pairs = np.array(bonded_atom_pairs)        
        n_bonds = bonded_atom_pairs.shape[0]

        aux_bonds_dataframe = Bonds_DataFrame(n_bonds=n_bonds)
        aux_bonds_dataframe.atom1_index=bonded_atom_pairs[:,0]
        aux_bonds_dataframe.atom2_index=bonded_atom_pairs[:,1]

        df_concatenado = pd.concat([self.bonds, aux_bonds_dataframe], ignore_index=True)

        self.bonds = Bonds_DataFrame(n_bonds=df_concatenado.shape[0])
        self.bonds['atom1_index'] = df_concatenado['atom1_index']
        self.bonds['atom2_index'] = df_concatenado['atom2_index']
        self.bonds['order'] = df_concatenado['order']
        self.bonds['type'] = df_concatenado['type']

        self.bonds._sort_bonds()
        self.bonds._remove_empty_columns()

        self.rebuild_components()

        del(df_concatenado, aux_bonds_dataframe)

    def remove_bonds(self, bond_indices='all', skip_digestion=False):
        """Drop bonds by index."""

        if is_all(bond_indices):

            self.bonds = Bonds_DataFrame(n_bonds=0)

        else:

            self.bonds.drop(bond_indices, inplace=True)
            self.bonds.reset_index(drop=True, inplace=True)

        self.rebuild_components(redefine_indices=True, redefine_ids=False, redefine_names=False, redefine_types=False)


    def add_missing_bonds(self, selection='all', syntax='MolSysMT', skip_digestion=False):
        """Infer and add missing bonds using geometric templates."""

        from molsysmt.build import get_missing_bonds as _get_missing_bonds

        bonds = _get_missing_bonds(self, selection=selection, syntax=syntax,
                                   engine='MolSysMT', with_templates=True, with_distances=False,
                                   skip_digestion=True)

        self.add_bonds(bonds, skip_digestion=True)

        self.rebuild_components(redefine_indices=True, redefine_ids=False, redefine_names=False, redefine_types=False)

    def rebuild_atoms(self, redefine_ids=True, redefine_types=True):
        """Regenerate atom ids/types from names and current counts."""

        if redefine_ids:

            self.atoms['atom_id']=np.arange(self.atoms.shape[0], dtype=int).astype(str)

        if redefine_types:

            from molsysmt.element.atom import get_atom_type_from_atom_name

            aux_dict = {}

            atom_types = []

            for atom_name in self.atoms['atom_name'].values:
                if atom_name not in aux_dict:
                    atom_type=get_atom_type_from_atom_name(atom_name)
                    aux_dict[atom_name]=atom_type
                    atom_types.append(atom_type)
                else:
                    atom_types.append(aux_dict[atom_name])

            self.atoms.atom_type = np.array(atom_types, dtype=object)

            del aux_dict, atom_types
        self._coerce_id_columns_to_string()

    def rebuild_groups(self, redefine_ids=True, redefine_types=True):
        """Regenerate group ids/types from names and current counts."""

        if redefine_ids:

            self.groups['group_id']=np.arange(self.groups.shape[0], dtype=int).astype(str)

        if redefine_types:

            from molsysmt.element.group import get_group_type_from_group_name
            from molsysmt.element.group.small_molecule import small_molecule_is_amino_acid

            aux_dict = {}

            group_types = []

            for group_name in self.groups['group_name'].values:
                if group_name not in aux_dict:
                    group_type = get_group_type_from_group_name(group_name)
                    if group_type == 'small molecule':
                        if small_molecule_is_amino_acid(self, group_name):
                            group_type = 'amino acid'
                    aux_dict[group_name]= group_type
                    group_types.append(group_type)
                else:
                    group_types.append(aux_dict[group_name])

            self.groups.group_type = np.array(group_types, dtype=object)

            del aux_dict, group_types
        self._coerce_id_columns_to_string()

    @signal(tags=['native'])
    def rebuild_components(self, redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True):
        """Rebuild component mapping and metadata."""

        from molsysmt.element.component import get_component_index, get_component_id, get_component_name, get_component_type

        if redefine_indices:

            component_index_of_atoms = get_component_index(self, element='atom', selection='all', 
                                                           redefine_indices=True, skip_digestion=True)
            self.atoms['component_index'] = np.array(component_index_of_atoms, dtype=int)
            n_components = component_index_of_atoms[-1]+1
            self.components = Components_DataFrame(n_components=n_components)

            del component_index_of_atoms

        if redefine_ids:

            component_id_of_components = get_component_id(self, element='component', selection='all',
                                                          redefine_indices=False, redefine_ids=True,
                                                          skip_digestion=True)
            self.components['component_id'] = np.array(component_id_of_components).astype(str)

            del component_id_of_components

        if redefine_types:

            component_type_of_components = get_component_type(self, element='component', selection='all',
                                                              redefine_indices=False, redefine_types=True,
                                                              skip_digestion=True)
            self.components["component_type"] = np.array(component_type_of_components, dtype=object)

            del component_type_of_components

        if redefine_names:

            component_name = get_component_name(self, element='component', selection='all',
                                                redefine_indices=False,redefine_names=True,
                                                skip_digestion=True)
            self.components["component_name"] = np.array(component_name, dtype=object)
            del component_name
        self._coerce_id_columns_to_string()

    @signal(tags=['native'])
    def rebuild_molecules(self, redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True,
                          molecules_as_components=True):
        """Rebuild molecule mapping and metadata."""

        from molsysmt.element.molecule import get_molecule_index, get_molecule_id, get_molecule_name, get_molecule_type

        if redefine_indices:

            molecule_index_of_groups = get_molecule_index(self, element='group', selection='all',
                                                          redefine_indices=True,
                                                          skip_digestion=True)

            self.groups["molecule_index"] = np.array(molecule_index_of_groups, dtype=int)
            n_molecules = molecule_index_of_groups[-1]+1
            self.reset_molecules(n_molecules = n_molecules)

            del molecule_index_of_groups

        if redefine_ids:

            molecule_id_of_molecules = get_molecule_id(self, element='molecule', selection='all',
                                                       redefine_indices=False, redefine_ids=True,
                                                       skip_digestion=True)
            self.molecules["molecule_id"]=np.array(molecule_id_of_molecules).astype(str)

            del molecule_id_of_molecules

        if redefine_names:

            molecule_name_of_molecules = get_molecule_name(self, element='molecule', selection='all',
                                                           redefine_indices=False, redefine_names=True,
                                                           skip_digestion=True)
            self.molecules["molecule_name"]=np.array(molecule_name_of_molecules, dtype=object)

            del molecule_name_of_molecules

        if redefine_types:

            molecule_type_of_molecules = get_molecule_type(self, element='molecule', selection='all',
                                                           redefine_indices=False, redefine_types=True,
                                                           skip_digestion=True)
            self.molecules["molecule_type"]=np.array(molecule_type_of_molecules, dtype=object)

            del molecule_type_of_molecules
        self._coerce_id_columns_to_string()

    @signal(tags=['native'])
    def rebuild_chains(self, redefine_indices=True, redefine_ids=True, redefine_types=True, redefine_names=True):
        """Rebuild chain mapping and metadata."""

        from molsysmt.element.chain import get_chain_index, get_chain_id, get_chain_name, get_chain_type

        if redefine_indices:

            chain_index_of_atoms = get_chain_index(self, element='atom', selection='all',
                                                   redefine_indices=True, skip_digestion=True)

            self.atoms["chain_index"] = np.array(chain_index_of_atoms, dtype=int)
            n_chains = chain_index_of_atoms[-1]+1
            self.reset_chains(n_chains = n_chains)

            del chain_index_of_atoms

        if redefine_ids:

            chain_ids_from_chain = get_chain_id(self, element='chain', selection='all',
                                                redefine_indices=False, redefine_ids=True,
                                                skip_digestion=True)

            self.chains["chain_id"] = np.array(chain_ids_from_chain).astype(str)

            del chain_ids_from_chain

        if redefine_types:

            chain_types_from_chain = get_chain_type(self, element='chain', selection='all',
                                                    redefine_indices=False, redefine_types=True,
                                                    skip_digestion=True)

            self.chains["chain_type"] = np.array(chain_types_from_chain, dtype=object)

            del chain_types_from_chain

        if redefine_names:

            chain_names_from_chain = get_chain_name(self, element='chain', selection='all',
                                                    redefine_indices=False, redefine_names=True,
                                                    skip_digestion=True)

            self.chains["chain_name"] = np.array(chain_names_from_chain, dtype=object)

            del chain_names_from_chain

        self._coerce_id_columns_to_string()


    @signal(tags=['native'])
    def rebuild_entities(self, redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True):
        """Rebuild entity mapping and metadata."""

        from molsysmt.element.entity import get_entity_index, get_entity_id, get_entity_name, get_entity_type

        if redefine_indices:

            entity_index_of_molecules = get_entity_index(self, element='molecule', selection='all',
                                                         redefine_indices=True, skip_digestion=True)

            self.molecules["entity_index"] = np.array(entity_index_of_molecules, dtype=int)
            n_entities = entity_index_of_molecules[-1]+1
            self.reset_entities(n_entities = n_entities)

            del entity_index_of_molecules

        if redefine_ids:

            entity_ids_from_entity = get_entity_id(self, element='entity', selection='all',
                                                  redefine_indices=False, redefine_ids=True,
                                                  skip_digestion=True)

            self.entities["entity_id"] = np.array(entity_ids_from_entity).astype(str)

            del entity_ids_from_entity

        if redefine_names:

            entity_names_from_entity = get_entity_name(self, element='entity', selection='all',
                                                      redefine_indices=False, redefine_names=True,
                                                      skip_digestion=True)

            self.entities["entity_name"] = np.array(entity_names_from_entity, dtype=object)

            del entity_names_from_entity

        if redefine_types:

            entity_types_from_entity = get_entity_type(self, element='entity', selection='all',
                                                      redefine_indices=False, redefine_types=True,
                                                      skip_digestion=True)

            self.entities["entity_type"] = np.array(entity_types_from_entity, dtype=object)

            del entity_types_from_entity
        self._coerce_id_columns_to_string()

    def _join_molecules(self, indices=None):
        """Merge multiple molecules into a single entry."""
        raise NotImplementedError

    def _fix_null_values(self):
        """Normalize null values across all tables."""

        self.atoms._fix_null_values()
        self.groups._fix_null_values()
        self.components._fix_null_values()
        self.molecules._fix_null_values()
        self.entities._fix_null_values()
        self.chains._fix_null_values()
        self.bonds._fix_null_values()
        self._coerce_id_columns_to_string()

    def _sort_bonds(self):
        """Sort bond table in place."""

        self.bonds._sort_bonds()

    @arg_digest()
    def compare(self, item, rule='equal', output_type='boolean', skip_digestion=False, **kwargs):
        """Compare topology content with another topology."""

        if rule == 'equal':

            output = {}

            if 'n_atoms' in kwargs:

                tmp_output = (self.atoms.shape[0]==item.atoms.shape[0])
                output['n_atoms'] = (kwargs['n_atoms'] == tmp_output)

            if 'atom_index' in kwargs:

                tmp_output = (self.atoms.shape[0]==item.atoms.shape[0])
                output['atom_index'] = (kwargs['atom_index'] == tmp_output)

            if 'atom_id' in kwargs:

                tmp_output = (self.atoms['atom_id'].values==item.atoms['atom_id'].values).all()
                output['atom_id'] = (kwargs['atom_id'] == tmp_output)

            if 'atom_name' in kwargs:

                tmp_output = (self.atoms['atom_name'].values==item.atoms['atom_name'].values).all()
                output['atom_name'] = (kwargs['atom_name'] == tmp_output)

            if 'atom_type' in kwargs:

                tmp_output = (self.atoms['atom_type'].values==item.atoms['atom_type'].values).all()
                output['atom_type'] = (kwargs['atom_type'] == tmp_output)

            if 'n_groups' in kwargs:

                tmp_output = (self.groups.shape[0]==item.groups.shape[0])
                output['n_groups'] = (kwargs['n_groups'] == tmp_output)

            if 'group_index' in kwargs:

                tmp_output = (self.atoms['group_index'].values==item.atoms['group_index'].values).all()
                output['group_index'] = (kwargs['group_index'] == tmp_output)

            if 'group_id' in kwargs:

                tmp_output = (self.groups['group_id'].values==item.groups['group_id'].values).all()
                output['group_id'] = (kwargs['group_id'] == tmp_output)

            if 'group_name' in kwargs:

                tmp_output = (self.groups['group_name'].values==item.groups['group_name'].values).all()
                output['group_name'] = (kwargs['group_name'] == tmp_output)

            if 'group_type' in kwargs:

                tmp_output = (self.groups['group_type'].values==item.groups['group_type'].values).all()
                output['group_type'] = (kwargs['group_type'] == tmp_output)

            if 'component_index' in kwargs:

                tmp_output = (self.atoms['component_index'].values==item.atoms['component_index'].values).all()
                output['component_index'] = (kwargs['component_index'] == tmp_output)

            if 'component_id' in kwargs:

                tmp_output = (self.components['component_id'].values==item.components['component_id'].values).all()
                output['component_id'] = (kwargs['component_id'] == tmp_output)

            if 'component_name' in kwargs:

                tmp_output = (self.components['component_name'].values==item.components['component_name'].values).all()
                output['component_name'] = (kwargs['component_name'] == tmp_output)

            if 'component_type' in kwargs:

                tmp_output = (self.components['component_type'].values==item.components['component_type'].values).all()
                output['component_type'] = (kwargs['component_type'] == tmp_output)

            if 'molecule_index' in kwargs:

                tmp_output = (self.groups['molecule_index'].values==item.groups['molecule_index'].values).all()
                output['molecule_index'] = (kwargs['molecule_index'] == tmp_output)

            if 'molecule_id' in kwargs:

                tmp_output = (self.molecules['molecule_id'].values==item.molecules['molecule_id'].values).all()
                output['molecule_id'] = (kwargs['molecule_id'] == tmp_output)

            if 'molecule_name' in kwargs:

                tmp_output = (self.molecules['molecule_name'].values==item.molecules['molecule_name'].values).all()
                output['molecule_name'] = (kwargs['molecule_name'] == tmp_output)

            if 'molecule_type' in kwargs:

                tmp_output = (self.molecules['molecule_type'].values==item.molecules['molecule_type'].values).all()
                output['molecule_type'] = (kwargs['molecule_type'] == tmp_output)

            if 'entity_index' in kwargs:

                tmp_output = (self.molecules['entity_index'].values==item.molecules['entity_index'].values).all()
                output['entity_index'] = (kwargs['entity_index'] == tmp_output)

            if 'entity_id' in kwargs:

                tmp_output = (self.entities['entity_id'].values==item.entities['entity_id'].values).all()
                output['entity_id'] = (kwargs['entity_id'] == tmp_output)

            if 'entity_name' in kwargs:

                tmp_output = (self.entities['entity_name'].values==item.entities['entity_name'].values).all()
                output['entity_name'] = (kwargs['entity_name'] == tmp_output)

            if 'entity_type' in kwargs:

                tmp_output = (self.entities['entity_type'].values==item.entities['entity_type'].values).all()
                output['entity_type'] = (kwargs['entity_type'] == tmp_output)

            if 'chain_index' in kwargs:

                tmp_output = (self.atoms['chain_index'].values==item.atoms['chain_index'].values).all()
                output['chain_index'] = (kwargs['chain_index'] == tmp_output)

            if 'chain_id' in kwargs:

                tmp_output = (self.chains['chain_id'].values==item.chains['chain_id'].values).all()
                output['chain_id'] = (kwargs['chain_id'] == tmp_output)

            if 'chain_name' in kwargs:

                tmp_output = (self.chains['chain_name'].values==item.chains['chain_name'].values).all()
                output['chain_name'] = (kwargs['chain_name'] == tmp_output)

            if 'chain_type' in kwargs:

                tmp_output = (self.chains['chain_type'].values==item.chains['chain_type'].values).all()
                output['chain_type'] = (kwargs['chain_type'] == tmp_output)

            if 'n_bonds' in kwargs:

                tmp_output = (self.bonds.shape[0]==item.bonds.shape[0]).all()
                output['n_bonds'] = (kwargs['n_bonds'] == tmp_output)

            if 'bonded_atom_pairs' in kwargs:

                tmp_output1 = (self.bonds['atom1_index'] == item.bonds['atom1_index']).all()
                tmp_output2 = (self.bonds['atom2_index'] == item.bonds['atom2_index']).all()
                tmp_output = tmp_output1*tmp_output2
                output['bonded_atom_pairs'] = (kwargs['bonded_atom_pairs'] == tmp_output)

        if output_type=='boolean':
            output = all(list(output.values()))

        return output

    def get_atom_indices(self, **kwargs):
        """Select atom indices matching the provided hierarchical filters."""

        for aux in kwargs:
            if isinstance(kwargs[aux], (str, int)):
                kwargs[aux] = [kwargs[aux]]
            if aux.endswith('_id') and kwargs[aux] is not None:
                kwargs[aux] = [str(ii) for ii in kwargs[aux]]

        atom_columns = []
        group_columns = []
        component_columns = []
        molecule_columns = []
        entity_columns = []
        chain_columns = []

        for aux in self.atoms.keys():
            if aux in kwargs:
                if kwargs[aux] is not None:
                    atom_columns.append(aux)

        for aux in self.groups.keys():
            if aux in kwargs:
                if kwargs[aux] is not None:
                    group_columns.append(aux)

        for aux in self.components.keys():
            if aux in kwargs:
                if kwargs[aux] is not None:
                    component_columns.append(aux)

        for aux in self.molecules.keys():
            if aux in kwargs:
                if kwargs[aux] is not None:
                    molecule_columns.append(aux)

        for aux in self.entities.keys():
            if aux in kwargs:
                if kwargs[aux] is not None:
                    entity_columns.append(aux)

        for aux in self.chains.keys():
            if aux in kwargs:
                if kwargs[aux] is not None:
                    chain_columns.append(aux)

        if len(entity_columns):
            if 'entity_index' not in molecule_columns:
                molecule_columns.append('entity_index')

        if len(molecule_columns):
            if 'molecule_index' not in group_columns:
                group_columns.append('molecule_index')

        if len(group_columns):
            if 'group_index' not in atom_columns:
                atom_columns.append('group_index')

        if len(component_columns):
            if 'component_index' not in atom_columns:
                atom_columns.append('component_index')

        if len(chain_columns):
            if 'chain_index' not in atom_columns:
                atom_columns.append('chain_index')

        aux_df = None

        if len(entity_columns):

            aux_df = pd.merge(self.molecules[molecule_columns], self.entities[entity_columns],
                              left_on='entity_index', right_index=True)

        if len(molecule_columns):

            if aux_df is None:

                aux_df = pd.merge(self.groups[group_columns], self.molecules[molecule_columns],
                                  left_on='molecule_index', right_index=True)

            else:

                aux_df = pd.merge(self.groups[group_columns], aux_df,
                                  left_on='molecule_index', right_index=True)

        if len(group_columns):

            if aux_df is None:

                aux_df = pd.merge(self.atoms[atom_columns], self.groups[group_columns],
                                  left_on='group_index', right_index=True)

            else:

                aux_df = pd.merge(self.atoms[atom_columns], aux_df,
                                  left_on='group_index', right_index=True)

        else:

            aux_df = self.atoms[atom_columns]

        if len(component_columns):

            aux_df = pd.merge(aux_df, self.components[component_columns],
                              left_on='component_index', right_index=True)

        if len(chain_columns):

            aux_df = pd.merge(aux_df, self.chains[chain_columns],
                              left_on='chain_index', right_index=True)

        mask = pd.Series(True, index=aux_df.index)

        for col, valores in kwargs.items():
            mask &= aux_df[col].isin(valores)

        return aux_df.index[mask].tolist()
