from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np
import pandas as pd
from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
import types
from networkx import Graph
from collections import defaultdict
from itertools import chain, compress

form = 'molsysmt.Topology'


#######################################################################
#                 To be customized for each form                      #
#######################################################################

# From atom


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = list(range(item.atoms.shape[0]))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    atom_id_from_atom = item.atoms['atom_id'].to_numpy()

    if indices=='all':
        output = atom_id_from_atom.tolist()
    else:
        output = atom_id_from_atom[indices].tolist()

    del atom_id_from_atom

    return output


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    atom_name_from_atom = item.atoms['atom_name'].to_numpy()

    if indices=='all':
        output = atom_name_from_atom.tolist()
    else:
        output = atom_name_from_atom[indices].tolist()

    del atom_name_from_atom

    return output


@arg_digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    atom_type_from_atom = item.atoms['atom_type'].to_numpy()

    if indices=='all':
        output = atom_type_from_atom.tolist()
    else:
        output = atom_type_from_atom[indices].tolist()

    del atom_type_from_atom

    return output


@arg_digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()

    if indices=='all':
        output = group_index_from_atom.tolist()
    else:
        output = group_index_from_atom[indices].tolist()

    del group_index_from_atom

    return output


@arg_digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    group_id_from_group = item.groups['group_id'].to_numpy()

    if indices=='all':
        output = group_id_from_group[group_index_from_atom].tolist()
    else:
        aux = group_index_from_atom[indices]
        output = group_id_from_group[aux].tolist()

    del group_index_from_atom, group_id_from_group

    return output


@arg_digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    group_name_from_group = item.groups['group_name'].to_numpy()

    if indices=='all':
        output = group_name_from_group[group_index_from_atom].tolist()
    else:
        aux = group_index_from_atom[indices]
        output = group_name_from_group[aux].tolist()

    del group_index_from_atom, group_name_from_group

    return output


@arg_digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    group_type_from_group = item.groups['group_type'].to_numpy()

    if indices=='all':
        output = group_type_from_group[group_index_from_atom].tolist()
    else:
        aux = group_index_from_atom[indices]
        output = group_type_from_group[aux].tolist()

    del group_index_from_atom, group_type_from_group

    return output


@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()       
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()  

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom].tolist()
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux].tolist()
        del aux

    del group_index_from_atom, molecule_index_from_group

    return output


@arg_digest(form=form)
def get_molecule_id_from_atom(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()       
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()  
    molecule_id_from_molecule = item.molecules['molecule_id'].to_numpy()

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = molecule_id_from_molecule[output].tolist()

    del group_index_from_atom, molecule_index_from_group, molecule_id_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_name_from_atom(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()       
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()  
    molecule_name_from_molecule = item.molecules['molecule_name'].to_numpy()

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = molecule_name_from_molecule[output].tolist()

    del group_index_from_atom, molecule_index_from_group, molecule_name_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_type_from_atom(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()       
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()  
    molecule_type_from_molecule = item.molecules['molecule_type'].to_numpy()

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = molecule_type_from_molecule[output].tolist()

    del group_index_from_atom, molecule_index_from_group, molecule_type_from_molecule

    return output


@arg_digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()       
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()  
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = entity_index_from_molecule[output].tolist()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    return output


@arg_digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()       
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()  
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    entity_id_from_entity = item.entities['entity_id'].to_numpy()

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = entity_index_from_molecule[output]
    output = entity_id_from_entity[output].tolist()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule, entity_id_from_entity

    return output


@arg_digest(form=form)
def get_entity_name_from_atom(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()       
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()  
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    entity_name_from_entity = item.entities['entity_name'].to_numpy()

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = entity_index_from_molecule[output]
    output = entity_name_from_entity[output].tolist()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule, entity_name_from_entity

    return output


@arg_digest(form=form)
def get_entity_type_from_atom(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()       
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()  
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    entity_type_from_entity = item.entities['entity_type'].to_numpy()

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = entity_index_from_molecule[output]
    output = entity_type_from_entity[output].tolist()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule, entity_type_from_entity

    return output


@arg_digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()

    if indices=='all':
        output = component_index_from_atom.tolist()
    else:
        output = component_index_from_atom[indices].tolist()

    del component_index_from_atom

    return output


@arg_digest(form=form)
def get_component_id_from_atom(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_id_from_component = item.components['component_id'].to_numpy()

    if indices=='all':
        output = component_id_from_component[component_index_from_atom].tolist()
    else:
        aux = component_index_from_atom[indices]
        output = component_id_from_component[aux].tolist()

    del component_index_from_atom, component_id_from_component

    return output


@arg_digest(form=form)
def get_component_name_from_atom(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_name_from_component = item.components['component_name'].to_numpy()

    if indices=='all':
        output = component_name_from_component[component_index_from_atom].tolist()
    else:
        aux = component_index_from_atom[indices]
        output = component_name_from_component[aux].tolist()

    del component_index_from_atom, component_name_from_component

    return output


@arg_digest(form=form)
def get_component_type_from_atom(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_type_from_component = item.components['component_type'].to_numpy()

    if indices=='all':
        output = component_type_from_component[component_index_from_atom].tolist()
    else:
        aux = component_index_from_atom[indices]
        output = component_type_from_component[aux].tolist()

    del component_index_from_atom, component_type_from_component

    return output


@arg_digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()

    if indices=='all':
        output = chain_index_from_atom.tolist()
    else:
        output = chain_index_from_atom[indices].tolist()

    del chain_index_from_atom

    return output


@arg_digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_id_from_chain = item.chains['chain_id'].to_numpy()

    if indices=='all':
        output = chain_id_from_chain[chain_index_from_atom].tolist()
    else:
        aux = chain_index_from_atom[indices]
        output = chain_id_from_chain[aux].tolist()

    del chain_index_from_atom, chain_id_from_chain

    return output


@arg_digest(form=form)
def get_chain_name_from_atom(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_name_from_chain = item.chains['chain_name'].to_numpy()

    if indices=='all':
        output = chain_name_from_chain[chain_index_from_atom].tolist()
    else:
        aux = chain_index_from_atom[indices]
        output = chain_name_from_chain[aux].tolist()

    del chain_index_from_atom, chain_name_from_chain

    return output


@arg_digest(form=form)
def get_chain_type_from_atom(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_type_from_chain = item.chains['chain_type'].to_numpy()

    if indices=='all':
        output = chain_type_from_chain[chain_index_from_atom].tolist()
    else:
        aux = chain_index_from_atom[indices]
        output = chain_type_from_chain[aux].tolist()

    del chain_index_from_atom, chain_type_from_chain

    return output


@arg_digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False):

    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    n_bonds = len(edges)
    edge_indices = np.array([{'index': ii} for ii in range(n_bonds)]).reshape([n_bonds, 1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if indices=='all':

        indices = get_atom_index_from_atom(item, skip_digestion=True)

    output = []

    for ii in indices:
        if ii in G:
            output.append([n['index'] for n in G[ii].values()])
        else:
            output.append([])

    del G, edges, edge_indices

    return output


@arg_digest(form=form)
def get_bond_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    output = []
    for ii in aux_indices:
        aux_vals = get_bond_type_from_bond(item, indices=ii, skip_digestion=True)
        output.append(aux_vals)

    return output


@arg_digest(form=form)
def get_bond_order_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    output = []
    for ii in aux_indices:
        aux_vals = get_bond_order_from_bond(item, indices=ii, skip_digestion=True)
        output.append(aux_vals)

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    
    G.add_edges_from(edges)

    if indices=='all':

        indices = get_atom_index_from_atom(item, skip_digestion=True)

    output = []

    for ii in indices:
        if ii in G:
            output.append(list(G.neighbors(ii)))
        else:
            output.append([])

    del G, edges

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    output = None

    if indices=='all':

        output = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
   
    else:

        pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
        pairs = np.array(pairs)
        mask = np.isin(pairs[:,0], indices) | np.isin(pairs[:,1], indices)
        output = pairs[mask,:].tolist()

        del pairs, mask

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_atom(item, indices='all', skip_digestion=False):

    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    n_bonds = len(edges)
    edge_indices = np.array([{'index': ii} for ii in range(n_bonds)]).reshape([n_bonds, 1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if indices=='all':

        indices = get_atom_index_from_atom(item)

    else:

        G = G.subgraph(indices)

    output = []

    for ii in indices:
        if ii in G:
            output.append([n['index'] for n in G[ii].values()])
        else:
            output.append([])

    del G, edges, edge_indices

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    
    G.add_edges_from(edges)

    if not indices=='all':

        G = G.subgraph(indices)

    output = []
    for nodo in G.nodes():
        output.append(list(G.neighbors(nodo)))

    del G, edges

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    output = None

    if indices=='all':

        output = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
   
    else:

        pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
        if len(pairs):
            pairs = np.array(pairs)
            mask = np.isin(pairs[:,0], indices) * np.isin(pairs[:,1], indices)
            output = pairs[mask,:].tolist()
            del mask
        else:
            output = []

        del pairs

    return output


@arg_digest(form=form)
def get_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = item.atoms.shape[0]
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    return get_n_atoms_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_groups_from_atom(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = item.groups.shape[0]
    else:
        group_indices_from_atom = item.atoms['group_index'].to_numpy()
        output = np.unique(group_indices_from_atom[indices]).size
        del group_indices_from_atom

    return output


@arg_digest(form=form)
def get_total_n_groups_from_atom(item, indices='all', skip_digestion=False):

    return get_n_groups_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = item.molecules.shape[0]
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        molecule_indices_from_groups = item.groups['molecule_index'].to_numpy()
        aux = group_indices_from_atoms[indices]
        aux = molecule_indices_from_groups[aux]
        output = np.unique(aux).size
        del group_indices_from_atoms, molecule_indices_from_groups, aux

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    return get_n_molecules_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_atom(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = item.entities.shape[0]
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        molecule_indices_from_groups = item.groups['molecule_index'].to_numpy()
        entity_indices_from_molecules = item.molecules['entity_index'].to_numpy()
        aux = group_indices_from_atoms[indices]
        aux = molecule_indices_from_groups[aux]
        aux = entity_indices_from_molecules[aux]
        output = np.unique(aux).size
        del group_indices_from_atoms, molecule_indices_from_groups, entity_indices_from_molecules, aux

    return output


@arg_digest(form=form)
def get_total_n_entities_from_atom(item, indices='all', skip_digestion=False):

    return get_n_entities_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_atom(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = item.components.shape[0]
    else:
        component_indices_from_atoms = item.atoms['component_index'].to_numpy()
        output = np.unique(component_indices_from_atoms[indices]).size
        del component_indices_from_atoms

    return output


@arg_digest(form=form)
def get_total_n_components_from_atom(item, indices='all', skip_digestion=False):

    return get_n_components_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_chains_from_atom(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = item.chains.shape[0]
    else:
        chain_indices_from_atoms = item.atoms['chain_index'].to_numpy()
        output = np.unique(chain_indices_from_atoms[indices]).size
        del chain_indices_from_atoms

    return output


@arg_digest(form=form)
def get_total_n_chains_from_atom(item, indices='all', skip_digestion=False):

    return get_n_chains_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    bond_indices = get_bond_index_from_atom(item, indices, skip_digestion=True)
    output = [len(ii) for ii in bond_indices]
    del bond_indices

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        bond_indices = get_bond_index_from_atom(item, indices, skip_digestion=True)
        output = np.unique(np.concatenate(bond_indices)).shape[0]
        del bond_indices

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    inner_bond_indices = get_inner_bond_index_from_atom(item, indices, skip_digestion=True)
    output = [len(ii) for ii in inner_bond_indices]
    del inner_bond_indices

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        bond_indices = get_inner_bond_index_from_atom(item, indices, skip_digestion=True)
        output = np.unique(np.concatenate(bond_indices)).size
        del bond_indices

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):

    group_type_from_groups = item.groups['group_type'].to_numpy()

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='amino acid')
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='amino acid')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):

    return get_n_amino_acids_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    group_type_from_groups = item.groups['group_type'].to_numpy()

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='nucleotide')
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='nucleotide')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    return get_n_nucleotides_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_ions_from_atom(item, indices='all', skip_digestion=False):

    group_type_from_groups = item.groups['group_type'].to_numpy()

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='ion')
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='ion')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_ions_from_atom(item, indices='all', skip_digestion=False):

    return get_n_ions_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_waters_from_atom(item, indices='all', skip_digestion=False):

    group_type_from_groups = item.groups['group_type'].to_numpy()

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='water')
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='water')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_waters_from_atom(item, indices='all', skip_digestion=False):

    return get_n_waters_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    group_type_from_groups = item.groups['group_type'].to_numpy()

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='small molecule')
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='small molecule')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    return get_n_small_molecules_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    group_type_from_groups = item.groups['group_type'].to_numpy()

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='lipid')
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='lipid')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    return get_n_lipids_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    group_type_from_groups = item.groups['group_type'].to_numpy()

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='saccharide')
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='saccharide')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    return get_n_saccharides_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    molecule_type_from_molecules = item.molecules['molecule_type'].to_numpy()

    if indices=='all':
        output = np.count_nonzero(molecule_type_from_molecules=='peptide')
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        molecule_indices_from_groups = item.groups['molecule_index'].to_numpy()
        aux = np.unique(group_indices_from_atoms[indices])
        aux = np.unique(molecule_indices_from_groups[aux])
        output = np.count_nonzero(molecule_type_from_molecules[aux]=='peptide')
        del group_indices_from_atoms, molecule_indices_from_groups, aux

    del molecule_type_from_molecules

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    return get_n_peptides_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    molecule_type_from_molecules = item.molecules['molecule_type'].to_numpy()

    if indices=='all':
        output = np.count_nonzero(molecule_type_from_molecules=='protein')
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        molecule_indices_from_groups = item.groups['molecule_index'].to_numpy()
        aux = np.unique(group_indices_from_atoms[indices])
        aux = np.unique(molecule_indices_from_groups[aux])
        output = np.count_nonzero(molecule_type_from_molecules[aux]=='protein')
        del group_indices_from_atoms, molecule_indices_from_groups, aux

    del molecule_type_from_molecules

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    return get_n_proteins_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    molecule_type_from_molecules = item.molecules['molecule_type'].to_numpy()

    if indices=='all':
        output = np.count_nonzero(molecule_type_from_molecules=='dna')
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        molecule_indices_from_groups = item.groups['molecule_index'].to_numpy()
        aux = np.unique(group_indices_from_atoms[indices])
        aux = np.unique(molecule_indices_from_groups[aux])
        output = np.count_nonzero(molecule_type_from_molecules[aux]=='dna')
        del group_indices_from_atoms, molecule_indices_from_groups, aux

    del molecule_type_from_molecules

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    return get_n_dnas_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    molecule_type_from_molecules = item.molecules['molecule_type'].to_numpy()

    if indices=='all':
        output = np.count_nonzero(molecule_type_from_molecules=='rna')
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        molecule_indices_from_groups = item.groups['molecule_index'].to_numpy()
        aux = np.unique(group_indices_from_atoms[indices])
        aux = np.unique(molecule_indices_from_groups[aux])
        output = np.count_nonzero(molecule_type_from_molecules[aux]=='rna')
        del group_indices_from_atoms, molecule_indices_from_groups, aux

    del molecule_type_from_molecules

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    return get_n_rnas_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False):

    molecule_type_from_molecules = item.molecules['molecule_type'].to_numpy()

    if indices=='all':
        output = np.count_nonzero(molecule_type_from_molecules=='polysaccharide')
    else:
        group_indices_from_atoms = item.atoms['group_index'].to_numpy()
        molecule_indices_from_groups = item.groups['molecule_index'].to_numpy()
        aux = np.unique(group_indices_from_atoms[indices])
        aux = np.unique(molecule_indices_from_groups[aux])
        output = np.count_nonzero(molecule_type_from_molecules[aux]=='polysaccharide')
        del group_indices_from_atoms, molecule_indices_from_groups, aux

    del molecule_type_from_molecules

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False):

    return get_n_polysaccharides_from_atom(item, indices=indices, skip_digestion=True)


# From group


@arg_digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].append(atom_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].append(atom_index)

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_group(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    atom_id_from_atom = item.atoms['atom_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].append(atom_id_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].append(atom_id_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, atom_id_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_name_from_group(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    atom_name_from_atom = item.atoms['atom_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].append(atom_name_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].append(atom_name_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, atom_name_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_type_from_group(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    atom_type_from_atom = item.atoms['atom_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].append(atom_type_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].append(atom_type_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, atom_type_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_group_index_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = list(range(item.groups.shape[0]))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    group_id_from_group = item.groups['group_id'].to_numpy()

    if indices=='all':
        output = group_id_from_group.tolist()
    else:
        output = group_id_from_group[indices].tolist()

    del group_id_from_group

    return output


@arg_digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    group_name_from_group = item.groups['group_name'].to_numpy()

    if indices=='all':
        output = group_name_from_group.tolist()
    else:
        output = group_name_from_group[indices].tolist()

    del group_name_from_group

    return output


@arg_digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    group_type_from_group = item.groups['group_type'].to_numpy()

    if indices=='all':
        output = group_type_from_group.tolist()
    else:
        output = group_type_from_group[indices].tolist()

    del group_type_from_group

    return output


@arg_digest(form=form)
def get_molecule_index_from_group(item, indices='all', skip_digestion=False):

    molecule_index_from_group = item.groups['molecule_index'].to_numpy()

    if indices=='all':
        output = molecule_index_from_group.tolist()
    else:
        output = molecule_index_from_group[indices].tolist()

    del molecule_index_from_group

    return output


@arg_digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False):

    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_id_from_molecule = item.molecules['molecule_id'].to_numpy()

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = molecule_id_from_molecule[output].tolist()

    del molecule_index_from_group, molecule_id_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False):

    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_name_from_molecule = item.molecules['molecule_name'].to_numpy()

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = molecule_name_from_molecule[output].tolist()

    del molecule_index_from_group, molecule_name_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False):

    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_type_from_molecule = item.molecules['molecule_type'].to_numpy()

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = molecule_type_from_molecule[output].tolist()

    del molecule_index_from_group, molecule_type_from_molecule

    return output


@arg_digest(form=form)
def get_entity_index_from_group(item, indices='all', skip_digestion=False):

    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = entity_index_from_molecule[output].tolist()

    del molecule_index_from_group, entity_index_from_molecule

    return output


@arg_digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False):

    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    entity_id_from_entity = item.entities['entity_id'].to_numpy()

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = entity_index_from_molecule[output]
    output = entity_id_from_entity[output].tolist()

    del molecule_index_from_group, entity_index_from_molecule, entity_id_from_entity

    return output


@arg_digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False):

    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    entity_name_from_entity = item.entities['entity_name'].to_numpy()

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = entity_index_from_molecule[output]
    output = entity_name_from_entity[output].tolist()

    del molecule_index_from_group, entity_index_from_molecule, entity_name_from_entity

    return output


@arg_digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False):

    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    entity_type_from_entity = item.entities['entity_type'].to_numpy()

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = entity_index_from_molecule[output]
    output = entity_type_from_entity[output].tolist()

    del molecule_index_from_group, entity_index_from_molecule, entity_type_from_entity

    return output


@arg_digest(form=form)
def get_component_index_from_group(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    component_index_from_atom = item.atoms['component_index'].to_numpy()

    if indices =='all':
        from molsysmt.form.molsysmt_Topology.get_topological_attributes import get_n_groups_from_system
        n_groups = get_n_groups_from_system(item)
        indices = range(n_groups)

    aux_dict = {ii: set() for ii in indices}
    for atom_index, group_index in enumerate(group_index_from_atom):
        if group_index in aux_dict:
            aux_dict[group_index].add(component_index_from_atom[atom_index])

    output = []
    for ii in indices:
        val = aux_dict[ii]
        clean_val = [int(jj) for jj in val if jj is not None and not pd.isna(jj)]
        if clean_val:
            output.append(clean_val[0])
        else:
            output.append(None)

    return output


@arg_digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_id_from_component = item.components['component_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(component_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ component_id_from_component[next(iter(ii))] if len(ii) == 1 else
               component_id_from_component[list(ii)].tolist() for ii in output]

    del group_index_from_atom, component_index_from_atom, component_id_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_name_from_component = item.components['component_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(component_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ component_name_from_component[next(iter(ii))] if len(ii) == 1 else
               component_name_from_component[list(ii)].tolist() for ii in output]

    del group_index_from_atom, component_index_from_atom, component_name_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_type_from_component = item.components['component_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(component_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ component_type_from_component[next(iter(ii))] if len(ii) == 1 else
               component_type_from_component[list(ii)].tolist() for ii in output]

    del group_index_from_atom, component_index_from_atom, component_type_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_chain_index_from_group(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, chain_index_from_atom, aux_dict

    output = [ next(iter(ii)) if len(ii) == 1 else list(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_id_from_chain = item.chains['chain_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ chain_id_from_chain[next(iter(ii))] if len(ii) == 1 else
               chain_id_from_chain[list(ii)].tolist() for ii in output]

    del group_index_from_atom, chain_index_from_atom, chain_id_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_name_from_chain = item.chains['chain_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ chain_name_from_chain[next(iter(ii))] if len(ii) == 1 else
               chain_name_from_chain[list(ii)].tolist() for ii in output]

    del group_index_from_atom, chain_index_from_atom, chain_name_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_type_from_chain = item.chains['chain_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ chain_type_from_chain[next(iter(ii))] if len(ii) == 1 else
               chain_type_from_chain[list(ii)].tolist() for ii in output]

    del group_index_from_atom, chain_index_from_atom, chain_type_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_bond_index_from_group(item, indices='all', skip_digestion=False):

    atom_indices_from_group = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_group:
        if len(jj):
            output.append(sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))))
        else:
            output.append([])

    del atom_indices_from_group, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_bond_type_from_group(item, indices='all', skip_digestion=False):

    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)

    del bond_type, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bond_order_from_group(item, indices='all', skip_digestion=False):

    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)

    del bond_order, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_group(item, indices='all', skip_digestion=False):

    atom_indices_from_group = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_group:
        aux = sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj])))
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:,0], jj) & np.isin(pairs[:,1], jj)
            aux = list(compress(aux, mask))
        else:
            aux=[]
        output.append(aux)

    del atom_indices_from_group, bonded_atom_pairs, bond_indices_from_atom, pairs

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)
    atom_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)

    output = []
    for ii,jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))

    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_group(item, indices=indices, skip_digestion=True)

    if indices=='all':

        output = bonded_atom_pairs
    
    else:

        atom_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)

        output = []

        for ii,jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:,0], ii) | np.isin(jj[:,1], ii)
                output.append(jj[mask,:].tolist())

    return output


@arg_digest(form=form)
def get_n_atoms_from_group(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_group(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_group(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = item.groups.shape[0]
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_groups_from_group(item, indices='all', skip_digestion=False):

    return get_n_groups_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_molecules_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_group(item, indices='all', skip_digestion=False):

    return get_n_molecules_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_entities_from_group(item, indices='all', skip_digestion=False):

    return get_n_entities_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_group(item, indices='all', skip_digestion=False):

    output = get_component_index_from_group(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_components_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        aux = get_component_index_from_group(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output

@arg_digest(form=form)
def get_n_chains_from_group(item, indices='all', skip_digestion=False):

    output = get_chain_index_from_group(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_chains_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        aux = get_chain_index_from_group(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_bonds_from_group(item, indices='all', skip_digestion=False):

    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)
    output = [len(ii) for ii in bond_indices]
    del bond_indices

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        atom_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
        atom_indices = list(chain.from_iterable(atom_indices))
        output = get_total_n_bonds_from_atom(item, indices=atom_indices, skip_digestion=True)
        del atom_indices

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_group(item, indices='all', skip_digestion=False):

    inner_bond_indices = get_inner_bond_index_from_group(item, indices=indices, skip_digestion=True)
    output = [len(ii) for ii in inner_bond_indices]
    del inner_bond_indices

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        atom_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
        atom_indices = list(chain.from_iterable(atom_indices))
        output = get_total_n_inner_bonds_from_atom(item, indices=atom_indices, skip_digestion=True)
        del atom_indices

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('amino acid')

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_group(item, indices='all', skip_digestion=False):

    return get_n_amino_acids_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_nucleotides_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('nucleotide')

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_group(item, indices='all', skip_digestion=False):

    return get_n_nucleotides_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_ions_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('ion')

    return output


@arg_digest(form=form)
def get_total_n_ions_from_group(item, indices='all', skip_digestion=False):

    return get_n_ions_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_waters_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('water')

    return output


@arg_digest(form=form)
def get_total_n_waters_from_group(item, indices='all', skip_digestion=False):

    return get_n_waters_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_small_molecules_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('small molecule')

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_group(item, indices='all', skip_digestion=False):

    return get_n_small_molecules_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_lipids_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('lipid')

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_group(item, indices='all', skip_digestion=False):

    return get_n_lipids_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('saccharide')

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_group(item, indices='all', skip_digestion=False):

    return get_n_saccharides_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_peptides_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('peptide')

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_group(item, indices='all', skip_digestion=False):

    return get_n_peptides_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_proteins_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_proteins_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('protein')

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_group(item, indices='all', skip_digestion=False):

    return get_n_proteins_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_dnas_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_dnas_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('dna')

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_group(item, indices='all', skip_digestion=False):

    return get_n_dnas_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_rnas_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_rnas_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('rna')

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_group(item, indices='all', skip_digestion=False):

    return get_n_rnas_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_polysaccharides_from_group(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_polysaccharides_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('polysaccharide')

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_group(item, indices='all', skip_digestion=False):

    return get_n_polysaccharides_from_group(item, indices=indices, skip_digestion=True)


# From molecule

@arg_digest(form=form)
def get_atom_index_from_molecule(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(atom_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(atom_index)

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, molecule_index_from_group, molecule_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_molecule(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    atom_id_from_atom = item.atoms['atom_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(atom_id_from_atom[atom_index])

        output = [aux_dict[m] for m in sorted(aux_dict.keys())]

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(atom_id_from_atom[atom_index])

        output = list(aux_dict.values())

    del group_index_from_atom, molecule_index_from_atom, atom_id_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_name_from_molecule(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    atom_name_from_atom = item.atoms['atom_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(atom_name_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(atom_name_from_atom[atom_index])

        output = [aux_dict.get(m, []) for m in indices]

    del group_index_from_atom, molecule_index_from_atom, molecule_index_from_group, atom_name_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_type_from_molecule(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    atom_type_from_atom = item.atoms['atom_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(atom_type_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(atom_type_from_atom[atom_index])

        output = [aux_dict.get(m, []) for m in indices]

    del group_index_from_atom, molecule_index_from_atom, molecule_index_from_group, atom_type_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_group_index_from_molecule(item, indices='all', skip_digestion=False):

    molecule_index_from_group = item.groups['molecule_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            aux_dict[molecule_index].append(group_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(group_index)

        output = [aux_dict[m] for m in indices]

    del molecule_index_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_group_id_from_molecule(item, indices='all', skip_digestion=False):

    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    group_id_from_group = item.groups['group_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            aux_dict[molecule_index].append(group_id_from_group[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(group_id_from_group[group_index])

        output = [aux_dict[m] for m in indices]

    del molecule_index_from_group, group_id_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_group_name_from_molecule(item, indices='all', skip_digestion=False):

    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    group_name_from_group = item.groups['group_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            aux_dict[molecule_index].append(group_name_from_group[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(group_name_from_group[group_index])

        output = [aux_dict[m] for m in indices]

    del molecule_index_from_group, group_name_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_group_type_from_molecule(item, indices='all', skip_digestion=False):

    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    group_type_from_group = item.groups['group_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            aux_dict[molecule_index].append(group_type_from_group[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(group_type_from_group[group_index])

        output = [aux_dict[m] for m in indices]

    del molecule_index_from_group, group_type_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_index_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = list(range(item.molecules.shape[0]))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False):

    molecule_id_from_molecule = item.molecules['molecule_id'].to_numpy()

    if indices=='all':
        output = molecule_id_from_molecule.tolist()
    else:
        output = molecule_id_from_molecule[indices].tolist()

    del molecule_id_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    molecule_name_from_molecule = item.molecules['molecule_name'].to_numpy()

    if indices=='all':
        output = molecule_name_from_molecule.tolist()
    else:
        output = molecule_name_from_molecule[indices].tolist()

    del molecule_name_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    molecule_type_from_molecule = item.molecules['molecule_type'].to_numpy()

    if indices=='all':
        output = molecule_type_from_molecule.tolist()
    else:
        output = molecule_type_from_molecule[indices].tolist()

    del molecule_type_from_molecule

    return output


@arg_digest(form=form)
def get_entity_index_from_molecule(item, indices='all', skip_digestion=False):

    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()

    if indices=='all':
        output = entity_index_from_molecule.tolist()
    else:
        output = entity_index_from_molecule[indices].tolist()

    del entity_index_from_molecule

    return output


@arg_digest(form=form)
def get_entity_id_from_molecule(item, indices='all', skip_digestion=False):

    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    entity_id_from_entity = item.entities['entity_id'].to_numpy()

    if indices=='all':
        output = entity_index_from_molecule
    else:
        output = entity_index_from_molecule[indices]

    output = entity_id_from_entity[output].tolist()

    del entity_index_from_molecule, entity_id_from_entity

    return output


@arg_digest(form=form)
def get_entity_name_from_molecule(item, indices='all', skip_digestion=False):

    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    entity_name_from_entity = item.entities['entity_name'].to_numpy()

    if indices=='all':
        output = entity_index_from_molecule
    else:
        output = entity_index_from_molecule[indices]

    output = entity_name_from_entity[output].tolist()

    del entity_index_from_molecule, entity_name_from_entity

    return output


@arg_digest(form=form)
def get_entity_type_from_molecule(item, indices='all', skip_digestion=False):

    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    entity_type_from_entity = item.entities['entity_type'].to_numpy()

    if indices=='all':
        output = entity_index_from_molecule
    else:
        output = entity_index_from_molecule[indices]

    output = entity_type_from_entity[output].tolist()

    del entity_index_from_molecule, entity_type_from_entity

    return output


@arg_digest(form=form)
def get_component_index_from_molecule(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    component_index_from_atom = item.atoms['component_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(component_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    del group_index_from_atom, molecule_index_from_atom, component_index_from_atom, aux_dict

    output = [list(np.unique(ii)) for ii in output] 

    return output


@arg_digest(form=form)
def get_component_id_from_molecule(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_id_from_component = item.components['component_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(component_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [component_id_from_component[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_atom, component_index_from_atom, component_id_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_component_name_from_molecule(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_name_from_component = item.components['component_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(component_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [component_name_from_component[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_atom, component_index_from_atom, component_name_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_component_type_from_molecule(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_name_from_component = item.components['component_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(component_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [component_name_from_component[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_atom, component_index_from_atom, component_name_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_chain_index_from_molecule(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    del group_index_from_atom, molecule_index_from_atom, chain_index_from_atom, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii))
        for ii in output
    ]

    return output


@arg_digest(form=form)
def get_chain_id_from_molecule(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_id_from_chain = item.chains['chain_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [chain_id_from_chain[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_atom, chain_index_from_atom, chain_id_from_chain, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii))
        for ii in output
    ]

    return output


@arg_digest(form=form)
def get_chain_name_from_molecule(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_name_from_chain = item.chains['chain_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [chain_name_from_chain[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_atom, chain_index_from_atom, chain_name_from_chain, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii))
        for ii in output
    ]

    return output


@arg_digest(form=form)
def get_chain_type_from_molecule(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_type_from_chain = item.chains['chain_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [chain_type_from_chain[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_atom, chain_index_from_atom, chain_type_from_chain, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii))
        for ii in output
    ]

    return output


@arg_digest(form=form)
def get_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    atom_indices_from_molecule = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_molecule:
        if len(jj):
            output.append(sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))))
        else:
            output.append([])

    del atom_indices_from_molecule, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_bond_type_from_molecule(item, indices='all', skip_digestion=False):

    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)

    del bond_type, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bond_order_from_molecule(item, indices='all', skip_digestion=False):

    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)

    del bond_order, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    atom_indices_from_molecule = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_molecule:
        aux = sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj])))
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:,0], jj) & np.isin(pairs[:,1], jj)
            aux = list(compress(aux, mask))
        else:
            aux=[]
        output.append(aux)

    del atom_indices_from_molecule, bonded_atom_pairs, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)
    atom_indices = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii,jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))

    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_molecule(item, indices=indices, skip_digestion=True)

    if indices=='all':

        output = bonded_atom_pairs
    
    else:

        atom_indices = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)

        output = []

        for ii,jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:,0], ii) | np.isin(jj[:,1], ii)
                output.append(jj[mask,:].tolist())

    return output


@arg_digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    output = get_group_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        aux = get_n_groups_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    return get_n_molecules_from_molecule(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    return get_n_entities_from_molecule(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_molecule(item, indices='all', skip_digestion=False):

    output = get_component_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_components_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        aux = get_component_index_from_molecule(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    output = get_chain_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        aux = get_chain_index_from_molecule(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False): 

    output = get_bond_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_molecule(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    output = get_inner_bond_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        atom_indices = get_atom_index_from_molecule(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('amino acid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_amino_acids_from_system(item, skip_digestion=True)

    else:

        output = get_n_amino_acids_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('nucleotide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_nucleotides_from_system(item, skip_digestion=True)

    else:

        output = get_n_nucleotides_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('ion') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_ions_from_system(item, skip_digestion=True)

    else:

        output = get_n_ions_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('water') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_waters_from_system(item, skip_digestion=True)

    else:

        output = get_n_waters_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('small molecule') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_small_molecules_from_system(item, skip_digestion=True)

    else:

        output = get_n_small_molecules_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('lipid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_lipids_from_system(item, skip_digestion=True)

    else:

        output = get_n_lipids_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('saccharide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_saccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_saccharides_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = molecule_types.count('peptide')

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    output = get_n_peptides_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = molecule_types.count('protein')

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    output = get_n_proteins_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = molecule_types.count('polysaccharide')

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False):

    output = get_n_polysaccharides_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = molecule_types.count('dna')

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    output = get_n_dnas_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = molecule_types.count('rna')

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    output = get_n_rnas_from_molecule(item, indices=indices, skip_digestion=True)

    return output


# From entity


@arg_digest(form=form)
def get_atom_index_from_entity(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(atom_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(atom_index)

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_entity(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    atom_id_from_atom = item.atoms['atom_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(atom_id_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(atom_id_from_atom[atom_index])

        output = list(aux_dict.values())

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, atom_id_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_name_from_entity(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    atom_name_from_atom = item.atoms['atom_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(atom_name_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(atom_name_from_atom[atom_index])

        output = list(aux_dict.values())

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, atom_name_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_type_from_entity(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    atom_type_from_atom = item.atoms['atom_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(atom_type_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(atom_type_from_atom[atom_index])

        output = list(aux_dict.values())

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, atom_type_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_group_index_from_entity(item, indices='all', skip_digestion=False):

    molecule_index_from_group     = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule     = item.molecules['entity_index'].to_numpy()
    entity_index_from_group   = entity_index_from_molecule[molecule_index_from_group]

    if indices == 'all':

        aux_dict = defaultdict(list)
        for group_index, entity_index in enumerate(entity_index_from_group):
            aux_dict[entity_index].append(group_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, entity_index in enumerate(entity_index_from_group):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(group_index)

        output = [aux_dict[ii] for ii in indices]

    del molecule_index_from_group, entity_index_from_molecule, entity_index_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_group_id_from_entity(item, indices='all', skip_digestion=False):

    molecule_index_from_group     = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule     = item.molecules['entity_index'].to_numpy()
    entity_index_from_group   = entity_index_from_molecule[molecule_index_from_group]
    group_id_from_group = item.groups['group_id'].to_numpy()

    if indices == 'all':

        aux_dict = defaultdict(list)
        for group_index, entity_index in enumerate(entity_index_from_group):
            aux_dict[entity_index].append(group_id_from_group[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, entity_index in enumerate(entity_index_from_group):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(group_id_from_group[group_index])

        output = [aux_dict[ii] for ii in indices]

    del molecule_index_from_group, entity_index_from_molecule, entity_index_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_group_name_from_entity(item, indices='all', skip_digestion=False):

    molecule_index_from_group     = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule     = item.molecules['entity_index'].to_numpy()
    entity_index_from_group   = entity_index_from_molecule[molecule_index_from_group]
    group_name_from_group = item.groups['group_name'].to_numpy()

    if indices == 'all':

        aux_dict = defaultdict(list)
        for group_index, entity_index in enumerate(entity_index_from_group):
            aux_dict[entity_index].append(group_name_from_group[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, entity_index in enumerate(entity_index_from_group):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(group_name_from_group[group_index])

        output = [aux_dict[ii] for ii in indices]

    del molecule_index_from_group, entity_index_from_molecule, entity_index_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_group_type_from_entity(item, indices='all', skip_digestion=False):

    molecule_index_from_group     = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule     = item.molecules['entity_index'].to_numpy()
    entity_index_from_group   = entity_index_from_molecule[molecule_index_from_group]
    group_type_from_group = item.groups['group_type'].to_numpy()

    if indices == 'all':

        aux_dict = defaultdict(list)
        for group_index, entity_index in enumerate(entity_index_from_group):
            aux_dict[entity_index].append(group_type_from_group[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, entity_index in enumerate(entity_index_from_group):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(group_type_from_group[group_index])

        output = [aux_dict[ii] for ii in indices]

    del molecule_index_from_group, entity_index_from_molecule, entity_index_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_index_from_entity(item, indices='all', skip_digestion=False):

    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            aux_dict[entity_index].append(molecule_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(molecule_index)

        output = [aux_dict[m] for m in indices]

    del entity_index_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_id_from_entity(item, indices='all', skip_digestion=False):

    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_id_from_molecule = item.molecules['molecule_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            aux_dict[entity_index].append(molecule_id_from_molecule[molecule_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(molecule_id_from_molecule[molecule_index])

        output = [aux_dict[m] for m in indices]

    del entity_index_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_name_from_entity(item, indices='all', skip_digestion=False):

    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_name_from_molecule = item.molecules['molecule_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            aux_dict[entity_index].append(molecule_name_from_molecule[molecule_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(molecule_name_from_molecule[molecule_index])

        output = [aux_dict[m] for m in indices]

    del entity_index_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_type_from_entity(item, indices='all', skip_digestion=False):

    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_type_from_molecule = item.molecules['molecule_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            aux_dict[entity_index].append(molecule_type_from_molecule[molecule_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(molecule_type_from_molecule[molecule_index])

        output = [aux_dict[m] for m in indices]

    del entity_index_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_entity_index_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = list(range(item.entities.shape[0]))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):

    entity_id_from_entity = item.entities['entity_id'].to_numpy()

    if indices=='all':
        output = entity_id_from_entity.tolist()
    else:
        output = entity_id_from_entity[indices].tolist()

    del entity_id_from_entity

    return output


@arg_digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    entity_name_from_entity = item.entities['entity_name'].to_numpy()

    if indices=='all':
        output = entity_name_from_entity.tolist()
    else:
        output = entity_name_from_entity[indices].tolist()

    del entity_name_from_entity

    return output


@arg_digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    entity_type_from_entity = item.entities['entity_type'].to_numpy()

    if indices=='all':
        output = entity_type_from_entity.tolist()
    else:
        output = entity_type_from_entity[indices].tolist()

    del entity_type_from_entity

    return output


@arg_digest(form=form)
def get_component_index_from_entity(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    component_index_from_atom = item.atoms['component_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(component_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, component_index_from_atom, aux_dict

    output = [list(np.unique(ii)) for ii in output] 

    return output


@arg_digest(form=form)
def get_component_id_from_entity(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_id_from_component = item.components['component_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(component_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [component_id_from_component[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, component_index_from_atom, aux_dict
    del component_id_from_component

    return output


@arg_digest(form=form)
def get_component_name_from_entity(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_name_from_component = item.components['component_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(component_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [component_name_from_component[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, component_index_from_atom, aux_dict
    del component_name_from_component

    return output


@arg_digest(form=form)
def get_component_type_from_entity(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_type_from_component = item.components['component_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(component_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [component_type_from_component[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, component_index_from_atom, aux_dict
    del component_type_from_component

    return output


@arg_digest(form=form)
def get_chain_index_from_entity(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, chain_index_from_atom, aux_dict

    output = [list(np.unique(ii)) for ii in output] 

    return output


@arg_digest(form=form)
def get_chain_id_from_entity(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_id_from_chain = item.chains['chain_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [chain_id_from_chain[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, chain_index_from_atom, aux_dict
    del chain_id_from_chain

    return output


@arg_digest(form=form)
def get_chain_name_from_entity(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_name_from_chain = item.chains['chain_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [chain_name_from_chain[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, chain_index_from_atom, aux_dict
    del chain_name_from_chain

    return output


@arg_digest(form=form)
def get_chain_type_from_entity(item, indices='all', skip_digestion=False):

    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_type_from_chain = item.chains['chain_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [chain_type_from_chain[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, chain_index_from_atom, aux_dict
    del chain_type_from_chain

    return output


@arg_digest(form=form)
def get_bond_index_from_entity(item, indices='all', skip_digestion=False):

    atom_indices_from_entity = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_entity:
        if len(jj):
            output.append(sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))))
        else:
            output.append([])

    del atom_indices_from_entity, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_bond_type_from_entity(item, indices='all', skip_digestion=False):

    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)

    del bond_type, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bond_order_from_entity(item, indices='all', skip_digestion=False):

    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)

    del bond_order, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_entity(item, indices='all', skip_digestion=False):

    atom_indices_from_entity = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_entity:
        aux = sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj])))
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:,0], jj) & np.isin(pairs[:,1], jj)
            aux = list(compress(aux, mask))
        else:
            aux=[]
        output.append(aux)

    del atom_indices_from_entity, bonded_atom_pairs, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(item, indices=indices, skip_digestion=True)
    atom_indices = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)

    output = []
    for ii,jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))

    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_entity(item, indices=indices, skip_digestion=True)

    if indices=='all':

        output = bonded_atom_pairs
    
    else:

        atom_indices = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)

        output = []

        for ii,jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:,0], ii) | np.isin(jj[:,1], ii)
                output.append(jj[mask,:].tolist())

    return output


@arg_digest(form=form)
def get_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):

    output = get_group_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_groups_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        aux = get_n_groups_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    output = get_molecule_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        aux = get_n_molecules_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_entities_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_entities_from_system(item)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_entities_from_entity(item, indices='all', skip_digestion=False):

    return get_n_entities_from_molecule(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_entity(item, indices='all', skip_digestion=False):

    output = get_component_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_components_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        aux = get_component_index_from_entity(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_chains_from_entity(item, indices='all', skip_digestion=False):

    output = get_chain_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_chains_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        aux = get_chain_index_from_entity(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    output = get_bond_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_entity(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    output = get_inner_bond_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        atom_indices = get_atom_index_from_entity(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('amino acid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_amino_acids_from_system(item, skip_digestion=True)

    else:

        output = get_n_amino_acids_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('nucleotide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_nucleotides_from_system(item, skip_digestion=True)

    else:

        output = get_n_nucleotides_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_ions_from_entity(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('ion') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_ions_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_ions_from_system(item, skip_digestion=True)

    else:

        output = get_n_ions_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_waters_from_entity(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('water') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_waters_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_waters_from_system(item, skip_digestion=True)

    else:

        output = get_n_waters_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('small molecule') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_small_molecules_from_system(item, skip_digestion=True)

    else:

        output = get_n_small_molecules_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('lipid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_lipids_from_system(item, skip_digestion=True)

    else:

        output = get_n_lipids_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('saccharide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_saccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_saccharides_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('peptide') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_peptides_from_system(item, skip_digestion=True)

    else:

        output = get_n_peptides_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('protein') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_proteins_from_system(item, skip_digestion=True)

    else:

        output = get_n_proteins_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_entity(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('polysaccharide') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_polysaccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_polysaccharides_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('dna') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_dnas_from_system(item, skip_digestion=True)

    else:

        output = get_n_dnas_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('rna') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_rnas_from_system(item, skip_digestion=True)

    else:

        output = get_n_rnas_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


# From component


@arg_digest(form=form)
def get_atom_index_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].append(atom_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].append(atom_index)

        output = [aux_dict[m] for m in indices]

    del component_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    atom_id_from_atom = item.atoms['atom_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].append(atom_id_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].append(atom_id_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del component_index_from_atom, atom_id_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_name_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    atom_name_from_atom = item.atoms['atom_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].append(atom_name_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].append(atom_name_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del component_index_from_atom, atom_name_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_type_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    atom_type_from_atom = item.atoms['atom_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].append(atom_type_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].append(atom_type_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del component_index_from_atom, atom_type_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_group_index_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(group_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            component_index = component_index_from_atom[atom_index]
            if component_index in aux_dict:
                aux_dict[component_index].add(group_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, component_index_from_atom, aux_dict

    output = [list(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_group_id_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    group_id_from_group = item.groups['group_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(group_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(group_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [group_id_from_group[sorted(ii)].tolist() for ii in output]

    del group_index_from_atom, component_index_from_atom, group_id_from_group
    del aux_dict

    return output


@arg_digest(form=form)
def get_group_name_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    group_name_from_group = item.groups['group_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(group_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(group_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [group_name_from_group[sorted(ii)].tolist() for ii in output]

    del group_index_from_atom, component_index_from_atom, group_name_from_group
    del aux_dict

    return output


@arg_digest(form=form)
def get_group_type_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    group_type_from_group = item.groups['group_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(group_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(group_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [group_type_from_group[sorted(ii)].tolist() for ii in output]

    del group_index_from_atom, component_index_from_atom, group_type_from_group
    del aux_dict

    return output


@arg_digest(form=form)
def get_molecule_index_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(molecule_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(molecule_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ next(iter(ii)) if len(ii) == 1 else sorted(ii) for ii in output]

    del component_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_id_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    molecule_id_from_molecule = item.molecules['molecule_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(molecule_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(molecule_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ molecule_id_from_molecule[next(iter(ii))] if len(ii) == 1 else molecule_id_from_molecule[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_id_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_name_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    molecule_name_from_molecule = item.molecules['molecule_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(molecule_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(molecule_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ molecule_name_from_molecule[next(iter(ii))] if len(ii) == 1 else molecule_name_from_molecule[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_name_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_type_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom.astype(int)]
    molecule_type_from_molecule = item.molecules['molecule_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(molecule_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(molecule_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [molecule_type_from_molecule[next(iter(ii))] if len(ii) == 1 else molecule_type_from_molecule[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_type_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_entity_index_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(entity_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(entity_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ next(iter(ii)) if len(ii) == 1 else sorted(ii) for ii in output]

    del component_index_from_atom, entity_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_entity_id_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_id_from_entity = item.entities['entity_id'].to_numpy()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(entity_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(entity_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ entity_id_from_entity[next(iter(ii))] if len(ii) == 1 else entity_id_from_entity[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, entity_index_from_atom, entity_id_from_entity, aux_dict

    return output


@arg_digest(form=form)
def get_entity_name_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_name_from_entity = item.entities['entity_name'].to_numpy()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(entity_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(entity_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ entity_name_from_entity[next(iter(ii))] if len(ii) == 1 else entity_name_from_entity[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, entity_index_from_atom, entity_name_from_entity, aux_dict

    return output


@arg_digest(form=form)
def get_entity_type_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_type_from_entity = item.entities['entity_type'].to_numpy()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(entity_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(entity_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ entity_type_from_entity[next(iter(ii))] if len(ii) == 1 else entity_type_from_entity[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, entity_index_from_atom, entity_type_from_entity, aux_dict

    return output


@arg_digest(form=form)
def get_component_index_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = list(range(item.components.shape[0]))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False):

    component_id_from_component = item.components['component_id'].to_numpy()

    if indices=='all':
        output = component_id_from_component.tolist()
    else:
        output = component_id_from_component[indices].tolist()

    del component_id_from_component

    return output


@arg_digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    component_name_from_component = item.components['component_name'].to_numpy()

    if indices=='all':
        output = component_name_from_component.tolist()
    else:
        output = component_name_from_component[indices].tolist()

    del component_name_from_component

    return output


@arg_digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    component_type_from_component = item.components['component_type'].to_numpy()

    if indices=='all':
        output = component_type_from_component.tolist()
    else:
        output = component_type_from_component[indices].tolist()

    del component_type_from_component

    return output


@arg_digest(form=form)
def get_chain_index_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(chain_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ next(iter(ii)) if len(ii) == 1 else sorted(ii) for ii in output]

    del component_index_from_atom, chain_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_chain_id_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_id_from_chain = item.chains['chain_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(chain_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ chain_id_from_chain[next(iter(ii))] if len(ii) == 1 else chain_id_from_chain[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, chain_index_from_atom, chain_id_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_chain_name_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_name_from_chain = item.chains['chain_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(chain_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ chain_name_from_chain[next(iter(ii))] if len(ii) == 1 else chain_name_from_chain[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, chain_index_from_atom, chain_name_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_chain_type_from_component(item, indices='all', skip_digestion=False):

    component_index_from_atom = item.atoms['component_index'].to_numpy()
    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    chain_type_from_chain = item.chains['chain_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(chain_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [chain_type_from_chain[next(iter(ii))] if len(ii) == 1 else chain_type_from_chain[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, chain_index_from_atom, chain_type_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_bond_index_from_component(item, indices='all', skip_digestion=False):

    atom_indices_from_component = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_component:
        if len(jj):
            output.append(sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))))
        else:
            output.append([])

    del atom_indices_from_component, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_bond_type_from_component(item, indices='all', skip_digestion=False):

    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)

    del bond_type, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bond_order_from_component(item, indices='all', skip_digestion=False):

    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)

    del bond_order, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_component(item, indices='all', skip_digestion=False):

    atom_indices_from_component = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_component:
        aux = sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj])))
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:,0], jj) & np.isin(pairs[:,1], jj)
            aux = list(compress(aux, mask))
        else:
            aux=[]
        output.append(aux)

    del atom_indices_from_component, bonded_atom_pairs, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(item, indices=indices, skip_digestion=True)
    atom_indices = get_atom_index_from_component(item, indices=indices, skip_digestion=True)

    output = []
    for ii,jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))

    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_component(item, indices=indices, skip_digestion=True)

    if indices=='all':

        output = bonded_atom_pairs
    
    else:

        atom_indices = get_atom_index_from_component(item, indices=indices, skip_digestion=True)

        output = []

        for ii,jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:,0], ii) | np.isin(jj[:,1], ii)
                output.append(jj[mask,:].tolist())

    return output


@arg_digest(form=form)
def get_n_atoms_from_component(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_component(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_component(item, indices='all', skip_digestion=False):

    output = get_group_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_groups_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        aux = get_group_index_from_component(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_molecules_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_component(item, indices='all', skip_digestion=False):

    return get_n_molecules_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_entities_from_component(item, indices='all', skip_digestion=False):

    return get_n_entities_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = item.components.shape[0]
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_components_from_component(item, indices='all', skip_digestion=False):

    return get_n_components_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_chains_from_component(item, indices='all', skip_digestion=False):

    output = get_chain_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_chains_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        aux = get_chain_index_from_component(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_bonds_from_component(item, indices='all', skip_digestion=False):

    output = get_bond_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_component(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    output = get_bond_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_component(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_component(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('amino acid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_amino_acids_from_system(item, skip_digestion=True)

    else:

        output = get_n_amino_acids_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('nucleotide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_nucleotides_from_system(item, skip_digestion=True)

    else:

        output = get_n_nucleotides_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_ions_from_component(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('ion') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_ions_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_ions_from_system(item, skip_digestion=True)

    else:

        output = get_n_ions_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_waters_from_component(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('water') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_waters_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_waters_from_system(item, skip_digestion=True)

    else:

        output = get_n_waters_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('small molecule') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_small_molecules_from_system(item, skip_digestion=True)

    else:

        output = get_n_small_molecules_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_lipids_from_component(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('lipid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_lipids_from_system(item, skip_digestion=True)

    else:

        output = get_n_lipids_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('saccharide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_saccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_saccharides_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_polysaccharides_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('polysaccharide')

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_component(item, indices='all', skip_digestion=False):

    return get_n_polysaccharides_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_peptides_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('peptide')

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_component(item, indices='all', skip_digestion=False):

    return get_n_peptides_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_proteins_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_proteins_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('protein')

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_component(item, indices='all', skip_digestion=False):

    return get_n_proteins_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_dnas_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_dnas_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('dna')

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_component(item, indices='all', skip_digestion=False):

    return get_n_dnas_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_rnas_from_component(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_rnas_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('rna')

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_component(item, indices='all', skip_digestion=False):

    return get_n_rnas_from_component(item, indices=indices, skip_digestion=True)


# From chain


@arg_digest(form=form)
def get_atom_index_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].append(atom_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].append(atom_index)

        output = [aux_dict[m] for m in indices]

    del chain_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    atom_id_from_atom = item.atoms['atom_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].append(atom_id_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].append(atom_id_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del chain_index_from_atom, atom_id_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_name_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    atom_name_from_atom = item.atoms['atom_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].append(atom_name_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].append(atom_name_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del chain_index_from_atom, atom_name_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_type_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    atom_type_from_atom = item.atoms['atom_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].append(atom_type_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].append(atom_type_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del chain_index_from_atom, atom_type_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_group_index_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(group_index_from_atom[atom_index].tolist())

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(group_index_from_atom[atom_index].tolist())

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, chain_index_from_atom, aux_dict

    output = [list(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_group_id_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    group_id_from_group = item.groups['group_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [group_id_from_group[sorted(ii)].tolist() for ii in output]

    del group_index_from_atom, chain_index_from_atom, group_id_from_group
    del aux_dict

    return output


@arg_digest(form=form)
def get_group_name_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    group_name_from_group = item.groups['group_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [group_name_from_group[sorted(ii)].tolist() for ii in output]

    del group_index_from_atom, chain_index_from_atom, group_name_from_group
    del aux_dict

    return output


@arg_digest(form=form)
def get_group_type_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    group_type_from_group = item.groups['group_type'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [group_type_from_group[sorted(ii)].tolist() for ii in output]

    del group_index_from_atom, chain_index_from_atom, group_type_from_group
    del aux_dict

    return output


@arg_digest(form=form)
def get_molecule_index_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]

    if indices =='all':
        from molsysmt.form.molsysmt_Topology.get_topological_attributes import get_n_chains_from_system
        n_chains = get_n_chains_from_system(item)
        indices = range(n_chains)

    aux_dict = {ii: set() for ii in indices}
    for atom_index, chain_index in enumerate(chain_index_from_atom):
        if chain_index in aux_dict:
            aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

    output = [aux_dict[m] for m in indices]

    aux_list = output
    output = []
    for ii in aux_list:
        clean_ii = [int(jj) for jj in ii if jj is not None and not pd.isna(jj)]
        output.append(sorted(clean_ii))

    del chain_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_id_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    molecule_id_from_molecule = item.molecules['molecule_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ molecule_id_from_molecule[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_id_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_name_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    molecule_name_from_molecule = item.molecules['molecule_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ molecule_name_from_molecule[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_name_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_type_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom.astype(int)]
    molecule_type_from_molecule = item.molecules['molecule_type'].to_numpy()

    if indices =='all':
        from molsysmt.form.molsysmt_Topology.get_topological_attributes import get_n_chains_from_system
        n_chains = get_n_chains_from_system(item)
        indices = range(n_chains)

    aux_dict = {ii: set() for ii in indices}
    for atom_index, chain_index in enumerate(chain_index_from_atom):
        if chain_index in aux_dict:
            aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

    output = [aux_dict[m] for m in indices]

    aux_list = output
    output = []
    for ii in aux_list:
        clean_ii = [int(jj) for jj in ii if jj is not None and not pd.isna(jj)]
        if clean_ii:
            output.append(molecule_type_from_molecule[sorted(clean_ii)].tolist())
        else:
            output.append([])

    del chain_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_type_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_entity_index_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(entity_index_from_atom[atom_index].tolist())

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(entity_index_from_atom[atom_index].tolist())

        output = [aux_dict[m] for m in indices]

    output = [ sorted(ii) for ii in output]

    del chain_index_from_atom, entity_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_entity_id_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_id_from_entity = item.entities['entity_id'].to_numpy()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [entity_id_from_entity[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, entity_index_from_atom, entity_id_from_entity, aux_dict

    return output


@arg_digest(form=form)
def get_entity_name_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_name_from_entity = item.entities['entity_name'].to_numpy()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [entity_name_from_entity[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, entity_index_from_atom, entity_name_from_entity, aux_dict

    return output


@arg_digest(form=form)
def get_entity_type_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    group_index_from_atom = item.atoms['group_index'].to_numpy()
    molecule_index_from_group = item.groups['molecule_index'].to_numpy()
    entity_index_from_molecule = item.molecules['entity_index'].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_type_from_entity = item.entities['entity_type'].to_numpy()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [entity_type_from_entity[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, entity_index_from_atom, entity_type_from_entity, aux_dict

    return output


@arg_digest(form=form)
def get_component_index_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    component_index_from_atom = item.atoms['component_index'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(component_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [sorted(ii) for ii in output]

    del chain_index_from_atom, component_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_component_id_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_id_from_component = item.components['component_id'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(component_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [component_id_from_component[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, component_index_from_atom, component_id_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_component_name_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_name_from_component = item.components['component_name'].to_numpy()

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            chain_index = chain_index_from_atom[atom_index]
            if chain_index in aux_dict:
                aux_dict[chain_index].add(component_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [component_name_from_component[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, component_index_from_atom, component_name_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_component_type_from_chain(item, indices='all', skip_digestion=False):

    chain_index_from_atom = item.atoms['chain_index'].to_numpy()
    component_index_from_atom = item.atoms['component_index'].to_numpy()
    component_type_from_component = item.components['component_type'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(component_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(component_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [component_type_from_component[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, component_index_from_atom, component_type_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_chain_index_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = list(range(item.chains.shape[0]))
    else:
        output = indices

    return output

@arg_digest(form=form)
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):

    chain_id_from_chain = item.chains['chain_id'].to_numpy()

    if indices=='all':
        output = chain_id_from_chain.tolist()
    else:
        output = chain_id_from_chain[indices].tolist()

    del chain_id_from_chain

    return output


@arg_digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    chain_name_from_chain = item.chains['chain_name'].to_numpy()

    if indices=='all':
        output = chain_name_from_chain.tolist()
    else:
        output = chain_name_from_chain[indices].tolist()

    del chain_name_from_chain

    return output


@arg_digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    chain_type_from_chain = item.chains['chain_type'].to_numpy()

    if indices=='all':
        output = chain_type_from_chain.tolist()
    else:
        output = chain_type_from_chain[indices].tolist()

    del chain_type_from_chain

    return output


@arg_digest(form=form)
def get_bond_index_from_chain(item, indices='all', skip_digestion=False):

    atom_indices_from_chain = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_chain:
        if len(jj):
            output.append(sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))))
        else:
            output.append([])

    del atom_indices_from_chain, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_bond_type_from_chain(item, indices='all', skip_digestion=False):

    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_chain(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)

    del bond_type, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bond_order_from_chain(item, indices='all', skip_digestion=False):

    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_chain(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)

    del bond_order, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_chain(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_chain(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_chain(item, indices='all', skip_digestion=False):

    atom_indices_from_chain = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_chain:
        aux = sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj])))
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:,0], jj) & np.isin(pairs[:,1], jj)
            aux = list(compress(aux, mask))
        else:
            aux=[]
        output.append(aux)

    del atom_indices_from_chain, bonded_atom_pairs, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_chain(item, indices=indices, skip_digestion=True)
    atom_indices = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)

    output = []
    for ii,jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))

    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    bonded_atom_pairs = get_bonded_atom_pairs_from_chain(item, indices=indices, skip_digestion=True)

    if indices=='all':

        output = bonded_atom_pairs
    
    else:

        atom_indices = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)

        output = []

        for ii,jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:,0], ii) | np.isin(jj[:,1], ii)
                output.append(jj[mask,:].tolist())

    return output


@arg_digest(form=form)
def get_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_chain(item, indices='all', skip_digestion=False):

    output = get_group_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_groups_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        aux = get_group_index_from_chain(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    output = get_molecule_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        aux = get_molecule_index_from_chain(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_entities_from_chain(item, indices='all', skip_digestion=False):

    output = get_entity_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_entities_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        aux = get_entity_index_from_chain(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output

@arg_digest(form=form)
def get_n_components_from_chain(item, indices='all', skip_digestion=False):

    aux = get_component_index_from_chain(item, indices, skip_digestion=True)
    output = []
    for ii in aux:
        try:
            output.append(len(ii))
        except Exception:
            output.append(1)

    return output


@arg_digest(form=form)
def get_total_n_components_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        aux = get_component_index_from_chain(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_chains_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = item.chains.shape[0]
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_chains_from_chain(item, indices='all', skip_digestion=False):

    return get_n_chains_from_chain(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    output = get_bond_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_chain(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    output = get_bond_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_chain(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('amino acid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_amino_acids_from_system(item, skip_digestion=True)

    else:

        output = get_n_amino_acids_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('nucleotide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_nucleotides_from_system(item, skip_digestion=True)

    else:

        output = get_n_nucleotides_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_ions_from_chain(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('ion') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_ions_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_ions_from_system(item, skip_digestion=True)

    else:

        output = get_n_ions_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_waters_from_chain(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('water') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_waters_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_waters_from_system(item, skip_digestion=True)

    else:

        output = get_n_waters_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('small molecule') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_small_molecules_from_system(item, skip_digestion=True)

    else:

        output = get_n_small_molecules_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_lipids_from_chain(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('lipid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_lipids_from_system(item, skip_digestion=True)

    else:

        output = get_n_lipids_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_chain(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('saccharide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_saccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_saccharides_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_chain(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('polysaccharide') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_polysaccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_polysaccharides_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_peptides_from_chain(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('peptide') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_peptides_from_system(item, skip_digestion=True)

    else:

        output = get_n_peptides_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_proteins_from_chain(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('protein') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_proteins_from_system(item, skip_digestion=True)

    else:

        output = get_n_proteins_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_dnas_from_chain(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('dna') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_dnas_from_system(item, skip_digestion=True)

    else:

        output = get_n_dnas_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_rnas_from_chain(item, indices='all', skip_digestion=False):

    molecule_types = get_molecule_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('rna') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_chain(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = get_n_rnas_from_system(item, skip_digestion=True)

    else:

        output = get_n_rnas_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


# From bond


@arg_digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    if indices=='all':
        n_aux = get_n_bonds_from_system(item)
        output = np.arange(n_aux, dtype=int).tolist()
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    if 'order' in item.bonds:

        if indices=='all':
            output = item.bonds['order'].to_list()
        else:
            output = item.bonds['order'][indices].to_list()

    else:

        if indices=='all':
            n_aux = get_n_bonds_from_system(item, skip_digestion=True)
            output = [None] * n_aux
        else:
            output = [None] * len(indices)

    return output


@arg_digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    if 'type' in item.bonds:

        if indices=='all':
            output = item.bonds['type'].to_list()
        else:
            output = item.bonds['type'][indices].to_list()

    else:

        if indices=='all':
            n_aux = get_n_bonds_from_system(item, skip_digestion=True)
            output = [None] * n_aux
        else:
            output = [None] * len(indices)

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = np.unique([item.bonds.atom1_index, item.bonds.atom2_index]).tolist()

    else:

        output = [[bond.atom1_index, bond.atom2_index] for bond in item.bonds.iloc[indices].itertuples(index=False)]
        output = np.unique(output).tolist()

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_bond(item, indices='all', skip_digestion=False):

    if indices=='all':

        output = [[bond.atom1_index, bond.atom2_index] for bond in item.bonds.itertuples(index=False)]

    else:

        output = [[bond.atom1_index, bond.atom2_index] for bond in item.bonds.iloc[indices].itertuples(index=False)]

    return output


@arg_digest(form=form)
def get_n_bonds_from_bond(item, indices='all', skip_digestion=False):

    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


# From system


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    return item.atoms.shape[0]


@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    return item.groups.shape[0]


@arg_digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    if item.groups['molecule_index'].isnull().any():
        item.rebuild_molecules()

    return item.molecules.shape[0]


@arg_digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    if item.molecules['entity_index'].isnull().any():
        item.rebuild_entities()

    return item.entities.shape[0]


@arg_digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    if item.atoms['component_index'].isnull().any():
        item.rebuild_components()

    return item.components.shape[0]


@arg_digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    return item.chains.shape[0]


@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    return item.bonds.shape[0]


@arg_digest(form=form)
def get_n_amino_acids_from_system(item, skip_digestion=False):

    output = item.groups['group_type'].tolist().count('amino acid')

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_system(item, skip_digestion=False):

    output = item.groups['group_type'].tolist().count('nucleotide')

    return output


@arg_digest(form=form)
def get_n_ions_from_system(item, skip_digestion=False):

    output = item.groups['group_type'].tolist().count('ion')

    return output


@arg_digest(form=form)
def get_n_waters_from_system(item, skip_digestion=False):

    output = item.groups['group_type'].tolist().count('water')

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_system(item, skip_digestion=False):

    output = item.groups['group_type'].tolist().count('small molecule')

    return output


@arg_digest(form=form)
def get_n_lipids_from_system(item, skip_digestion=False):

    output = item.groups['group_type'].tolist().count('lipid')

    return output


@arg_digest(form=form)
def get_n_saccharides_from_system(item, skip_digestion=False):

    output = item.groups['group_type'].tolist().count('saccharide')

    return output


@arg_digest(form=form)
def get_n_peptides_from_system(item, skip_digestion=False):

    output = item.molecules['molecule_type'].tolist().count('peptide')

    return output


@arg_digest(form=form)
def get_n_proteins_from_system(item, skip_digestion=False):

    output = item.molecules['molecule_type'].tolist().count('protein')

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_system(item, skip_digestion=False):

    output = item.molecules['molecule_type'].tolist().count('polysaccharide')

    return output


@arg_digest(form=form)
def get_n_dnas_from_system(item, skip_digestion=False):

    output = item.molecules['molecule_type'].tolist().count('dna')

    return output


@arg_digest(form=form)
def get_n_rnas_from_system(item, skip_digestion=False):

    output = item.molecules['molecule_type'].tolist().count('rna')

    return output


@arg_digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):

    return get_bond_index_from_bond(item, skip_digestion=True)


@arg_digest(form=form)
def get_inner_bonded_atoms_from_system(item, skip_digestion=False):

    return get_bonded_atoms_from_bond(item, skip_digestion=True)


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_system(item, skip_digestion=False):

    return get_bonded_atom_pairs_from_bond(item, skip_digestion=True)


@arg_digest(form=form)
def get_bonded_atoms_from_system(item, skip_digestion=False):

    return get_bonded_atoms_from_bond(item, skip_digestion=True)


@arg_digest(form=form)
def get_bonded_atom_pairs_from_system(item, skip_digestion=False):

    return get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
   

# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

