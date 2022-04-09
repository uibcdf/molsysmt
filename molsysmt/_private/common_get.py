## From atom

def get_atom_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_aux = get_n_atoms_from_system(item, check=False)
        output = _np.arange(n_aux, dtype=int)
    else:
        output = _np.array(indices, dtype=int)

    return output

def get_group_id_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_group_name_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_group_type_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_component_id_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_component_name_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_component_type_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_id_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_name_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_type_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_id_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_name_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_type_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_id_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_name_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_type_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_n_atoms_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_atoms_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

def get_n_groups_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_groups_from_system(item, check=False)
    else:
        output = get_group_index_from_atom(item, indices=indices, check=True)
        output = _np.unique(output).shape[0]

    return output

def get_n_components_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_components_from_system(item, check=False)
    else:
        output = get_component_index_from_atom(item, indices=indices, check=True)
        output = _np.unique(output).shape[0]

    return output

def get_n_molecules_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_molecules_from_system(item, check=False)
    else:
        output = get_molecule_index_from_atom(item, indices=indices, check=True)
        output = _np.unique(output).shape[0]

    return output

def get_n_chains_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_chains_from_system(item, check=False)
    else:
        output = get_chain_index_from_atom(item, indices=indices, check=True)
        output = _np.unique(output).shape[0]

    return output

def get_n_entities_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_entities_from_system(item, check=False)
    else:
        output = get_entity_index_from_atom(item, indices=indices, check=True)
        output = _np.unique(output).shape[0]

    return output

def get_bonded_atoms_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = None

    G = _Graph()
    edges = get_atom_index_from_bond(item, check=False)
    G.add_edges_from(edges)

    if indices is 'all':

        indices = get_atom_index_from_atom(item, check=False)

    output = []

    for ii in indices:
        if ii in G:
            output.append(_np.array([n for n in G[ii]]))
        else:
            output.append(_np.array([]))

    output = _np.array(output, dtype=object)

    del(G, edges)

    return output

def get_bond_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = None

    G = _Graph()
    edges = get_atom_index_from_bond(item, check=False)
    n_bonds = edges.shape[0]
    edge_indices = _np.array([{'index':ii} for ii in range(n_bonds)]).reshape([n_bonds,1])
    G.add_edges_from(_np.hstack([edges, edge_indices]))

    if indices is 'all':

        indices = get_atom_index_from_atom(item, check=False)

    output = []

    for ii in indices:
        if ii in G:
            output.append(_np.array([n['index'] for n in G[ii].values()]))
        else:
            output.append(_np.array([]))

    output = _np.array(output, dtype=object)

    del(G, edges, edge_indices)

    return output

def get_n_bonds_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = None

    G = _Graph()
    edges = get_atom_index_from_bond(item, check=False)
    G.add_edges_from(edges)

    if indices is 'all':

        indices = get_atom_index_from_atom(item, check=False)

    output = []

    for ii in indices:
        if ii in G:
            output.append(len(G[ii]))
        else:
            output.append(0)

    output = _np.array(output)

    del(G, edges)

    return output

def get_inner_bond_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise _NotImplementedMethodError


## From group

def get_atom_index_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_group_index_from_group(item, indices=indices, check=False)
    attribute_from_atom = get_atom_index_from_atom(item, check=False)
    target_index_from_atom = get_group_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_atom_id_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_group(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_group(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_group(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_aux = get_n_groups_from_system(item, check=False)
        output = _np.arange(n_aux, dtype=int)
    else:
        output = _np.array(indices, dtype=int)

    return output

def get_component_index_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, check=False)
    first_atom_index_from_target = _np.array([ii[0] for ii in atom_index_from_target])
    output = get_component_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_component_id_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_component_name_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_component_type_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_chain_index_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, check=False)
    first_atom_index_from_target = _np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_chain_id_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_chain_name_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_chain_type_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_molecule_index_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, check=False)
    first_atom_index_from_target = _np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_molecule_id_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_molecule_name_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_molecule_type_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_entity_index_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, check=False)
    first_atom_index_from_target = _np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_entity_id_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_entity_name_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_entity_type_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_n_atoms_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_atom_index_from_group(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_groups_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_groups_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

def get_n_components_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        return get_n_components_from_system(item, check=False)
    else:
        output = get_component_index_from_group(item, indices=indices, check=False)
        output = _np.unique(output).shape[0]

    return output

def get_n_molecules_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        return get_n_molecules_from_system(item, check=False)
    else:
        output = get_molecule_index_from_group(item, indices=indices, check=False)
        output = _np.unique(output).shape[0]

    return output

def get_n_chains_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        return get_n_chains_from_system(item, check=False)
    else:
        output = get_chain_index_from_group(item, indices=indices, check=False)
        output = _np.unique(output).shape[0]

    return output

def get_n_entities_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        return get_n_entities_from_system(item, check=False)
    else:
        output = get_entity_index_from_group(item, indices=indices, check=False)
        output = _np.unique(output).shape[0]

    return output


## From component

def get_atom_index_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_component_index_from_component(item, indices=indices, check=False)
    attribute_from_atom = get_atom_index_from_atom(item, check=False)
    target_index_from_atom = get_component_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_atom_id_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_component(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_component(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_component(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_component_index_from_component(item, indices=indices, check=False)
    attribute_from_atom = get_group_index_from_atom(item, check=False)
    target_index_from_atom = get_component_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_group_id_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_component(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_name_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_component(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_type_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_component(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_index_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_aux = get_n_components_from_system(item, check=False)
        output = _np.arange(n_aux, dtype=int)
    else:
        output = _np.array(indices, dtype=int)

    return output

def get_chain_index_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, check=False)
    first_atom_index_from_target = _np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_chain_id_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_name_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_type_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_index_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, check=False)
    first_atom_index_from_target = _np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_molecule_id_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_name_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_type_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_index_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, check=False)
    first_atom_index_from_target = _np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_entity_id_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_name_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_type_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_n_atoms_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_atom_index_from_component(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_groups_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_group_index_from_component(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_components_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_components_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

def get_n_molecules_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_molecules_from_system(item, check=False)
    else:
        output = get_molecule_index_from_component(item, indices=indices, check=True)
        output = _np.unique(output).shape[0]

    return output

def get_n_chains_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_chains_from_system(item, check=False)
    else:
        output = get_chain_index_from_component(item, indices=indices, check=True)
        output = _np.unique(output).shape[0]

    return output

def get_n_entities_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_entities_from_system(item, check=False)
    else:
        output = get_entity_index_from_component(item, indices=indices, check=True)
        output = _np.unique(output).shape[0]

    return output

## molecule

def get_atom_index_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_molecule_index_from_molecule(item, indices=indices, check=False)
    attribute_from_atom = get_atom_index_from_atom(item, check=False)
    target_index_from_atom = get_molecule_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_atom_id_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_molecule_index_from_molecule(item, indices=indices, check=False)
    attribute_from_atom = get_group_index_from_atom(item, check=False)
    target_index_from_atom = get_molecule_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_group_id_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_name_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_type_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_index_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_molecule_index_from_molecule(item, indices=indices, check=False)
    attribute_from_atom = get_component_index_from_atom(item, check=False)
    target_index_from_atom = get_molecule_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_component_id_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_name_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_type_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_index_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_atom_indices = get_atom_index_from_molecule(item, indices=indices, check=False)
    aux_indices = get_molecule_index_from_atom(item, check=False)
    aux_vals = get_chain_index_from_atom(item, check=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(_np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_chain_id_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_name_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_type_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_index_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_aux = get_n_molecules_from_system(item, check=False)
        output = _np.arange(n_aux, dtype=int)
    else:
        output = _np.array(indices, dtype=int)

    return output

def get_entity_index_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    atom_index_from_target = get_atom_index_from_molecule(item, indices=indices, check=False)
    first_atom_index_from_target = _np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_entity_id_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_molecule(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_name_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_molecule(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_type_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_molecule(item, indices=indices, check=False)
    aux_unique_indices = _np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = _np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_n_atoms_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_atom_index_from_molecule(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_groups_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_group_index_from_molecule(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_components_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_component_index_from_molecule(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_molecules_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_molecules_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

def get_n_chains_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_chain_index_from_molecule(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_entities_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_entities_from_system(item, check=False)
    else:
        output = get_entity_index_from_molecule(item, indices=indices, check=True)
        output = _np.unique(output).shape[0]

    return output

## chain

def get_atom_index_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_chain_index_from_chain(item, indices=indices, check=False)
    attribute_from_atom = get_atom_index_from_atom(item, check=False)
    target_index_from_atom = get_chain_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_atom_id_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_chain_index_from_chain(item, indices=indices, check=False)
    attribute_from_atom = get_group_index_from_atom(item, check=False)
    target_index_from_atom = get_chain_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_group_id_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_name_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_type_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_index_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_chain_index_from_chain(item, indices=indices, check=False)
    attribute_from_atom = get_component_index_from_atom(item, check=False)
    target_index_from_atom = get_chain_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_component_id_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_name_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_type_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_index_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_aux = get_n_chains_from_system(item, check=False)
        output = _np.arange(n_aux, dtype=int)
    else:
        output = _np.array(indices, dtype=int)

    return output

def get_molecule_index_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, check=False)
    aux_indices = get_chain_index_from_atom(item, check=False)
    aux_vals = get_molecule_index_from_atom(item, check=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(_np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_molecule_id_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_name_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_type_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_entity_index_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, check=False)
    aux_indices = get_chain_index_from_atom(item, check=False)
    aux_vals = get_entity_index_from_atom(item, check=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(_np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_entity_id_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_entity_name_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_entity_type_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_entity_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_n_atoms_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_atom_index_from_chain(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_groups_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_group_index_from_chain(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_components_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_component_index_from_chain(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_molecules_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_molecule_index_from_chain(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_chains_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_chains_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

def get_n_entities_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_entities_from_system(item, check=False)
    else:
        output = get_entity_index_from_chain(item, indices=indices, check=True)
        output = _np.unique(output).shape[0]

    return output

## From entity

def get_atom_index_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_entity_index_from_entity(item, indices=indices, check=False)
    attribute_from_atom = get_atom_index_from_atom(item, check=False)
    target_index_from_atom = get_entity_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_atom_id_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_atom_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_entity_index_from_entity(item, indices=indices, check=False)
    attribute_from_atom = get_group_index_from_atom(item, check=False)
    target_index_from_atom = get_entity_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_group_id_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_name_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_type_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_group_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_index_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_entity_index_from_entity(item, indices=indices, check=False)
    attribute_from_atom = get_component_index_from_atom(item, check=False)
    target_index_from_atom = get_entity_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_component_id_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_name_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_type_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_component_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_index_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices, check=False)
    aux_indices = get_entity_index_from_atom(item, check=False)
    aux_vals = get_chain_index_from_atom(item, check=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(_np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_chain_id_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_name_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_type_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_chain_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_index_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    indices_aux = get_entity_index_from_entity(item, indices=indices, check=False)
    attribute_from_atom = get_molecule_index_from_atom(item, check=False)
    target_index_from_atom = get_entity_index_from_atom(item, check=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(_np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = _np.array(output)
    else:
        output = _np.array(output, dtype=object)

    return output

def get_molecule_id_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_name_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_type_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    aux_indices = get_molecule_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = _np.unique(_np.concatenate(aux_indices))
        aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = _np.vectorize(aux_dict.__getitem__)
        output = _np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = _np.array([], dtype=object)

    del(aux_indices)

    return output

def get_entity_index_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_aux = get_n_entities_from_system(item, check=False)
        output = _np.arange(n_aux, dtype=int)
    else:
        output = _np.array(indices, dtype=int)

    return output

def get_n_atoms_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_atom_index_from_entity(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_groups_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_group_index_from_entity(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_components_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_component_index_from_entity(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_molecules_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_molecule_index_from_entity(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_chains_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_chain_index_from_entity(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = _np.array(output)
    return output

def get_n_entities_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_entities_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

## system

def get_n_aminoacids_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    group_types = get_group_type_from_group(item, check=False)
    return (group_types=='aminoacid').sum()

def get_n_nucleotides_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    group_types = get_group_type_from_group(item, check=False)
    return (group_types=='nucleotide').sum()

def get_n_ions_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    molecule_types = get_group_type_from_group(item, check=False)
    return (molecule_types=='ion').sum()

def get_n_waters_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    molecule_types = get_group_type_from_group(item, check=False)
    return (molecule_types=='water').sum()

def get_n_cosolutes_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    molecule_types = get_group_type_from_group(item, check=False)
    return (molecule_types=='cosolute').sum()

def get_n_small_molecules_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    molecule_types = get_group_type_from_group(item, check=False)
    return (molecule_types=='small molecule').sum()

def get_n_peptides_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    molecule_types = get_molecule_type_from_molecule(item, check=False)
    return (molecule_types=='peptide').sum()

def get_n_proteins_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    molecule_types = get_molecule_type_from_molecule(item, check=False)
    return (molecule_types=='protein').sum()

def get_n_dnas_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    molecule_types = get_molecule_type_from_molecule(item, check=False)
    return (molecule_types=='dna').sum()

def get_n_rnas_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    molecule_types = get_molecule_type_from_molecule(item, check=False)
    return (molecule_types=='rna').sum()

def get_n_lipids_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    molecule_types = get_molecule_type_from_molecule(item, check=False)
    return (molecule_types=='lipid').sum()

def get_coordinates_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    return get_coordinates_from_atom(item, structure_indices=structure_indices, check=False)

def get_box_shape_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    from molsysmt.pbc import box_shape_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    output = box_shape_from_box_vectors(tmp_box, check=False)

    return output

def get_box_lengths_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    from molsysmt.pbc import box_lengths_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    output = box_lengths_from_box_vectors(tmp_box, check=False)

    return output

def get_box_angles_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    from molsysmt.pbc import box_angles_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    output = box_angles_from_box_vectors(tmp_box, check=False)

    return output

def get_box_volume_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    from molsysmt.pbc import box_volume_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    if tmp_box is None:
        output=None
    else:
        output = box_volume_from_box_vectors(tmp_box, check=False)

    return output

def get_bonded_atoms_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return get_bonded_atoms_from_atom(item, check=False)

def get_bond_index_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return get_bond_index_from_atom(item, check=False)

def get_inner_bonded_atoms_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return get_inner_bonded_atoms_from_atom(item, check=False)

def get_inner_bond_index_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return get_inner_bond_index_from_atom(item, check=False)

## bond

def get_bond_index_from_bond(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_aux = get_n_bonds_from_system(item, check=False)
        output = _np.arange(n_aux, dtype=int)
    else:
        output = _np.array(indices, dtype=int)

    return output

def get_n_bonds_from_bond(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        output = get_n_bonds_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

