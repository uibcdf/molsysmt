from molsysmt._private.variables import is_all
import numpy as np
from networkx import Graph

## From atom

@digest(form=form)
def get_atom_index_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_atoms_from_system(item, digest=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_group_id_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_group_name_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_group_type_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_component_id_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_component_name_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_component_type_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_atom(item, indices=indice, digest=Falses)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_chain_id_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_chain_name_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_chain_type_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_molecule_id_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_molecule_name_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_molecule_type_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_id_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_name_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_type_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_atom(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_n_atoms_from_atom(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_atoms_from_system(item, digest=False)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_groups_from_atom(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_groups_from_system(item, digest=False)
    else:
        output = get_group_index_from_atom(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_components_from_atom(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_components_from_system(item, digest=False)
    else:
        output = get_component_index_from_atom(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_molecules_from_atom(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_molecules_from_system(item, digest=False)
    else:
        output = get_molecule_index_from_atom(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_chains_from_atom(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_chains_from_system(item, digest=False)
    else:
        output = get_chain_index_from_atom(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_entities_from_atom(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item, digest=False)
    else:
        output = get_entity_index_from_atom(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    output = None

    G = Graph()
    edges = get_atom_index_from_bond(item, digest=False)
    G.add_edges_from(edges)

    if is_all(indices):

        indices = get_atom_index_from_atom(item, digest=False)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n for n in G[ii]]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    del(G, edges)

    return output

@digest(form=form)
def get_bond_index_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    output = None

    G = Graph()
    edges = get_atom_index_from_bond(item, digest=False)
    n_bonds = edges.shape[0]
    edge_indices = np.array([{'index':ii} for ii in range(n_bonds)]).reshape([n_bonds,1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if is_all(indices):

        indices = get_atom_index_from_atom(item, digest=False)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n['index'] for n in G[ii].values()]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    del(G, edges, edge_indices)

    return output

@digest(form=form)
def get_n_bonds_from_atom(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = None

    G = Graph()
    edges = get_atom_index_from_bond(item, digest=False)
    G.add_edges_from(edges)

    if is_all(indices):

        indices = get_atom_index_from_atom(item, digest=False)

    output = []

    for ii in indices:
        if ii in G:
            output.append(len(G[ii]))
        else:
            output.append(0)

    output = np.array(output)

    del(G, edges)

    return output

@digest(form=form)
def get_inner_bond_index_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    raise _NotImplementedMethodError


## From group

@digest(form=form)
def get_atom_index_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_group_index_from_group(item, indices=indices, digest=False)
    attribute_from_atom = get_atom_index_from_atom(item, digest=False)
    target_index_from_atom = get_group_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_atom_id_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_group(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_name_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_group(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_type_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_group(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_index_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_groups_from_system(item, digest=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_component_index_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, digest=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_component_index_from_atom(item, indices=first_atom_index_from_target)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_component_id_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_group(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_component_name_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_group(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_component_type_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_group(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_chain_index_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, digest=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, digest=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_chain_id_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_group(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_chain_name_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_group(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_chain_type_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_group(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_molecule_index_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, digest=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, digest=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_molecule_id_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_group(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_molecule_name_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_group(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_molecule_type_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_group(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_entity_index_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, digest=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, digest=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_entity_id_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_group(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_entity_name_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_group(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_entity_type_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_group(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_n_atoms_from_group(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_atom_index_from_group(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_group(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_groups_from_system(item, digest=False)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_components_from_group(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_components_from_system(item, digest=False)
    else:
        output = get_component_index_from_group(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_molecules_from_group(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_molecules_from_system(item, digest=False)
    else:
        output = get_molecule_index_from_group(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_chains_from_group(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_chains_from_system(item, digest=False)
    else:
        output = get_chain_index_from_group(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_entities_from_group(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_entities_from_system(item, digest=False)
    else:
        output = get_entity_index_from_group(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output


## From component

@digest(form=form)
def get_atom_index_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_component_index_from_component(item, indices=indices, digest=False)
    attribute_from_atom = get_atom_index_from_atom(item, digest=False)
    target_index_from_atom = get_component_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_atom_id_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_component(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_name_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_component(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_type_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_component(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_index_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_component_index_from_component(item, indices=indices, digest=False)
    attribute_from_atom = get_group_index_from_atom(item, digest=False)
    target_index_from_atom = get_component_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_group_id_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_component(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_name_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_component(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_type_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_component(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_index_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_components_from_system(item, digest=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_chain_index_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, digest=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, digest=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_chain_id_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_component(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_chain_name_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_component(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_chain_type_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_component(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_molecule_index_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, digest=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, digest=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_molecule_id_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_component(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_molecule_name_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_component(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_molecule_type_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_component(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_index_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, digest=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, digest=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_entity_id_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_component(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_name_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_component(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_type_from_component(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_component(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_n_atoms_from_component(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_atom_index_from_component(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_component(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_group_index_from_component(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_components_from_component(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_components_from_system(item, digest=False)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_molecules_from_component(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_molecules_from_system(item, digest=False)
    else:
        output = get_molecule_index_from_component(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_chains_from_component(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_chains_from_system(item, digest=False)
    else:
        output = get_chain_index_from_component(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_entities_from_component(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item, digest=False)
    else:
        output = get_entity_index_from_component(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

## molecule

@digest(form=form)
def get_atom_index_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_molecule_index_from_molecule(item, indices=indices, digest=False)
    attribute_from_atom = get_atom_index_from_atom(item, digest=False)
    target_index_from_atom = get_molecule_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_atom_id_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_molecule(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_name_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_molecule(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_type_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_molecule(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_index_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_molecule_index_from_molecule(item, indices=indices, digest=False)
    attribute_from_atom = get_group_index_from_atom(item, digest=False)
    target_index_from_atom = get_molecule_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_group_id_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_molecule(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_name_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_molecule(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_type_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_molecule(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_index_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_molecule_index_from_molecule(item, indices=indices, digest=False)
    attribute_from_atom = get_component_index_from_atom(item, digest=False)
    target_index_from_atom = get_molecule_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_component_id_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_molecule(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_name_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_molecule(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_type_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_molecule(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_index_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_atom_indices = get_atom_index_from_molecule(item, indices=indices, digest=False)
    aux_indices = get_molecule_index_from_atom(item, digest=False)
    aux_vals = get_chain_index_from_atom(item, digest=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_chain_id_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_molecule(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_name_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_molecule(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_type_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_molecule(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_index_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_molecules_from_system(item, digest=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_entity_index_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_molecule(item, indices=indices, digest=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, digest=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_entity_id_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_molecule(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_name_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_molecule(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_type_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_molecule(item, indices=indices, digest=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, digest=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_atom_index_from_molecule(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_group_index_from_molecule(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_components_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_component_index_from_molecule(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_molecules_from_system(item, digest=False)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_chains_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_chain_index_from_molecule(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_entities_from_molecule(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item, digest=False)
    else:
        output = get_entity_index_from_molecule(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

## chain

@digest(form=form)
def get_atom_index_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_chain_index_from_chain(item, indices=indices, digest=False)
    attribute_from_atom = get_atom_index_from_atom(item, digest=False)
    target_index_from_atom = get_chain_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_atom_id_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_name_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_type_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_index_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_chain_index_from_chain(item, indices=indices, digest=False)
    attribute_from_atom = get_group_index_from_atom(item, digest=False)
    target_index_from_atom = get_chain_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_group_id_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_name_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_type_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_index_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_chain_index_from_chain(item, indices=indices, digest=False)
    attribute_from_atom = get_component_index_from_atom(item, digest=False)
    target_index_from_atom = get_chain_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_component_id_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_name_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_type_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_index_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_chains_from_system(item, digest=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_molecule_index_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, digest=False)
    aux_indices = get_chain_index_from_atom(item, digest=False)
    aux_vals = get_molecule_index_from_atom(item, digest=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_molecule_id_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_name_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_type_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_entity_index_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, digest=False)
    aux_indices = get_chain_index_from_atom(item, digest=False)
    aux_vals = get_entity_index_from_atom(item, digest=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_entity_id_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_entity_name_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_entity_type_from_chain(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_chain(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_n_atoms_from_chain(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_atom_index_from_chain(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_chain(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_group_index_from_chain(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_components_from_chain(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_component_index_from_chain(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_molecules_from_chain(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_molecule_index_from_chain(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_chains_from_chain(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_chains_from_system(item, digest=False)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_entities_from_chain(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item, digest=False)
    else:
        output = get_entity_index_from_chain(item, indices=indices, digest=False)
        output = np.unique(output).shape[0]

    return output

## From entity

@digest(form=form)
def get_atom_index_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_entity_index_from_entity(item, indices=indices, digest=False)
    attribute_from_atom = get_atom_index_from_atom(item, digest=False)
    target_index_from_atom = get_entity_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_atom_id_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_name_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_type_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_index_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_entity_index_from_entity(item, indices=indices, digest=False)
    attribute_from_atom = get_group_index_from_atom(item, digest=False)
    target_index_from_atom = get_entity_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_group_id_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_name_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_type_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_group_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_index_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_entity_index_from_entity(item, indices=indices, digest=False)
    attribute_from_atom = get_component_index_from_atom(item, digest=False)
    target_index_from_atom = get_entity_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_component_id_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_name_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_type_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_component_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_index_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices, digest=False)
    aux_indices = get_entity_index_from_atom(item, digest=False)
    aux_vals = get_chain_index_from_atom(item, digest=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_chain_id_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_name_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_type_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_index_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    indices_aux = get_entity_index_from_entity(item, indices=indices, digest=False)
    attribute_from_atom = get_molecule_index_from_atom(item, digest=False)
    target_index_from_atom = get_entity_index_from_atom(item, digest=False)

    output=[]

    for ii in indices_aux:
        mask = (target_index_from_atom==ii)
        output.append(np.unique(attribute_from_atom[mask]))

    del(indices_aux, attribute_from_atom, target_index_from_atom)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_molecule_id_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_name_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_type_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_entity(item, indices=indices, digest=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, digest=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_entity_index_from_entity(item, indices='all', digest=True):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_entities_from_system(item, digest=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_n_atoms_from_entity(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_atom_index_from_entity(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_entity(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_group_index_from_entity(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_components_from_entity(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_component_index_from_entity(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_molecules_from_entity(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_molecule_index_from_entity(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_chains_from_entity(item, indices='all', digest=True):

    if indices is None:
        return 0

    output = get_chain_index_from_entity(item, indices=indices, digest=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_entities_from_entity(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item, digest=False)
    else:
        output = indices.shape[0]

    return output

## system

@digest(form=form)
def get_n_aminoacids_from_system(item, digest=True):

    group_types = get_group_type_from_group(item, digest=False)
    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_system(item, digest=True):

    group_types = get_group_type_from_group(item, digest=False)
    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_system(item, digest=True):

    molecule_types = get_group_type_from_group(item, digest=False)
    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_system(item, digest=True):

    molecule_types = get_group_type_from_group(item, digest=False)
    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_system(item, digest=True):

    molecule_types = get_group_type_from_group(item, digest=False)
    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_system(item, digest=True):

    molecule_types = get_molecule_type_from_molecule(item, digest=False)
    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_system(item, digest=True):

    molecule_types = get_molecule_type_from_molecule(item, digest=False)
    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_system(item, digest=True):

    molecule_types = get_molecule_type_from_molecule(item, digest=False)
    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_system(item, digest=True):

    molecule_types = get_molecule_type_from_molecule(item, digest=False)
    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_system(item, digest=True):

    molecule_types = get_molecule_type_from_molecule(item, digest=False)
    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_system(item, digest=True):

    molecule_types = get_molecule_type_from_molecule(item, digest=False)
    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', digest=True):

    if strucure_indices is None:
        return None

    return get_coordinates_from_atom(item, structure_indices=structure_indices, digest=False)

@digest(form=form)
def get_box_shape_from_system(item, structure_indices='all', digest=True):

    if strucure_indices is None:
        return None

    from molsysmt.pbc import box_shape_from_box

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, digest=False)
    output = box_shape_from_box(tmp_box, digest=False)

    return output

@digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all', digest=True):

    if strucure_indices is None:
        return None

    from molsysmt.pbc import box_lengths_from_box

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, digest=False)
    output = box_lengths_from_box(tmp_box, digest=False)

    return output

@digest(form=form)
def get_box_angles_from_system(item, structure_indices='all', digest=True):

    if strucure_indices is None:
        return None

    from molsysmt.pbc import box_angles_from_box

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, digest=False)
    output = box_angles_from_box(tmp_box, digest=False)

    return output

@digest(form=form)
def get_box_volume_from_system(item, structure_indices='all', digest=True):

    if strucure_indices is None:
        return None

    from molsysmt.pbc import box_volume_from_box

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, digest=False)
    if tmp_box is None:
        output=None
    else:
        output = box_volume_from_box(tmp_box, digest=False)

    return output

@digest(form=form)
def get_bonded_atoms_from_system(item, digest=True):

    return get_bonded_atoms_from_atom(item, digest=False)

@digest(form=form)
def get_bond_index_from_system(item, digest=True):

    return get_bond_index_from_atom(item, digest=False)

@digest(form=form)
def get_inner_bonded_atoms_from_system(item, digest=True):

    return get_inner_bonded_atoms_from_atom(item, digest=False)

@digest(form=form)
def get_inner_bond_index_from_system(item, digest=True):

    return get_inner_bond_index_from_atom(item, digest=False)

## bond

@digest(form=form)
def get_bond_index_from_bond(item, indices='all', digest=True):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_bonds_from_system(item, digest=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_n_bonds_from_bond(item, indices='all', digest=True):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_bonds_from_system(item, digest=False)
    else:
        output = indices.shape[0]

    return output

