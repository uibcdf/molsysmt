import pandas as pd
import numpy as np
from molsysmt._private.variables import is_all
from molsysmt._private.digestion import digest

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

        columns = ['molecule_id', 'molecule_name', 'molecule_type', 'entity_index']

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

        columns = ['atom1_index', 'atom2_index']
        columns += ['order', 'type'] # extra columns -not necessary-

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

    @digest()
    def __init__(self, n_atoms=0, n_groups=0, n_components=0, n_molecules=0, n_entities=0, n_chains=0, n_bonds=0,
                skip_digestion=False):

        self.reset_atoms(n_atoms=n_atoms)
        self.reset_groups(n_groups=n_groups)
        self.reset_components(n_components=n_components)
        self.reset_molecules(n_molecules=n_molecules)
        self.reset_entities(n_entities=n_entities)
        self.reset_chains(n_chains=n_chains)
        self.reset_bonds(n_bonds=n_bonds)

    def reset_atoms(self, n_atoms=0):

        self.atoms = Atoms_DataFrame(n_atoms=n_atoms)

    def reset_groups(self, n_groups=0):

        self.groups = Groups_DataFrame(n_groups=n_groups)

    def reset_components(self, n_components=0):

        self.components = Components_DataFrame(n_components=n_components)

    def reset_molecules(self, n_molecules=0):

        self.molecules = Molecules_DataFrame(n_molecules=n_molecules)

    def reset_entities(self, n_entities=0):

        self.entities = Entities_DataFrame(n_entities=n_entities)

    def reset_chains(self, n_chains=0):

        self.chains = Chains_DataFrame(n_chains=n_chains)

    def reset_bonds(self, n_bonds=0):

        self.bonds = Bonds_DataFrame(n_bonds=n_bonds)

    @digest()
    def extract(self, atom_indices='all', copy_if_all=False, skip_digestion=False):

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

            from molsysmt.lib.series import occurrence_order_sorted_serie as occurrence_order

            atom_indices = np.sort(atom_indices)

            tmp_item = Topology(skip_digestion=True)
            tmp_item.atoms = self.atoms.iloc[atom_indices].copy()
            tmp_item.atoms.reset_index(drop=True, inplace=True)

            old_group_indices = tmp_item.atoms['group_index'].unique()
            tmp_item.groups = self.groups.iloc[old_group_indices].copy()
            tmp_item.groups.reset_index(drop=True, inplace=True)
            del old_group_indices

            old_component_indices = tmp_item.groups['component_index'].unique()
            tmp_item.components = self.components.iloc[old_component_indices].copy()
            tmp_item.components.reset_index(drop=True, inplace=True)
            del old_component_indices

            old_molecule_indices = tmp_item.components['molecule_index'].unique()
            tmp_item.molecules = self.molecules.iloc[old_molecule_indices].copy()
            tmp_item.molecules.reset_index(drop=True, inplace=True)
            del old_molecule_indices

            old_entity_indices = tmp_item.molecules['entity_index'].unique()
            tmp_item.entities = self.molecules.iloc[old_entity_indices].copy()
            tmp_item.entities.reset_index(drop=True, inplace=True)
            del old_entity_indices

            old_chain_indices = tmp_item.atoms['chain_index'].unique()
            tmp_item.chains = self.chains.iloc[old_chain_indices].copy()
            tmp_item.chains.reset_index(drop=True, inplace=True)
            del old_chain_indices

            tmp_item.atoms['group_index'] = occurrence_order(tmp_item.atoms['group_index'].to_numpy())
            tmp_item.groups['component_index'] = occurrence_order(tmp_item.groups['component_index'].to_numpy())
            tmp_item.components['molecule_index'] = occurrence_order(tmp_item.components['molecule_index'].to_numpy())
            tmp_item.molecules['entity_index'] = occurrence_order(tmp_item.molecules['entity_index'].to_numpy())
            tmp_item.atoms['chain_index'] = occurrence_order(tmp_item.atoms['chain_index'].to_numpy())

            if self.bonds.shape[0]:

                mask_atom1 = np.in1d(self.bonds['atom1_index'], atom_indices)
                mask_atom2 = np.in1d(self.bonds['atom2_index'], atom_indices)
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

            return tmp_item

    @digest(form='molsysmt.Topology')
    def add(self, item, atom_indices='all', skip_digestion=False):

        if is_all(atom_indices):
            tmp_item = item
        else:
            tmp_item = item.extract(atom_indices=atom_indices, skip_digestion=True)

        n_atoms = tmp_item.atoms.shape[0]
        n_groups = tmp_item.groups.shape[0]
        n_components = tmp_item.components.shape[0]
        n_chains = tmp_item.chains.shape[0]
        n_molecules = tmp_item.molecules.shape[0]

        tmp_item.atoms['group_index'] += n_groups
        tmp_item.atoms['chain_index'] += n_chains
        tmp_item.groups['component_index'] += n_components
        tmp_item.components['molecule_index'] += n_molecules
        tmp_item.bonds['atom1_index'] += n_atoms
        tmp_item.bonds['atom2_index'] += n_atoms

        self.atoms = pd.concat([self.atoms, tmp_item.atoms], ignore_index=True, copy=False)
        self.groups = pd.concat([self.groups, tmp_item.groups], ignore_index=True, copy=False)
        self.components = pd.concat([self.components, tmp_item.components], ignore_index=True, copy=False)
        self.molecules = pd.concat([self.molecules, tmp_item.molecules], ignore_index=True, copy=False)
        self.bonds = pd.concat([self.bonds, tmp_item.bonds], ignore_index=True, copy=False)
        self.rebuild_components(redefine_indices=False, redefine_ids=False, redefine_names=True, redefine_types=False)
        self.rebuild_molecules()
        self.rebuild_entities()

        del tmp_item

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

    def rebuild_groups(self, redefine_ids=True, redefine_types=True):

        from molsysmt.element.group.get_group_type import _get_group_type_from_group_name

        group_types_from_groups = [_get_group_type_from_group_name(ii) for ii in self.groups['group_name'].values]
        self.groups["group_type"] = np.array(group_types_from_groups, dtype=object)

        del group_types_from_groups

    def rebuild_components(self, redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True):

        if redefine_indices:

            import networkx as nx
            from molsysmt.form.molsysmt_Topology import to_networkx_Graph
            from molsysmt.lib.series import occurrence_order

            g = to_networkx_Graph(self, skip_digestion=True)
            components = list(nx.connected_components(g))
            aux_n_components = len(components)
            component_index_of_atoms = np.empty((g.number_of_nodes()), dtype=int)
            for component_index, component in enumerate(components):
                component_index_of_atoms[list(component)] = component_index
            component_index_of_atoms = occurrence_order(component_index_of_atoms)

            group_index, first_atom_indices = np.unique(self.atoms['group_index'], return_index=True)
            component_index_of_groups = component_index_of_atoms[first_atom_indices]

            self.groups["component_index"] = np.array(component_index_of_groups, dtype=int)
            self.components = Components_DataFrame(n_components=aux_n_components)

            del g, components, component_index_of_atoms, group_index, first_atom_indices, component_index_of_groups

        if redefine_ids:

            self.components["component_id"] = np.arange(self.components.shape[0], dtype=int)

        #if redefine_names:
        #    component_name = get_component_name(self, element='component', redefine_names=True, skip_digestion=True)
        #    self.components["component_name"] = np.array(component_name, dtype=object)
        #    del component_name

        #if redefine_types:
        #    component_type = get_component_type(self, element='component', redefine_types=True, skip_digestion=True)
        #    self.components["component_type"] = np.array(component_type, dtype=object)
        #    del component_type


    def rebuild_molecules(self, redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True):

        if redefine_indices:

            component_indices_from_component = np.arange(self.components.shape[0])
            molecule_indices_from_component = component_indices_from_component

            self.components["molecule_index"] = molecule_indices_from_component
            self.reset_molecules(n_molecules = len(molecule_indices_from_component))

        if redefine_ids:

            self.molecules["molecule_id"]=np.arange(self.molecules.shape[0], dtype=int)

        if redefine_names:

            self.molecules['molecule_name']=self.components.groupby('molecule_index')['component_name'].first().to_numpy()

        if redefine_types:

            from molsysmt.config import min_length_protein

            aux_groups = self.components.groupby('molecule_index')['component_type']
            aux_dict = aux_groups.apply(list).to_dict()
            aux_dict_2 = self.components.groupby('molecule_index').indices

            for molecule_index, component_types in aux_dict.items():
                if len(component_types)==1:
                    self.molecules.iat[molecule_index,2]=component_types[0]
                else:
                    if 'protein' in component_types:
                        self.molecules.iat[molecule_index,2]='protein'
                    elif 'peptide' in component_types:
                        aux_components = aux_dict_2[molecule_index] 
                        group_types = df.loc[self.groups['component_index'].isin(aux_components), 'group_type']
                        n_amino_acids = np.sum(group_types=='amino acid')
                        if n_amino_acids >= min_length_protein:
                            self.molecules.iat[molecule_index,2]='protein'
                        else:
                            self.molecules.iat[molecule_index,2]='peptide'
                    else:
                        raise NotImplementedError

            del aux_groups, aux_dict, aux_dict_2

    def rebuild_chain_types(self):

        from molsysmt.element.chain import get_chain_type

        chain_type = get_chain_type(self, element='chain', redefine_types=True, redefine_molecules=False,
                                   redefine_molecule_types=False)
        self.chains["chain_type"] = np.array(chain_type, dtype=object)
        del chain_type

    def rebuild_entities(self, redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True):

        if redefine_indices:

            molecule_names = self.molecules['molecule_name'].to_numpy()
            molecule_types = self.molecules['molecule_type'].to_numpy()

            count = 0
            entity_indices = []
            aux_dict = {}

            for molecule_name, molecule_type in zip(molecule_names, molecule_types):
                if molecule_type == 'water':
                    if 'water' not in aux_dict:
                        aux_dict['water'] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict['water']
                elif molecule_type == 'ion':
                    if molecule_name not in aux_dict:
                        aux_dict[molecule_name] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict[molecule_name]
                elif molecule_type == 'lipid':
                    if molecule_name not in aux_dict:
                        aux_dict[molecule_name] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict[molecule_name]
                elif molecule_type == 'small molecule':
                    if molecule_name not in aux_dict:
                        aux_dict[molecule_name] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict[molecule_name]
                elif molecule_type == 'peptide':
                    if molecule_name not in aux_dict:
                        aux_dict[molecule_name] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict[molecule_name]
                elif molecule_type == 'protein':
                    if molecule_name not in aux_dict:
                        aux_dict[molecule_name] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict[molecule_name]
                else:
                    if 'unknown' in aux_dict:
                        aux_dict['unknown'] = count
                        entity_index = count
                        count += 1
                    else:
                        entity_index = aux_dict['unknown']

                entity_indices.append(entity_index)

            del molecule_names, molecule_types

            n_entities = count

            self.molecules['entity_index']=np.array(entity_indices, dtype=int)

            self.reset_entities(n_entities=n_entities)

        if redefine_ids:

            self.entities['entity_id']=np.arange(self.entities.shape[0], dtype=int)

        if redefine_names:

            self.entities['entity_name']=self.molecules.groupby('entity_index')['molecule_name'].first().to_numpy()

        if redefine_types:

            self.entities['entity_type']=self.molecules.groupby('entity_index')['molecule_type'].first().to_numpy()


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
