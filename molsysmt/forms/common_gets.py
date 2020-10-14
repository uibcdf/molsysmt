import numpy as np
import inspect
from molsysmt import get

_plural = {
    'atom':'atoms',
    'group':'groups',
    'component':'components',
    'chain':'chains',
    'molecule':'molecules',
    'entity':'entities',
    'bond':'bonds'
}

_singular = {value:key for key,value in _plural.items()}

def _aux_getter_attribute(item, method_name, indices):

    method_fields = method_name.split('_')
    from_target = method_fields[-1]
    attribute = method_fields[1]
    dict_aaa = {from_target+'_'+attribute:True}

    output = get(item, target=from_target, indices=indices, *dict_aaa)
    return output

def _aux_getter_attribute_from(item, method_name, indices):

    method_fields = method_name.split('_')
    from_target = method_fields[-1]
    to_target = method_fields[1]
    attribute = method_fields[2]
    dict_aaa = {to_target+'_index':True}
    dict_ccc = {to_target+'_'+attribute:True}

    aaa = get(item, target=from_target, indices=indices, *dict_aaa)
    bbb = np.unique(aaa)
    ccc = get(item, target=to_target, indices=bbb, *dict_ccc)
    aux_dict = dict(zip(bbb, ccc))
    output = np.vectorize(aux_dict.__getitem__)(aaa)
    del(aux_dict)
    return output

def _aux_getter_index(item, method_name, indices):

    method_fields = method_name.split('_')
    from_target = method_fields[-1]
    dict_aaa = {'n_'+_plural[from_target]:True}

    if indices is 'all':
        n_aux = get(item, target='system', indices=indices, *dict_aaa)
        return np.arange(n_aux)
    else:
        return np.array(indices)

def _aux_getter_big_index_from_small(item, method_name, indices):

    method_fields = method_name.split('_')
    from_target = method_fields[-1]
    to_target = method_fields[1]
    attribute = method_fields[2]
    dict_bbb = {to_target+'_'+attribute:True}

    aaa = get(item, target=from_target, indices=indices, atom_index=True)
    bbb = np.array([ii[0] for ii in aaa])
    output = get(item, target='atom', indices=bbb, *dict_bbb)
    return output

def _aux_getter_small_index_from_big(item, method_name, indices):

    method_fields = method_name.split('_')
    from_target = method_fields[-1]
    to_target = method_fields[1]
    attribute = method_fields[2]
    dict_aaa = {from_target+'_index':True}

    aaa = get(item, target=to_target, indices='all', *dict_aaa)
    indices_aux = get(item, target=from_target, indices=indices, *dict_aaa)

    output = []
    for ii in indices_aux:
        tmp_indices = np.where(aaa==ii)
        output.append(tmp_indices)

    output = np.array(output)

    return output

def _aux_n(item, method_name, indices):

    method_fields = method_name.split('_')
    from_target = method_fields[-1]
    targets = method_fields[2]
    dict_aaa = {'n_'+targets:True}

    if indices is 'all':
        return get(item, target='system', *dict_aaa)
    else:
        return indices.shape[0]

def _aux_n_big_from_small(item, method_name, indices):

    method_fields = method_name.split('_')
    from_target = method_fields[-1]
    targets = method_fields[2]
    dict_aaa = {'n_'+targets:True}
    dict_bbb = {_singular[targets]+'_index':True}

    if indices is 'all':
        return get(item, target='system', *dict_aaa)
    else:
        output = get(item, target=from_group, indices=indices, *dict_bbb)
        return np.unique(output).shape[0]

def _aux_n_small_from_big(item, method_name, indices):

    method_fields = method_name.split('_')
    from_target = method_fields[-1]
    targets = method_fields[2]
    dict_aaa = {'n_'+targets:True}
    dict_bbb = {_singular[targets]+'_index':True}

    if indices is 'all':
        return get(item, target='system', *dict_aaa)
    else:
        output = get(item, target=from_group, indices=indices, *dict_bbb)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

## atom

def get_index_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_index(item, method_name, indices)

#def get_atom_id_from_atom(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_atom_name_from_atom(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_atom_type_from_atom(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_group_index_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

#def get_component_index_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

#def get_chain_index_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

#def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

#def get_entity_index_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n(item, method_name, indices)

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

#def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_bond_index_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):
#
#    if indices is 'all':
#        return get_n_bonds_from_system (item)
#    else:
#        raise NotImplementedError

#def get_inner_bond_index_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):
#
#    if indices is 'all':
#        return get_n_inner_bonds_from_system (item)
#    else:
#        raise NotImplementedError

#def get_coordinates_from_atom(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    tmp_step, tmp_time, tmp_box = get(item, target='system', frame_indices=frame_indices, step=True, time=True, box=True)
    tmp_coordinates = get(item, target='atom', indices=indices, frame_indices=frame_indices, coordinates=True)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

def get_n_frames_from_atom(item, indices='all', frame_indices='all'):

    return get(item, target='system', indices='all', frame_indices=frame_indices, n_frames=True)

def get_form_from_atom(item, indices='all', frame_indices='all'):

    return get(item, target='system')

## group

def get_index_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_id_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_name_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_type_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_atom_index_from_group(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_index(item, method_name, indices)

#def get_group_id_from_group(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_group_name_from_group(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_group_type_from_group(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_big_index_from_small(item, method_name, indices)

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_big_index_from_small(item, method_name, indices)

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_big_index_from_small(item, method_name, indices)

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_big_index_from_small(item, method_name, indices)

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n(item, method_name, indices)

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

## component

def get_index_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_id_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_name_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_type_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_atom_index_from_component(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_index(item, method_name, indices)

#def get_component_id_from_component (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_component_name_from_component (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError


#def get_component_type_from_component (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_big_index_from_small(item, method_name, indices)

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_big_index_from_small(item, method_name, indices)

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_big_index_from_small(item, method_name, indices)

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n(item, method_name, indices)

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

## molecule

def get_index_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_id_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_name_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_type_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_atom_index_from_molecule(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_index(item, method_name, indices)

#def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_big_index_from_small(item, method_name, indices)

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n(item, method_name, indices)

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

## chain

def get_index_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_id_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_name_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_type_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_atom_index_from_chain(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_index(item, method_name, indices)

#def get_chain_id_from_chain (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_chain_name_from_chain (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_chain_type_from_chain (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_big_index_from_small(item, method_name, indices)

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n(item, method_name, indices)

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_big_from_small(item, method_name, indices)

## entity

def get_index_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_id_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_name_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_type_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_atom_index_from_entity(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_small_index_from_big(item, method_name, indices)

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute_from(item, method_name, indices)

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_index(item, method_name, indices)

#def get_entity_id_from_entity (item, indices='all', frame_indices='all'):     # EMPTY
#
#    raise NotImplementedError

#def get_entity_name_from_entity (item, indices='all', frame_indices='all'):     # EMPTY
#
#    raise NotImplementedError

#def get_entity_type_from_entity (item, indices='all', frame_indices='all'):     # EMPTY
#
#    raise NotImplementedError

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n_small_from_big(item, method_name, indices)

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n(item, method_name, indices)

## system

#def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_n_atoms_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_n_groups_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_n_components_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_n_chains_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_n_molecules_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_n_entities_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_n_bonds_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    group_types = get(item, target='group', indices='all', group_type=True)
    return (group_types=='aminoacid').sum()

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    group_types = get(item, target='group', indices='all', group_type=True)
    return (group_types=='nucleotide').sum()

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='ion').sum()

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='water').sum()

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='cosolute').sum()

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='small_molecule').sum()

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='peptide').sum()

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='protein').sum()

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='dna').sum()

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='rna').sum()

def get_n_lipids_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='lipid').sum()

#def get_coordinates_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_box_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_box_shape_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_box_lengths_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_box_angles_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_time_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_step_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_frame_from_system(item, indices='all', frame_indices='all'):

    tmp_step, tmp_time, tmp_box, tmp_coordinates = get(item, target='system', frame_indices=frame_indices,
                                      step=True, time=True, box=True, coordinates=True)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

#def get_n_frames_from_system(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

## bond

def get_index_from_bond(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_order_from_bond(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_type_from_bond(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_attribute(item, method_name, indices)

def get_bond_index_from_bond(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_getter_index(item, method_name, indices)

#def get_bond_order_from_bond(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_bond_type_from_bond(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

#def get_atom_index_from_bond(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_n_bonds_from_bond(item, indices='all', frame_indices='all'):

    method_name = inspect.stack()[0][3]
    return _aux_n(item, method_name, indices)

