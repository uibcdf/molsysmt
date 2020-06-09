from os.path import basename as _basename
from molsysmt.utils.exceptions import *
from molsysmt.native.topology import Topology
from numpy import array as _array, unique as _unique, ndenumerate as _ndenumerate, concatenate as _concatenate

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
     Topology : form_name,
    'molsysmt.Topology': form_name
}

info=["",""]
with_topology=True
with_trajectory=False

def to_aminoacids3_seq(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.seqs import to_aminoacids3_seq as molsysmt_DataFrame_to_aminoacids3_seq
    return molsysmt_DataFrame_to_aminoacids3_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_aminoacids1_seq(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.seqs import to_aminoacids1_seq as molsysmt_DataFrame_to_aminoacids1_seq
    return molsysmt_DataFrame_to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_molsysmt_DataFrame as molsysmt_DataFrame_to_molsysmt_Topology
    return molsysmt_DataFrame_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_openmm_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.classes import to_openmm_Topology as molsysmt_DataFrame_to_openmm_Topology
    return molsysmt_DataFrame_to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_mdtraj_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.classes import to_mdtraj_Topology as molsysmt_DataFrame_to_mdtraj_Topology
    return molsysmt_DataFrame_to_mdtraj_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_pdb(item, output_filepath=None, trajectory_item=None, atom_indices='all', frame_indices='all'):
    from molsysmt.native.io.dataframe.files import to_pdb as molsysmt_DataFrame_to_pdb
    return molsysmt_DataFrame_to_pdb(item, output_filepath=output_filepath,
                                    trajectory_item=trajectory_item,  atom_indices=atom_indices,
                                    frame_indices=frame_indices)


def extract(item, atom_indices='all', frame_indices='all'):

    return item.extract(atom_indices=atom_indices)

def copy(item):

    return item.copy()

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from molsysmt.native.selector import dataframe_select
    atom_indices = dataframe_select(item, selection)
    return atom_indices

###### Get

## Atom

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item.elements['atom_index'].to_numpy()
    else:
        output = indices
    return output

def get_atom_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['atom_id'][tmp_indices].to_numpy()
    return output

def get_atom_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['atom_name'][tmp_indices].to_numpy()
    return output

def get_atom_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['atom_type'][tmp_indices].to_numpy()
    return output

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['group_index'][tmp_indices].to_numpy()
    return output

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['group_id'][tmp_indices].to_numpy()
    return output

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['group_name'][tmp_indices].to_numpy()
    return output

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['group_type'][tmp_indices].to_numpy()
    return output

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['component_index'][tmp_indices].to_numpy()
    return output

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['component_id'][tmp_indices].to_numpy()
    return output

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['component_name'][tmp_indices].to_numpy()
    return output

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['component_type'][tmp_indices].to_numpy()
    return output

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['chain_index'][tmp_indices].to_numpy()
    return output

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['chain_id'][tmp_indices].to_numpy()
    return output

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['chain_name'][tmp_indices].to_numpy()
    return output

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['chain_type'][tmp_indices].to_numpy()
    return output

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['molecule_index'][tmp_indices].to_numpy()
    return output

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['molecule_id'][tmp_indices].to_numpy()
    return output

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['molecule_name'][tmp_indices].to_numpy()
    return output

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['molecule_type'][tmp_indices].to_numpy()
    return output

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['entity_index'][tmp_indices].to_numpy()
    return output

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['entity_id'][tmp_indices].to_numpy()
    return output

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['entity_name'][tmp_indices].to_numpy()
    return output

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.elements['entity_type'][tmp_indices].to_numpy()
    return output

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    output = get_group_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    output = get_component_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_atom (item, indices='all', frame_indices='all'):

    return form_name

## group

def get_index_from_group (item, indices='all', frame_indices='all'):

    return get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)

def get_id_from_group (item, indices='all', frame_indices='all'):

    return get_group_id_from_group(item, indices=indices, frame_indices=frame_indices)

def get_name_from_group (item, indices='all', frame_indices='all'):

    return get_group_name_from_group(item, indices=indices, frame_indices=frame_indices)

def get_type_from_group (item, indices='all', frame_indices='all'):

    return get_group_type_from_group(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_group (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['group_index']==ii)
        output.append(item.elements['atom_index'][mask].to_numpy())
    output = _array(output)
    return output

def get_atom_id_from_group (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_group(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_name_from_group (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_group(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_type_from_group (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_group(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_index_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item.elements['group_index'].unique()
    else:
        output = indices
    return output

def get_group_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['group_id'][right_locs].to_numpy()
    return output

def get_group_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['group_name'][right_locs].to_numpy()
    return output

def get_group_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['group_type'][right_locs].to_numpy()
    return output

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['component_index'][right_locs].to_numpy()
    return output

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['component_id'][right_locs].to_numpy()
    return output

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['component_name'][right_locs].to_numpy()
    return output

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['component_type'][right_locs].to_numpy()
    return output

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['chain_index'][right_locs].to_numpy()
    return output

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elemenents['chain_id'][right_locs].to_numpy()
    return output

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['chain_name'][right_locs].to_numpy()
    return output

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['chain_type'][right_locs].to_numpy()
    return output

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['molecule_index'][right_locs].to_numpy()
    return output

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['molecule_id'][right_locs].to_numpy()
    return output

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['molecule_name'][right_locs].to_numpy()
    return output

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['molecule_type'][right_locs].to_numpy()
    return output

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_index'][right_locs].to_numpy()
    return output

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_id'][right_locs].to_numpy()
    return output

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_name'][right_locs].to_numpy()
    return output

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    output = get_group_index_from_group (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    output = get_component_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## component

def get_index_from_component (item, indices='all', frame_indices='all'):

    return get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)

def get_id_from_component (item, indices='all', frame_indices='all'):

    return get_component_id_from_component(item, indices=indices, frame_indices=frame_indices)

def get_name_from_component (item, indices='all', frame_indices='all'):

    return get_component_name_from_component(item, indices=indices, frame_indices=frame_indices)

def get_type_from_component (item, indices='all', frame_indices='all'):

    return get_component_type_from_component(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_component (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['component_index']==ii)
        output.append(item.elements['atom_index'][mask].to_numpy())
    output = _array(output)
    return output

def get_atom_id_from_component (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_name_from_component (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_type_from_component (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_index_from_component (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['component_index']==ii)
        output.append(item.elements['group_index'][mask].unique())
    output = _array(output)
    return output

def get_group_id_from_component (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_name_from_component (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_type_from_component (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item.elements['component_index'].unique()
    else:
        output = indices
    return output

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['component_id'][right_locs].to_numpy()
    return output

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['component.name'][right_locs].to_numpy()
    return output

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['component_type'][right_locs].to_numpy()
    return output

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['chain_index'][right_locs].to_numpy()
    return output

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['chain_id'][right_locs].to_numpy()
    return output

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['chain_name'][right_locs].to_numpy()
    return output

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['chain_type'][right_locs].to_numpy()
    return output

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['molecule.index'][right_locs].to_numpy()
    return output

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['molecule_id'][right_locs].to_numpy()
    return output

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['molecule_name'][right_locs].to_numpy()
    return output

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['molecule_type'][right_locs].to_numpy()
    return output

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_index'][right_locs].to_numpy()
    return output

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_id'][right_locs].to_numpy()
    return output

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_name'][right_locs].to_numpy()
    return output

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    output = get_group_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    output = get_component_index_from_component (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## molecule

def get_index_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)

def get_id_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_id_from_molecule(item, indices=indices, frame_indices=frame_indices)

def get_name_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_name_from_molecule(item, indices=indices, frame_indices=frame_indices)

def get_type_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_type_from_molecule(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_molecule (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['molecule_index']==ii)
        output.append(item.elements['atom_index'][mask].to_numpy())
    output = _array(output)
    return output

def get_atom_id_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_name_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_type_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_index_from_molecule (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['molecule_index']==ii)
        output.append(item.elements['group_index'][mask].unique())
    output = _array(output)
    return output

def get_group_id_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_name_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_type_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['molecule_index']==ii)
        output.append(item.elements['component_index'][mask].unique())
    output = _array(output)
    return output

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_id_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_name_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_type_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['molecule_index']==ii)
        output.append(item.elements['chain_index'][mask].unique())
    output = _array(output)
    return output

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_id_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_name_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_type_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item.elements['molecule_index'].unique()
    else:
        output = indices
    return output

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['molecule_id'][right_locs].to_numpy()
    return output

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['molecule_name'][right_locs].to_numpy()
    return output

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['molecule_type'][right_locs].to_numpy()
    return output

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_index'][right_locs].to_numpy()
    return output

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_id'][right_locs].to_numpy()
    return output

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_name'][right_locs].to_numpy()
    return output

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    output = get_group_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    output = get_component_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## chain

def get_index_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)

def get_id_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_id_from_chain(item, indices=indices, frame_indices=frame_indices)

def get_name_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_name_from_chain(item, indices=indices, frame_indices=frame_indices)

def get_type_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_type_from_chain(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_chain (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['chain_index']==ii)
        output.append(item.elements['atom_index'][mask].to_numpy())
    output = _array(output)
    return output

def get_atom_id_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_name_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_type_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_index_from_chain (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['chain_index']==ii)
        output.append(item.elements['group_index'][mask].unique())
    output = _array(output)
    return output

def get_group_id_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_name_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_type_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['chain_index']==ii)
        output.append(item.elements['component_index'][mask].unique())
    output = _array(output)
    return output

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_id_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_name_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_type_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item.elements['chain_index'].unique()
    else:
        output = indices
    return output

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['chain_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['chain_id'][right_locs].to_numpy()
    return output

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['chain_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['chain_name'][right_locs].to_numpy()
    return output

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['chain_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['chain_type'][right_locs].to_numpy()
    return output

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['chain_index']==ii)
        output.append(item.elements['molecule_index'][mask].unique())
    output = _array(output)
    return output

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_molecule_id_from_molecule(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_molecule_name_from_molecule(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_molecule_type_from_molecule(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['chain_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_index'][right_locs].to_numpy()
    return output

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['chain_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_id'][right_locs].to_numpy()
    return output

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['chain_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_name'][right_locs].to_numpy()
    return output

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['chain_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    output = get_group_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    output = get_component_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## entity

def get_index_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_index_from_entity(item, indices=indices, frame_indices=frame_indices)

def get_id_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_id_from_entity(item, indices=indices, frame_indices=frame_indices)

def get_name_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_name_from_entity(item, indices=indices, frame_indices=frame_indices)

def get_type_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_type_from_entity(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_entity (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['entity_index']==ii)
        output.append(item.elements['atom_index'][mask].to_numpy())
    output = _array(output)
    return output

def get_atom_id_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_name_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_type_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_index_from_entity (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['entity_index']==ii)
        output.append(item.elements['group_index'][mask].unique())
    output = _array(output)
    return output

def get_group_id_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_name_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_type_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['entity_index']==ii)
        output.append(item.elements['component_index'][mask].unique())
    output = _array(output)
    return output

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_id_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_name_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_type_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['entity_index']==ii)
        output.append(item.elements['chain_index'][mask].unique())
    output = _array(output)
    return output

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_id_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_name_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_type_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.elements['entity_index']==ii)
        output.append(item.elements['molecule_index'][mask].unique())
    output = _array(output)
    return output

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_molecule_id_from_molecule(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_molecule_name_from_molecule(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_molecule_type_from_molecule(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item.elements['entity_index'].unique()
    else:
        output = indices
    return output

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    tmp_indices = get_entity_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['entity_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_id'][right_locs].to_numpy()
    return output

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    tmp_indices = get_entity_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['entity_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_name'][right_locs].to_numpy()
    return output

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    tmp_indices = get_entity_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.elements['entity_index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.elements['entity_type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    output = get_group_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    output = get_component_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## system

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.elements.shape[0]

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    output = item.elements['group_index'].unique()
    return output.shape[0]

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    output = item.elements['component_index'].unique()
    return output.shape[0]

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    output = item.elements['chain_index'].unique()
    return output.shape[0]

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    output = item.elements['molecule_index'].unique()
    return output.shape[0]

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    output = item.elements['entity_index'].unique()
    return output.shape[0]

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    mask=(item.elements['group_type']=='aminoacid').to_numpy()
    serie_indices=item.elements['group_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    mask=(item.elements['group_type']=='nucleotide').to_numpy()
    serie_indices=item.elements['group_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    mask=(item.elements['molecule_type']=='ion').to_numpy()
    serie_indices=item.elements['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    mask=(item.elements['molecule_type']=='water').to_numpy()
    serie_indices=item.elements['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    mask=(item.elements['molecule_type']=='cosolute').to_numpy()
    serie_indices=item.elements['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    mask=(item.elements['molecule_type']=='small_molecule').to_numpy()
    serie_indices=item.elements['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    mask=(item.elements['molecule_type']=='peptide').to_numpy()
    serie_indices=item.elements['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    mask=(item.elements['molecule_type']=='protein').to_numpy()
    serie_indices=item.elements['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    mask=(item.elements['molecule_type']=='dna').to_numpy()
    serie_indices=item.elements['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    mask=(item.elements['molecule_type']=='rna').to_numpy()
    serie_indices=item.elements['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_mass_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return 0

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

