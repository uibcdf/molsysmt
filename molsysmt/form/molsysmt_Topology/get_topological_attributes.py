from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import pandas as pd
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
import types
from networkx import Graph
from collections import defaultdict
from itertools import chain, compress

form = 'molsysmt.Topology'


#######################################################################
#                 To be customized for each form                      #
#######################################################################

# From atom


@digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = list(range(item.atoms.shape[0]))
    else:
        output = indices

    return output


@digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.atoms['atom_id'].to_list()
    else:
        output = item.atoms['atom_id'].take(indices).to_list()

    return output


@digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.atoms['atom_name'].to_list()
    else:
        output = item.atoms['atom_name'].take(indices).to_list()

    return output


@digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.atoms['atom_type'].to_list()
    else:
        output = item.atoms['atom_type'].take(indices).to_list()

    return output


@digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.atoms['group_index'].to_list()
    else:
        output = item.atoms['group_index'].take(indices).to_list()

    return output


@digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        group_indices = item.atoms['group_index']
    else:
        group_indices = item.atoms['group_index'].take(indices)

    output = item.groups['group_id'].take(group_indices).to_list()

    del group_indices

    return output


@digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        group_indices = item.atoms['group_index']
    else:
        group_indices = item.atoms['group_index'].take(indices)

    output = item.groups['group_name'].take(group_indices).to_list()

    del group_indices

    return output


@digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        group_indices = item.atoms['group_index']
    else:
        group_indices = item.atoms['group_index'].take(indices)

    output = item.groups['group_type'].take(group_indices).to_list()

    del group_indices

    return output


#@digest(form=form)
#def get_molecule_index_from_atom(item, indices='all', skip_digestion=False): ##x
#
#    if is_all(indices):
#        group_indices = item.atoms['group_index']
#    else:
#        group_indices = item.atoms['group_index'].take(indices)
#
#    output = item.groups['molecule_index'].take(group_indices).to_list()
#
#    del group_indices
#
#    return output


@digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False): ##x

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


@digest(form=form)
def get_molecule_id_from_atom(item, indices='all', skip_digestion=False): ##x

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


@digest(form=form)
def get_molecule_name_from_atom(item, indices='all', skip_digestion=False): ##x

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


@digest(form=form)
def get_molecule_type_from_atom(item, indices='all', skip_digestion=False): ##x

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

    del group_index_from_atom, molecule_index_from_group, molecule_name_from_molecule

    return output


@digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False): ##x

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


@digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False): ##x

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


@digest(form=form)
def get_entity_name_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        group_indices = item.atoms['group_index']
    else:
        group_indices = item.atoms['group_index'].take(indices)

    molecule_indices = item.groups['molecule_index'].take(group_indices)
    entity_indices = item.molecules['entity_index'].take(molecule_indices)
    output = item.entities['entity_name'].take(entity_indices).to_list()

    del group_indices, molecule_indices, entity_indices

    return output


@digest(form=form)
def get_entity_type_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        group_indices = item.atoms['group_index']
    else:
        group_indices = item.atoms['group_index'].take(indices)

    molecule_indices = item.groups['molecule_index'].take(group_indices)
    entity_indices = item.molecules['entity_index'].take(molecule_indices)
    output = item.entities['entity_type'].take(entity_indices).to_list()

    del group_indices, molecule_indices, entity_indices

    return output


@digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.atoms['component_index'].to_list()
    else:
        output = item.atoms['component_index'].take(indices).to_list()

    return output


@digest(form=form)
def get_component_id_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        component_indices = item.atoms['component_index']
    else:
        component_indices = item.atoms['component_index'].take(indices)

    output = item.components['component_id'].take(component_indices).to_list()

    del component_indices

    return output


@digest(form=form)
def get_component_name_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        component_indices = item.atoms['component_index']
    else:
        component_indices = item.atoms['component_index'].take(indices)

    output = item.components['component_name'].take(component_indices).to_list()

    del component_indices

    return output


@digest(form=form)
def get_component_type_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        component_indices = item.atoms['component_index']
    else:
        component_indices = item.atoms['component_index'].take(indices)

    output = item.components['component_type'].take(component_indices).to_list()

    del component_indices

    return output


@digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.atoms['chain_index'].to_list()
    else:
        output = item.atoms['chain_index'].take(indices).to_list()

    return output


@digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        chain_indices = item.atoms['chain_index']
    else:
        chain_indices = item.atoms['chain_index'].take(indices)

    output = item.chains['chain_id'].take(chain_indices).to_list()

    del chain_indices

    return output


@digest(form=form)
def get_chain_name_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        chain_indices = item.atoms['chain_index']
    else:
        chain_indices = item.atoms['chain_index'].take(indices)

    output = item.chains['chain_name'].take(chain_indices).to_list()

    del chain_indices

    return output


@digest(form=form)
def get_chain_type_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        chain_indices = item.atoms['chain_index']
    else:
        chain_indices = item.atoms['chain_index'].take(indices)

    output = item.chains['chain_type'].take(chain_indices).to_list()

    del chain_indices

    return output


@digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False): ##x

    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    n_bonds = len(edges)
    edge_indices = np.array([{'index': ii} for ii in range(n_bonds)]).reshape([n_bonds, 1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if is_all(indices):

        indices = get_atom_index_from_atom(item, skip_digestion=True)

    output = []

    for ii in indices:
        if ii in G:
            output.append([n['index'] for n in G[ii].values()])
        else:
            output.append([])

    del G, edges, edge_indices

    return output


@digest(form=form)
def get_bond_type_from_atom(item, indices='all', skip_digestion=False): ##x

    aux_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    output = []
    for ii in aux_indices:
        aux_vals = get_bond_type_from_bond(item, indices=ii, skip_digestion=True)
        output.append(aux_vals)

    return output


@digest(form=form)
def get_bond_order_from_atom(item, indices='all', skip_digestion=False): ##x

    aux_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    output = []
    for ii in aux_indices:
        aux_vals = get_bond_order_from_bond(item, indices=ii, skip_digestion=True)
        output.append(aux_vals)

    return output


@digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False): ##x

    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    
    G.add_edges_from(edges)

    if is_all(indices):

        indices = get_atom_index_from_atom(item, skip_digestion=True)

    output = []

    for ii in indices:
        if ii in G:
            output.append(list(G.neighbors(ii)))
        else:
            output.append([])

    del G, edges

    return output


@digest(form=form)
def get_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False): ##x

    output = None

    if is_all(indices):

        output = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
   
    else:

        pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
        pairs = np.array(pairs)
        mask = np.isin(pairs[:,0], indices) | np.isin(pairs[:,1], indices)
        output = pairs[mask,:].tolist()

        del pairs, mask

    return output


@digest(form=form)
def get_inner_bond_index_from_atom(item, indices='all', skip_digestion=False): ##x

    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    n_bonds = len(edges)
    edge_indices = np.array([{'index': ii} for ii in range(n_bonds)]).reshape([n_bonds, 1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if is_all(indices):

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


@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False): ##x

    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    
    G.add_edges_from(edges)

    if not is_all(indices):

        G = G.subgraph(indices)

    output = []
    for nodo in G.nodes():
        output.append(list(G.neighbors(nodo)))

    del G, edges

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False): ##x

    output = None

    if is_all(indices):

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


@digest(form=form)
def get_n_atoms_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.atoms.shape[0]
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_total_n_atoms_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_atoms_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_groups_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.groups.shape[0]
    else:
        output = item.atoms['group_index'].take(indices).nunique()

    return output


@digest(form=form)
def get_total_n_groups_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_groups_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_molecules_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.molecules.shape[0]
    else:
        group_indices = item.atoms['group_index'].take(indices)
        output = item.groups['molecule_index'].take(group_indices).nunique()
        del group_indices

    return output


@digest(form=form)
def get_total_n_molecules_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_molecules_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_entities_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.entities.shape[0]
    else:
        group_indices = item.atoms['group_index'].take(indices)
        molecule_indices = item.groups['molecule_index'].take(group_indices)
        output = item.molecules['entity_index'].take(molecule_indices).nunique()
        del group_indices, molecule_indices

    return output


@digest(form=form)
def get_total_n_entities_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_entities_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_components_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.components.shape[0]
    else:
        output = item.atoms['component_index'].take(indices).nunique()

    return output


@digest(form=form)
def get_total_n_components_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_components_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_chains_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.chains.shape[0]
    else:
        output = item.atoms['chain_index'].take(indices).nunique()

    return output


@digest(form=form)
def get_total_n_chains_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_chains_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_bonds_from_atom(item, indices='all', skip_digestion=False): ##x

    bond_indices = get_bond_index_from_atom(item, indices, skip_digestion=True)
    output = [len(ii) for ii in bond_indices]
    del bond_indices

    return output


@digest(form=form)
def get_total_n_bonds_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        bond_indices = get_bond_index_from_atom(item, indices, skip_digestion=True)
        output = np.unique(np.concatenate(bond_indices)).shape[0]
        del bond_indices

    return output


@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False): ##x

    inner_bond_indices = get_inner_bond_index_from_atom(item, indices, skip_digestion=True)
    output = [len(ii) for ii in inner_bond_indices]
    del inner_bond_indices

    return output


@digest(form=form)
def get_total_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        bond_indices = get_inner_bond_index_from_atom(item, indices, skip_digestion=True)
        output = np.unique(np.concatenate(bond_indices)).shape[0]
        del bond_indices

    return output


@digest(form=form)
def get_n_amino_acids_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = (item.groups['group_type'] == 'amino acid').sum()
    else:
        group_indices = item.atoms['group_index'].take(indices).unique()
        output = (item.groups['group_type'].take(group_indices) == 'amino acid').sum()
        del group_indices

    return output


@digest(form=form)
def get_total_n_amino_acids_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_amino_acids_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = (item.groups['group_type'] == 'nucleotide').sum()
    else:
        group_indices = item.atoms['group_index'].take(indices).unique()
        output = (item.groups['group_type'].take(group_indices) == 'nucleotide').sum()
        del group_indices

    return output


@digest(form=form)
def get_total_n_nucleotides_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_nucleotides_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_ions_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = (item.groups['group_type'] == 'ion').sum()
    else:
        group_indices = item.atoms['group_index'].take(indices).unique()
        output = (item.groups['group_type'].take(group_indices) == 'ion').sum()
        del group_indices

    return output


@digest(form=form)
def get_total_n_ions_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_ions_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_waters_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = (item.groups['group_type'] == 'water').sum()
    else:
        group_indices = item.atoms['group_index'].take(indices).unique()
        output = (item.groups['group_type'].take(group_indices) == 'water').sum()
        del group_indices

    return output


@digest(form=form)
def get_total_n_waters_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_waters_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = (item.groups['group_type'] == 'small molecule').sum()
    else:
        group_indices = item.atoms['group_index'].take(indices).unique()
        output = (item.groups['group_type'].take(group_indices) == 'small molecule').sum()
        del group_indices

    return output


@digest(form=form)
def get_total_n_small_molecules_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_small_molecules_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_lipids_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = (item.groups['group_type'] == 'lipid').sum()
    else:
        group_indices = item.atoms['group_index'].take(indices).unique()
        output = (item.groups['group_type'].take(group_indices) == 'lipid').sum()
        del group_indices

    return output


@digest(form=form)
def get_total_n_lipids_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_lipids_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_saccharides_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = (item.groups['group_type'] == 'saccharide').sum()
    else:
        group_indices = item.atoms['group_index'].take(indices).unique()
        output = (item.groups['group_type'].take(group_indices) == 'saccharide').sum()
        del group_indices

    return output


@digest(form=form)
def get_total_n_saccharides_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_saccharides_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_peptides_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = (item.molecules['molecule_type'] == 'peptide').sum()
    else:
        group_indices = item.atoms['group_index'].take(indices).unique()
        molecule_indices = item.groups['molecule_index'].take(group_indices).unique()
        output = (item.molecules['molecule_type'].take(molecule_indices) == 'peptide').sum()
        del group_indices, molecule_indices

    return output


@digest(form=form)
def get_total_n_peptides_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_peptides_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_proteins_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = (item.molecules['molecule_type'] == 'protein').sum()
    else:
        group_indices = item.atoms['group_index'].take(indices).unique()
        molecule_indices = item.groups['molecule_index'].take(group_indices).unique()
        output = (item.molecules['molecule_type'].take(molecule_indices) == 'protein').sum()
        del group_indices, molecule_indices

    return output


@digest(form=form)
def get_total_n_proteins_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_proteins_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_dnas_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = (item.molecules['molecule_type'] == 'dna').sum()
    else:
        group_indices = item.atoms['group_index'].take(indices).unique()
        molecule_indices = item.groups['molecule_index'].take(group_indices).unique()
        output = (item.molecules['molecule_type'].take(molecule_indices) == 'dna').sum()
        del group_indices, molecule_indices

    return output


@digest(form=form)
def get_total_n_dnas_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_dnas_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_rnas_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = (item.molecules['molecule_type'] == 'rna').sum()
    else:
        group_indices = item.atoms['group_index'].take(indices).unique()
        molecule_indices = item.groups['molecule_index'].take(group_indices).unique()
        output = (item.molecules['molecule_type'].take(molecule_indices) == 'rna').sum()
        del group_indices, molecule_indices

    return output


@digest(form=form)
def get_total_n_rnas_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_rnas_from_atom(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = (item.molecules['molecule_type'] == 'polysaccharide').sum()
    else:
        group_indices = item.atoms['group_index'].take(indices).unique()
        molecule_indices = item.groups['molecule_index'].take(group_indices).unique()
        output = (item.molecules['molecule_type'].take(molecule_indices) == 'polysaccharide').sum()
        del group_indices, molecule_indices

    return output


@digest(form=form)
def get_total_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False): ##x

    return get_n_polysaccharides_from_atom(item, indices=indices, skip_digestion=True)


# From group


@digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        grouped = item.atoms.groupby('group_index').groups
        output = [grouped[ii].tolist() for ii in grouped]
        del grouped
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]
        grouped = subset.groupby('group_index').groups
        output = [grouped.get(ii, []).tolist() for ii in indices]
        del grouped, subset

    return output


@digest(form=form)
def get_atom_id_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        series = item.atoms.groupby("group_index")["atom_id"].apply(list)
        output = series.tolist()
        del series
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]
        series = subset.groupby('group_index')['atom_id'].apply(list)
        output = series.reindex(indices, fill_value=[]).tolist()
        del subset, series

    return output


@digest(form=form)
def get_atom_name_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        series = item.atoms.groupby("group_index")["atom_name"].apply(list)
        output = series.tolist()
        del series
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]
        series = subset.groupby('group_index')['atom_name'].apply(list)
        output = series.reindex(indices, fill_value=[]).tolist()
        del subset, series

    return output


@digest(form=form)
def get_atom_type_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        series = item.atoms.groupby("group_index")["atom_type"].apply(list)
        output = series.tolist()
        del series
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]
        series = subset.groupby('group_index')['atom_type'].apply(list)
        output = series.reindex(indices, fill_value=[]).tolist()
        del subset, series

    return output


@digest(form=form)
def get_group_index_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = list(range(item.groups.shape[0]))
    else:
        output = indices

    return output


@digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.groups['group_id'].to_list()
    else:
        output = item.groups['group_id'].take(indices).to_list()

    return output


@digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.groups['group_name'].to_list()
    else:
        output = item.groups['group_name'].take(indices).to_list()

    return output


@digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.groups['group_type'].to_list()
    else:
        output = item.groups['group_type'].take(indices).to_list()

    return output


@digest(form=form)
def get_molecule_index_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.groups['molecule_index'].to_list()
    else:
        output = item.groups['molecule_index'].take(indices).to_list()

    return output


@digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        molecule_indices = item.groups['molecule_index']
    else:
        molecule_indices = item.groups['molecule_index'].take(indices)

    output = item.molecules['molecule_id'].take(molecule_indices).to_list()

    del molecule_indices

    return output


@digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        molecule_indices = item.groups['molecule_index']
    else:
        molecule_indices = item.groups['molecule_index'].take(indices)

    output = item.molecules['molecule_name'].take(molecule_indices).to_list()

    del molecule_indices

    return output


@digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        molecule_indices = item.groups['molecule_index']
    else:
        molecule_indices = item.groups['molecule_index'].take(indices)

    output = item.molecules['molecule_type'].take(molecule_indices).to_list()

    del molecule_indices

    return output


@digest(form=form)
def get_entity_index_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        molecule_indices = item.groups['molecule_index']
    else:
        molecule_indices = item.groups['molecule_index'].take(indices)

    output = item.molecules['entity_index'].take(molecule_indices).to_list()

    del molecule_indices

    return output


@digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        molecule_indices = item.groups['molecule_index']
    else:
        molecule_indices = item.groups['molecule_index'].take(indices)

    entity_indices = item.molecules['entity_index'].take(molecule_indices).to_list()
    output = item.entities['entity_id'].take(entity_indices).to_list()

    del molecule_indices, entity_indices

    return output


@digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        molecule_indices = item.groups['molecule_index']
    else:
        molecule_indices = item.groups['molecule_index'].take(indices)

    entity_indices = item.molecules['entity_index'].take(molecule_indices).to_list()
    output = item.entities['entity_name'].take(entity_indices).to_list()

    del molecule_indices, entity_indices

    return output


@digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        molecule_indices = item.groups['molecule_index']
    else:
        molecule_indices = item.groups['molecule_index'].take(indices)

    entity_indices = item.molecules['entity_index'].take(molecule_indices).to_list()
    output = item.entities['entity_type'].take(entity_indices).to_list()

    del molecule_indices, entity_indices

    return output


@digest(form=form)
def get_component_index_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        subset = item.atoms
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]

    series = subset.groupby('group_index')['component_index'].first()
    group_with_more_than_a_component = subset.groupby("group_index")["component_index"].nunique().gt(1)
    if group_with_more_than_a_component.any():
        series_aux = subset.groupby("group_index")["component_index"].apply(lambda s: list(pd.unique(s)))
        series[group_with_more_than_a_component] = series_aux[group_with_more_than_a_component]
        del series_aux

    if is_all(indices):
        output = series.tolist()
    else:
        output = series.reindex(indices, fill_value=None).tolist()

    del subset, series

    return output

@digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False): ##x

    comp_id_map = item.components['component_id'].to_dict()

    if is_all(indices):
        subset = item.atoms
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]

    series = subset.groupby('group_index')['component_index'].first()
    series = series.map(comp_id_map)
    group_with_more_than_a_component = subset.groupby("group_index")["component_index"].nunique().gt(1)
    if group_with_more_than_a_component.any():
        series_aux = subset.groupby("group_index")["component_index"].apply(lambda s: list(pd.unique(s)))
        series_aux = series_aux.apply(lambda x: [comp_id_map[ii] for ii in x])
        series[group_with_more_than_a_component] = series_aux[group_with_more_than_a_component]
        del series_aux

    if is_all(indices):
        output = series.tolist()
    else:
        output = series.reindex(indices, fill_value=None).tolist()

    del subset, series

    return output


@digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False): ##x

    comp_id_map = item.components['component_name'].to_dict()

    if is_all(indices):
        subset = item.atoms
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]

    series = subset.groupby('group_index')['component_index'].first()
    series = series.map(comp_id_map)
    group_with_more_than_a_component = subset.groupby("group_index")["component_index"].nunique().gt(1)
    if group_with_more_than_a_component.any():
        series_aux = subset.groupby("group_index")["component_index"].apply(lambda s: list(pd.unique(s)))
        series_aux = series_aux.apply(lambda x: [comp_id_map[ii] for ii in x])
        series[group_with_more_than_a_component] = series_aux[group_with_more_than_a_component]
        del series_aux

    if is_all(indices):
        output = series.tolist()
    else:
        output = series.reindex(indices, fill_value=None).tolist()

    del subset, series

    return output


@digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False): ##x

    comp_id_map = item.components['component_type'].to_dict()

    if is_all(indices):
        subset = item.atoms
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]

    series = subset.groupby('group_index')['component_index'].first()
    series = series.map(comp_id_map)
    group_with_more_than_a_component = subset.groupby("group_index")["component_index"].nunique().gt(1)
    if group_with_more_than_a_component.any():
        series_aux = subset.groupby("group_index")["component_index"].apply(lambda s: list(pd.unique(s)))
        series_aux = series_aux.apply(lambda x: [comp_id_map[ii] for ii in x])
        series[group_with_more_than_a_component] = series_aux[group_with_more_than_a_component]
        del series_aux

    if is_all(indices):
        output = series.tolist()
    else:
        output = series.reindex(indices, fill_value=None).tolist()

    del subset, series

    return output


@digest(form=form)
def get_chain_index_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        subset = item.atoms
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]

    series = subset.groupby('group_index')['chain_index'].first()
    group_with_more_than_a_chain = subset.groupby("group_index")["chain_index"].nunique().gt(1)
    if group_with_more_than_a_chain.any():
        series_aux = subset.groupby("group_index")["chain_index"].apply(lambda s: list(pd.unique(s)))
        series[group_with_more_than_a_chain] = series_aux[group_with_more_than_a_chain]
        del series_aux

    if is_all(indices):
        output = series.tolist()
    else:
        output = series.reindex(indices, fill_value=None).tolist()

    del subset, series

    return output


@digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False): ##x

    comp_id_map = item.chains['chain_id'].to_dict()

    if is_all(indices):
        subset = item.atoms
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]

    series = subset.groupby('group_index')['chain_index'].first()
    series = series.map(comp_id_map)
    group_with_more_than_a_chain = subset.groupby("group_index")["chain_index"].nunique().gt(1)
    if group_with_more_than_a_chain.any():
        series_aux = subset.groupby("group_index")["chain_index"].apply(lambda s: list(pd.unique(s)))
        series_aux = series_aux.apply(lambda x: [comp_id_map[ii] for ii in x])
        series[group_with_more_than_a_chain] = series_aux[group_with_more_than_a_chain]
        del series_aux

    if is_all(indices):
        output = series.tolist()
    else:
        output = series.reindex(indices, fill_value=None).tolist()

    del subset, series

    return output


@digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False): ##x

    comp_id_map = item.chains['chain_name'].to_dict()

    if is_all(indices):
        subset = item.atoms
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]

    series = subset.groupby('group_index')['chain_index'].first()
    series = series.map(comp_id_map)
    group_with_more_than_a_chain = subset.groupby("group_index")["chain_index"].nunique().gt(1)
    if group_with_more_than_a_chain.any():
        series_aux = subset.groupby("group_index")["chain_index"].apply(lambda s: list(pd.unique(s)))
        series_aux = series_aux.apply(lambda x: [comp_id_map[ii] for ii in x])
        series[group_with_more_than_a_chain] = series_aux[group_with_more_than_a_chain]
        del series_aux

    if is_all(indices):
        output = series.tolist()
    else:
        output = series.reindex(indices, fill_value=None).tolist()

    del subset, series

    return output


@digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False): ##x

    comp_id_map = item.chains['chain_type'].to_dict()

    if is_all(indices):
        subset = item.atoms
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]

    series = subset.groupby('group_index')['chain_index'].first()
    series = series.map(comp_id_map)
    group_with_more_than_a_chain = subset.groupby("group_index")["chain_index"].nunique().gt(1)
    if group_with_more_than_a_chain.any():
        series_aux = subset.groupby("group_index")["chain_index"].apply(lambda s: list(pd.unique(s)))
        series_aux = series_aux.apply(lambda x: [comp_id_map[ii] for ii in x])
        series[group_with_more_than_a_chain] = series_aux[group_with_more_than_a_chain]
        del series_aux

    if is_all(indices):
        output = series.tolist()
    else:
        output = series.reindex(indices, fill_value=None).tolist()

    del subset, series

    return output


@digest(form=form)
def get_bond_index_from_group(item, indices='all', skip_digestion=False): ##x

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


@digest(form=form)
def get_bond_type_from_group(item, indices='all', skip_digestion=False): ##x

    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)

    del bond_type, bond_indices, aux_vals, ii

    return output


@digest(form=form)
def get_bond_order_from_group(item, indices='all', skip_digestion=False): ##x

    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)

    del bond_order, bond_indices, aux_vals, ii

    return output


@digest(form=form)
def get_bonded_atoms_from_group(item, indices='all', skip_digestion=False): ##x

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@digest(form=form)
def get_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False): ##x

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@digest(form=form)
def get_inner_bond_index_from_group(item, indices='all', skip_digestion=False): ##x

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


@digest(form=form)
def get_inner_bonded_atoms_from_group(item, indices='all', skip_digestion=False): ##x

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)
    atom_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)

    output = []
    for ii,jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))

    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False): ##x

    bonded_atom_pairs = get_bonded_atom_pairs_from_group(item, indices=indices, skip_digestion=True)

    if is_all(indices):

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


@digest(form=form)
def get_n_atoms_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.atoms['group_index'].value_counts(sort=False).tolist()
    else:
        subset = item.atoms['group_index'][item.atoms['group_index'].isin(indices)]
        counts = subset.value_counts(sort=False)
        output = counts.reindex(indices, fill_value=0).tolist()
        del subset, counts

    return output


@digest(form=form)
def get_total_n_atoms_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_group(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@digest(form=form)
def get_n_groups_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.groups.shape[0]
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_total_n_groups_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_groups_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_molecules_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.molecules.shape[0]
    else:
        output = item.groups['molecule_index'].take(indices).nunique()

    return output


@digest(form=form)
def get_total_n_molecules_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_molecules_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_entities_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.entities.shape[0]
    else:
        molecule_indices = item.groups['molecule_index'].take(indices).unique()
        output = item.molecules['entity_index'].take(molecule_indices).nunique()
        del molecule_indices

    return output


@digest(form=form)
def get_total_n_entities_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_entities_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_components_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.components.shape[0]
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]
        output = subset['component_index'].nunique()
        del subset

    return output


@digest(form=form)
def get_total_n_components_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_components_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_chains_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.chains.shape[0]
    else:
        subset = item.atoms.loc[item.atoms['group_index'].isin(indices)]
        output = subset['chain_index'].nunique()
        del subset

    return output


@digest(form=form)
def get_total_n_chains_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_chains_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_bonds_from_group(item, indices='all', skip_digestion=False): ##x

    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)
    output = [len(ii) for ii in bond_indices]
    del bond_indices

    return output


@digest(form=form)
def get_total_n_bonds_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        atom_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
        atom_indices = list(chain.from_iterable(atom_indices))
        output = get_total_n_bonds_from_atom(item, indices=atom_indices, skip_digestion=True)
        del atom_indices

    return output


@digest(form=form)
def get_n_inner_bonds_from_group(item, indices='all', skip_digestion=False): ##x

    inner_bond_indices = get_inner_bond_index_from_group(item, indices=indices, skip_digestion=True)
    output = [len(ii) for ii in inner_bond_indices]
    del inner_bond_indices

    return output


@digest(form=form)
def get_total_n_inner_bonds_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        atom_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
        atom_indices = list(chain.from_iterable(atom_indices))
        output = get_total_n_inner_bonds_from_atom(item, indices=atom_indices, skip_digestion=True)
        del atom_indices

    return output


@digest(form=form)
def get_n_amino_acids_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        group_types = item.groups['group_type']
    else:
        group_types = item.groups['group_type'].take(indices)

    output = group_types.value_counts().get('amino acid', 0)

    del group_types

    return output


@digest(form=form)
def get_total_n_amino_acids_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_amino_acids_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_nucleotides_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        group_types = item.groups['group_type']
    else:
        group_types = item.groups['group_type'].take(indices)

    output = group_types.value_counts().get('nucleotide', 0)

    del group_types

    return output


@digest(form=form)
def get_total_n_nucleotides_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_nucleotides_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_ions_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        group_types = item.groups['group_type']
    else:
        group_types = item.groups['group_type'].take(indices)

    output = group_types.value_counts().get('ion', 0)

    del group_types

    return output


@digest(form=form)
def get_total_n_ions_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_ions_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_waters_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        group_types = item.groups['group_type']
    else:
        group_types = item.groups['group_type'].take(indices)

    output = group_types.value_counts().get('water', 0)

    del group_types

    return output


@digest(form=form)
def get_total_n_waters_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_waters_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_small_molecules_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        group_types = item.groups['group_type']
    else:
        group_types = item.groups['group_type'].take(indices)

    output = group_types.value_counts().get('small molecule', 0)

    del group_types

    return output


@digest(form=form)
def get_total_n_small_molecules_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_small_molecules_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_lipids_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        group_types = item.groups['group_type']
    else:
        group_types = item.groups['group_type'].take(indices)

    output = group_types.value_counts().get('lipid', 0)

    del group_types

    return output


@digest(form=form)
def get_total_n_lipids_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_lipids_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_saccharides_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        group_types = item.groups['group_type']
    else:
        group_types = item.groups['group_type'].take(indices)

    output = group_types.value_counts().get('saccharide', 0)

    del group_types

    return output


@digest(form=form)
def get_total_n_saccharides_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_saccharides_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_peptides_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        molecule_indices = item.groups['molecule_index']
    else:
        molecule_indices = item.groups['molecule_index'].take(indices)

    molecule_indices = molecule_indices.unique()
    molecule_types = item.molecules['molecule_type'].take(molecule_indices)

    output = molecule_types.value_counts().get('peptide', 0)

    del molecule_indices, molecule_types

    return output


@digest(form=form)
def get_total_n_peptides_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_peptides_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_proteins_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        molecule_indices = item.groups['molecule_index']
    else:
        molecule_indices = item.groups['molecule_index'].take(indices)

    molecule_indices = molecule_indices.unique()
    molecule_types = item.molecules['molecule_type'].take(molecule_indices)

    output = molecule_types.value_counts().get('protein', 0)

    del molecule_indices, molecule_types

    return output


@digest(form=form)
def get_total_n_proteins_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_proteins_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_dnas_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        molecule_indices = item.groups['molecule_index']
    else:
        molecule_indices = item.groups['molecule_index'].take(indices)

    molecule_indices = molecule_indices.unique()
    molecule_types = item.molecules['molecule_type'].take(molecule_indices)

    output = molecule_types.value_counts().get('dna', 0)

    del molecule_indices, molecule_types

    return output


@digest(form=form)
def get_total_n_dnas_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_dnas_from_group(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_rnas_from_group(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        molecule_indices = item.groups['molecule_index']
    else:
        molecule_indices = item.groups['molecule_index'].take(indices)

    molecule_indices = molecule_indices.unique()
    molecule_types = item.molecules['molecule_type'].take(molecule_indices)

    output = (molecule_types == 'rna').sum()

    del molecule_indices, molecule_types

    return output


@digest(form=form)
def get_total_n_rnas_from_group(item, indices='all', skip_digestion=False): ##x

    return get_n_rnas_from_group(item, indices=indices, skip_digestion=True)


# From molecule

@digest(form=form)
def get_atom_index_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    #mol_arr   = item.groups['molecule_index'].reindex(group_arr).to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[mol_arr[atom_index]].append(atom_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(n_atoms):
            ii = mol_arr[atom_index]
            if ii in aux_dict:
                aux_dict[ii].append(atom_index)

        output = [aux_dict[m] for m in indices]

    del group_arr, mol_arr, aux_dict

    return output


@digest(form=form)
def get_atom_id_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    aux_arr = item.atoms['atom_id'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[mol_arr[atom_index]].append(aux_arr[atom_index])

        output = [aux_dict[m] for m in sorted(aux_dict.keys())]

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(len(group_arr)):
            ii = mol_arr[atom_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    del group_arr, mol_arr, aux_arr, aux_dict

    return output


@digest(form=form)
def get_atom_name_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    aux_arr = item.atoms['atom_name'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[mol_arr[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(len(group_arr)):
            ii = mol_arr[atom_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[atom_index])

        output = [aux_dict.get(m, []) for m in indices]

    del group_arr, mol_arr, aux_arr, aux_dict

    return output


@digest(form=form)
def get_atom_type_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    aux_arr = item.atoms['atom_type'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[mol_arr[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(len(group_arr)):
            ii = mol_arr[atom_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[atom_index])

        output = [aux_dict.get(m, []) for m in indices]

    del group_arr, mol_arr, aux_arr, aux_dict

    return output


@digest(form=form)
def get_group_index_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        grouped = item.groups.groupby('molecule_index').groups
        output = [grouped[ii].tolist() for ii in grouped]
        del grouped
    else:
        subset = item.groups.loc[item.groups['molecule_index'].isin(indices)]
        grouped = subset.groupby('molecule_index').groups
        output = [grouped.get(ii, []).tolist() for ii in indices]
        del subset, grouped

    return output


@digest(form=form)
def get_group_id_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        series = item.groups.groupby('molecule_index')['group_id'].apply(list)
        output = series.tolist()
        del series
    else:
        subset = item.groups.loc[item.groups['molecule_index'].isin(indices)]
        series = subset.groupby('molecule_index')['group_id'].apply(list)
        output = series.reindex(indices, fill_value=[]).tolist()
        del subset, series

    return output


@digest(form=form)
def get_group_name_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        series = item.groups.groupby('molecule_index')['group_name'].apply(list)
        output = series.tolist()
        del series
    else:
        subset = item.groups.loc[item.groups['molecule_index'].isin(indices)]
        series = subset.groupby('molecule_index')['group_name'].apply(list)
        output = series.reindex(indices, fill_value=[]).tolist()
        del subset, series

    return output


@digest(form=form)
def get_group_type_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        series = item.groups.groupby('molecule_index')['group_type'].apply(list)
        output = series.tolist()
        del series
    else:
        subset = item.groups.loc[item.groups['molecule_index'].isin(indices)]
        series = subset.groupby('molecule_index')['group_type'].apply(list)
        output = series.reindex(indices, fill_value=[]).tolist()
        del subset, series

    return output


@digest(form=form)
def get_molecule_index_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = list(range(item.molecules.shape[0]))
    else:
        output = indices

    return output


@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.molecules['molecule_id'].to_list()
    else:
        output = item.molecules['molecule_id'].take(indices).to_list()

    return output


@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.molecules['molecule_name'].to_list()
    else:
        output = item.molecules['molecule_name'].take(indices).to_list()

    return output


@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.molecules['molecule_type'].to_list()
    else:
        output = item.molecules['molecule_type'].take(indices).to_list()

    return output


@digest(form=form)
def get_entity_index_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = item.molecules['entity_index'].to_list()
    else:
        output = item.molecules['entity_index'].take(indices).to_list()

    return output


@digest(form=form)
def get_entity_id_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        entity_indices = item.molecules['entity_index']
    else:
        entity_indices = item.molecules['entity_index'].take(indices)

    output = item.entities['entity_id'].take(entity_indices).to_list()

    del entity_indices

    return output


@digest(form=form)
def get_entity_name_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        entity_indices = item.molecules['entity_index']
    else:
        entity_indices = item.molecules['entity_index'].take(indices)

    output = item.entities['entity_name'].take(entity_indices).to_list()

    del entity_indices

    return output


@digest(form=form)
def get_entity_type_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        entity_indices = item.molecules['entity_index']
    else:
        entity_indices = item.molecules['entity_index'].take(indices)

    output = item.entities['entity_type'].take(entity_indices).to_list()

    del entity_indices

    return output


@digest(form=form)
def get_component_index_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    aux_arr = item.atoms['component_index'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[mol_arr[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(len(group_arr)):
            ii = mol_arr[atom_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[atom_index])

        output = [aux_dict[ii] for ii in indices]

    del group_arr, mol_arr, aux_arr, aux_dict

    output = [list(np.unique(ii)) for ii in output] 

    return output


@digest(form=form)
def get_component_id_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    aux_arr = item.atoms['component_index'].to_numpy()
    aux2_arr = item.components['component_id'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[mol_arr[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(len(group_arr)):
            ii = mol_arr[atom_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [aux2_arr[np.unique(ii)].tolist() for ii in output] 

    del group_arr, mol_arr, aux_arr, aux2_arr, aux_dict

    return output


@digest(form=form)
def get_component_name_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    aux_arr = item.atoms['component_index'].to_numpy()
    aux2_arr = item.components['component_name'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[mol_arr[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(len(group_arr)):
            ii = mol_arr[atom_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [aux2_arr[np.unique(ii)].tolist() for ii in output] 

    del group_arr, mol_arr, aux_arr, aux2_arr, aux_dict

    return output


@digest(form=form)
def get_component_type_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    aux_arr = item.atoms['component_index'].to_numpy()
    aux2_arr = item.components['component_type'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[mol_arr[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(len(group_arr)):
            ii = mol_arr[atom_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [aux2_arr[np.unique(ii)].tolist() for ii in output] 

    del group_arr, mol_arr, aux_arr, aux2_arr, aux_dict

    return output


@digest(form=form)
def get_chain_index_from_molecule(item, indices='all', skip_digestion=False):

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    aux_arr = item.atoms['chain_index'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[mol_arr[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(len(group_arr)):
            ii = mol_arr[atom_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[atom_index])

        output = [aux_dict[ii] for ii in indices]

    del group_arr, mol_arr, aux_arr, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii))
        for ii in output
    ]

    return output


@digest(form=form)
def get_chain_id_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    aux_arr = item.atoms['chain_index'].to_numpy()
    aux2_arr = item.chains['chain_id'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[mol_arr[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(len(group_arr)):
            ii = mol_arr[atom_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [aux2_arr[np.unique(ii)].tolist() for ii in output] 

    del group_arr, mol_arr, aux_arr, aux2_arr, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii))
        for ii in output
    ]

    return output


@digest(form=form)
def get_chain_name_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    aux_arr = item.atoms['chain_index'].to_numpy()
    aux2_arr = item.chains['chain_name'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[mol_arr[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(len(group_arr)):
            ii = mol_arr[atom_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [aux2_arr[np.unique(ii)].tolist() for ii in output] 

    del group_arr, mol_arr, aux_arr, aux2_arr, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii))
        for ii in output
    ]

    return output


@digest(form=form)
def get_chain_type_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    aux_arr = item.atoms['chain_index'].to_numpy()
    aux2_arr = item.chains['chain_type'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[mol_arr[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(len(group_arr)):
            ii = mol_arr[atom_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [aux2_arr[np.unique(ii)].tolist() for ii in output] 

    del group_arr, mol_arr, aux_arr, aux2_arr, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii))
        for ii in output
    ]

    return output


@digest(form=form)
def get_bond_index_from_molecule(item, indices='all', skip_digestion=False): ##x

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


@digest(form=form)
def get_bond_type_from_molecule(item, indices='all', skip_digestion=False): ##x

    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)

    del bond_type, bond_indices, aux_vals, ii

    return output


@digest(form=form)
def get_bond_order_from_molecule(item, indices='all', skip_digestion=False): ##x

    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)

    del bond_order, bond_indices, aux_vals, ii

    return output


@digest(form=form)
def get_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False): ##x

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@digest(form=form)
def get_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False): ##x

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@digest(form=form)
def get_inner_bond_index_from_molecule(item, indices='all', skip_digestion=False): ##x

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


@digest(form=form)
def get_inner_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False): ##x

    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)
    atom_indices = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii,jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))

    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False): ##x

    bonded_atom_pairs = get_bonded_atom_pairs_from_molecule(item, indices=indices, skip_digestion=True)

    if is_all(indices):

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


@digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', skip_digestion=False): ##x

    output = get_atom_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_total_n_atoms_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@digest(form=form)
def get_n_groups_from_molecule(item, indices='all', skip_digestion=False): ##x

    output = get_group_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_total_n_groups_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        aux = get_n_groups_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_total_n_molecules_from_molecule(item, indices='all', skip_digestion=False): ##x

    return get_n_molecules_from_molecule(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_entities_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_total_n_entities_from_molecule(item, indices='all', skip_digestion=False): ##x

    return get_n_entities_from_molecule(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_components_from_molecule(item, indices='all', skip_digestion=False): ##x

    output = get_component_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@digest(form=form)
def get_total_n_components_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        aux = get_n_components_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@digest(form=form)
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_molecule(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_total_n_chains_from_molecule(item, indices='all', skip_digestion=False): ##x

    return get_n_chains_from_molecule(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False): ##x 

    output = get_bond_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_total_n_bonds_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_molecule(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices)
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False): ##x

    output = get_inner_bond_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_total_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        atom_indices = get_atom_index_from_molecule(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices)
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ sum([jj=='amino acid' for jj in ii]) for ii in group_types ]

    return output


@digest(form=form)
def get_total_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):

        output = get_n_amino_acids_from_system(item, skip_digestion=True)

    else:

        output = get_n_amino_acids_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ sum([jj=='nucleotide' for jj in ii]) for ii in group_types ]

    return output


@digest(form=form)
def get_total_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):

        output = get_n_nucleotides_from_system(item, skip_digestion=True)

    else:

        output = get_n_nucleotides_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@digest(form=form)
def get_n_ions_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ sum([jj=='ion' for jj in ii]) for ii in group_types ]

    return output


@digest(form=form)
def get_total_n_ions_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):

        output = get_n_ions_from_system(item, skip_digestion=True)

    else:

        output = get_n_ions_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@digest(form=form)
def get_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ sum([jj=='water' for jj in ii]) for ii in group_types ]

    return output


@digest(form=form)
def get_total_n_waters_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):

        output = get_n_waters_from_system(item, skip_digestion=True)

    else:

        output = get_n_waters_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ sum([jj=='small molecule' for jj in ii]) for ii in group_types ]

    return output


@digest(form=form)
def get_total_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):

        output = get_n_small_molecules_from_system(item, skip_digestion=True)

    else:

        output = get_n_small_molecules_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@digest(form=form)
def get_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ sum([jj=='lipid' for jj in ii]) for ii in group_types ]

    return output


@digest(form=form)
def get_total_n_lipids_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):

        output = get_n_lipids_from_system(item, skip_digestion=True)

    else:

        output = get_n_lipids_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ sum([jj=='saccharide' for jj in ii]) for ii in group_types ]

    return output


@digest(form=form)
def get_total_n_saccharides_from_molecule(item, indices='all', skip_digestion=False): ##x

    if is_all(indices):

        output = get_n_saccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_saccharides_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@digest(form=form)
def get_n_peptides_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'peptide').sum()

    return output


@digest(form=form)
def get_total_n_peptides_from_molecule(item, indices='all', skip_digestion=False): ##x

    output = get_n_peptides_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_proteins_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'protein').sum()

    return output


@digest(form=form)
def get_total_n_proteins_from_molecule(item, indices='all', skip_digestion=False): ##x

    output = get_n_proteins_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'polysaccharide').sum()

    return output


@digest(form=form)
def get_total_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False): ##x

    output = get_n_polysaccharides_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_dnas_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'dna').sum()

    return output


@digest(form=form)
def get_total_n_dnas_from_molecule(item, indices='all', skip_digestion=False): ##x

    output = get_n_dnas_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_rnas_from_molecule(item, indices='all', skip_digestion=False): ##x

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'rna').sum()

    return output


@digest(form=form)
def get_total_n_rnas_from_molecule(item, indices='all', skip_digestion=False): ##x

    output = get_n_rnas_from_molecule(item, indices=indices, skip_digestion=True)

    return output


# From entity


@digest(form=form)
def get_atom_index_from_entity(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    ent_idx_arr = item.molecules['entity_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    ent_per_atom = ent_idx_arr[mol_arr]
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[ent_per_atom[atom_index]].append(atom_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(n_atoms):
            ent = ent_per_atom[atom_index]
            if ent in aux_dict:
                aux_dict[ent].append(atom_index)

        output = [aux_dict[m] for m in indices]

    del group_arr, mol_idx_arr, ent_idx_arr, mol_arr, ent_per_atom, aux_dict

    return output


@digest(form=form)
def get_atom_id_from_entity(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    ent_idx_arr = item.molecules['entity_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    ent_per_atom = ent_idx_arr[mol_arr]
    aux_arr = item.atoms['atom_id'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[ent_per_atom[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(n_atoms):
            ent = ent_per_atom[atom_index]
            if ent in aux_dict:
                aux_dict[ent].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    del group_arr, mol_idx_arr, ent_idx_arr, mol_arr, ent_per_atom, aux_arr, aux_dict

    return output


@digest(form=form)
def get_atom_name_from_entity(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    ent_idx_arr = item.molecules['entity_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    ent_per_atom = ent_idx_arr[mol_arr]
    aux_arr = item.atoms['atom_name'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[ent_per_atom[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(n_atoms):
            ent = ent_per_atom[atom_index]
            if ent in aux_dict:
                aux_dict[ent].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    del group_arr, mol_idx_arr, ent_idx_arr, mol_arr, ent_per_atom, aux_arr, aux_dict

    return output


@digest(form=form)
def get_atom_type_from_entity(item, indices='all', skip_digestion=False): ##x

    group_arr = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    ent_idx_arr = item.molecules['entity_index'].to_numpy()
    mol_arr     = mol_idx_arr[group_arr]
    ent_per_atom = ent_idx_arr[mol_arr]
    aux_arr = item.atoms['atom_type'].to_numpy()
    n_atoms = item.atoms.shape[0]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index in range(n_atoms):
            aux_dict[ent_per_atom[atom_index]].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index in range(n_atoms):
            ent = ent_per_atom[atom_index]
            if ent in aux_dict:
                aux_dict[ent].append(aux_arr[atom_index])

        output = list(aux_dict.values())

    del group_arr, mol_idx_arr, ent_idx_arr, mol_arr, ent_per_atom, aux_arr, aux_dict

    return output


@digest(form=form)
def get_group_index_from_entity(item, indices='all', skip_digestion=False): ##x

    mol_idx_arr     = item.groups['molecule_index'].to_numpy()
    ent_idx_arr     = item.molecules['entity_index'].to_numpy()
    ent_per_group   = ent_idx_arr[mol_idx_arr]
    n_groups = len(ent_per_group)

    if indices == 'all':

        aux_dict = defaultdict(list)
        for group_index in range(n_groups):
            aux_dict[ent_per_group[group_index]].append(group_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index in range(n_groups):
            ii = ent_per_group[group_index]
            if ii in aux_dict:
                aux_dict[ii].append(group_index)

        output = [aux_dict[ii] for ii in indices]

    del mol_idx_arr, ent_idx_arr, ent_per_group, n_groups, aux_dict

    return output


@digest(form=form)
def get_group_id_from_entity(item, indices='all', skip_digestion=False): ##x

    mol_idx_arr     = item.groups['molecule_index'].to_numpy()
    ent_idx_arr     = item.molecules['entity_index'].to_numpy()
    ent_per_group   = ent_idx_arr[mol_idx_arr]
    aux_arr = item.groups['group_id'].to_numpy()
    n_groups = len(ent_per_group)

    if indices == 'all':

        aux_dict = defaultdict(list)
        for group_index in range(n_groups):
            aux_dict[ent_per_group[group_index]].append(aux_arr[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index in range(n_groups):
            ii = ent_per_group[group_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[group_index])

        output = [aux_dict[ii] for ii in indices]

    del mol_idx_arr, ent_idx_arr, ent_per_group, n_groups, aux_dict

    return output


@digest(form=form)
def get_group_name_from_entity(item, indices='all', skip_digestion=False): ##x

    mol_idx_arr     = item.groups['molecule_index'].to_numpy()
    ent_idx_arr     = item.molecules['entity_index'].to_numpy()
    ent_per_group   = ent_idx_arr[mol_idx_arr]
    aux_arr = item.groups['group_name'].to_numpy()
    n_groups = len(ent_per_group)

    if indices == 'all':

        aux_dict = defaultdict(list)
        for group_index in range(n_groups):
            aux_dict[ent_per_group[group_index]].append(aux_arr[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index in range(n_groups):
            ii = ent_per_group[group_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[group_index])

        output = [aux_dict[ii] for ii in indices]

    del mol_idx_arr, ent_idx_arr, ent_per_group, n_groups, aux_dict

    return output


@digest(form=form)
def get_group_type_from_entity(item, indices='all', skip_digestion=False): ##x

    mol_idx_arr     = item.groups['molecule_index'].to_numpy()
    ent_idx_arr     = item.molecules['entity_index'].to_numpy()
    ent_per_group   = ent_idx_arr[mol_idx_arr]
    aux_arr = item.groups['group_type'].to_numpy()
    n_groups = len(ent_per_group)

    if indices == 'all':

        aux_dict = defaultdict(list)
        for group_index in range(n_groups):
            aux_dict[ent_per_group[group_index]].append(aux_arr[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index in range(n_groups):
            ii = ent_per_group[group_index]
            if ii in aux_dict:
                aux_dict[ii].append(aux_arr[group_index])

        output = [aux_dict[ii] for ii in indices]

    del mol_idx_arr, ent_idx_arr, ent_per_group, n_groups, aux_dict

    return output


@digest(form=form)
def get_molecule_index_from_entity(item, indices='all', skip_digestion=False):

    if is_all(indices):
        grouped = item.molecules.groupby('entity_index').groups
        output = [grouped[ii].tolist() for ii in grouped]
        del grouped
    else:
        subset = item.molecules.loc[item.molecules['entity_index'].isin(indices)]
        grouped = subset.groupby('entity_index').groups
        output = [grouped.get(ii, []).tolist() for ii in indices]
        del subset, grouped

    return output


@digest(form=form)
def get_molecule_id_from_entity(item, indices='all', skip_digestion=False):

    aux = item.molecules.groupby('entity_index')['molecule_id']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_molecule_name_from_entity(item, indices='all', skip_digestion=False):

    aux = item.molecules.groupby('entity_index')['molecule_name']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_molecule_type_from_entity(item, indices='all', skip_digestion=False):

    aux = item.molecules.groupby('entity_index')['molecule_type']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_entity_index_from_entity(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_entities_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@digest(form=form)
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.entities['entity_id'].to_list()
    else:
        output = item.entities['entity_id'][indices].to_list()

    return output


@digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.entities['entity_name'].to_list()
    else:
        output = item.entities['entity_name'][indices].to_list()

    return output


@digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.entities['entity_type'].to_list()
    else:
        output = item.entities['entity_type'][indices].to_list()

    return output


@digest(form=form)
def get_component_index_from_entity(item, indices='all', skip_digestion=False):

    target_index = get_entity_index_from_component(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_component_id_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_component_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_component_name_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_component_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_component_type_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_component_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_chain_index_from_entity(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    output = []
    for aux in atom_index_from_target:
        aux2 = get_chain_index_from_atom(item, indices=aux, skip_digestion=True)
        aux2 = np.unique(aux2).tolist()
        if len(aux2)==1:
            aux2=aux2[0]
        output.append(aux2)

    del atom_index_from_target, aux

    return output


@digest(form=form)
def get_chain_id_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.hstack(target_indices), return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        if isinstance(aux, (list, tuple)):
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].tolist())
        elif isinstance(aux, int):
            jj = ii+1
            output.append(aux_output[ii])
        else:
            raise ValueError
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_chain_name_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.hstack(target_indices), return_inverse=True)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        if isinstance(aux, (list, tuple)):
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].tolist())
        elif isinstance(aux, int):
            jj = ii+1
            output.append(aux_output[ii])
        else:
            raise ValueError
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_chain_type_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.hstack(target_indices), return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        if isinstance(aux, (list, tuple)):
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].tolist())
        elif isinstance(aux, int):
            jj = ii+1
            output.append(aux_output[ii])
        else:
            raise ValueError
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_bond_index_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_type_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_order_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bond_index_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):

    output = get_group_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_components_from_entity(item, indices='all', skip_digestion=False):

    output = get_component_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    output = get_molecule_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_entities_from_entity(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_chains_from_entity(item, indices='all', skip_digestion=False):

    aux = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
    output = []
    for ii in aux:
        try:
            output.append(len(ii))
        except:
            output.append(1)

    return output


@digest(form=form)
def get_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    output = []
    atom_indices = get_atom_index_from_entity(item, indices, skip_digestion=True)
    for aux_atom_indices in atom_indices:
        bond_indices = get_bond_index_from_atom(item, aux_atom_indices, skip_digestion=True)
        output.append(np.unique(np.concatenate(bond_indices)).shape[0])

    return output


@digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    output = []
    atom_indices = get_atom_index_from_entity(item, indices, skip_digestion=True)
    for aux_atom_indices in atom_indices:
        bond_indices = get_inner_bond_index_from_atom(item, aux_atom_indices, skip_digestion=True)
        output.append(np.unique(np.concatenate(bond_indices)).shape[0])

    return output


@digest(form=form)
def get_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@digest(form=form)
def get_n_ions_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@digest(form=form)
def get_n_waters_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@digest(form=form)
def get_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@digest(form=form)
def get_n_polysaccharides_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'polysaccharide').sum()

    return output


@digest(form=form)
def get_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@digest(form=form)
def get_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@digest(form=form)
def get_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@digest(form=form)
def get_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@digest(form=form)
def get_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


# From component


@digest(form=form)
def get_atom_index_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        grouped = item.atoms.groupby('component_index').groups
        output = [grouped[ii] for ii in grouped]
        del grouped
    else:
        selected_groups = item.atoms.loc[item.atoms['component_index'].isin(indices)]
        grouped = selected_groups.groupby('component_index').groups
        output = [grouped.get(ii, []) for ii in indices]
        del grouped, selected_groups

    return output


@digest(form=form)
def get_atom_id_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        grouped = item.atoms.groupby('component_index')['atom_id'].groups
        output = [item.atoms['atom_id'].take(grouped[ii]).tolist() for ii in grouped]
        del grouped
    else:
        selected_groups = item.atoms.loc[item.atoms['component_index'].isin(indices)]
        grouped = selected_groups.groupby('component_index')['atom_id'].groups
        output = [subset['atom_id'].take(grouped.get(ii, [])).tolist() for ii in indices]
        del selected_groups, grouped

    return output

@digest(form=form)
def get_atom_name_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        grouped = item.atoms.groupby('component_index')['atom_name'].groups
        output = [item.atoms['atom_name'].take(grouped[ii]).tolist() for ii in grouped]
        del grouped
    else:
        selected_groups = item.atoms.loc[item.atoms['component_index'].isin(indices)]
        grouped = selected_groups.groupby('component_index')['atom_name'].groups
        output = [subset['atom_name'].take(grouped.get(ii, [])).tolist() for ii in indices]
        del selected_groups, grouped

    return output


@digest(form=form)
def get_atom_type_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        grouped = item.atoms.groupby('component_index')['atom_type'].groups
        output = [item.atoms['atom_type'].take(grouped[ii]).tolist() for ii in grouped]
        del grouped
    else:
        selected_groups = item.atoms.loc[item.atoms['component_index'].isin(indices)]
        grouped = selected_groups.groupby('component_index')['atom_type'].groups
        output = [subset['atom_type'].take(grouped.get(ii, [])).tolist() for ii in indices]
        del selected_groups, grouped

    return output


@digest(form=form)
def get_group_index_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        output = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        output = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    return output


@digest(form=form)
def get_group_id_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        group_indices = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        group_indices = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    output = [item.groups['group_id'].take(ii).tolist() for ii in group_indices]

    del group_indices

    return output


@digest(form=form)
def get_group_name_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        group_indices = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        group_indices = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    output = [item.groups['group_name'].take(ii).tolist() for ii in group_indices]

    del group_indices

    return output


@digest(form=form)
def get_group_type_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        group_indices = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        group_indices = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    output = [item.groups['group_type'].take(ii).tolist() for ii in group_indices]

    del group_indices

    return output


@digest(form=form)
def get_component_index_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        output = list(range(item.components.shape[0]))
    else:
        output = indices

    return output


@digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        output = item.components['component_id'].to_list()
    else:
        output = item.components['component_id'][indices].to_list()

    return output


@digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        output = item.components['component_name'].to_list()
    else:
        output = item.components['component_name'][indices].to_list()

    return output


@digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        output = item.components['component_type'].to_list()
    else:
        output = item.components['component_type'][indices].to_list()

    return output


@digest(form=form)
def get_molecule_index_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    output = item.groups['molecule_index'].take(group_indices).to_list()

    del atom_indices, group_indices

    return output


@digest(form=form)
def get_molecule_id_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    molecule_indices = item.groups['molecule_index'].take(group_indices)
    output = item.molecules['molecule_id'].take(molecule_indices).to_list()

    del atom_indices, group_indices, molecule_indices

    return output


@digest(form=form)
def get_molecule_name_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    molecule_indices = item.groups['molecule_index'].take(group_indices)
    output = item.molecules['molecule_name'].take(molecule_indices).to_list()

    del atom_indices, group_indices, molecule_indices

    return output


@digest(form=form)
def get_molecule_type_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    molecule_indices = item.groups['molecule_index'].take(group_indices)
    output = item.molecules['molecule_type'].take(molecule_indices).to_list()

    del atom_indices, group_indices, molecule_indices

    return output


@digest(form=form)
def get_entity_index_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    molecule_indices = item.groups['molecule_index'].take(group_indices)
    output = item.molecules['entity_index'].take(molecule_indices).to_list()

    del atom_indices, group_indices, molecule_indices

    return output


@digest(form=form)
def get_entity_id_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    molecule_indices = item.groups['molecule_index'].take(group_indices)
    entity_indices = item.molecules['entity_index'].take(molecule_indices)
    output = item.entities['entity_id'].take(entity_indices).to_list()

    del atom_indices, group_indices, molecule_indices, entity_indices

    return output


@digest(form=form)
def get_entity_name_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    molecule_indices = item.groups['molecule_index'].take(group_indices)
    entity_indices = item.molecules['entity_index'].take(molecule_indices)
    output = item.entities['entity_name'].take(entity_indices).to_list()

    del atom_indices, group_indices, molecule_indices, entity_indices

    return output


@digest(form=form)
def get_entity_type_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    molecule_indices = item.groups['molecule_index'].take(group_indices)
    entity_indices = item.molecules['entity_index'].take(molecule_indices)
    output = item.entities['entity_type'].take(entity_indices).to_list()

    del atom_indices, group_indices, molecule_indices, entity_indices

    return output


@digest(form=form)
def get_chain_index_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    output = item.groups['chain_index'].take(group_indices).to_list()

    del atom_indices, group_indices

    return output


@digest(form=form)
def get_chain_id_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    chain_indices = item.groups['chain_index'].take(group_indices)
    output = item.chains['chain_id'].take(chain_indices).to_list()

    del atom_indices, group_indices, chain_indices

    return output


@digest(form=form)
def get_chain_name_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    chain_indices = item.groups['chain_index'].take(group_indices)
    output = item.chains['chain_name'].take(chain_indices).to_list()

    del atom_indices, group_indices, chain_indices

    return output


@digest(form=form)
def get_chain_type_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    chain_indices = item.groups['chain_index'].take(group_indices)
    output = item.chains['chain_type'].take(chain_indices).to_list()

    del atom_indices, group_indices, chain_indices

    return output


@digest(form=form)
def get_bond_index_from_component(item, indices='all', skip_digestion=False): ##

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_type_from_component(item, indices='all', skip_digestion=False): ##

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_order_from_component(item, indices='all', skip_digestion=False): ##

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atoms_from_component(item, indices='all', skip_digestion=False): ##

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False): ##

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bond_index_from_component(item, indices='all', skip_digestion=False): ##

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bonded_atoms_from_component(item, indices='all', skip_digestion=False): ##

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False): ##

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_atoms_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    output = [len(ii) for ii in atom_indices]

    del atom_indices

    return output


@digest(form=form)
def get_n_groups_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        group_indices = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        group_indices = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    output = [len(ii) for ii in group_indices]

    del group_indices

    return output


@digest(form=form)
def get_n_components_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        output = item.components.shape[0]
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_molecules_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        output = item.molecules.shape[0]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]
        group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
        molecule_indices = item.groups['molecule_index'].take(group_indices).to_list()
        output = np.unique(molecule_indices).shape[0]
        del atom_indices, group_indices, molecule_indices

    return output


@digest(form=form)
def get_n_entities_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        output = item.entities.shape[0]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]
        group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
        molecule_indices = item.groups['molecule_index'].take(group_indices).to_list()
        entity_indices = item.molecules['entity_index'].take(molecule_indices).to_list()
        output = np.unique(entity_indices).shape[0]
        del atom_indices, group_indices, molecule_indices, entity_indices

    return output


@digest(form=form)
def get_n_chains_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        output = item.chains.shape[0]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]
        group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
        chain_indices = item.groups['chain_index'].take(group_indices).to_list()
        output = np.unique(chain_indices).shape[0]
        del atom_indices, group_indices, chain_indices

    return output


@digest(form=form)
def get_n_bonds_from_component(item, indices='all', skip_digestion=False): ##

    output = []
    atom_indices = get_atom_index_from_component(item, indices, skip_digestion=True)
    for aux_atom_indices in atom_indices:
        bond_indices = get_bond_index_from_atom(item, aux_atom_indices, skip_digestion=True)
        output.append(np.unique(np.concatenate(bond_indices)).shape[0])

    return output


@digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all', skip_digestion=False): ##

    output = []
    atom_indices = get_atom_index_from_component(item, indices, skip_digestion=True)
    for aux_atom_indices in atom_indices:
        bond_indices = get_inner_bond_index_from_atom(item, aux_atom_indices, skip_digestion=True)
        output.append(np.unique(np.concatenate(bond_indices)).shape[0])

    return output


@digest(form=form)
def get_n_amino_acids_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        group_indices = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        group_indices = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    group_indices=np.concatenate(group_indices)
    group_indices = np.unique(group_indices)
    group_types = item.groups['group_type'].take(indices)
    output = (group_types == 'amino acid').sum()

    del group_indices, group_types

    return output


@digest(form=form)
def get_n_nucleotides_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        group_indices = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        group_indices = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    group_indices=np.concatenate(group_indices)
    group_indices = np.unique(group_indices)
    group_types = item.groups['group_type'].take(indices)
    output = (group_types == 'nucleotide').sum()

    del group_indices, group_types

    return output


@digest(form=form)
def get_n_ions_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        group_indices = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        group_indices = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    group_indices=np.concatenate(group_indices)
    group_indices = np.unique(group_indices)
    group_types = item.groups['group_type'].take(indices)
    output = (group_types == 'ion').sum()

    del group_indices, group_types

    return output


@digest(form=form)
def get_n_waters_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        group_indices = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        group_indices = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    group_indices=np.concatenate(group_indices)
    group_indices = np.unique(group_indices)
    group_types = item.groups['group_type'].take(indices)
    output = (group_types == 'water').sum()

    del group_indices, group_types

    return output


@digest(form=form)
def get_n_small_molecules_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        group_indices = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        group_indices = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    group_indices=np.concatenate(group_indices)
    group_indices = np.unique(group_indices)
    group_types = item.groups['group_type'].take(indices)
    output = (group_types == 'small molecule').sum()

    del group_indices, group_types

    return output


@digest(form=form)
def get_n_lipids_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        group_indices = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        group_indices = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    group_indices=np.concatenate(group_indices)
    group_indices = np.unique(group_indices)
    group_types = item.groups['group_type'].take(indices)
    output = (group_types == 'lipid').sum()

    del group_indices, group_types

    return output


@digest(form=form)
def get_n_polysaccharides_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        group_indices = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        group_indices = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    group_indices=np.concatenate(group_indices)
    group_indices = np.unique(group_indices)
    group_types = item.groups['group_type'].take(indices)
    output = (group_types == 'polysaccharide').sum()

    del group_indices, group_types

    return output


@digest(form=form)
def get_n_saccharides_from_component(item, indices='all', skip_digestion=False): ##

    if is_all(indices):
        group_indices = item.atoms.groupby('component_index')['group_index'].unique().apply(list).to_list()
    else:
        group_indices = (
            item.atoms.loc[item.atoms['component_index'].isin(indices)]
            .groupby('component_index')['group_index']
            .unique().reindex(indices, fill_value=np.array([], int))
            .apply(list).to_list()
        )

    group_indices=np.concatenate(group_indices)
    group_indices = np.unique(group_indices)
    group_types = item.groups['group_type'].take(indices)
    output = (group_types == 'saccharide').sum()

    del group_indices, group_types

    return output


@digest(form=form)
def get_n_peptides_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    molecule_indices = item.groups['molecule_index'].take(group_indices).unique()
    molecule_types = item.molecules['molecule_type'].take(molecule_indices)

    output = (molecule_types == 'peptide').sum()

    del atom_indices, group_indices, molecule_indices, molecule_types

    return output


@digest(form=form)
def get_n_proteins_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    molecule_indices = item.groups['molecule_index'].take(group_indices).unique()
    molecule_types = item.molecules['molecule_type'].take(molecule_indices)

    output = (molecule_types == 'protein').sum()

    del atom_indices, group_indices, molecule_indices, molecule_types

    return output


@digest(form=form)
def get_n_dnas_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    molecule_indices = item.groups['molecule_index'].take(group_indices).unique()
    molecule_types = item.molecules['molecule_type'].take(molecule_indices)

    output = (molecule_types == 'dna').sum()

    del atom_indices, group_indices, molecule_indices, molecule_types

    return output


@digest(form=form)
def get_n_rnas_from_component(item, indices='all', skip_digestion=False): ##

    aux = item.atoms.groupby('component_index')

    if is_all(indices):
        atom_indices = [jj.tolist() for _, jj in aux.groups.items()]
    else:
        atom_indices = [aux.groups[ii].tolist() for ii in indices]

    del aux

    group_indices = item.atoms['group_index'].take([ii[0] for ii in atom_indices])
    molecule_indices = item.groups['molecule_index'].take(group_indices).unique()
    molecule_types = item.molecules['molecule_type'].take(molecule_indices)

    output = (molecule_types == 'rna').sum()

    del atom_indices, group_indices, molecule_indices, molecule_types

    return output


# From chain


@digest(form=form)
def get_atom_index_from_chain(item, indices='all', skip_digestion=False):

    aux = item.atoms.groupby('chain_index')

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux.groups.items()]
    else:
        output = [aux.groups[ii].tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_atom_id_from_chain(item, indices='all', skip_digestion=False):

    aux = item.atoms.groupby('chain_index')['atom_id']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_atom_name_from_chain(item, indices='all', skip_digestion=False):

    aux = item.atoms.groupby('chain_index')['atom_name']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_atom_type_from_chain(item, indices='all', skip_digestion=False):

    aux = item.atoms.groupby('chain_index')['atom_type']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_group_index_from_chain(item, indices='all', skip_digestion=False):

    aux = item.groups.groupby('chain_index')

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux.groups.items()]
    else:
        output = [aux.groups[ii].tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_group_id_from_chain(item, indices='all', skip_digestion=False):

    aux = item.groups.groupby('chain_index')['group_id']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_group_name_from_chain(item, indices='all', skip_digestion=False):

    aux = item.groups.groupby('chain_index')['group_name']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_group_type_from_chain(item, indices='all', skip_digestion=False):

    aux = item.groups.groupby('chain_index')['group_type']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_component_index_from_chain(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    output = []
    for aux in atom_index_from_target:
        aux2 = get_component_index_from_atom(item, indices=aux, skip_digestion=True)
        aux2 = np.unique(aux2).tolist()
        if len(aux2)==1:
            aux2=aux2[0]
        output.append(aux2)

    del atom_index_from_target, aux

    return output


@digest(form=form)
def get_component_id_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_component_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.hstack(target_indices), return_inverse=True)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        if isinstance(aux, (list, tuple)):
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].tolist())
        elif isinstance(aux, int):
            jj = ii+1
            output.append(aux_output[ii])
        else:
            raise ValueError
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_component_name_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_component_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.hstack(target_indices), return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        if isinstance(aux, (list, tuple)):
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].tolist())
        elif isinstance(aux, int):
            jj = ii+1
            output.append(aux_output[ii])
        else:
            raise ValueError
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_component_type_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_component_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.hstack(target_indices), return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        if isinstance(aux, (list, tuple)):
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].tolist())
        elif isinstance(aux, int):
            jj = ii+1
            output.append(aux_output[ii])
        else:
            raise ValueError
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_molecule_index_from_chain(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    output = []
    for aux in atom_index_from_target:
        aux2 = get_molecule_index_from_atom(item, indices=aux, skip_digestion=True)
        aux2 = np.unique(aux2).tolist()
        if len(aux2)==1:
            aux2=aux2[0]
        output.append(aux2)

    del atom_index_from_target, aux

    return output


@digest(form=form)
def get_molecule_id_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.hstack(target_indices), return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        if isinstance(aux, (list, tuple)):
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].tolist())
        elif isinstance(aux, int):
            jj = ii+1
            output.append(aux_output[ii])
        else:
            raise ValueError
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_molecule_name_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.hstack(target_indices), return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        if isinstance(aux, (list, tuple)):
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].tolist())
        elif isinstance(aux, int):
            jj = ii+1
            output.append(aux_output[ii])
        else:
            raise ValueError
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_molecule_type_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.hstack(target_indices), return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        if isinstance(aux, (list, tuple)):
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].tolist())
        elif isinstance(aux, int):
            jj = ii+1
            output.append(aux_output[ii])
        else:
            raise ValueError
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_entity_index_from_chain(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    output = []
    for aux in atom_index_from_target:
        aux2 = get_entity_index_from_atom(item, indices=aux, skip_digestion=True)
        aux2 = np.unique(aux2).tolist()
        if len(aux2)==1:
            aux2=aux2[0]
        output.append(aux2)

    del atom_index_from_target, aux

    return output


@digest(form=form)
def get_entity_id_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_entity_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.hstack(target_indices), return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        if isinstance(aux, (list, tuple)):
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].tolist())
        elif isinstance(aux, int):
            jj = ii+1
            output.append(aux_output[ii])
        else:
            raise ValueError
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_entity_name_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_entity_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.hstack(target_indices), return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        if isinstance(aux, (list, tuple)):
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].tolist())
        elif isinstance(aux, int):
            jj = ii+1
            output.append(aux_output[ii])
        else:
            raise ValueError
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_entity_type_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_entity_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.hstack(target_indices), return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        if isinstance(aux, (list, tuple)):
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].tolist())
        elif isinstance(aux, int):
            jj = ii+1
            output.append(aux_output[ii])
        else:
            raise ValueError
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@digest(form=form)
def get_chain_index_from_chain(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_chains_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@digest(form=form)
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.chains['chain_id'].to_list()
    else:
        output = item.chains['chain_id'][indices].to_list()

    return output


@digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.chains['chain_name'].to_list()
    else:
        output = item.chains['chain_name'][indices].to_list()

    return output


@digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.chains['chain_type'].to_list()
    else:
        output = item.chains['chain_type'][indices].to_list()

    return output


@digest(form=form)
def get_bond_index_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_type_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_order_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bond_index_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_groups_from_chain(item, indices='all', skip_digestion=False):

    aux = get_group_index_from_chain(item, indices, skip_digestion=True)
    output = []
    for ii in aux:
        try:
            output.append(len(ii))
        except:
            output.append(1)

    return output


@digest(form=form)
def get_n_components_from_chain(item, indices='all', skip_digestion=False):

    aux = get_component_index_from_chain(item, indices, skip_digestion=True)
    output = []
    for ii in aux:
        try:
            output.append(len(ii))
        except:
            output.append(1)

    return output


@digest(form=form)
def get_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    aux = get_molecule_index_from_chain(item, indices, skip_digestion=True)
    output = []
    for ii in aux:
        try:
            output.append(len(ii))
        except:
            output.append(1)

    return output


@digest(form=form)
def get_n_entities_from_chain(item, indices='all', skip_digestion=False):

    aux = get_entity_index_from_chain(item, indices, skip_digestion=True)
    output = []
    for ii in aux:
        try:
            output.append(len(ii))
        except:
            output.append(1)

    return output


@digest(form=form)
def get_n_chains_from_chain(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    output = []
    atom_indices = get_atom_index_from_chain(item, indices, skip_digestion=True)
    for aux_atom_indices in atom_indices:
        bond_indices = get_bond_index_from_atom(item, aux_atom_indices, skip_digestion=True)
        output.append(np.unique(np.concatenate(bond_indices)).shape[0])

    return output


@digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    output = []
    atom_indices = get_atom_index_from_chain(item, indices, skip_digestion=True)
    for aux_atom_indices in atom_indices:
        bond_indices = get_inner_bond_index_from_atom(item, aux_atom_indices, skip_digestion=True)
        output.append(np.unique(np.concatenate(bond_indices)).shape[0])

    return output


@digest(form=form)
def get_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@digest(form=form)
def get_n_ions_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@digest(form=form)
def get_n_waters_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@digest(form=form)
def get_n_lipids_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@digest(form=form)
def get_n_polysaccharides_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'polysaccharide').sum()

    return output


@digest(form=form)
def get_n_saccharides_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@digest(form=form)
def get_n_peptides_from_chain(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@digest(form=form)
def get_n_proteins_from_chain(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@digest(form=form)
def get_n_dnas_from_chain(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@digest(form=form)
def get_n_rnas_from_chain(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


# From bond


@digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_bonds_from_system(item)
        output = np.arange(n_aux, dtype=int).tolist()
    else:
        output = indices

    return output


@digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    if 'order' in item.bonds:

        if is_all(indices):
            output = item.bonds['order'].to_list()
        else:
            output = item.bonds['order'][indices].to_list()

    else:

        if is_all(indices):
            n_aux = get_n_bonds_from_system(item, skip_digestion=True)
            output = [None] * n_aux
        else:
            output = [None] * len(indices)

    return output


@digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    if 'type' in item.bonds:

        if is_all(indices):
            output = item.bonds['type'].to_list()
        else:
            output = item.bonds['type'][indices].to_list()

    else:

        if is_all(indices):
            n_aux = get_n_bonds_from_system(item, skip_digestion=True)
            output = [None] * n_aux
        else:
            output = [None] * len(indices)

    return output


@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    if is_all(indices):

        return [[bond.atom1_index, bond.atom2_index] for bond in item.bonds.itertuples(index=False)]

    else:

        return [[bond.atom1_index, bond.atom2_index] for bond in item.bonds.iloc[indices].itertuples(index=False)]

    return tmp_out


@digest(form=form)
def get_bonded_atom_pairs_from_bond(item, indices='all', skip_digestion=False):

    return get_bonded_atoms_from_bond(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_bonds_from_bond(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


# From system


@digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    return item.atoms.shape[0]


@digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    return item.groups.shape[0]


@digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    return item.components.shape[0]


@digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    return item.molecules.shape[0]


@digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    return item.entities.shape[0]


@digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    return item.chains.shape[0]


@digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    return item.bonds.shape[0]


@digest(form=form)
def get_n_amino_acids_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@digest(form=form)
def get_n_nucleotides_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@digest(form=form)
def get_n_ions_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@digest(form=form)
def get_n_waters_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@digest(form=form)
def get_n_small_molecules_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@digest(form=form)
def get_n_lipids_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@digest(form=form)
def get_n_polysaccharides_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'polysaccharide').sum()

    return output


@digest(form=form)
def get_n_saccharides_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@digest(form=form)
def get_n_peptides_from_system(item, skip_digestion=False):

    molecule_types = get_molecule_type_from_molecule(item, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@digest(form=form)
def get_n_proteins_from_system(item, skip_digestion=False):

    molecule_types = get_molecule_type_from_molecule(item, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@digest(form=form)
def get_n_dnas_from_system(item, skip_digestion=False):

    molecule_types = get_molecule_type_from_molecule(item, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@digest(form=form)
def get_n_rnas_from_system(item, skip_digestion=False):

    molecule_types = get_molecule_type_from_molecule(item, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


@digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):

    n_bonds = get_n_bonds_from_system(item, skip_digestion=True)
    output = list(range(n_bonds))

    return output


@digest(form=form)
def get_bonded_atoms_from_system(item, skip_digestion=False):

    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    
    G.add_edges_from(edges)

    indices = get_atom_index_from_atom(item, skip_digestion=True)

    output = []

    for ii in indices:
        if ii in G:
            output.append(list(G.neighbors(ii)))
        else:
            output.append([])

    del G, edges

    return output


@digest(form=form)
def get_bonded_atom_pairs_from_system(item, skip_digestion=False):

    output = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
   
    return output


@digest(form=form)
def get_inner_bond_index_from_system(item, skip_digestion=False):

    n_bonds = get_n_bonds_from_system(item, skip_digestion=True)
    output = list(range(n_bonds))

    return output


@digest(form=form)
def get_inner_bonded_atoms_from_system(item, skip_digestion=False):

    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    
    G.add_edges_from(edges)

    output = []
    for nodo in G.nodes():
        output.append(list(G.neighbors(nodo)))

    del G, edges

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_system(item, skip_digestion=False):

    output = get_bonded_atom_pairs_from_bond(item)
   
    return output


# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

