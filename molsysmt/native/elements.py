import pandas as pd
import numpy as np
from molsysmt._private.variables import is_all
from molsysmt.lib import bonds as libbonds


class Atoms(pd.DataFrame):

    def __init__(self, n_atoms=0):

        attributes = ['atom_name', 'atom_id', 'atom_type',
                'group_index', 'component_index', 'chain_index',
                'molecule_index', 'entity_index', 'formal_charge',
                'partial_charge', 'b_factors']

        super().__init__(columns=attributes)

        if n_atoms:
            for column in self.columns:
                for column in self.columns:
                    self[column] = np.full(n_atoms, None, dtype=object)

    def _nan_to_None(self):

        for column in self:
            self[column].where(self[column].notnull(), None, inplace=True)

    def copy(self):

        return self.extract()

    def extract(self, indices='all', mask=None):

        tmp_item = Atoms()

        if is_all(indices):

            if mask is None:

                for column in self.columns:
                    tmp_item[column]=self[column].to_numpy()

            else:

                for column in self.columns:
                    tmp_item[column]=self[column][mask].to_numpy()

        else:

            for column in self.columns:
                tmp_item[column]=self[column].iloc[indices].to_numpy()

        return tmp_item


class Groups(pd.DataFrame):

    def __init__(self, n_groups=0):

        attributes = ['group_name', 'group_id', 'group_type']

        super().__init__(columns=attributes)

        if n_groups:
            for column in self.columns:
                for column in self.columns:
                    self[column] = np.full(n_groups, None, dtype=object)

    def _nan_to_None(self):

        for column in self:
            self[column].where(self[column].notnull(), None, inplace=True)

    def copy(self):

        return self.extract()

    def extract(self, indices='all', mask=None):

        tmp_item = Groups()

        if is_all(indices):

            if mask is None:

                for column in self.columns:
                    tmp_item[column]=self[column].to_numpy()

            else:

                for column in self.columns:
                    tmp_item[column]=self[column][mask].to_numpy()

        else:

            for column in self.columns:
                tmp_item[column]=self[column].iloc[indices].to_numpy()

        return tmp_item


class Components(pd.DataFrame):

    def __init__(self, n_components=0):

        attributes = ['component_name', 'component_id', 'component_type']

        super().__init__(columns=attributes)

        if n_components:
            for column in self.columns:
                for column in self.columns:
                    self[column] = np.full(n_components, None, dtype=object)

    def _nan_to_None(self):

        for column in self:
            self[column].where(self[column].notnull(), None, inplace=True)

    def copy(self):

        return self.extract()

    def extract(self, indices='all', mask=None):

        tmp_item = Components()

        if is_all(indices):

            if mask is None:

                for column in self.columns:
                    tmp_item[column]=self[column].to_numpy()

            else:

                for column in self.columns:
                    tmp_item[column]=self[column][mask].to_numpy()

        else:

            for column in self.columns:
                tmp_item[column]=self[column].iloc[indices].to_numpy()

        return tmp_item


class Chains(pd.DataFrame):

    def __init__(self, n_chains=0):

        attributes = ['chain_name', 'chain_id', 'chain_type']

        super().__init__(columns=attributes)

        if n_chains:
            for column in self.columns:
                for column in self.columns:
                    self[column] = np.full(n_chains, None, dtype=object)

    def _nan_to_None(self):

        for column in self:
            self[column].where(self[column].notnull(), None, inplace=True)

    def copy(self):

        return self.extract()

    def extract(self, indices='all', mask=None):

        tmp_item = Chains()

        if is_all(indices):

            if mask is None:

                for column in self.columns:
                    tmp_item[column]=self[column].to_numpy()

            else:

                for column in self.columns:
                    tmp_item[column]=self[column][mask].to_numpy()

        else:

            for column in self.columns:
                tmp_item[column]=self[column].iloc[indices].to_numpy()

        return tmp_item


class Molecules(pd.DataFrame):

    def __init__(self, n_molecules=0):

        attributes = ['molecule_name', 'molecule_id', 'molecule_type']

        super().__init__(columns=attributes)

        if n_molecules:
            for column in self.columns:
                for column in self.columns:
                    self[column] = np.full(n_molecules, None, dtype=object)

    def _nan_to_None(self):

        for column in self:
            self[column].where(self[column].notnull(), None, inplace=True)

    def copy(self):

        return self.extract()

    def extract(self, indices='all', mask=None):

        tmp_item = Molecules()

        if is_all(indices):

            if mask is None:

                for column in self.columns:
                    tmp_item[column]=self[column].to_numpy()

            else:

                for column in self.columns:
                    tmp_item[column]=self[column][mask].to_numpy()

        else:

            for column in self.columns:
                tmp_item[column]=self[column].iloc[indices].to_numpy()

        return tmp_item


class Entities(pd.DataFrame):

    def __init__(self, n_entities=0):

        attributes = ['entity_name', 'entity_id', 'entity_type']

        super().__init__(columns=attributes)

        if n_entities:
            for column in self.columns:
                for column in self.columns:
                    self[column] = np.full(n_entities, None, dtype=object)

    def _nan_to_None(self):

        for column in self:
            self[column].where(self[column].notnull(), None, inplace=True)

    def copy(self):

        return self.extract()

    def extract(self, indices='all', mask=None):

        tmp_item = Entities()

        if is_all(indices):

            if mask is None:

                for column in self.columns:
                    tmp_item[column]=self[column].to_numpy()

            else:

                for column in self.columns:
                    tmp_item[column]=self[column][mask].to_numpy()

        else:

            for column in self.columns:
                tmp_item[column]=self[column].iloc[indices].to_numpy()

        return tmp_item


class Bonds(pd.DataFrame):

    def __init__(self, n_bonds=0):

        attributes = ['atom1_index', 'atom2_index', 'order']

        super().__init__(columns=attributes)

        if n_bonds:
            for column in self.columns:
                for column in self.columns:
                    self[column] = np.full(n_bonds, None, dtype=object)

    def _nan_to_None(self):

        for column in self:
            self[column].where(self[column].notnull(), None, inplace=True)

    def copy(self):

        return self.extract()

    def extract(self, indices='all', mask=None):

        tmp_item = Bonds()

        if is_all(indices):

            if mask is None:

                for column in self.columns:
                    tmp_item[column]=self[column].to_numpy()

            else:

                for column in self.columns:
                    tmp_item[column]=self[column][mask].to_numpy()

        else:

            for column in self.columns:
                tmp_item[column]=self[column].iloc[indices].to_numpy()

        return tmp_item


class Elements():

    def __init__(self, n_atoms=0, n_groups=0, n_components=0, n_chains=0, n_molecules=0,
                 n_entities=0, n_bonds=0):

        self.atoms=Atoms(n_atoms=n_atoms)
        self.groups=Groups(n_groups=n_groups)
        self.components=Components(n_components=n_components)
        self.chains=Chains(n_chains=n_chains)
        self.molecules=Molecules(n_molecules=n_molecules)
        self.entities=Entities(n_entities=n_entities)
        self.bonds=Bonds(n_bonds=n_bonds)

    def copy(self):

        tmp_item = Elements()

        tmp_atoms = self.atoms.copy()
        tmp_groups = self.groups.copy()
        tmp_components = self.components.copy()
        tmp_chains = self.chains.copy()
        tmp_molecules = self.molecules.copy()
        tmp_entities = self.entities.copy()
        tmp_bonds = self.bonds.copy()

    def extract(self, atom_indices='all', structure_indices='all'):

        if is_all(atom_indices):

            tmp_item = self.copy()

        else:

            tmp_item = Elements()

            # atoms

            tmp_item.atoms = self.atoms.extract(indices=atom_indices)

            # bonds

            bond_atom1 = self.bonds['atom1_index'].to_numpy()
            bond_atom2 = self.bonds['atom2_index'].to_numpy()
            mask_atom1 = np.in1d(bond_atom1, atom_indices)
            mask_atom2 = np.in1d(bond_atom2, atom_indices)
            mask = mask_atom1*mask_atom2
            tmp_item.bonds = self.bonds.extract(mask=mask)
            del(bond_atom1, bond_atom2, mask_atom1, mask_atom2)

            old_to_new_indices = dict(zip(range(atom_indices.shape[0], atom_indices)))

            tmp_item.atoms['atom1_index'].map(old_to_new_indices)
            tmp_item.atoms['atom2_index'].map(old_to_new_indices)

            # groups

            old_indices = np.sort(tmp_item.atoms['group_index'].unique())
            old_to_new_indices = dict(enumerate(old_indices))

            tmp_item.groups = self.groups.extract(indices=old_indices)
            tmp_item.atoms['group_index'].map(old_to_new_indices)

            # components

            tmp_item._init_components()

            # chains

            old_indices = np.sort(tmp_item.atoms['chain_index'].unique())
            old_to_new_indices = dict(enumerate(old_indices))

            tmp_item.chains = self.chains.extract(indices=old_indices)
            tmp_item.atoms['chain_index'].map(old_to_new_indices)

            # molecules

            old_indices = np.sort(tmp_item.atoms['molecule_index'].unique())
            old_to_new_indices = dict(enumerate(old_indices))

            tmp_item.molecules = self.molecules.extract(indices=old_indices)
            tmp_item.atoms['molecule_index'].map(old_to_new_indices)

            # entities

            old_indices = np.sort(tmp_item.atoms['entity_index'].unique())
            old_to_new_indices = dict(enumerate(old_indices))

            tmp_item.entities = self.entities.extract(indices=old_indices)
            tmp_item.atoms['entity_index'].map(old_to_new_indices)
            tmp_item._build_components()

        return tmp_item


    def add(self, item, selection='all', structure_indices='all', syntax='MolSysMT'):

        from molsysmt import convert, get

        tmp_item = convert(item, to_form='molsysmt.Elements', selection=selection,
            structure_indices=structure_indices, syntax=syntax)

        tmp_item.atoms['group_index'] += self.groups.shape[0]
        tmp_item.atoms['component_index'] += self.components.shape[0]
        tmp_item.atoms['chain_index'] += self.chains.shape[0]
        tmp_item.atoms['molecule_index'] += self.molecules.shape[0]
        tmp_item.atoms['entity_index'] += self.entities.shape[0]
        tmp_item.bonds['atom1_index'] += self.atoms.shape[0]
        tmp_item.bonds['atom2_index'] += self.atoms.shape[0]

        aux_dataframe = pd.concat([self.atoms, tmp_item.atoms], ignore_index=True)
        self.atoms = Atoms()
        for column in self.atoms.columns:
            self.atoms[column]=aux_dataframe[column].to_numpy()
        del(aux_dataframe)

        aux_dataframe = pd.concat([self.groups, tmp_item.groups], ignore_index=True)
        self.atoms = Groups()
        for column in self.groups.columns:
            self.groups[column]=aux_dataframe[column].to_numpy()
        del(aux_dataframe)

        aux_dataframe = pd.concat([self.components, tmp_item.components], ignore_index=True)
        self.atoms = Components()
        for column in self.components.columns:
            self.components[column]=aux_dataframe[column].to_numpy()
        del(aux_dataframe)

        aux_dataframe = pd.concat([self.chains, tmp_item.chains], ignore_index=True)
        self.atoms = Chains()
        for column in self.chains.columns:
            self.chains[column]=aux_dataframe[column].to_numpy()
        del(aux_dataframe)

        aux_dataframe = pd.concat([self.molecules, tmp_item.molecules], ignore_index=True)
        self.atoms = Molecules()
        for column in self.molecules.columns:
            self.molecules[column]=aux_dataframe[column].to_numpy()
        del(aux_dataframe)

        aux_dataframe = pd.concat([self.entities, tmp_item.entities], ignore_index=True)
        self.atoms = Entities()
        for column in self.entities.columns:
            self.entities[column]=aux_dataframe[column].to_numpy()
        del(aux_dataframe)

        del(tmp_item)

        self._remove_duplicate_entities()


    def build_groups(self):

        n_groups = self.atoms.iloc[-1]['group_index']+1

        self.groups = Groups(n_groups=n_groups)

    def build_components(self):

        #self.atoms['component_index'], n_components = libbonds.component_indices(self.bonds[['atom1_index', 'atom2_index']].to_numpy(),
        #    self.atoms.shape[0], self.bonds.shape[0])

        component_indices = libbonds.component_indices(self.bonds[['atom1_index', 'atom2_index']].to_numpy(),
            self.atoms.shape[0], self.bonds.shape[0])

        n_components = component_indices[-1]+1

        self.atoms['component_index'] = component_indices

        self.components = Components(n_components=n_components)

    def build_chains(self):

        n_chains = self.atoms.iloc[-1]['chain_index']+1

        self.chains = Chains(n_chains=n_chains)

    def build_molecules(self):

        n_molecules = self.atoms.iloc[-1]['molecule_index']+1

        self.molecules = Molecules(n_molecules=n_molecules)

    def build_entities(self):

        n_entities = self.atoms.iloc[-1]['entity_index']+1

        self.entities = Molecules(n_entities=n_entities)

    def _remove_duplicate_entities(self):

        if np.any(self.entities['name'].duplicated()):

            aux_entities = Entities()

            aux_dict = {ii:jj for ii,jj in enumerate(self.entities['name'])}
            self.atoms['entity_index'].map(aux_dict)
            new_entities_list = self.atoms['entity_index'].unique()
            aux_dict = {jj:ii for ii,jj in enumerate(new_entities_list)}
            self.atoms['entity_index'].map(aux_dict)

            for new_entity_index, entity_name in enumerate(new_entities_list):
                old_entity_index = self.entities[self.entities['name']==entity_name].index.tolist()[0]
                aux_entities = pd.concatenate([aux_entites,self.entities.iloc(old_entity_index)], ignore_index=True)

            self.entities = Entities()
            for column in self.entities.columns:
                self.entities[column]=aux_entities[column].to_numpy()

    def _nan_to_None(self):

        self.atoms._nan_to_None()
        self.groups._nan_to_None()
        self.components._nan_to_None()
        self.chains._nan_to_None()
        self.molecules._nan_to_None()
        self.entities._nan_to_None()
        self.bonds._nan_to_None()


### From the former Topology class
#    def _build_molecules(self):
#
#        component_index_from_atom = self.atoms['component_index'].to_numpy()
#        component_type_from_atom = self.atoms['component_type'].to_numpy()
#
#        n_atoms=component_index_from_atom.shape[0]
#        index_array = component_index_from_atom.copy()
#        id_array = np.full(n_atoms, None, dtype=object)
#        name_array = np.full(n_atoms, None, dtype=object)
#        type_array = component_type_from_atom.copy()
#
#        self.atoms["molecule_index"] = index_array
#        self.atoms["molecule_id"] = id_array
#        self.atoms["molecule_name"] = name_array
#        self.atoms["molecule_type"] = type_array
#
#        del(component_index_from_atom, component_type_from_atom, index_array, id_array, name_array,
#                type_array)
#
#    def _build_entities(self):
#
#        molecule_index_from_atom = self.atoms['molecule_index'].to_numpy()
#        molecule_type_from_atom = self.atoms['molecule_type'].to_numpy()
#        group_name_from_atom = self.atoms['group_name'].to_numpy()
#
#        n_atoms = molecule_index_from_atom.shape[0]
#        not_None = np.where(molecule_index_from_atom!=None)
#        molecule_indices = np.unique(molecule_index_from_atom[not_None])
#
#        index_array = np.full(n_atoms, None, dtype=object)
#        id_array = np.full(n_atoms, None, dtype=object)
#        name_array = np.full(n_atoms, None, dtype=object)
#        type_array = np.full(n_atoms, None, dtype=object)
#
#        entities = {}
#        n_entities = 0
#        n_peptides = 0
#        n_proteins = 0
#
#        for molecule_index in molecule_indices:
#
#            mask = (molecule_index_from_atom==molecule_index)
#            molecule_type = molecule_type_from_atom[mask][0]
#
#            if molecule_type == 'water':
#                entity_name = 'water'
#                entity_type = 'water'
#                try:
#                    entity_index = entities[entity_name]
#                except:
#                    entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#
#            elif molecule_type == 'ion':
#                entity_name = group_name_from_atom[mask][0]
#                entity_type = 'ion'
#                try:
#                    entity_index = entities[entity_name]
#                except:
#                    entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#
#            elif molecule_type == 'peptide':
#                entity_name = 'Peptide_'+str(n_peptides)
#                entity_type = 'peptide'
#                n_peptides+=1
#                try:
#                    index = entities[entity_name]
#                except:
#                    entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#
#            elif molecule_type == 'protein':
#                entity_name = 'Protein_'+str(n_proteins)
#                entity_type = 'protein'
#                n_proteins+=1
#                try:
#                    entity_index = entities[entity_name]
#                except:
#                    entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#
#            elif molecule_type == 'lipid':
#                entity_name = group_name_from_atom[mask][0]
#                entity_type = 'lipid'
#                try:
#                    entity_index = entities[entity_name]
#                except:
#                    entity_entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#
#            elif molecule_type == 'small molecule':
#                entity_name = group_name_from_atom[mask][0]
#                entity_type = 'small molecule'
#                try:
#                    entity_index = entities[entity_name]
#                except:
#                    entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#            else:
#                entity_name = 'unknown'
#                entity_type = 'unknown'
#                try:
#                    entity_index = entities[entity_name]
#                except:
#                    entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#
#            index_array[mask]=entity_index
#            name_array[mask]=entity_name
#            type_array[mask]=entity_type
#
#        self.atoms["entity_index"] = index_array
#        self.atoms["entity_id"] = id_array
#        self.atoms["entity_name"] = name_array
#        self.atoms["entity_type"] = type_array
#
#        del(molecule_index_from_atom, molecule_type_from_atom, group_name_from_atom, index_array, id_array, name_array,
#                type_array)
#
#
#    def _build_molecules(self):
#
#        component_index_from_atom = self.atoms['component_index'].to_numpy()
#        component_type_from_atom = self.atoms['component_type'].to_numpy()
#
#        n_atoms=component_index_from_atom.shape[0]
#        index_array = component_index_from_atom.copy()
#        id_array = np.full(n_atoms, None, dtype=object)
#        name_array = np.full(n_atoms, None, dtype=object)
#        type_array = component_type_from_atom.copy()
#
#        self.atoms["molecule_index"] = index_array
#        self.atoms["molecule_id"] = id_array
#        self.atoms["molecule_name"] = name_array
#        self.atoms["molecule_type"] = type_array
#
#        del(component_index_from_atom, component_type_from_atom, index_array, id_array, name_array,
#                type_array)
#
#    def _build_entities(self):
#
#        molecule_index_from_atom = self.atoms['molecule_index'].to_numpy()
#        molecule_type_from_atom = self.atoms['molecule_type'].to_numpy()
#        group_name_from_atom = self.atoms['group_name'].to_numpy()
#
#        n_atoms = molecule_index_from_atom.shape[0]
#        not_None = np.where(molecule_index_from_atom!=None)
#        molecule_indices = np.unique(molecule_index_from_atom[not_None])
#
#        index_array = np.full(n_atoms, None, dtype=object)
#        id_array = np.full(n_atoms, None, dtype=object)
#        name_array = np.full(n_atoms, None, dtype=object)
#        type_array = np.full(n_atoms, None, dtype=object)
#
#        entities = {}
#        n_entities = 0
#        n_peptides = 0
#        n_proteins = 0
#
#        for molecule_index in molecule_indices:
#
#            mask = (molecule_index_from_atom==molecule_index)
#            molecule_type = molecule_type_from_atom[mask][0]
#
#            if molecule_type == 'water':
#                entity_name = 'water'
#                entity_type = 'water'
#                try:
#                    entity_index = entities[entity_name]
#                except:
#                    entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#
#            elif molecule_type == 'ion':
#                entity_name = group_name_from_atom[mask][0]
#                entity_type = 'ion'
#                try:
#                    entity_index = entities[entity_name]
#                except:
#                    entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#
#            elif molecule_type == 'peptide':
#                entity_name = 'Peptide_'+str(n_peptides)
#                entity_type = 'peptide'
#                n_peptides+=1
#                try:
#                    index = entities[entity_name]
#                except:
#                    entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#
#            elif molecule_type == 'protein':
#                entity_name = 'Protein_'+str(n_proteins)
#                entity_type = 'protein'
#                n_proteins+=1
#                try:
#                    entity_index = entities[entity_name]
#                except:
#                    entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#
#            elif molecule_type == 'lipid':
#                entity_name = group_name_from_atom[mask][0]
#                entity_type = 'lipid'
#                try:
#                    entity_index = entities[entity_name]
#                except:
#                    entity_entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#
#            elif molecule_type == 'small molecule':
#                entity_name = group_name_from_atom[mask][0]
#                entity_type = 'small molecule'
#                try:
#                    entity_index = entities[entity_name]
#                except:
#                    entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#            else:
#                entity_name = 'unknown'
#                entity_type = 'unknown'
#                try:
#                    entity_index = entities[entity_name]
#                except:
#                    entities[entity_name]=n_entities
#                    entity_index=n_entities
#                    n_entities+=1
#
#            index_array[mask]=entity_index
#            name_array[mask]=entity_name
#            type_array[mask]=entity_type
#
#        self.atoms["entity_index"] = index_array
#        self.atoms["entity_id"] = id_array
#        self.atoms["entity_name"] = name_array
#        self.atoms["entity_type"] = type_array
#
#        del(molecule_index_from_atom, molecule_type_from_atom, group_name_from_atom, index_array, id_array, name_array,
#                type_array)
#
