from .is_molsysmt_Topology import is_molsysmt_Topology
from molsysmt._private_tools.exceptions import WrongFormError, WrongIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.indices import digest_indices
from molsysmt._private_tools.structure_indices import digest_structure_indices
import numpy as np
from networkx import Graph

## From atom

def get_atom_index_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = item.atoms_dataframe['atom_index'].to_numpy()
    else:
        output = indices
    return output

def get_atom_id_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['atom_id'][tmp_indices].to_numpy()
    return output

def get_atom_name_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['atom_name'][tmp_indices].to_numpy()
    return output

def get_atom_type_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['atom_type'][tmp_indices].to_numpy()
    return output

def get_group_index_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['group_index'][tmp_indices].to_numpy()
    return output

def get_group_id_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['group_id'][tmp_indices].to_numpy()
    return output

def get_group_name_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['group_name'][tmp_indices].to_numpy()
    return output

def get_group_type_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['group_type'][tmp_indices].to_numpy()
    return output

def get_component_index_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['component_index'][tmp_indices].to_numpy()
    return output

def get_component_id_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['component_id'][tmp_indices].to_numpy()
    return output

def get_component_name_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['component_name'][tmp_indices].to_numpy()
    return output

def get_component_type_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['component_type'][tmp_indices].to_numpy()
    return output

def get_chain_index_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['chain_index'][tmp_indices].to_numpy()
    return output

def get_chain_id_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['chain_id'][tmp_indices].to_numpy()
    return output

def get_chain_name_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['chain_name'][tmp_indices].to_numpy()
    return output

def get_chain_type_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['chain_type'][tmp_indices].to_numpy()
    return output

def get_molecule_index_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['molecule_index'][tmp_indices].to_numpy()
    return output

def get_molecule_id_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['molecule_id'][tmp_indices].to_numpy()
    return output

def get_molecule_name_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['molecule_name'][tmp_indices].to_numpy()
    return output

def get_molecule_type_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['molecule_type'][tmp_indices].to_numpy()
    return output

def get_entity_index_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['entity_index'][tmp_indices].to_numpy()
    return output

def get_entity_id_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices, check=False)
    output = item.atoms_dataframe['entity_id'][tmp_indices].to_numpy()
    return output

def get_entity_name_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['entity_name'][tmp_indices].to_numpy()
    return output

def get_entity_type_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    output = item.atoms_dataframe['entity_type'][tmp_indices].to_numpy()
    return output

def get_n_atoms_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_atoms_from_system(item, check=False)
    else:
        return indices.shape[0]

def get_n_groups_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_groups_from_system (item, check=False)
    else:
        output = get_group_index_from_atom (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

def get_n_components_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_components_from_system (item, check=False)
    else:
        output = get_component_index_from_atom (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

def get_n_molecules_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_molecules_from_system (item, check=False)
    else:
        output = get_molecule_index_from_atom (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

def get_n_chains_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_chains_from_system (item, check=False)
    else:
        output = get_chain_index_from_atom (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

def get_n_entities_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_entities_from_system (item, check=False)
    else:
        output = get_entity_index_from_atom (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

def get_bonded_atoms_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = None

    G = Graph()
    edges = get_atom_index_from_bond(item, check=False)
    G.add_edges_from(edges)

    if indices is 'all':

        indices = get_atom_index_from_atom(item, check=False)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n for n in G[ii]]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    del(Graph, G, edges)

    return output

def get_bond_index_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = None

    G = Graph()
    edges = get_atom_index_from_bond(item, check=False)
    n_bonds = edges.shape[0]
    edge_indices = np.array([{'index':ii} for ii in range(n_bonds)]).reshape([n_bonds,1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if indices is 'all':

        indices = get_atom_index_from_atom(item, check=False)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n['index'] for n in G[ii].values()]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    del(Graph, G, edges, edge_indices)

    return output

def get_n_bonds_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = None

    G = Graph()
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

    output = np.array(output)

    del(Graph, G, edges)

    return output

def get_inner_bond_index_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = None

    if indices is 'all':
        output = get_bond_index_from_bond(item, check=False)
    else:
        aux_list = list(indices)
        output = item.bonds_dataframe.query('atom1_index==@aux_list and atom2_index==@aux_list').index.to_numpy(dtype=int, copy=True)

    return output

def get_inner_bonded_atoms_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':

        output = get_atom_index_from_bond(item, indices='all', check=False)

    else:

        bond_indices = get_inner_bond_index_from_atom (item, indices=indices, check=False)
        output = get_atom_index_from_bond(item, indices=bond_indices, check=False)
        del(bond_indices)

    return(output)

def get_n_inner_bonds_from_atom (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    bond_indices = get_inner_bond_index_from_atom(item, indices=indices, check=False)
    output = bond_indices.shape[0]
    del(bond_indices)
    return(output)

## group

def get_atom_index_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_groups_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['group_index']==ii)
        output.append(item.atoms_dataframe['atom_index'][mask].to_numpy())
    output = np.array(output, dtype=object)
    return output

def get_atom_id_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_group(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_atom_name_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_group(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_atom_type_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_group(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_group_index_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = item.atoms_dataframe['group_index'].unique()
    else:
        output = indices
    return output

def get_group_id_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['group_id'][right_locs].to_numpy()
    return output

def get_group_name_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['group_name'][right_locs].to_numpy()
    return output

def get_group_type_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['group_type'][right_locs].to_numpy()
    return output

def get_component_index_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_index'][right_locs].to_numpy()
    return output

def get_component_id_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_id'][right_locs].to_numpy()
    return output

def get_component_name_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_name'][right_locs].to_numpy()
    return output

def get_component_type_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_type'][right_locs].to_numpy()
    return output

def get_chain_index_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_index'][right_locs].to_numpy()
    return output

def get_chain_id_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_id'][right_locs].to_numpy()
    return output

def get_chain_name_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_name'][right_locs].to_numpy()
    return output

def get_chain_type_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_type'][right_locs].to_numpy()
    return output

def get_molecule_index_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_index'][right_locs].to_numpy()
    return output

def get_molecule_id_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_id'][right_locs].to_numpy()
    return output

def get_molecule_name_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_name'][right_locs].to_numpy()
    return output

def get_molecule_type_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_type'][right_locs].to_numpy()
    return output

def get_entity_index_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_index'][right_locs].to_numpy()
    return output

def get_entity_id_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_id'][right_locs].to_numpy()
    return output

def get_entity_name_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_name'][right_locs].to_numpy()
    return output

def get_entity_type_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_group_index_from_group(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['group_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_atom_index_from_group (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_groups_from_system (item, check=False)
    else:
        output = get_group_index_from_group (item, indices=indices, check=False)
        return output.shape[0]

def get_n_components_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_components_from_system (item, check=False)
    else:
        output = get_component_index_from_group (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

def get_n_molecules_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_molecules_from_system (item, check=False)
    else:
        output = get_molecule_index_from_group (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

def get_n_chains_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_chains_from_system (item, check=False)
    else:
        output = get_chain_index_from_group (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

def get_n_entities_from_group (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_chains_from_system (item, check=False)
    else:
        output = get_entity_index_from_group (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]


## component

def get_atom_index_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_components_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['component_index']==ii)
        output.append(item.atoms_dataframe['atom_index'][mask].to_numpy())
    output = np.array(output, dtype=object)
    return output

def get_atom_id_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_component(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_atom_name_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_component(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_atom_type_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_component(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_group_index_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_components_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['component_index']==ii)
        output.append(item.atoms_dataframe['group_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_group_id_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_group_name_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_group_type_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_component_index_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = item.atoms_dataframe['component_index'].unique()
    else:
        output = indices
    return output

def get_component_id_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_id'][right_locs].to_numpy()
    return output

def get_component_name_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_name'][right_locs].to_numpy()
    return output

def get_component_type_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['component_type'][right_locs].to_numpy()
    return output

def get_chain_index_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_index'][right_locs].to_numpy()
    return output

def get_chain_id_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_id'][right_locs].to_numpy()
    return output

def get_chain_name_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_name'][right_locs].to_numpy()
    return output

def get_chain_type_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_type'][right_locs].to_numpy()
    return output

def get_molecule_index_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_index'][right_locs].to_numpy()
    return output

def get_molecule_id_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_id'][right_locs].to_numpy()
    return output

def get_molecule_name_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_name'][right_locs].to_numpy()
    return output

def get_molecule_type_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_type'][right_locs].to_numpy()
    return output

def get_entity_index_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_index'][right_locs].to_numpy()
    return output

def get_entity_id_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_id'][right_locs].to_numpy()
    return output

def get_entity_name_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_name'][right_locs].to_numpy()
    return output

def get_entity_type_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_component_index_from_component(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['component_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_atom_index_from_component (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_group_index_from_component (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_components_from_system (item, check=False)
    else:
        output = get_component_index_from_component (item, indices=indices, check=False)
        return output.shape[0]

def get_n_molecules_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_molecules_from_system (item, check=False)
    else:
        output = get_molecule_index_from_component (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

def get_n_chains_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_chains_from_system (item, check=False)
    else:
        output = get_chain_index_from_component (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

def get_n_entities_from_component (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_entities_from_system (item, check=False)
    else:
        output = get_entity_index_from_component (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

## molecule

def get_atom_index_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_molecules_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['molecule_index']==ii)
        output.append(item.atoms_dataframe['atom_index'][mask].to_numpy())
    output = np.array(output, dtype=object)
    return output

def get_atom_id_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_atom_name_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_atom_type_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_group_index_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_molecules_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['molecule_index']==ii)
        output.append(item.atoms_dataframe['group_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_group_id_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_group_name_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_group_type_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_component_index_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_molecules_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['molecule_index']==ii)
        output.append(item.atoms_dataframe['component_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_component_id_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_component_id_from_component(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_component_name_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_component_name_from_component(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_component_type_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_component_type_from_component(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_chain_index_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_molecules_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['molecule_index']==ii)
        output.append(item.atoms_dataframe['chain_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_chain_id_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_chain_id_from_chain(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_chain_name_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_chain_name_from_chain(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_chain_type_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_chain_type_from_chain(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_molecule_index_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = item.atoms_dataframe['molecule_index'].unique()
    else:
        output = indices
    return output

def get_molecule_id_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_id'][right_locs].to_numpy()
    return output

def get_molecule_name_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_name'][right_locs].to_numpy()
    return output

def get_molecule_type_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['molecule_type'][right_locs].to_numpy()
    return output

def get_entity_index_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_index'][right_locs].to_numpy()
    return output

def get_entity_id_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_id'][right_locs].to_numpy()
    return output

def get_entity_name_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_name'][right_locs].to_numpy()
    return output

def get_entity_type_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_molecule_index_from_molecule(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['molecule_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_atom_index_from_molecule (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_group_index_from_molecule (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_component_index_from_molecule (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_molecules_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_molecules_from_system (item, check=False)
    else:
        output = get_molecule_index_from_molecule (item, indices=indices, check=False)
        return output.shape[0]

def get_n_chains_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_chain_index_from_molecule (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_entities_from_molecule (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_entities_from_system (item, check=False)
    else:
        output = get_entity_index_from_molecule (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

## chain

def get_atom_index_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['chain_index']==ii)
        output.append(item.atoms_dataframe['atom_index'][mask].to_numpy())
    output = np.array(output, dtype=object)
    return output

def get_atom_id_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_atom_name_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_atom_type_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_group_index_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['chain_index']==ii)
        output.append(item.atoms_dataframe['group_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_group_id_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_group_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_group_name_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_group_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_group_type_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_group_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_component_index_from_chain (item, indices='all', check=True):
    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['chain_index']==ii)
        output.append(item.atoms_dataframe['component_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_component_id_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_component_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_component_id_from_component(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

    if check:
        if not is_molsysmt_Topology(item):
            raise WrongFormError('molsysmt.Topology')

def get_component_name_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_component_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_component_name_from_component(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_component_type_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_component_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_component_type_from_component(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_chain_index_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = item.atoms_dataframe['chain_index'].unique()
    else:
        output = indices
    return output

def get_chain_id_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_chain_index_from_chain(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['chain_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_id'][right_locs].to_numpy()
    return output

def get_chain_name_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_chain_index_from_chain(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['chain_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_name'][right_locs].to_numpy()
    return output

def get_chain_type_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_chain_index_from_chain(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['chain_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['chain_type'][right_locs].to_numpy()
    return output

def get_molecule_index_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['chain_index']==ii)
        output.append(item.atoms_dataframe['molecule_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_molecule_id_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_molecule_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_molecule_id_from_molecule(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_molecule_name_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_molecule_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_molecule_name_from_molecule(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_molecule_type_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_molecule_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_molecule_type_from_molecule(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_entity_index_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['chain_index']==ii)
        output.append(item.atoms_dataframe['entity_index'][mask].unique())
    output = np.array(output)
    return output

def get_entity_id_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_entity_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_entity_id_from_entity(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_entity_name_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_entity_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_entity_name_from_entity(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_entity_type_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_entity_index_from_chain(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_entity_type_from_entity(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_n_atoms_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_atom_index_from_chain (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_group_index_from_chain (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_chain (item, indices='all', check=True):
    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_component_index_from_chain (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_molecules_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_molecule_index_from_chain (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_chains_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        output = get_chain_index_from_chain (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

def get_n_entities_from_chain (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_entities_from_system (item, check=False)
    else:
        output = get_entity_index_from_chain (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

## entity

def get_atom_index_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_entities_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['entity_index']==ii)
        output.append(item.atoms_dataframe['atom_index'][mask].to_numpy())
    output = np.array(output, dtype=object)
    return output

def get_atom_id_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_atom_name_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_atom_type_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_atom_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, structure_indices=structure_indices))
    output = np.array(output, dtype=object)
    return output

def get_group_index_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_entities_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['entity_index']==ii)
        output.append(item.atoms_dataframe['group_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_group_id_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_group_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_group_name_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_group_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_group_type_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_group_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, check=False))
    output = np.array(output, dtype=object)
    return output

def get_component_index_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_entities_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['entity_index']==ii)
        output.append(item.atoms_dataframe['component_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_component_id_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_component_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_component_id_from_component(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_component_name_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_component_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_component_name_from_component(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_component_type_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_component_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_component_type_from_component(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_chain_index_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_entities_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['entity_index']==ii)
        output.append(item.atoms_dataframe['chain_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_chain_id_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_chain_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_chain_id_from_chain(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_chain_name_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_chain_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_chain_name_from_chain(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_chain_type_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_chain_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_chain_type_from_chain(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_molecule_index_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = []
    if indices is 'all':
        n_indices = get_n_entities_from_system(item, check=False)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms_dataframe['entity_index']==ii)
        output.append(item.atoms_dataframe['molecule_index'][mask].unique())
    output = np.array(output, dtype=object)
    return output

def get_molecule_id_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_molecule_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_molecule_id_from_molecule(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_molecule_name_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_molecule_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_molecule_name_from_molecule(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_molecule_type_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]
    tmp_indices = get_molecule_index_from_entity(item, indices=indices, check=False)
    for aux_indices in tmp_indices:
        output.append(get_molecule_type_from_molecule(item, indices=aux_indices, check=False))
    output = np.array(output)
    return output

def get_entity_index_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = item.atoms_dataframe['entity_index'].unique()
    else:
        output = indices
    return output

def get_entity_id_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_entity_index_from_entity(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['entity_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_id'][right_locs].to_numpy()
    return output

def get_entity_name_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_entity_index_from_entity(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['entity_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_name'][right_locs].to_numpy()
    return output

def get_entity_type_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_entity_index_from_entity(item, indices=indices, check=False)
    all_indices = item.atoms_dataframe['entity_index'].to_numpy()
    right_locs = [next((idx for idx, val in np.ndenumerate(all_indices) if val==ii))[0] for ii in tmp_indices]
    output = item.atoms_dataframe['entity_type'][right_locs].to_numpy()
    return output

def get_n_atoms_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_atom_index_from_entity (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_group_index_from_entity (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_component_index_from_entity (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_molecules_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_molecule_index_from_entity (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_chains_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_chain_index_from_entity (item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_entities_from_entity (item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        output = get_entity_index_from_entity (item, indices=indices, check=False)
        output = np.unique(output)
        return output.shape[0]

## system

def get_n_atoms_from_system(item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    return item.atoms_dataframe.shape[0]

def get_n_groups_from_system(item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    output = item.atoms_dataframe['group_index'].unique()
    return output.shape[0]

def get_n_components_from_system(item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    output = item.atoms_dataframe['component_index'].unique()
    indices_not_None = np.where(output!=None)
    output = output[indices_not_None]
    return output.shape[0]

def get_n_chains_from_system(item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    output = item.atoms_dataframe['chain_index'].unique()
    indices_not_None = np.where(output!=None)
    output = output[indices_not_None]
    return output.shape[0]

def get_n_molecules_from_system(item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    output = item.atoms_dataframe['molecule_index'].unique()
    indices_not_None = np.where(output!=None)
    output = output[indices_not_None]
    return output.shape[0]

def get_n_entities_from_system(item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    output = item.atoms_dataframe['entity_index'].unique()
    indices_not_None = np.where(output!=None)
    output = output[indices_not_None]
    return output.shape[0]

def get_n_bonds_from_system(item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    return item.bonds_dataframe.shape[0]

def get_n_aminoacids_from_system (item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    mask=(item.atoms_dataframe['group_type']=='aminoacid').to_numpy()
    serie_indices=item.atoms_dataframe['group_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_nucleotides_from_system (item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    mask=(item.atoms_dataframe['group_type']=='nucleotide').to_numpy()
    serie_indices=item.atoms_dataframe['group_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_ions_from_system (item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    mask=(item.atoms_dataframe['molecule_type']=='ion').to_numpy()
    serie_indices=item.atoms_dataframe['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_waters_from_system (item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    mask=(item.atoms_dataframe['molecule_type']=='water').to_numpy()
    serie_indices=item.atoms_dataframe['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_cosolutes_from_system (item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    mask=(item.atoms_dataframe['molecule_type']=='cosolute').to_numpy()
    serie_indices=item.atoms_dataframe['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_small_molecules_from_system (item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    mask=(item.atoms_dataframe['molecule_type']=='small molecule').to_numpy()
    serie_indices=item.atoms_dataframe['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_peptides_from_system (item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    mask=(item.atoms_dataframe['molecule_type']=='peptide').to_numpy()
    serie_indices=item.atoms_dataframe['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_proteins_from_system (item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    mask=(item.atoms_dataframe['molecule_type']=='protein').to_numpy()
    serie_indices=item.atoms_dataframe['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_dnas_from_system (item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    mask=(item.atoms_dataframe['molecule_type']=='dna').to_numpy()
    serie_indices=item.atoms_dataframe['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_rnas_from_system (item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    mask=(item.atoms_dataframe['molecule_type']=='rna').to_numpy()
    serie_indices=item.atoms_dataframe['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_lipids_from_system (item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    mask=(item.atoms_dataframe['molecule_type']=='lipid').to_numpy()
    serie_indices=item.atoms_dataframe['molecule_index'][mask]
    return serie_indices.unique().shape[0]

def get_n_structures_from_system(item, check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

    return 0

## bond

def get_bond_index_from_bond(item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_out = None

    if indices is 'all':
        n_bonds = get_n_bonds_from_system(item, check=False)
        tmp_out = np.arange(n_bonds, dtype=int)

    else:
        tmp_out = indices

    return tmp_out

def get_bond_order_from_bond(item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_out = None

    if indices is 'all':
        tmp_out = item.bonds_dataframe['order'].to_numpy(copy=True)
    else:
        tmp_out = item.bonds_dataframe.iloc[indices]['order'].to_numpy(copy=True)

    return tmp_out

def get_bond_type_from_bond(item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_out = None

    if indices is 'all':
        tmp_out = item.bonds_dataframe['type'].to_numpy(copy=True)
    else:
        tmp_out = item.bonds_dataframe.iloc[indices]['type'].to_numpy(copy=True)

    return tmp_out

def get_atom_index_from_bond(item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_out = None

    if indices is 'all':
        tmp_out = item.bonds_dataframe[['atom1_index','atom2_index']].to_numpy(dtype=int, copy=True)
    else:
        tmp_out = item.bonds_dataframe.iloc[indices][['atom1_index','atom2_index']].to_numpy(dtype=int, copy=True)

    return tmp_out

def get_n_bonds_from_bond(item, indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_bonds_from_system(item, check=False)
    else:
        return len(indices)

