from pandas import DataFrame as Pandas_DataFrame
import numpy as np

class Atoms_DataFrame(Pandas_DataFrame):

    def __init__(self):

        topology_columns = ['atom_index', 'atom_name', 'atom_id', 'atom_type',
                            'group_index', 'group_name', 'group_id', 'group_type',
                            'component_index', 'component_name', 'component_id', 'component_type',
                            'chain_index', 'chain_name', 'chain_id', 'chain_type',
                            'molecule_index', 'molecule_name', 'molecule_id', 'molecule_type',
                            'entity_index', 'entity_name', 'entity_id', 'entity_type']


        super().__init__(columns=topology_columns)

    def _nan_to_None(self):

        list_columns_where_nan = ['group_type', 'component_name', 'component_type',
                                 'chain_name', 'chain_type', 'molecule_name', 'molecule_type',
                                 'entity_name', 'entity_type']

        for column in list_columns_where_nan:
            self[column].where(self[column].notnull(), None, inplace=True)


class Bonds_DataFrame(Pandas_DataFrame):

    def __init__(self):

        topology_columns = ['atom1_index', 'atom2_index', 'order', 'type']


        super().__init__(columns=topology_columns)

    def _nan_to_None(self):

        list_columns_where_nan = ['order','type']

        for column in list_columns_where_nan:
            self[column].where(self[column].notnull(), None, inplace=True)

class Topology():

    def __init__(self):

        self.atoms_dataframe=Atoms_DataFrame()
        self.bonds_dataframe=Bonds_DataFrame()

    def extract(self, atom_indices='all', structure_indices='all'):

        if type(atom_indices)==str:

            if atom_indices in ['all', 'All', 'ALL']:
                return self.copy()

        else:

            tmp_item = Topology()
            tmp_item.atoms_dataframe = self.atoms_dataframe.iloc[atom_indices].copy()

            bond_atom1 = self.bonds_dataframe['atom1_index'].to_numpy()
            bond_atom2 = self.bonds_dataframe['atom2_index'].to_numpy()
            mask_atom1 = np.in1d(bond_atom1, atom_indices)
            mask_atom2 = np.in1d(bond_atom2, atom_indices)
            mask = mask_atom1*mask_atom2
            tmp_item.bonds_dataframe = self.bonds_dataframe[mask].copy()
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

            tmp_item._build_components()

            for column in ['group_index', 'molecule_index', 'chain_index', 'entity_index']:
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

        tmp_item = convert(item, selection=selection, structure_indices=structure_indices, to_form='molsysmt.Topology')

        n_atoms, n_groups, n_components, n_chains, n_molecules = get(self, target='system', n_atoms=True, n_groups=True,
                n_components=True, n_chains=True, n_molecules=True)

        tmp_item.atoms_dataframe['atom_index'] += n_atoms
        tmp_item.atoms_dataframe['group_index'] += n_groups
        tmp_item.atoms_dataframe['component_index'] += n_components
        tmp_item.atoms_dataframe['chain_index'] += n_chains
        tmp_item.atoms_dataframe['molecule_index'] += n_molecules
        tmp_item.bonds_dataframe['atom1_index'] += n_atoms
        tmp_item.bonds_dataframe['atom2_index'] += n_atoms

        self.atoms_dataframe = self.atoms_dataframe.append(tmp_item.atoms_dataframe, ignore_index=True)
        self.bonds_dataframe = self.bonds_dataframe.append(tmp_item.bonds_dataframe, ignore_index=True)

        self._build_entities()


    def copy(self):

        tmp_item = Topology()

        tmp_item.atoms_dataframe = Atoms_DataFrame()
        tmp_item.bonds_dataframe = Bonds_DataFrame()

        for column in self.atoms_dataframe.columns:
            tmp_item.atoms_dataframe[column]=self.atoms_dataframe[column].to_numpy()

        for column in self.bonds_dataframe.columns:
            tmp_item.bonds_dataframe[column]=self.bonds_dataframe[column].to_numpy()

        return tmp_item

    def _to_pdb_string(self, trajectory_item, structure_indices='all'):

        from molsysmt.native.io.topology import to_pdb as molsysmt_Topology_to_pdb

        return molsysmt_Topology_to_pdb(self, trajectory_item=trajectory_item, output_filepath='.pdb',
                                         atom_indices='all', structure_indices=structure_indices)

    def _build_components(self):

        from molsysmt.lib import bonds as _libbonds
        from molsysmt.element.component import get_component_type_from_group_names

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

            index_array = _libbonds.component_indices(atom_index_from_bond, n_atoms, n_bonds)
            index_array = np.ascontiguousarray(index_array, dtype=int)

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

        molecule_index_from_atom = self.atoms_dataframe['molecule_index'].to_numpy()
        molecule_type_from_atom = self.atoms_dataframe['molecule_type'].to_numpy()
        group_name_from_atom = self.atoms_dataframe['group_name'].to_numpy()

        n_atoms = molecule_index_from_atom.shape[0]
        not_None = np.where(molecule_index_from_atom!=None)
        molecule_indices = np.unique(molecule_index_from_atom[not_None])

        index_array = np.full(n_atoms, None, dtype=object)
        id_array = np.full(n_atoms, None, dtype=object)
        name_array = np.full(n_atoms, None, dtype=object)
        type_array = np.full(n_atoms, None, dtype=object)

        entities = {}
        n_entities = 0
        n_peptides = 0
        n_proteins = 0

        for molecule_index in molecule_indices:

            mask = (molecule_index_from_atom==molecule_index)
            molecule_type = molecule_type_from_atom[mask][0]

            if molecule_type == 'water':
                entity_name = 'water'
                entity_type = 'water'
                try:
                    entity_index = entities[entity_name]
                except:
                    entities[entity_name]=n_entities
                    entity_index=n_entities
                    n_entities+=1

            elif molecule_type == 'ion':
                entity_name = group_name_from_atom[mask][0]
                entity_type = 'ion'
                try:
                    entity_index = entities[entity_name]
                except:
                    entities[entity_name]=n_entities
                    entity_index=n_entities
                    n_entities+=1

            elif molecule_type == 'peptide':
                entity_name = 'Peptide_'+str(n_peptides)
                entity_type = 'peptide'
                n_peptides+=1
                try:
                    index = entities[entity_name]
                except:
                    entities[entity_name]=n_entities
                    entity_index=n_entities
                    n_entities+=1

            elif molecule_type == 'protein':
                entity_name = 'Protein_'+str(n_proteins)
                entity_type = 'protein'
                n_proteins+=1
                try:
                    entity_index = entities[entity_name]
                except:
                    entities[entity_name]=n_entities
                    entity_index=n_entities
                    n_entities+=1

            elif molecule_type == 'lipid':
                entity_name = group_name_from_atom[mask][0]
                entity_type = 'lipid'
                try:
                    entity_index = entities[entity_name]
                except:
                    entity_entities[entity_name]=n_entities
                    entity_index=n_entities
                    n_entities+=1

            elif molecule_type == 'small molecule':
                entity_name = group_name_from_atom[mask][0]
                entity_type = 'small molecule'
                try:
                    entity_index = entities[entity_name]
                except:
                    entities[entity_name]=n_entities
                    entity_index=n_entities
                    n_entities+=1
            else:
                entity_name = 'unknown'
                entity_type = 'unknown'
                try:
                    entity_index = entities[entity_name]
                except:
                    entities[entity_name]=n_entities
                    entity_index=n_entities
                    n_entities+=1

            index_array[mask]=entity_index
            name_array[mask]=entity_name
            type_array[mask]=entity_type

        self.atoms_dataframe["entity_index"] = index_array
        self.atoms_dataframe["entity_id"] = id_array
        self.atoms_dataframe["entity_name"] = name_array
        self.atoms_dataframe["entity_type"] = type_array

        del(molecule_index_from_atom, molecule_type_from_atom, group_name_from_atom, index_array, id_array, name_array,
                type_array)

    def _join_molecules(self, indices=None):

        pass

    def _nan_to_None(self):

        self.atoms_dataframe._nan_to_None()
        self.bonds_dataframe._nan_to_None()

