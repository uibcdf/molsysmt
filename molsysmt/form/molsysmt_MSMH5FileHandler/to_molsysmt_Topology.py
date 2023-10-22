from molsysmt._private.digestion import digest
import pandas as pd
import numpy as np

@digest(form='molsysmt.MSMH5FileHandler')
def to_molsysmt_Topology(item, atom_indices='all'):

    from molsysmt.native import Topology

    topology_ds = item.file['topology']

    n_atoms = topology_ds['atoms'].attrs['n_atoms']
    n_bonds = topology_ds['bonds'].attrs['n_bonds']

    tmp_item = Topology()

    # Atoms

    tmp_item.atoms_dataframe['atom_index']=np.arange(n_atoms)
    tmp_item.atoms_dataframe['atom_id']=topology_ds['atoms']['id'][:]
    tmp_item.atoms_dataframe['atom_type']=topology_ds['atoms']['type'].asstr()[:]
    tmp_item.atoms_dataframe['atom_name']=topology_ds['atoms']['name'].asstr()[:]
    tmp_item.atoms_dataframe['group_index']=topology_ds['atoms']['group_index'][:]

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

    # Bonds

    tmp_item.bonds_dataframe['atom1_index']=topology_ds['bonds']['atom1_index'][:]
    tmp_item.bonds_dataframe['atom2_index']=topology_ds['bonds']['atom2_index'][:]
    tmp_item.bonds_dataframe['type']=topology_ds['bonds']['type'].asstr()[:]
    tmp_item.bonds_dataframe['order']=topology_ds['bonds']['order'].asstr()[:]

    return tmp_item

