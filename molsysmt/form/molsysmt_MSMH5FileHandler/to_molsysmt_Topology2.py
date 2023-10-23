from molsysmt._private.digestion import digest
import pandas as pd
import numpy as np

@digest(form='molsysmt.MSMH5FileHandler')
def to_molsysmt_Topology2(item, atom_indices='all'):

    from molsysmt.native import Topology2

    topology_ds = item.file['topology']

    tmp_item = Topology2()

    # Atoms

    n_atoms = topology_ds['atoms'].attrs['n_atoms']

    tmp_item.atoms['atom_id']=topology_ds['atoms']['id'][:]
    tmp_item.atoms['atom_type']=topology_ds['atoms']['type'].asstr()[:]
    tmp_item.atoms['atom_name']=topology_ds['atoms']['name'].asstr()[:]
    tmp_item.atoms['group_index']=topology_ds['atoms']['group_index'][:]
    tmp_item.atoms['chain_index']=topology_ds['atoms']['chain_index'][:]

    # Groups

    tmp_item.groups['group_id']=topology_ds['groups']['id'][:]
    tmp_item.groups['group_name']=topology_ds['groups']['name'].asstr()[:]
    tmp_item.groups['group_type']=topology_ds['groups']['type'].asstr()[:]
    tmp_item.groups['component_index']=topology_ds['groups']['component_index'][:]

    # Components

    tmp_item.components['component_id']=topology_ds['components']['id'][:]
    tmp_item.components['component_name']=topology_ds['components']['name'].asstr()[:]
    tmp_item.components['component_type']=topology_ds['components']['type'].asstr()[:]
    tmp_item.components['molecule_index']=topology_ds['components']['molecule_index'][:]

    # Molecules

    tmp_item.molecules['molecule_id']=topology_ds['molecules']['id'][:]
    tmp_item.molecules['molecule_name']=topology_ds['molecules']['name'].asstr()[:]
    tmp_item.molecules['molecule_type']=topology_ds['molecules']['type'].asstr()[:]
    tmp_item.molecules['entity_index']=topology_ds['molecules']['entity_index'][:]

    # Entities

    tmp_item.entities['entity_id']=topology_ds['entities']['id'][:]
    tmp_item.entities['entity_name']=topology_ds['entities']['name'].asstr()[:]
    tmp_item.entities['entity_type']=topology_ds['entities']['type'].asstr()[:]

    # Entities

    tmp_item.chains['chain_id']=topology_ds['chains']['id'][:]
    tmp_item.chains['chain_name']=topology_ds['chains']['name'].asstr()[:]
    tmp_item.chains['chain_type']=topology_ds['chains']['type'].asstr()[:]

    # Bonds

    tmp_item.bonds['atom1_index']=topology_ds['bonds']['atom1_index'][:]
    tmp_item.bonds['atom2_index']=topology_ds['bonds']['atom2_index'][:]
    tmp_item.bonds['type']=topology_ds['bonds']['type'].asstr()[:]
    tmp_item.bonds['order']=topology_ds['bonds']['order'].asstr()[:]

    return tmp_item

