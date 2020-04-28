from os.path import basename as _basename
from molsysmt.utils.exceptions import *
from molsysmt.native.dataframe import DataFrame
from numpy import array as _array, unique as _unique, ndenumerate as _ndenumerate, concatenate as _concatenate

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
     DataFrame : form_name,
    'molsysmt.DataFrame': form_name
}

info=["",""]

def to_aminoacids3_seq(item, atom_indices='all', frame_indices='all'):


    from molsysmt.native.io.dataframe.seqs import to_aminoacids3_seq as molsysmt_DataFrame_to_aminoacids3_seq
    return molsysmt_DataFrame_to_aminoacids3_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_aminoacids1_seq(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.seqs import to_aminoacids1_seq as molsysmt_DataFrame_to_aminoacids1_seq
    return molsysmt_DataFrame_to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_Composition(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.composition.classes import from_molsysmt_DataFrame as molsysmt_DataFrame_to_molsysmt_Composition
    return molsysmt_DataFrame_to_molsysmt_Composition(item, atom_indices=atom_indices, frame_indices=frame_indices)

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.iloc(atom_indices)

def duplicate(item):

    raise NotImplementedError

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
        output = item['atom.index'].to_numpy()
    else:
        output = indices
    return output

def get_atom_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['atom.id'][tmp_indices].to_numpy()
    return output

def get_atom_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['atom.name'][tmp_indices].to_numpy()
    return output

def get_atom_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['atom.type'][tmp_indices].to_numpy()
    return output

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['group.index'][tmp_indices].to_numpy()
    return output

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['group.id'][tmp_indices].to_numpy()
    return output

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['group.name'][tmp_indices].to_numpy()
    return output

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['group.type'][tmp_indices].to_numpy()
    return output

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['component.index'][tmp_indices].to_numpy()
    return output

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['component.id'][tmp_indices].to_numpy()
    return output

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['component.name'][tmp_indices].to_numpy()
    return output

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['component.type'][tmp_indices].to_numpy()
    return output

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['chain.index'][tmp_indices].to_numpy()
    return output

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['chain.id'][tmp_indices].to_numpy()
    return output

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['chain.name'][tmp_indices].to_numpy()
    return output

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['chain.type'][tmp_indices].to_numpy()
    return output

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['molecule.index'][tmp_indices].to_numpy()
    return output

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['molecule.id'][tmp_indices].to_numpy()
    return output

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['molecule.name'][tmp_indices].to_numpy()
    return output

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['molecule.type'][tmp_indices].to_numpy()
    return output

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['entity.index'][tmp_indices].to_numpy()
    return output

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['entity.id'][tmp_indices].to_numpy()
    return output

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['entity.name'][tmp_indices].to_numpy()
    return output

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item['entity.type'][tmp_indices].to_numpy()
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
        mask = (item['group.index']==ii)
        output.append(item['atom.index'][mask].to_numpy())
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
        output = item['group.index'].unique()
    else:
        output = indices
    return output

def get_group_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['group.id'][right_locs].to_numpy()
    return output

def get_group_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['group.name'][right_locs].to_numpy()
    return output

def get_group_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['group.type'][right_locs].to_numpy()
    return output

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['component.index'][right_locs].to_numpy()
    return output

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['component.id'][right_locs].to_numpy()
    return output

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['component.name'][right_locs].to_numpy()
    return output

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['component.type'][right_locs].to_numpy()
    return output

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['chain.index'][right_locs].to_numpy()
    return output

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['chain.id'][right_locs].to_numpy()
    return output

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['chain.name'][right_locs].to_numpy()
    return output

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['chain.type'][right_locs].to_numpy()
    return output

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['molecule.index'][right_locs].to_numpy()
    return output

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['molecule.id'][right_locs].to_numpy()
    return output

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['molecule.name'][right_locs].to_numpy()
    return output

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['molecule.type'][right_locs].to_numpy()
    return output

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.index'][right_locs].to_numpy()
    return output

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.id'][right_locs].to_numpy()
    return output

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.name'][right_locs].to_numpy()
    return output

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['group.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

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
        mask = (item['component.index']==ii)
        output.append(item['atom.index'][mask].to_numpy())
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
        mask = (item['component.index']==ii)
        output.append(item['group.index'][mask].unique())
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
        output = item['component.index'].unique()
    else:
        output = indices
    return output

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['component.id'][right_locs].to_numpy()
    return output

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['component.name'][right_locs].to_numpy()
    return output

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['component.type'][right_locs].to_numpy()
    return output

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['chain.index'][right_locs].to_numpy()
    return output

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['chain.id'][right_locs].to_numpy()
    return output

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['chain.name'][right_locs].to_numpy()
    return output

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['chain.type'][right_locs].to_numpy()
    return output

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['molecule.index'][right_locs].to_numpy()
    return output

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['molecule.id'][right_locs].to_numpy()
    return output

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['molecule.name'][right_locs].to_numpy()
    return output

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['molecule.type'][right_locs].to_numpy()
    return output

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.index'][right_locs].to_numpy()
    return output

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.id'][right_locs].to_numpy()
    return output

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.name'][right_locs].to_numpy()
    return output

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['component.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    output = get_group_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

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
        mask = (item['molecule.index']==ii)
        output.append(item['atom.index'][mask].to_numpy())
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
        mask = (item['molecule.index']==ii)
        output.append(item['group.index'][mask].unique())
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
        mask = (item['molecule.index']==ii)
        output.append(item['component.index'][mask].unique())
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
        mask = (item['molecule.index']==ii)
        output.append(item['chain.index'][mask].unique())
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
        output = item['molecule.index'].unique()
    else:
        output = indices
    return output

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['molecule.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['molecule.id'][right_locs].to_numpy()
    return output

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['molecule.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['molecule.name'][right_locs].to_numpy()
    return output

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['molecule.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['molecule.type'][right_locs].to_numpy()
    return output

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['molecule.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.index'][right_locs].to_numpy()
    return output

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['molecule.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.id'][right_locs].to_numpy()
    return output

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['molecule.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.name'][right_locs].to_numpy()
    return output

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['molecule.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    output = get_group_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    output = get_component_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

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
        mask = (item['chain.index']==ii)
        output.append(item['atom.index'][mask].to_numpy())
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
        mask = (item['chain.index']==ii)
        output.append(item['group.index'][mask].unique())
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
        mask = (item['chain.index']==ii)
        output.append(item['component.index'][mask].unique())
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
        output = item['chain.index'].unique()
    else:
        output = indices
    return output

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['chain.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['chain.id'][right_locs].to_numpy()
    return output

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['chain.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['chain.name'][right_locs].to_numpy()
    return output

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['chain.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['chain.type'][right_locs].to_numpy()
    return output

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item['chain.index']==ii)
        output.append(item['molecule.index'][mask].unique())
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
    all_indices = item['chain.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.index'][right_locs].to_numpy()
    return output

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['chain.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.id'][right_locs].to_numpy()
    return output

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['chain.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.name'][right_locs].to_numpy()
    return output

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    tmp_indices = get_chain_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['chain.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    output = get_group_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    output = get_component_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

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
        mask = (item['entity.index']==ii)
        output.append(item['atom.index'][mask].to_numpy())
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
        mask = (item['entity.index']==ii)
        output.append(item['group.index'][mask].unique())
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
        mask = (item['entity.index']==ii)
        output.append(item['component.index'][mask].unique())
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
        mask = (item['entity.index']==ii)
        output.append(item['chain.index'][mask].unique())
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
        mask = (item['entity.index']==ii)
        output.append(item['molecule.index'][mask].unique())
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
        output = item['entity.index'].unique()
    else:
        output = indices
    return output

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    tmp_indices = get_entity_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['entity.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.id'][right_locs].to_numpy()
    return output

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    tmp_indices = get_entity_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['entity.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.name'][right_locs].to_numpy()
    return output

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    tmp_indices = get_entity_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    all_indices = item['entity.index'].to_numpy()
    right_locs = [next((idx for idx, val in _ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item['entity.type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    output = get_group_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    output = get_component_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = _unique(_concatenate(output))
    return output.shape[0]

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

    return item.shape[0]

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    output = item['group.index'].unique()
    return output.shape[0]

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    output = item['component.index'].unique()
    return output.shape[0]

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    output = item['chain.index'].unique()
    return output.shape[0]

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    output = item['molecule.index'].unique()
    return output.shape[0]

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    output = item['entity.index'].unique()
    return output.shape[0]

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    mask=(item['group.type']=='aminoacid').to_numpy()
    serie_indices=item['group.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    mask=(item['group.type']=='nucleotide').to_numpy()
    serie_indices=item['group.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='ion').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='water').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='cosolute').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='small_molecule').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='peptide').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='protein').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='dna').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    mask=(item['molecule.type']=='rna').to_numpy()
    serie_indices=item['molecule.index'][mask]
    return serie_indices.unique().shape[0]

def get_mass_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return 0

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

