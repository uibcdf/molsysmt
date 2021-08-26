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

    def extract(self, atom_indices='all', frame_indices='all'):

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

    def add(self, item, selection='all', frame_indices='all'):

        from molsysmt import convert, get

        tmp_item = convert(item, selection=selection, frame_indices=frame_indices, to_form='molsysmt.Topology')

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

    def _to_pdb_string(self, trajectory_item, frame_indices='all'):

        from molsysmt.native.io.topology.files import to_pdb as molsysmt_Topology_to_pdb

        return molsysmt_Topology_to_pdb(self, trajectory_item=trajectory_item, output_filepath='.pdb',
                                         atom_indices='all', frame_indices=frame_indices)

    def _build_components(self):

        from molsysmt.elements.component.component import _shortpath_to_build_components

        n_atoms = self.atoms_dataframe.shape[0]
        n_bonds = self.bonds_dataframe.shape[0]

        group_index_from_atom = self.atoms_dataframe['group_index'].to_numpy()
        group_type_from_atom = self.atoms_dataframe['group_type'].to_numpy()
        atom_index_from_bond = self.bonds_dataframe[['atom1_index','atom2_index']].to_numpy(dtype=int, copy=True)

        index_array, id_array, name_array, type_array = _shortpath_to_build_components(n_atoms,
                n_bonds, atom_index_from_bond, group_index_from_atom, group_type_from_atom)

        self.atoms_dataframe["component_index"] = index_array
        self.atoms_dataframe["component_id"] = id_array
        self.atoms_dataframe["component_name"] = name_array
        self.atoms_dataframe["component_type"] = type_array

        del(group_index_from_atom, group_type_from_atom, atom_index_from_bond, index_array,
                id_array, name_array, type_array)

    def _build_molecules(self):

        from molsysmt.elements.molecule.molecule import _shortpath_to_build_molecules

        component_index_from_atom = self.atoms_dataframe['component_index'].to_numpy()
        component_type_from_atom = self.atoms_dataframe['component_type'].to_numpy()

        index_array, id_array, name_array, type_array = _shortpath_to_build_molecules(component_index_from_atom, component_type_from_atom)

        self.atoms_dataframe["molecule_index"] = index_array
        self.atoms_dataframe["molecule_id"] = id_array
        self.atoms_dataframe["molecule_name"] = name_array
        self.atoms_dataframe["molecule_type"] = type_array

        del(component_index_from_atom, component_type_from_atom, index_array, id_array, name_array,
                type_array)

    def _build_entities(self):

        from molsysmt.elements.entity.entity import _shortpath_to_build_entities

        molecule_index_from_atom = self.atoms_dataframe['molecule_index'].to_numpy()
        molecule_type_from_atom = self.atoms_dataframe['molecule_type'].to_numpy()
        group_name_from_atom = self.atoms_dataframe['group_name'].to_numpy()

        index_array, id_array, name_array, type_array = _shortpath_to_build_entities(molecule_index_from_atom, molecule_type_from_atom, group_name_from_atom)

        self.atoms_dataframe["entity_index"] = index_array
        self.atoms_dataframe["entity_id"] = id_array
        self.atoms_dataframe["entity_name"] = name_array
        self.atoms_dataframe["entity_type"] = type_array

        del(molecule_index_from_atom, molecule_type_from_atom, group_name_from_atom, index_array, id_array, name_array,
                type_array)

    def _build_components_molecules_and_entities(self):

        from molsysmt.elements.component.component import _shortpath_to_build_components
        from molsysmt.elements.molecule.molecule import _shortpath_to_build_molecules
        from molsysmt.elements.entity.entity import _shortpath_to_build_entities

        n_atoms = self.atoms_dataframe.shape[0]
        n_bonds = self.bonds_dataframe.shape[0]
        group_index_from_atom = self.atoms_dataframe['group_index'].to_numpy()
        group_type_from_atom = self.atoms_dataframe['group_type'].to_numpy()
        group_name_from_atom = self.atoms_dataframe['group_name'].to_numpy()
        atom_index_from_bond = self.bonds_dataframe[['atom1_index','atom2_index']].to_numpy(dtype=int, copy=True)

        component_index_from_atom, component_id_from_atom, component_name_from_atom,\
        component_type_from_atom = _shortpath_to_build_components(n_atoms, n_bonds, atom_index_from_bond,
                group_index_from_atom, group_type_from_atom)

        self.atoms_dataframe["component_index"] = component_index_from_atom
        self.atoms_dataframe["component_id"] = component_id_from_atom
        self.atoms_dataframe["component_name"] = component_name_from_atom
        self.atoms_dataframe["component_type"] = component_type_from_atom

        del(n_atoms, n_bonds, group_index_from_atom, group_type_from_atom, atom_index_from_bond,
                component_id_from_atom, component_name_from_atom)

        molecule_index_from_atom, molecule_id_from_atom, molecule_name_from_atom,\
        molecule_type_from_atom = _shortpath_to_build_molecules(component_index_from_atom, component_type_from_atom)


        self.atoms_dataframe["molecule_index"] = molecule_index_from_atom
        self.atoms_dataframe["molecule_id"] = molecule_id_from_atom
        self.atoms_dataframe["molecule_name"] = molecule_name_from_atom
        self.atoms_dataframe["molecule_type"] = molecule_type_from_atom

        del(component_index_from_atom, component_type_from_atom, molecule_id_from_atom, molecule_name_from_atom)

        entity_index_from_atom, entity_id_from_atom, entity_name_from_atom,\
        entity_type_from_atom = _shortpath_to_build_entities(molecule_index_from_atom, molecule_type_from_atom, group_name_from_atom)

        self.atoms_dataframe["entity_index"] = entity_index_from_atom
        self.atoms_dataframe["entity_id"] = entity_id_from_atom
        self.atoms_dataframe["entity_name"] = entity_name_from_atom
        self.atoms_dataframe["entity_type"] = entity_type_from_atom

        del(group_name_from_atom, molecule_index_from_atom, molecule_type_from_atom,
                entity_index_from_atom, entity_id_from_atom, entity_name_from_atom,
                entity_type_from_atom)

    def _join_molecules(self, indices=None):

        pass


    def _nan_to_None(self):

        self.atoms_dataframe._nan_to_None()
        self.bonds_dataframe._nan_to_None()

