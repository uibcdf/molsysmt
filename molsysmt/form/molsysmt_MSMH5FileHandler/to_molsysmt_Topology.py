from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import pandas as pd
import numpy as np

@digest(form='molsysmt.MSMH5FileHandler')
def to_molsysmt_Topology(item, atom_indices='all'):

    from molsysmt.native import Topology

    topology_ds = item.file['topology']

    tmp_item = Topology()

    if is_all(atom_indices):

        n_atoms = topology_ds.attrs['n_atoms']
        n_bonds = topology_ds.attrs['n_bonds']

        # Atoms

        tmp_item.atoms_dataframe['atom_index']=np.arange(n_atoms)
        tmp_item.atoms_dataframe['atom_id']=topology_ds['atoms']['id'][:]
        tmp_item.atoms_dataframe['atom_type']=topology_ds['atoms']['type'].asstr()[:]
        tmp_item.atoms_dataframe['atom_name']=topology_ds['atoms']['name'].asstr()[:]
        tmp_item.atoms_dataframe['group_index']=topology_ds['atoms']['group_index'][:]
        tmp_item.atoms_dataframe['chain_index']=topology_ds['atoms']['chain_index'][:]

        # Groups

        groups_df = pd.DataFrame({
            'group_id':topology_ds['groups']['id'][:],
            'group_name':topology_ds['groups']['name'].asstr()[:],
            'group_type':topology_ds['groups']['type'].asstr()[:],
            'component_index':topology_ds['groups']['component_index'][:],
            })

        aux_df = groups_df.iloc[tmp_item.atoms_dataframe['group_index'].to_numpy()]
        aux_df.reset_index(inplace=True, drop=True)

        tmp_item.atoms_dataframe['group_id']=aux_df['group_id']
        tmp_item.atoms_dataframe['group_name']=aux_df['group_name']
        tmp_item.atoms_dataframe['group_type']=aux_df['group_type']
        tmp_item.atoms_dataframe['component_index']=aux_df['component_index']

        del(groups_df, aux_df)

        # Components

        components_df = pd.DataFrame({
            'component_id':topology_ds['components']['id'][:],
            'component_name':topology_ds['components']['name'].asstr()[:],
            'component_type':topology_ds['components']['type'].asstr()[:],
            'molecule_index':topology_ds['components']['molecule_index'][:],
            })

        aux_df = components_df.iloc[tmp_item.atoms_dataframe['component_index'].to_numpy()]
        aux_df.reset_index(inplace=True, drop=True)

        tmp_item.atoms_dataframe['component_id']=aux_df['component_id']
        tmp_item.atoms_dataframe['component_name']=aux_df['component_name']
        tmp_item.atoms_dataframe['component_type']=aux_df['component_type']
        tmp_item.atoms_dataframe['molecule_index']=aux_df['molecule_index']

        del(components_df, aux_df)

        # Molecules

        molecules_df = pd.DataFrame({
            'molecule_id':topology_ds['molecules']['id'][:],
            'molecule_name':topology_ds['molecules']['name'].asstr()[:],
            'molecule_type':topology_ds['molecules']['type'].asstr()[:],
            'entity_index':topology_ds['molecules']['entity_index'][:],
            })

        aux_df = molecules_df.iloc[tmp_item.atoms_dataframe['molecule_index'].to_numpy()]
        aux_df.reset_index(inplace=True, drop=True)

        tmp_item.atoms_dataframe['molecule_id']=aux_df['molecule_id']
        tmp_item.atoms_dataframe['molecule_name']=aux_df['molecule_name']
        tmp_item.atoms_dataframe['molecule_type']=aux_df['molecule_type']
        tmp_item.atoms_dataframe['entity_index']=aux_df['entity_index']

        del(molecules_df, aux_df)

        # Entities

        entities_df = pd.DataFrame({
            'entity_id':topology_ds['entities']['id'][:],
            'entity_name':topology_ds['entities']['name'].asstr()[:],
            'entity_type':topology_ds['entities']['type'].asstr()[:],
            })

        aux_df = entities_df.iloc[tmp_item.atoms_dataframe['entity_index'].to_numpy()]
        aux_df.reset_index(inplace=True, drop=True)

        tmp_item.atoms_dataframe['entity_id']=aux_df['entity_id']
        tmp_item.atoms_dataframe['entity_name']=aux_df['entity_name']
        tmp_item.atoms_dataframe['entity_type']=aux_df['entity_type']

        del(entities_df, aux_df)

        # Chains

        chains_df = pd.DataFrame({
            'chain_id':topology_ds['chains']['id'][:],
            'chain_name':topology_ds['chains']['name'].asstr()[:],
            'chain_type':topology_ds['chains']['type'].asstr()[:],
            })

        aux_df = chains_df.iloc[tmp_item.atoms_dataframe['chain_index'].to_numpy()]
        aux_df.reset_index(inplace=True, drop=True)

        tmp_item.atoms_dataframe['chain_id']=aux_df['chain_id']
        tmp_item.atoms_dataframe['chain_name']=aux_df['chain_name']
        tmp_item.atoms_dataframe['chain_type']=aux_df['chain_type']

        del(chains_df, aux_df)

        # Bonds

        tmp_item.bonds_dataframe['atom1_index']=topology_ds['bonds']['atom1_index'][:]
        tmp_item.bonds_dataframe['atom2_index']=topology_ds['bonds']['atom2_index'][:]
        tmp_item.bonds_dataframe['type']=topology_ds['bonds']['type'].asstr()[:]
        tmp_item.bonds_dataframe['order']=topology_ds['bonds']['order'].asstr()[:]

    else:

        n_atoms = len(atom_indices)

        # Atoms

        tmp_item.atoms_dataframe['atom_index']=atom_indices
        tmp_item.atoms_dataframe['atom_id']=topology_ds['atoms']['id'][atom_indices].astype('int64')
        tmp_item.atoms_dataframe['atom_type']=topology_ds['atoms']['type'].asstr()[atom_indices]
        tmp_item.atoms_dataframe['atom_name']=topology_ds['atoms']['name'].asstr()[atom_indices]

        group_indices, aux = np.unique(topology_ds['atoms']['group_index'][atom_indices].astype('int64'),
                return_inverse=True)
        tmp_item.atoms_dataframe['group_index']=aux

        chain_indices, aux = np.unique(topology_ds['atoms']['chain_index'][atom_indices].astype('int64'),
                return_inverse=True)
        tmp_item.atoms_dataframe['chain_index']=aux

        # Groups

        component_indices, aux = np.unique(topology_ds['groups']['component_index'][group_indices].astype('int64'),
                return_inverse=True)

        groups_df = pd.DataFrame({
            'group_id':topology_ds['groups']['id'][group_indices],
            'group_name':topology_ds['groups']['name'].asstr()[group_indices],
            'group_type':topology_ds['groups']['type'].asstr()[group_indices],
            'component_index':aux,
            })

        aux_df = groups_df.iloc[tmp_item.atoms_dataframe['group_index'].to_numpy()]
        aux_df.reset_index(inplace=True, drop=True)

        tmp_item.atoms_dataframe['group_id']=aux_df['group_id']
        tmp_item.atoms_dataframe['group_name']=aux_df['group_name']
        tmp_item.atoms_dataframe['group_type']=aux_df['group_type']
        tmp_item.atoms_dataframe['component_index']=aux_df['component_index']

        del(groups_df, aux_df, group_indices)

        # Components

        molecule_indices, aux = np.unique(topology_ds['components']['molecule_index'][component_indices].astype('int64'),
                return_inverse=True)

        components_df = pd.DataFrame({
            'component_id':topology_ds['components']['id'][component_indices],
            'component_name':topology_ds['components']['name'].asstr()[component_indices],
            'component_type':topology_ds['components']['type'].asstr()[component_indices],
            'molecule_index':aux,
            })

        aux_df = components_df.iloc[tmp_item.atoms_dataframe['component_index'].to_numpy()]
        aux_df.reset_index(inplace=True, drop=True)

        tmp_item.atoms_dataframe['component_id']=aux_df['component_id']
        tmp_item.atoms_dataframe['component_name']=aux_df['component_name']
        tmp_item.atoms_dataframe['component_type']=aux_df['component_type']
        tmp_item.atoms_dataframe['molecule_index']=aux_df['molecule_index']

        del(components_df, aux_df, component_indices)

        # Molecules

        entity_indices, aux = np.unique(topology_ds['molecules']['entity_index'][molecule_indices].astype('int64'),
                return_inverse=True)

        molecules_df = pd.DataFrame({
            'molecule_id':topology_ds['molecules']['id'][molecule_indices],
            'molecule_name':topology_ds['molecules']['name'].asstr()[molecule_indices],
            'molecule_type':topology_ds['molecules']['type'].asstr()[molecule_indices],
            'entity_index':aux,
            })

        aux_df = molecules_df.iloc[tmp_item.atoms_dataframe['molecule_index'].to_numpy()]
        aux_df.reset_index(inplace=True, drop=True)

        tmp_item.atoms_dataframe['molecule_id']=aux_df['molecule_id']
        tmp_item.atoms_dataframe['molecule_name']=aux_df['molecule_name']
        tmp_item.atoms_dataframe['molecule_type']=aux_df['molecule_type']
        tmp_item.atoms_dataframe['entity_index']=aux_df['entity_index']

        del(molecules_df, aux_df, molecule_indices)

        # Entities

        entities_df = pd.DataFrame({
            'entity_id':topology_ds['entities']['id'][entity_indices],
            'entity_name':topology_ds['entities']['name'].asstr()[entity_indices],
            'entity_type':topology_ds['entities']['type'].asstr()[entity_indices],
            })

        aux_df = entities_df.iloc[tmp_item.atoms_dataframe['entity_index'].to_numpy()]
        aux_df.reset_index(inplace=True, drop=True)

        tmp_item.atoms_dataframe['entity_id']=aux_df['entity_id']
        tmp_item.atoms_dataframe['entity_name']=aux_df['entity_name']
        tmp_item.atoms_dataframe['entity_type']=aux_df['entity_type']

        del(entities_df, aux_df, entity_indices)

        # Chains

        chains_df = pd.DataFrame({
            'chain_id':topology_ds['chains']['id'][chain_indices],
            'chain_name':topology_ds['chains']['name'].asstr()[chain_indices],
            'chain_type':topology_ds['chains']['type'].asstr()[chain_indices],
            })

        aux_df = chains_df.iloc[tmp_item.atoms_dataframe['chain_index'].to_numpy()]
        aux_df.reset_index(inplace=True, drop=True)

        tmp_item.atoms_dataframe['chain_id']=aux_df['chain_id']
        tmp_item.atoms_dataframe['chain_name']=aux_df['chain_name']
        tmp_item.atoms_dataframe['chain_type']=aux_df['chain_type']

        del(chains_df, aux_df, chain_indices)

        # Bonds

        mask1 = np.in1d(topology_ds['bonds']['atom1_index'][:], atom_indices)
        mask2 = np.in1d(topology_ds['bonds']['atom2_index'][:], atom_indices)
        mask = mask1*mask2

        tmp_item.bonds_dataframe['atom1_index']=np.searchsorted(atom_indices,
                topology_ds['bonds']['atom1_index'][mask].astype('int64'), side='left')
        tmp_item.bonds_dataframe['atom2_index']=np.searchsorted(atom_indices,
                topology_ds['bonds']['atom1_index'][mask].astype('int64'), side='left')
        tmp_item.bonds_dataframe['type']=topology_ds['bonds']['type'].asstr()[mask]
        tmp_item.bonds_dataframe['order']=topology_ds['bonds']['order'].asstr()[mask]


    return tmp_item

