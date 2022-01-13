from molsysmt.tools.common.get import *

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
        output = item.atoms_dataframe['atom_index'].to_numpy()
    else:
        output = indices
    return output

def get_atom_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['atom_id'][tmp_indices].to_numpy()
    return output

def get_atom_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['atom_name'][tmp_indices].to_numpy()
    return output

def get_atom_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['atom_type'][tmp_indices].to_numpy()
    return output

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['group_index'][tmp_indices].to_numpy()
    return output

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['group_id'][tmp_indices].to_numpy()
    return output

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['group_name'][tmp_indices].to_numpy()
    return output

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['group_type'][tmp_indices].to_numpy()
    return output

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['component_index'][tmp_indices].to_numpy()
    return output

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['component_id'][tmp_indices].to_numpy()
    return output

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['component_name'][tmp_indices].to_numpy()
    return output

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['component_type'][tmp_indices].to_numpy()
    return output

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['chain_index'][tmp_indices].to_numpy()
    return output

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['chain_id'][tmp_indices].to_numpy()
    return output

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['chain_name'][tmp_indices].to_numpy()
    return output

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['chain_type'][tmp_indices].to_numpy()
    return output

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['molecule_index'][tmp_indices].to_numpy()
    return output

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['molecule_id'][tmp_indices].to_numpy()
    return output

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['molecule_name'][tmp_indices].to_numpy()
    return output

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['molecule_type'][tmp_indices].to_numpy()
    return output

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['entity_index'][tmp_indices].to_numpy()
    return output

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['entity_id'][tmp_indices].to_numpy()
    return output

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['entity_name'][tmp_indices].to_numpy()
    return output

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = item.atoms_dataframe['entity_type'][tmp_indices].to_numpy()
    return output

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system (item)
    else:
        return indices.shape[0]

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_groups_from_system (item)
    else:
        output = get_group_index_from_atom (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_components_from_system (item)
    else:
        output = get_component_index_from_atom (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_molecules_from_system (item)
    else:
        output = get_molecule_index_from_atom (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        output = get_chain_index_from_atom (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        output = get_entity_index_from_atom (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    output = None

    from networkx import Graph

    G = Graph()
    edges = get_atom_index_from_bond(item)
    G.add_edges_from(edges)

    if indices is 'all':

        indices = get_atom_index_from_atom(item)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n for n in G[ii]]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    del(Graph, G, edges)

    return output

def get_bond_index_from_atom (item, indices='all', frame_indices='all'):

    output = None

    from networkx import Graph

    G = Graph()
    edges = get_atom_index_from_bond(item)
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

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):

    output = None

    from networkx import Graph

    G = Graph()
    edges = get_atom_index_from_bond(item)
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

def get_inner_bond_index_from_atom (item, indices='all', frame_indices='all'):

    output = None

    if indices is 'all':
        output = get_bond_index_from_bond(item)
    else:
        aux_list = list(indices)
        output = item.bonds_dataframe.query('atom1_index==@aux_list and atom2_index==@aux_list').index.to_numpy(dtype=int, copy=True)

    return output

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':

        output = get_atom_index_from_bond(item, indices='all')

    else:

        bond_indices = get_inner_bond_index_from_atom (item, indices=indices)
        output = get_atom_index_from_bond(item, indices=bond_indices)
        del(bond_indices)

    return(output)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    bond_indices = get_inner_bond_index_from_atom(item, indices=indices)
    output = bond_indices.shape[0]
    del(bond_indices)
    return(output)

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
        mask = (item.atoms_dataframe['group_index']==ii)
        output.append(item.atoms_dataframe['atom_index'][mask].to_numpy())
    output = np.array(output, dtype=object)
    return output

def get_atom_id_from_group (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_group(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output)
    return output

def get_atom_name_from_group (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_group(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output, dtype=object)
    return output

def get_atom_type_from_group (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_group(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output, dtype=object)
    return output

def get_group_index_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item.atoms_dataframe['group_index'].unique()
    else:
        output = indices
    return output

def get_group_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['group_id'][right_locs].to_numpy()
    return output

def get_group_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['group_name'][right_locs].to_numpy()
    return output

def get_group_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['group_type'][right_locs].to_numpy()
    return output

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_index'][right_locs].to_numpy()
    return output

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_id'][right_locs].to_numpy()
    return output

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_name'][right_locs].to_numpy()
    return output

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_type'][right_locs].to_numpy()
    return output

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_index'][right_locs].to_numpy()
    return output

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_id'][right_locs].to_numpy()
    return output

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_name'][right_locs].to_numpy()
    return output

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_type'][right_locs].to_numpy()
    return output

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_index'][right_locs].to_numpy()
    return output

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_id'][right_locs].to_numpy()
    return output

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_name'][right_locs].to_numpy()
    return output

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_type'][right_locs].to_numpy()
    return output

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_index'][right_locs].to_numpy()
    return output

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_id'][right_locs].to_numpy()
    return output

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_name'][right_locs].to_numpy()
    return output

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    tmp_indices = get_group_index_from_group(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_groups_from_system (item)
    else:
        output = get_group_index_from_group (item, indices=indices, frame_indices=frame_indices)
        return output.shape[0]

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_components_from_system (item)
    else:
        output = get_component_index_from_group (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_molecules_from_system (item)
    else:
        output = get_molecule_index_from_group (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        output = get_chain_index_from_group (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        output = get_entity_index_from_group (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

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
        mask = (item.atoms_dataframe['component_index']==ii)
        output.append(item.atoms_dataframe['atom_index'][mask].to_numpy())
    output = np.array(output, dtype=object)
    return output

def get_atom_id_from_component (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output, dtype=object)
    return output

def get_atom_name_from_component (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output, dtype=object)
    return output

def get_atom_type_from_component (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output, dtype=object)
    return output

def get_group_index_from_component (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['component_index']==ii)
        output.append(item.atoms_dataframe['group_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_group_id_from_component (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output, dtype=object)
    return output

def get_group_name_from_component (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output, dtype=object)
    return output

def get_group_type_from_component (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output, dtype=object)
    return output

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item.atoms_dataframe['component_index'].unique()
    else:
        output = indices
    return output

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_id'][right_locs].to_numpy()
    return output

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_name'][right_locs].to_numpy()
    return output

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_type'][right_locs].to_numpy()
    return output

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_index'][right_locs].to_numpy()
    return output

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_id'][right_locs].to_numpy()
    return output

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_name'][right_locs].to_numpy()
    return output

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_type'][right_locs].to_numpy()
    return output

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_index'][right_locs].to_numpy()
    return output

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_id'][right_locs].to_numpy()
    return output

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_name'][right_locs].to_numpy()
    return output

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_type'][right_locs].to_numpy()
    return output

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_index'][right_locs].to_numpy()
    return output

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_id'][right_locs].to_numpy()
    return output

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_name'][right_locs].to_numpy()
    return output

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    tmp_indices = get_component_index_from_component(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_type'][right_locs].to_numpy()
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

    if indices is 'all':
        return get_n_components_from_system (item)
    else:
        output = get_component_index_from_component (item, indices=indices, frame_indices=frame_indices)
        return output.shape[0]

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_molecules_from_system (item)
    else:
        output = get_molecule_index_from_component (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        output = get_chain_index_from_component (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        output = get_entity_index_from_component (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

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
        mask = (item.atoms_dataframe['molecule_index']==ii)
        output.append(item.atoms_dataframe['atom_index'][mask].to_numpy())
    output = np.array(output, dtype=object)
    return output

def get_atom_id_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output)
    return output

def get_atom_name_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output)
    return output

def get_atom_type_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output)
    return output

def get_group_index_from_molecule (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['molecule_index']==ii)
        output.append(item.atoms_dataframe['group_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_group_id_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output, dtype=object)
    return output

def get_group_name_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output, dtype=object)
    return output

def get_group_type_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output, dtype=object)
    return output

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['molecule_index']==ii)
        output.append(item.atoms_dataframe['component_index'][mask].unique())
    output = np.array(output)
    return output


def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_id_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output)
    return output

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_name_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output)
    return output

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_type_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output)
    return output

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    output = []
    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['molecule_index']==ii)
        output.append(item.atoms_dataframe['chain_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_id_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output)
    return output


def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_name_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output)
    return output

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_type_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = np.array(output)
    return output

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = item.atoms_dataframe['molecule_index'].unique()
    else:
        output = indices
    return output

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_id'][right_locs].to_numpy()
    return output

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_name'][right_locs].to_numpy()
    return output

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    all_indices = item.atoms_dataframe['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_type'][right_locs].to_numpy()
    return output


