from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
from networkx import Graph

## From atom

@digest(form=form)
def get_atom_index_from_atom(item, indices='all'):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_atoms_from_system(item)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_group_id_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_group_name_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_group_type_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_component_id_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_component_name_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_component_type_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_chain_id_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_chain_name_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_chain_type_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_molecule_id_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_molecule_name_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_molecule_type_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_id_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_name_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_type_from_atom(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_atom(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_n_atoms_from_atom(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_atoms_from_system(item)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_groups_from_atom(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_groups_from_system(item)
    else:
        output = get_group_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_components_from_atom(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_components_from_system(item)
    else:
        output = get_component_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_molecules_from_atom(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_molecules_from_system(item)
    else:
        output = get_molecule_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_chains_from_atom(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_chains_from_system(item)
    else:
        output = get_chain_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_entities_from_atom(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = get_entity_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all'):

    if indices is None:
        return None

    output = None

    G = Graph()
    edges = get_bonded_atoms_from_bond(item)
    G.add_edges_from(edges)

    if is_all(indices):

        indices = get_atom_index_from_atom(item)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n for n in G[ii]]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    for ii in range(output.shape[0]):
        output[ii] = np.sort(output[ii])

    del(G, edges)

    return output

@digest(form=form)
def get_bond_index_from_atom(item, indices='all'):

    if indices is None:
        return None

    output = None

    G = Graph()
    edges = get_bonded_atoms_from_bond(item)
    n_bonds = edges.shape[0]
    edge_indices = np.array([{'index':ii} for ii in range(n_bonds)]).reshape([n_bonds,1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if is_all(indices):

        indices = get_atom_index_from_atom(item)

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
def get_n_bonds_from_atom(item, indices='all'):

    if indices is None:
        return 0

    output = None

    G = Graph()
    edges = get_bonded_atoms_from_bond(item)
    G.add_edges_from(edges)

    if is_all(indices):

        indices = get_atom_index_from_atom(item)

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
def get_inner_bond_index_from_atom(item, indices='all'):

    if indices is None:
        return None

    raise _NotImplementedMethodError

@digest(form=form)
def get_n_aminoacids_from_atom(item, indices='all'):

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all'):

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='saccharide').sum()


## From group

@digest(form=form)
def get_atom_index_from_group(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_group_index_from_group(item, indices=indices)
    attribute_from_atom = get_atom_index_from_atom(item)
    target_index_from_atom = get_group_index_from_atom(item)

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
def get_atom_id_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_group(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_name_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_group(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_type_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_group(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_index_from_group(item, indices='all'):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_groups_from_system(item)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_component_index_from_group(item, indices='all'):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_group(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_component_index_from_atom(item, indices=first_atom_index_from_target)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_component_id_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_group(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_component_name_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_group(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_component_type_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_group(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_chain_index_from_group(item, indices='all'):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_group(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_chain_id_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_group(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_chain_name_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_group(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_chain_type_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_group(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_molecule_index_from_group(item, indices='all'):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_group(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_molecule_id_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_group(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_molecule_name_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_group(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_molecule_type_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_group(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_entity_index_from_group(item, indices='all'):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_group(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_entity_id_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_group(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_entity_name_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_group(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_entity_type_from_group(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_group(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

@digest(form=form)
def get_n_atoms_from_group(item, indices='all'):

    if indices is None:
        return 0

    output = get_atom_index_from_group(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_group(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_groups_from_system(item)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_components_from_group(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_components_from_system(item)
    else:
        output = get_component_index_from_group(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_molecules_from_group(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_molecules_from_system(item)
    else:
        output = get_molecule_index_from_group(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_chains_from_group(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_chains_from_system(item)
    else:
        output = get_chain_index_from_group(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_entities_from_group(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        return get_n_entities_from_system(item)
    else:
        output = get_entity_index_from_group(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_formal_charge_from_group(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_group(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_formal_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = puw.concatenate(output, type_value='numpy.ndarray', standardized=True)

    return output

@digest(form=form)
def get_partial_charge_from_group(item, indices='all'):

    if indices is None:
        return None

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_group(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_partial_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_n_aminoacids_from_group(item, indices='all'):

    group_types = get_group_type_from_group(item, indices=indices)

    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_group(item, indices='all'):

    group_types = get_group_type_from_group(item, indices=indices)

    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_group(item, indices='all'):

    molecule_indices = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='saccharide').sum()


## From component

@digest(form=form)
def get_atom_index_from_component(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_component_index_from_component(item, indices=indices)
    attribute_from_atom = get_atom_index_from_atom(item)
    target_index_from_atom = get_component_index_from_atom(item)

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
def get_atom_id_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_component(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_name_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_component(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_type_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_component(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_index_from_component(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_component_index_from_component(item, indices=indices)
    attribute_from_atom = get_group_index_from_atom(item)
    target_index_from_atom = get_component_index_from_atom(item)

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
def get_group_id_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_component(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_name_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_component(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_type_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_component(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_index_from_component(item, indices='all'):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_components_from_system(item)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_chain_index_from_component(item, indices='all'):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_component(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_chain_id_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_component(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_chain_name_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_component(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_chain_type_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_component(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_molecule_index_from_component(item, indices='all'):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_component(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_molecule_id_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_component(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_molecule_name_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_component(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_molecule_type_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_component(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_index_from_component(item, indices='all'):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_component(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_entity_id_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_component(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_name_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_component(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_type_from_component(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_component(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_n_atoms_from_component(item, indices='all'):

    if indices is None:
        return 0

    output = get_atom_index_from_component(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_component(item, indices='all'):

    if indices is None:
        return 0

    output = get_group_index_from_component(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_components_from_component(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_components_from_system(item)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_molecules_from_component(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_molecules_from_system(item)
    else:
        output = get_molecule_index_from_component(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_chains_from_component(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_chains_from_system(item)
    else:
        output = get_chain_index_from_component(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_n_entities_from_component(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = get_entity_index_from_component(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_formal_charge_from_component(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_component(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_formal_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_partial_charge_from_group(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_component(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_partial_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_n_aminoacids_from_component(item, indices='all'):

    group_indices = get_group_index_from_component(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_component(item, indices='all'):

    group_indices = get_group_index_from_component(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_component(item, indices='all'):

    molecule_indices = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='saccharide').sum()


## molecule

@digest(form=form)
def get_atom_index_from_molecule(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_molecule_index_from_molecule(item, indices=indices)
    attribute_from_atom = get_atom_index_from_atom(item)
    target_index_from_atom = get_molecule_index_from_atom(item)

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
def get_atom_id_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_molecule(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_name_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_molecule(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_type_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_molecule(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_index_from_molecule(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_molecule_index_from_molecule(item, indices=indices)
    attribute_from_atom = get_group_index_from_atom(item)
    target_index_from_atom = get_molecule_index_from_atom(item)

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
def get_group_id_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_molecule(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_name_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_molecule(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_type_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_molecule(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_index_from_molecule(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_molecule_index_from_molecule(item, indices=indices)
    attribute_from_atom = get_component_index_from_atom(item)
    target_index_from_atom = get_molecule_index_from_atom(item)

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
def get_component_id_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_molecule(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_name_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_molecule(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_type_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_molecule(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_index_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_atom_indices = get_atom_index_from_molecule(item, indices=indices)
    aux_indices = get_molecule_index_from_atom(item)
    aux_vals = get_chain_index_from_atom(item)

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
def get_chain_id_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_molecule(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_name_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_molecule(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_type_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_molecule(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_index_from_molecule(item, indices='all'):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_molecules_from_system(item)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_entity_index_from_molecule(item, indices='all'):

    if indices is None:
        return None

    atom_index_from_target = get_atom_index_from_molecule(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

@digest(form=form)
def get_entity_id_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_molecule(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_name_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_molecule(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_entity_type_from_molecule(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_molecule(item, indices=indices)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

@digest(form=form)
def get_n_atoms_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    output = get_atom_index_from_molecule(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    output = get_group_index_from_molecule(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_components_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    output = get_component_index_from_molecule(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_molecules_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_molecules_from_system(item)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_chains_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    output = get_chain_index_from_molecule(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_entities_from_molecule(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = get_entity_index_from_molecule(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_formal_charge_from_molecule(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_molecule(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_formal_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_partial_charge_from_molecule(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_molecule(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_partial_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_n_aminoacids_from_molecule(item, indices='all'):

    group_indices = get_group_index_from_molecule(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all'):

    group_indices = get_group_index_from_molecule(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices)

    return (molecule_types=='saccharide').sum()


## chain

@digest(form=form)
def get_atom_index_from_chain(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_chain_index_from_chain(item, indices=indices)
    attribute_from_atom = get_atom_index_from_atom(item)
    target_index_from_atom = get_chain_index_from_atom(item)

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
def get_atom_id_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_name_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_type_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_index_from_chain(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_chain_index_from_chain(item, indices=indices)
    attribute_from_atom = get_group_index_from_atom(item)
    target_index_from_atom = get_chain_index_from_atom(item)

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
def get_group_id_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_name_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_type_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_index_from_chain(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_chain_index_from_chain(item, indices=indices)
    attribute_from_atom = get_component_index_from_atom(item)
    target_index_from_atom = get_chain_index_from_atom(item)

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
def get_component_id_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_name_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_type_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_index_from_chain(item, indices='all'):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_chains_from_system(item)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_molecule_index_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices)
    aux_indices = get_chain_index_from_atom(item)
    aux_vals = get_molecule_index_from_atom(item)

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
def get_molecule_id_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_name_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_type_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_entity_index_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices)
    aux_indices = get_chain_index_from_atom(item)
    aux_vals = get_entity_index_from_atom(item)

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
def get_entity_id_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_entity_name_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_entity_type_from_chain(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_entity_index_from_chain(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_n_atoms_from_chain(item, indices='all'):

    if indices is None:
        return 0

    output = get_atom_index_from_chain(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_chain(item, indices='all'):

    if indices is None:
        return 0

    output = get_group_index_from_chain(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_components_from_chain(item, indices='all'):

    if indices is None:
        return 0

    output = get_component_index_from_chain(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_molecules_from_chain(item, indices='all'):

    if indices is None:
        return 0

    output = get_molecule_index_from_chain(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_chains_from_chain(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_chains_from_system(item)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_n_entities_from_chain(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = get_entity_index_from_chain(item, indices=indices)
        output = np.unique(output).shape[0]

    return output

@digest(form=form)
def get_formal_charge_from_chain(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_chain(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_formal_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_partial_charge_from_chain(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_chain(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_partial_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_n_aminoacids_from_chain(item, indices='all'):

    group_indices = get_group_index_from_chain(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all'):

    group_indices = get_group_index_from_chain(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_chain(item, indices='all'):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='saccharide').sum()


## From entity

@digest(form=form)
def get_atom_index_from_entity(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_entity_index_from_entity(item, indices=indices)
    attribute_from_atom = get_atom_index_from_atom(item)
    target_index_from_atom = get_entity_index_from_atom(item)

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
def get_atom_id_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_name_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_atom_type_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_atom_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_index_from_entity(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_entity_index_from_entity(item, indices=indices)
    attribute_from_atom = get_group_index_from_atom(item)
    target_index_from_atom = get_entity_index_from_atom(item)

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
def get_group_id_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_name_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_group_type_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_group_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_index_from_entity(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_entity_index_from_entity(item, indices=indices)
    attribute_from_atom = get_component_index_from_atom(item)
    target_index_from_atom = get_entity_index_from_atom(item)

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
def get_component_id_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_name_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_component_type_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_component_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_index_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices)
    aux_indices = get_entity_index_from_atom(item)
    aux_vals = get_chain_index_from_atom(item)

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
def get_chain_id_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_name_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_chain_type_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_chain_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_index_from_entity(item, indices='all'):

    if indices is None:
        return None

    indices_aux = get_entity_index_from_entity(item, indices=indices)
    attribute_from_atom = get_molecule_index_from_atom(item)
    target_index_from_atom = get_entity_index_from_atom(item)

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
def get_molecule_id_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_name_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_molecule_type_from_entity(item, indices='all'):

    if indices is None:
        return None

    aux_indices = get_molecule_index_from_entity(item, indices=indices)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

@digest(form=form)
def get_entity_index_from_entity(item, indices='all'):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_entities_from_system(item)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_n_atoms_from_entity(item, indices='all'):

    if indices is None:
        return 0

    output = get_atom_index_from_entity(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_groups_from_entity(item, indices='all'):

    if indices is None:
        return 0

    output = get_group_index_from_entity(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_components_from_entity(item, indices='all'):

    if indices is None:
        return 0

    output = get_component_index_from_entity(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_molecules_from_entity(item, indices='all'):

    if indices is None:
        return 0

    output = get_molecule_index_from_entity(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_chains_from_entity(item, indices='all'):

    if indices is None:
        return 0

    output = get_chain_index_from_entity(item, indices=indices)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

@digest(form=form)
def get_n_entities_from_entity(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = indices.shape[0]

    return output

@digest(form=form)
def get_formal_charge_from_entity(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_entity(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_formal_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_partial_charge_from_entity(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_entity(item, indices)
    output = []
    for atom_indices in atom_indices_per_element:
        charges = get_partial_charge_from_atom(item, atom_indices)
        output.append(np.sum(charges))

    output = np.array(output)

    return output

@digest(form=form)
def get_n_aminoacids_from_entity(item, indices='all'):

    group_indices = get_group_index_from_entity(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all'):

    group_indices = get_group_index_from_entity(item, indices=indices)
    group_indices = np.unique(group_indices).shape[0]
    group_types = get_group_type_from_group(item, indices=group_indices)

    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_entity(item, indices='all'):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_indices).shape[0]
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)

    return (molecule_types=='saccharide').sum()


## system

@digest(form=form)
def get_n_aminoacids_from_system(item):

    group_types = get_group_type_from_group(item)
    return (group_types=='aminoacid').sum()

@digest(form=form)
def get_n_nucleotides_from_system(item):

    group_types = get_group_type_from_group(item)
    return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_system(item):

    molecule_types = get_group_type_from_group(item)
    return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_system(item):

    molecule_types = get_group_type_from_group(item)
    return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_system(item):

    molecule_types = get_group_type_from_group(item)
    return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_system(item):

    molecule_types = get_molecule_type_from_molecule(item)
    return (molecule_types=='saccharide').sum()

@digest(form=form)
def get_coordinates_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    return get_coordinates_from_atom(item, structure_indices=structure_indices)

@digest(form=form)
def get_velocities_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    return get_velocities_from_atom(item, structure_indices=structure_indices)

@digest(form=form)
def get_box_shape_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    from molsysmt.pbc import get_shape_from_box

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    output = get_shape_from_box(tmp_box)

    return output

@digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    from molsysmt.pbc import get_lengths_and_angles_from_box

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    output, _ = get_lengths_and_angles_from_box(tmp_box)

    return output

@digest(form=form)
def get_box_angles_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    from molsysmt.pbc import get_lengths_and_angles_from_box

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    _, output = get_lengths_and_angles_from_box(tmp_box)

    return output

@digest(form=form)
def get_box_volume_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    from molsysmt.pbc import get_volume_from_box

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    if tmp_box is None:
        output=None
    else:
        output = get_volume_from_box(tmp_box)

    return output

@digest(form=form)
def get_occupancy_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    return get_occupancy_from_atom(item, indices='all', structure_indices=structure_indices)

@digest(form=form)
def get_b_factor_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    return get_b_factor_from_atom(item, indices='all', structure_indices=structure_indices)

@digest(form=form)
def get_alternate_location_from_system(item, structure_indices='all'):

    if structure_indices is None:
        return None

    return get_alternate_location_from_atom(item, indices='all', structure_indices=structure_indices)

@digest(form=form)
def get_formal_charge_from_system(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_system(item, indices)
    charges = get_formal_charge_from_atom(item, atom_indices)
    output = np.sum(charges)

    return output

@digest(form=form)
def get_partial_charge_from_system(item, indices='all'):

    if indices is None:
        return None

    atom_indices_per_element = get_atom_index_from_system(item, indices)
    charges = get_partial_charge_from_atom(item, atom_indices)
    output = np.sum(charges)

    return output

@digest(form=form)
def get_bonded_atoms_from_system(item):

    return get_bonded_atoms_from_atom(item)

@digest(form=form)
def get_bond_index_from_system(item):

    return get_bond_index_from_atom(item)

@digest(form=form)
def get_inner_bonded_atoms_from_system(item):

    return get_inner_bonded_atoms_from_atom(item)

@digest(form=form)
def get_inner_bond_index_from_system(item):

    return get_inner_bond_index_from_atom(item)

## bond

@digest(form=form)
def get_bond_index_from_bond(item, indices='all'):

    if indices is None:
        return None

    if is_all(indices):
        n_aux = get_n_bonds_from_system(item)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

@digest(form=form)
def get_n_bonds_from_bond(item, indices='all'):

    if indices is None:
        return 0

    if is_all(indices):
        output = get_n_bonds_from_system(item)
    else:
        output = indices.shape[0]

    return output

