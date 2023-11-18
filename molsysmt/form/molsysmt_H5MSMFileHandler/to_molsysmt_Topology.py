from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import pandas as pd
import numpy as np

@digest(form='molsysmt.H5MSMFileHandler')
def to_molsysmt_Topology(item, atom_indices='all'):

    from molsysmt.native import Topology

    topology_ds = item.file['topology']

    tmp_item = Topology()

    if is_all(atom_indices):

        # Atoms

        tmp_item.atoms['atom_id']=topology_ds['atoms']['id'][:].astype('int64')
        tmp_item.atoms['atom_type']=topology_ds['atoms']['type'].asstr()[:]
        tmp_item.atoms['atom_name']=topology_ds['atoms']['name'].asstr()[:]
        tmp_item.atoms['group_index']=topology_ds['atoms']['group_index'][:].astype('int64')
        tmp_item.atoms['chain_index']=topology_ds['atoms']['chain_index'][:].astype('int64')

        # Groups

        tmp_item.groups['group_id']=topology_ds['groups']['id'][:].astype('int64')
        tmp_item.groups['group_name']=topology_ds['groups']['name'].asstr()[:]
        tmp_item.groups['group_type']=topology_ds['groups']['type'].asstr()[:]
        tmp_item.groups['component_index']=topology_ds['groups']['component_index'][:].astype('int64')

        # Components

        tmp_item.components['component_id']=topology_ds['components']['id'][:].astype('int64')
        tmp_item.components['component_name']=topology_ds['components']['name'].asstr()[:]
        tmp_item.components['component_type']=topology_ds['components']['type'].asstr()[:]
        tmp_item.components['molecule_index']=topology_ds['components']['molecule_index'][:].astype('int64')

        # Molecules

        tmp_item.molecules['molecule_id']=topology_ds['molecules']['id'][:].astype('int64')
        tmp_item.molecules['molecule_name']=topology_ds['molecules']['name'].asstr()[:]
        tmp_item.molecules['molecule_type']=topology_ds['molecules']['type'].asstr()[:]
        tmp_item.molecules['entity_index']=topology_ds['molecules']['entity_index'][:].astype('int64')

        # Entities

        tmp_item.entities['entity_id']=topology_ds['entities']['id'][:].astype('int64')
        tmp_item.entities['entity_name']=topology_ds['entities']['name'].asstr()[:]
        tmp_item.entities['entity_type']=topology_ds['entities']['type'].asstr()[:]

        # Chains

        tmp_item.chains['chain_id']=topology_ds['chains']['id'][:].astype('int64')
        tmp_item.chains['chain_name']=topology_ds['chains']['name'].asstr()[:]
        tmp_item.chains['chain_type']=topology_ds['chains']['type'].asstr()[:]

        # Bonds

        tmp_item.bonds['atom1_index']=topology_ds['bonds']['atom1_index'][:].astype('int64')
        tmp_item.bonds['atom2_index']=topology_ds['bonds']['atom2_index'][:].astype('int64')
        tmp_item.bonds['type']=topology_ds['bonds']['type'].asstr()[:]
        tmp_item.bonds['order']=topology_ds['bonds']['order'].asstr()[:]

    else:

        # Atoms

        tmp_item.atoms['atom_id'] = topology_ds['atoms']['id'][atom_indices].astype('int64')
        tmp_item.atoms['atom_type'] = topology_ds['atoms']['type'].asstr()[atom_indices]
        tmp_item.atoms['atom_name'] = topology_ds['atoms']['name'].asstr()[atom_indices]

        group_indices, aux = np.unique(topology_ds['atoms']['group_index'][atom_indices].astype('int64'),
                    return_inverse=True)
        tmp_item.atoms['group_index'] = aux

        chain_indices, aux = np.unique(topology_ds['atoms']['chain_index'][atom_indices].astype('int64'),
                    return_inverse=True)
        tmp_item.atoms['chain_index']=aux


        # Groups

        tmp_item.groups['group_id']=topology_ds['groups']['id'][group_indices].astype('int64')
        tmp_item.groups['group_name']=topology_ds['groups']['name'].asstr()[group_indices]
        tmp_item.groups['group_type']=topology_ds['groups']['type'].asstr()[group_indices]

        component_indices, aux = np.unique(topology_ds['groups']['component_index'][group_indices].astype('int64'),
                    return_inverse=True)
        tmp_item.atoms['component_index']=aux

        # Components

        tmp_item.components['component_id']=topology_ds['components']['id'][component_indices].astype('int64')
        tmp_item.components['component_name']=topology_ds['components']['name'].asstr()[component_indices]
        tmp_item.components['component_type']=topology_ds['components']['type'].asstr()[component_indices]

        molecule_indices, aux = np.unique(topology_ds['components']['molecule_index'][component_indices].astype('int64'),
                    return_inverse=True)
        tmp_item.components['molecule_index']=aux

        # Molecules

        tmp_item.molecules['molecule_id']=topology_ds['molecules']['id'][molecule_indices].astype('int64')
        tmp_item.molecules['molecule_name']=topology_ds['molecules']['name'].asstr()[molecule_indices]
        tmp_item.molecules['molecule_type']=topology_ds['molecules']['type'].asstr()[molecule_indices]

        entity_indices, aux = np.unique(topology_ds['molecules']['entity_index'][molecule_indices].astype('int64'),
                    return_inverse=True)
        tmp_item.molecules['entity_index']=aux

        # Entities

        tmp_item.entities['entity_id']=topology_ds['entities']['id'][entity_indices].astype('int64')
        tmp_item.entities['entity_name']=topology_ds['entities']['name'].asstr()[entity_indices]
        tmp_item.entities['entity_type']=topology_ds['entities']['type'].asstr()[entity_indices]

        # Entities

        tmp_item.chains['chain_id']=topology_ds['chains']['id'][chain_indices].astype('int64')
        tmp_item.chains['chain_name']=topology_ds['chains']['name'].asstr()[chain_indices]
        tmp_item.chains['chain_type']=topology_ds['chains']['type'].asstr()[chain_indices]

        # Bonds

        mask1 = np.in1d(topology_ds['bonds']['atom1_index'][:], atom_indices)
        mask2 = np.in1d(topology_ds['bonds']['atom2_index'][:], atom_indices)
        mask = mask1*mask2
       
        tmp_item.bonds['atom1_index']=np.searchsorted(atom_indices,
                    topology_ds['bonds']['atom1_index'][mask].astype('int64'),
                    side='left')
        tmp_item.bonds['atom2_index']=np.searchsorted(atom_indices,
                    topology_ds['bonds']['atom2_index'][mask].astype('int64'),
                    side='left')
        tmp_item.bonds['type']=topology_ds['bonds']['type'].asstr()[mask]
        tmp_item.bonds['order']=topology_ds['bonds']['order'].asstr()[mask]

        del(aux, mask1, mask2, mask)

    return tmp_item

