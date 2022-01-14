import numpy as np

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

#def _aux_getter_attribute(item, attribute, from_target, indices):
#
#    from molsysmt.basic import get
#
#    dict_attribute = {from_target+'_'+attribute:True}
#
#    output = get(item, target=from_target, indices=indices, **dict_attribute)
#    return output

def _aux_getter_big_attribute_from_small(item, attribute, from_target, indices):

    from molsysmt.basic import get

    auxtarget = attribute.split('_')[0]
    dict_auxtarget_index = {auxtarget+'_index':True}
    dict_attribute = {attribute:True}

    auxtarget_index_from_target = get(item, target=from_target, indices=indices, **dict_auxtarget_index)
    auxtarget_indices = np.unique(auxtarget_index_from_target)
    attribute_from_auxtarget = get(item, target=auxtarget, indices=auxtarget_indices, **dict_attribute)
    aux_dict = dict(zip(auxtarget_indices, attribute_from_auxtarget))
    output = np.vectorize(aux_dict.__getitem__)(auxtarget_index_from_target)
    del(aux_dict)
    return output

def _aux_getter_small_attribute_from_big(item, attribute, from_target, indices):

    from molsysmt.basic import get

    auxtarget = attribute.split('_')[0]
    dict_auxtarget_index = {auxtarget+'_index':True}
    dict_attribute = {attribute:True}

    auxtarget_index_from_target = get(item, target=from_target, indices=indices, **dict_auxtarget_index)

    if len(auxtarget_index_from_target)>0:
        auxtarget_indices = np.unique(np.concatenate(auxtarget_index_from_target))
        attribute_from_auxtarget = get(item, target=auxtarget, indices=auxtarget_indices, **dict_attribute)
        aux_dict = dict(zip(auxtarget_indices, attribute_from_auxtarget))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in auxtarget_index_from_target],dtype=object)
        del(aux_dict)
    else:
        output = np.array([], dtype=object)

    return output

def _aux_getter_index(item, from_target, indices):

    from molsysmt.basic import get

    if indices is 'all':
        dict_n_targets = {'n_'+_plural[from_target]:True}
        n_aux = get(item, target='system', **dict_n_targets)
        return np.arange(n_aux, dtype=int)
    else:
        return np.array(indices, dtype=int)

def _aux_getter_big_index_from_small(item, attribute, from_target, indices):

    from molsysmt.basic import get

    auxtarget = attribute.split('_')[0]
    dict_attribute = {attribute:True}

    atom_index_from_target = get(item, target=from_target, indices=indices, atom_index=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get(item, target='atom', indices=first_atom_index_from_target, **dict_attribute)
    return output

def _aux2_getter_big_index_from_small(item, attribute, from_target, indices):

    from molsysmt.basic import get

    dict_bbb = {attribute:True}
    atom_index_from_target = get(item, target=from_target, indices=indices, atom_index=True)
    attribute_from_atom = get(item, target='atom', indices='all', **dict_bbb)

    output = []
    for atom_indices in atom_index_from_target:
        output.append(attribuet_from_atom[atom_indices[0]])

    output = np.array(output)
    return output

def _aux_getter_small_index_from_big(item, attribute, from_target, indices):

    return _aux2_getter_small_index_from_big(item, attribute, from_target, indices)

def _aux2_getter_small_index_from_big(item, attribute, from_target, indices):

    from molsysmt.basic import get

    dict_index_from_target = {from_target+'_index':True}
    dict_attribute = {attribute:True}

    indices_aux = get(item, target=from_target, indices=indices, **dict_index_from_target)

    attribute_from_atom = get(item, target='atom', indices='all', **dict_attribute)
    target_index_from_atom = get(item, target='atom', indices='all', **dict_index_from_target)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def _aux_n(item, from_target, indices):

    from molsysmt.basic import get

    targets = _plural[from_target]
    dict_n_targets = {'n_'+targets:True}

    if indices is 'all':
        return get(item, target='system', **dict_n_targets)
    else:
        return indices.shape[0]

def _aux_n_big_from_small(item, attribute, from_target, indices):

    from molsysmt.basic import get

    auxtargets = attribute.split('_')[1]
    dict_attribute = {attribute:True}
    dict_index_auxtarget = {_singular[auxtargets]+'_index':True}

    if indices is 'all':
        return get(item, target='system', **dict_attribute)
    else:
        output = get(item, target=from_target, indices=indices, **dict_index_auxtarget)
        return np.unique(output).shape[0]

def _aux_n_small_from_big(item, attribute, from_target, indices):

    from molsysmt.basic import get

    auxtargets = attribute.split('_')[1]
    dict_index_auxtarget = {_singular[auxtargets]+'_index':True}
    output = get(item, target=from_target, indices=indices, **dict_index_auxtarget)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

## atom

def get_atom_index_from_atom(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_index(item, 'atom', indices)

#def get_atom_id_from_atom (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'id', 'atom', indices)
#
#def get_atom_name_from_atom (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'name', 'atom', indices)
#
#def get_atom_type_from_atom (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'type', 'atom', indices)

def get_group_id_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'group_id', 'atom', indices)

def get_group_name_from_atom (item, indices='all', frame_indices='all', check_form=True):

    output = _aux_getter_big_attribute_from_small(item, 'group_name', 'atom', indices)
    return output.astype(object)

def get_group_type_from_atom (item, indices='all', frame_indices='all', check_form=True):

    output = _aux_getter_big_attribute_from_small(item, 'group_type', 'atom', indices)
    return output.astype(object)

#def get_component_index_from_atom (item, indices='all', frame_indices='all', check_form=True):
#    raise NotImplementedError

def get_component_id_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'component_id', 'atom', indices)

def get_component_name_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'component_name', 'atom', indices)

def get_component_type_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'component_type', 'atom', indices)

#def get_chain_index_from_atom (item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

def get_chain_id_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'chain_id', 'atom', indices)

def get_chain_name_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'chain_name', 'atom', indices)

def get_chain_type_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'chain_type', 'atom', indices)

#def get_molecule_index_from_atom (item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

def get_molecule_id_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'molecule_id', 'atom', indices)

def get_molecule_name_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'molecule_name', 'atom', indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'molecule_type', 'atom', indices)

#def get_entity_index_from_atom (item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

def get_entity_id_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'entity_id', 'atom', indices)

def get_entity_name_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'entity_name', 'atom', indices)

def get_entity_type_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'entity_type', 'atom', indices)

def get_n_atoms_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n(item, 'atom', indices)

def get_n_groups_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_groups', 'atom', indices)

def get_n_components_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_components', 'atom', indices)

def get_n_molecules_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_molecules', 'atom', indices)

def get_n_chains_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_chains', 'atom', indices)

def get_n_entities_from_atom (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_entities', 'atom', indices)

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all', check_form=True):

    output = None

    from networkx import Graph
    from molsysmt.basic import get

    G = Graph()
    edges = get(item, target='bond', atom_index=True)
    G.add_edges_from(edges)

    if indices is 'all':

        indices = get(item, target='atom', atom_index=True)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n for n in G[ii]]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    del(Graph, G, edges)

    return output

def get_bond_index_from_atom (item, indices='all', frame_indices='all', check_form=True):

    output = None

    from networkx import Graph
    from molsysmt.basic import get

    G = Graph()
    edges = get(item, target='bond', atom_index=True)
    n_bonds = edges.shape[0]
    edge_indices = np.array([{'index':ii} for ii in range(n_bonds)]).reshape([n_bonds,1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if indices is 'all':

        indices = get_atom_index_from_atom(item)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n['index'] for n in G[ii].values()]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    del(Graph, G, edges, edge_indices)

    return output

def get_n_bonds_from_atom (item, indices='all', frame_indices='all', check_form=True):

    output = None

    from networkx import Graph
    from molsysmt.basic import get

    G = Graph()
    edges = get(item, target='bond', atom_index=True)
    G.add_edges_from(edges)

    if indices is 'all':

        indices = get_atom_index_from_atom(item)


    output = []

    for ii in indices:
        if ii in G:
            output.append(len(G[ii]))
        else:
            output.append(0)

    output = np.array(output)

    del(Graph, G, edges)

    return output

def get_inner_bond_index_from_atom (item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get

    output = None

    if indices is 'all':
        output = get(item, target='bond', index=True)
    else:
        edges = get(item, target='bond', atom_index=True)
        aux_list = list(indices)
        output = item.bonds_dataframe.query('atom1_index==@aux_list and atom2_index==@aux_list').index.to_numpy(dtype=int, copy=True)

    return output

#def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all', check_form=True):
#
#    if indices is 'all':
#        return get_n_inner_bonds_from_system (item)
#    else:
#        raise NotImplementedError

#def get_coordinates_from_atom(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_frame_from_atom(item, indices='all', frame_indices='all', check_form=True):
#
#    from molsysmt.basic import get
#
#    tmp_step, tmp_time, tmp_box = get(item, target='system', frame_indices=frame_indices, step=True, time=True, box=True)
#    tmp_coordinates = get(item, target='atom', indices=indices, frame_indices=frame_indices, coordinates=True)
#
#    return tmp_step, tmp_time, tmp_coordinates, tmp_box

def get_n_frames_from_atom(item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get

    return get(item, target='system', indices='all', frame_indices=frame_indices, n_frames=True)

## group

def get_atom_index_from_group(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'atom_index', 'group', indices)

def get_atom_id_from_group(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_id', 'group', indices)

def get_atom_name_from_group(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_name', 'group', indices)

def get_atom_type_from_group(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_type', 'group', indices)

def get_group_index_from_group(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_index(item, 'group', indices)

#def get_group_id_from_group (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'id', 'group', indices)
#
#def get_group_name_from_group (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'name', 'group', indices)
#
#def get_group_type_from_group (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'type', 'group', indices)

def get_component_index_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_index_from_small(item, 'component_index', 'group', indices)

def get_component_id_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'component_id', 'group', indices)

def get_component_name_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'component_name', 'group', indices)

def get_component_type_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'component_type', 'group', indices)

def get_chain_index_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_index_from_small(item, 'chain_index', 'group', indices)

def get_chain_id_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'chain_id', 'group', indices)

def get_chain_name_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'chain_name', 'group', indices)

def get_chain_type_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'chain_type', 'group', indices)

def get_molecule_index_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_index_from_small(item, 'molecule_index', 'group', indices)

def get_molecule_id_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'molecule_id', 'group', indices)

def get_molecule_name_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'molecule_name', 'group', indices)

def get_molecule_type_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'molecule_type', 'group', indices)

def get_entity_index_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_index_from_small(item, 'entity_index', 'group', indices)

def get_entity_id_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'entity_id', 'group', indices)

def get_entity_name_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'entity_name', 'group', indices)

def get_entity_type_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'entity_type', 'group', indices)

def get_n_atoms_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_atoms', 'group', indices)

def get_n_groups_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n(item, 'group', indices)

def get_n_components_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_components', 'group', indices)

def get_n_molecules_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_molecules', 'group', indices)

def get_n_chains_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_chains', 'group', indices)

def get_n_entities_from_group (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_entities', 'group', indices)

## component

def get_atom_index_from_component(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'atom_index', 'component', indices)

def get_atom_id_from_component(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_id', 'component', indices)

def get_atom_name_from_component(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_name', 'component', indices)

def get_atom_type_from_component(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_type', 'component', indices)

def get_group_index_from_component(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'group_index', 'component', indices)

def get_group_id_from_component(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'group_id', 'component', indices)

def get_group_name_from_component(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'group_name', 'component', indices)

def get_group_type_from_component(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'group_type', 'component', indices)

def get_component_index_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_index(item, 'component', indices)

#def get_component_id_from_component (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'id', 'component', indices)
#
#def get_component_name_from_component (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'name', 'component', indices)
#
#def get_component_type_from_component (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'type', 'component', indices)

def get_chain_index_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_index_from_small(item, 'chain_index', 'component', indices)

def get_chain_id_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'chain_id', 'component', indices)

def get_chain_name_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'chain_name', 'component', indices)

def get_chain_type_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'chain_type', 'component', indices)

def get_molecule_index_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_index_from_small(item, 'molecule_index', 'component', indices)

def get_molecule_id_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'molecule_id', 'component', indices)

def get_molecule_name_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'molecule_name', 'component', indices)

def get_molecule_type_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'molecule_type', 'component', indices)

def get_entity_index_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_index_from_small(item, 'entity_index', 'component', indices)

def get_entity_id_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'entity_id', 'component', indices)

def get_entity_name_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'entity_name', 'component', indices)

def get_entity_type_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'entity_type', 'component', indices)

def get_n_atoms_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_atoms', 'component', indices)

def get_n_groups_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_groups', 'component', indices)

def get_n_components_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n(item, 'component', indices)

def get_n_molecules_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_molecules', 'component', indices)

def get_n_chains_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_chains', 'component', indices)

def get_n_entities_from_component (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_entities', 'component', indices)

## molecule

def get_atom_index_from_molecule(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'atom_index', 'molecule', indices)

def get_atom_id_from_molecule(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_id', 'molecule', indices)

def get_atom_name_from_molecule(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_name', 'molecule', indices)

def get_atom_type_from_molecule(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_type', 'molecule', indices)

def get_group_index_from_molecule(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'group_index', 'molecule', indices)

def get_group_id_from_molecule(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'group_id', 'molecule', indices)

def get_group_name_from_molecule(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'group_name', 'molecule', indices)

def get_group_type_from_molecule(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'group_type', 'molecule', indices)

def get_component_index_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'component_index', 'molecule', indices)

def get_component_id_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'component_id', 'molecule', indices)

def get_component_name_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'component_name', 'molecule', indices)

def get_component_type_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'component_type', 'molecule', indices)

def get_chain_index_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux2_getter_small_index_from_big(item, 'chain_index', 'molecule', indices)

def get_chain_id_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'chain_id', 'molecule', indices)

def get_chain_name_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'chain_name', 'molecule', indices)

def get_chain_type_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'chain_type', 'molecule', indices)

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_index(item, 'molecule', indices)

#def get_molecule_id_from_molecule (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'id', 'molecule', indices)
#
#def get_molecule_name_from_molecule (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'name', 'molecule', indices)
#
#def get_molecule_type_from_molecule (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'type', 'molecule', indices)

def get_entity_index_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_index_from_small(item, 'entity_index', 'molecule', indices)

def get_entity_id_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'entity_id', 'molecule', indices)

def get_entity_name_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'entity_name', 'molecule', indices)

def get_entity_type_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_big_attribute_from_small(item, 'entity_type', 'molecule', indices)

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_atoms', 'molecule', indices)

def get_n_groups_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_groups', 'molecule', indices)

def get_n_components_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_components', 'molecule', indices)

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n(item, 'molecule', indices)

def get_n_chains_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_chains', 'molecule', indices)

def get_n_entities_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_entities', 'molecule', indices)

## chain

def get_atom_index_from_chain(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'atom_index', 'chain', indices)

def get_atom_id_from_chain(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_id', 'chain', indices)

def get_atom_name_from_chain(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_name', 'chain', indices)

def get_atom_type_from_chain(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_type', 'chain', indices)

def get_group_index_from_chain(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'group_index', 'chain', indices)

def get_group_id_from_chain(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'group_id', 'chain', indices)

def get_group_name_from_chain(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'group_name', 'chain', indices)

def get_group_type_from_chain(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'group_type', 'chain', indices)

def get_component_index_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'component_index', 'chain', indices)

def get_component_id_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'component_id', 'chain', indices)

def get_component_name_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'component_name', 'chain', indices)

def get_component_type_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'component_type', 'chain', indices)

def get_chain_index_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_index(item, 'chain', indices)

#def get_chain_id_from_chain (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'id', 'chain', indices)
#
#def get_chain_name_from_chain (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'name', 'chain', indices)
#
#def get_chain_type_from_chain (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'type', 'chain', indices)

def get_molecule_index_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux2_getter_small_index_from_big(item, 'molecule_index', 'chain', indices)

def get_molecule_id_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'molecule_id', 'chain', indices)

def get_molecule_name_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'molecule_name', 'chain', indices)

def get_molecule_type_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'molecule_type', 'chain', indices)

def get_entity_index_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux2_getter_small_index_from_big(item, 'entity_index', 'chain', indices)

def get_entity_id_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'entity_id', 'chain', indices)

def get_entity_name_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'entity_name', 'chain', indices)

def get_entity_type_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'entity_type', 'chain', indices)

def get_n_atoms_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_atoms', 'chain', indices)

def get_n_groups_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_groups', 'chain', indices)

def get_n_components_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_components', 'chain', indices)

def get_n_molecules_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_molecules', 'chain', indices)

def get_n_chains_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n(item, 'chain', indices)

def get_n_entities_from_chain (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_big_from_small(item, 'n_entities', 'chain', indices)

## entity

def get_atom_index_from_entity(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'atom_index', 'entity', indices)

def get_atom_id_from_entity(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_id', 'entity', indices)

def get_atom_name_from_entity(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_name', 'entity', indices)

def get_atom_type_from_entity(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'atom_type', 'entity', indices)

def get_group_index_from_entity(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'group_index', 'entity', indices)

def get_group_id_from_entity(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'group_id', 'entity', indices)

def get_group_name_from_entity(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'group_name', 'entity', indices)

def get_group_type_from_entity(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'group_type', 'entity', indices)

def get_component_index_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'component_index', 'entity', indices)

def get_component_id_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'component_id', 'entity', indices)

def get_component_name_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'component_name', 'entity', indices)

def get_component_type_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'component_type', 'entity', indices)

def get_chain_index_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux2_getter_small_index_from_big(item, 'chain_index', 'entity', indices)

def get_chain_id_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'chain_id', 'entity', indices)

def get_chain_name_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'chain_name', 'entity', indices)

def get_chain_type_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'chain_type', 'entity', indices)

def get_molecule_index_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_index_from_big(item, 'molecule_index', 'entity', indices)

def get_molecule_id_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'molecule_id', 'entity', indices)

def get_molecule_name_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'molecule_name', 'entity', indices)

def get_molecule_type_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_small_attribute_from_big(item, 'molecule_type', 'entity', indices)

def get_entity_index_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_index(item, 'entity', indices)

#def get_entity_id_from_entity (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'id', 'entity', indices)
#
#def get_entity_name_from_entity (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'name', 'entity', indices)
#
#def get_entity_type_from_entity (item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'type', 'entity', indices)

def get_n_atoms_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_atoms', 'entity', indices)

def get_n_groups_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_groups', 'entity', indices)

def get_n_components_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_components', 'entity', indices)

def get_n_molecules_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_molecules', 'entity', indices)

def get_n_chains_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n_small_from_big(item, 'n_chains', 'entity', indices)

def get_n_entities_from_entity (item, indices='all', frame_indices='all', check_form=True):

    return _aux_n(item, 'entity', indices)

## system

#def get_bonded_atoms_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_atoms_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_groups_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_components_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_chains_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_molecules_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_entities_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_bonds_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get

    group_types = get(item, target='group', indices='all', group_type=True)
    return (group_types=='aminoacid').sum()

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get

    group_types = get(item, target='group', indices='all', group_type=True)
    return (group_types=='nucleotide').sum()

def get_n_ions_from_system (item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='ion').sum()

def get_n_waters_from_system (item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True, check_form=True)
    return (molecule_types=='water').sum()

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True, check_form=True)
    return (molecule_types=='cosolute').sum()

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='small molecule').sum()

def get_n_peptides_from_system (item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='peptide').sum()

def get_n_proteins_from_system (item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='protein').sum()

def get_n_dnas_from_system (item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='dna').sum()

def get_n_rnas_from_system (item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='rna').sum()

def get_n_lipids_from_system (item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='lipid').sum()

def get_coordinates_from_system(item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get
    return get(item, target='atom', frame_indices=frame_indices)

#def get_box_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_box_shape_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_box_lengths_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_box_angles_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_time_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_step_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

def get_frame_from_system(item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get
    return get(item, target='atom', frame_indices=frame_indices, frame=True)

#def get_n_frames_from_system(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get
    return get(item, target='atoms', indices='all', bonded_atoms=True)

def get_bond_index_from_system(item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get
    return get(item, target='atoms', indices='all', bond_index=True)

def get_inner_bonded_atoms_from_system(item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get
    return get(item, target='bond', indices='all', atom_index=True)

def get_inner_bond_index_from_system(item, indices='all', frame_indices='all', check_form=True):

    from molsysmt.basic import get
    return get(item, target='bond', indices='all', bond_index=True)

## bond

def get_bond_index_from_bond(item, indices='all', frame_indices='all', check_form=True):

    return _aux_getter_index(item, 'bond', indices)

#def get_bond_order_from_bond(item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'order', 'bond', indices)
#
#def get_bond_type_from_bond(item, indices='all', frame_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'type', 'bond', indices)

#def get_bond_order_from_bond(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_bond_type_from_bond(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_atom_index_from_bond(item, indices='all', frame_indices='all', check_form=True):
#
#    raise NotImplementedError

def get_n_bonds_from_bond(item, indices='all', frame_indices='all', check_form=True):

    return _aux_n(item, 'bond', indices)

