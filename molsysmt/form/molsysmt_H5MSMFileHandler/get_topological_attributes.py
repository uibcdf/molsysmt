from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import pandas as pd
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
import types
from networkx import Graph


form='molsysmt.H5MSMFileHandler'

#######################################################################
#                 To be customized for each form                      #
#######################################################################

# From atom

@digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_atoms_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['atoms']['id'][:].astype('int64')
    else:
        output = item.file['topology']['atoms']['id'][indices].astype('int64')

    return output.tolist()


@digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['atoms']['name'][:].astype('str')
    else:
        output = item.file['topology']['atoms']['name'][indices].astype('str')

    return output.tolist()


@digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['atoms']['type'][:].astype('str')
    else:
        output = item.file['topology']['atoms']['type'][indices].astype('str')

    return output.tolist()


@digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['atoms']['group_index'][:].astype('int')
    else:
        output = item.file['topology']['atoms']['group_index'][indices].astype('int')

    return output.tolist()


@digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    group_index = get_group_index_from_atom(item, indices, skip_digestion=False)
    output = item.file['topology']['groups']['component_index'][group_index].astype('int')

    return output.tolist()


@digest(form=form)
def get_component_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_component_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_component_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    component_index = get_component_index_from_atom(item, indices, skip_digestion=False)
    output = item.file['topology']['components']['molecule_index'][component_index].astype('int')

    return output.tolist()


@digest(form=form)
def get_molecule_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    molecule_index = get_molecule_index_from_atom(item, indices, skip_digestion=False)
    output = item.file['topology']['molecules']['entity_index'][molecule_index].astype('int')

    return output.tolist()


@digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['atoms']['chain_index'][:].astype('int')
    else:
        output = item.file['topology']['atoms']['chain_index'][indices].astype('int')

    return output.tolist()


@digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False):

    output = None

    G = Graph()
    edges = get_bonded_atoms_pairs_from_bond(item, skip_digestion=True)
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
def get_bond_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_bond_type_from_bond(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_bond_order_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_bond_order_from_bond(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    output = None

    G = Graph()
    edges = get_bonded_atoms_pairs_from_bond(item, skip_digestion=True)
    
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
def get_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

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
def get_inner_bond_index_from_atom(item, indices='all', skip_digestion=False):

    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    n_bonds = len(edges)
    edge_indices = np.array([{'index': ii} for ii in range(n_bonds)]).reshape([n_bonds, 1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if is_all(indices):

        indices = get_atom_index_from_atom(item, skip_digestion=True)

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
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

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
def get_inner_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    output = None

    if is_all(indices):

        output = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
   
    else:

        pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
        pairs = np.array(pairs)
        mask = np.isin(pairs[:,0], indices) * np.isin(pairs[:,1], indices)
        output = pairs[mask,:].tolist()

        del pairs, mask

    return output


@digest(form=form)
def get_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_groups_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        output = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_components_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        output = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_entities_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_chains_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        bond_indices = get_bond_index_from_atom(item, indices, skip_digestion=True)
        output = np.unique(np.concatenate(bond_indices)).shape[0]
        del bond_indices

    return output


@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        bond_indices = get_inner_bond_index_from_atom(item, indices, skip_digestion=True)
        output = np.unique(np.concatenate(bond_indices)).shape[0]
        del bond_indices

    return output


@digest(form=form)
def get_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@digest(form=form)
def get_n_ions_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@digest(form=form)
def get_n_waters_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@digest(form=form)
def get_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@digest(form=form)
def get_n_oligosaccharides_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'olicosaccharide').sum()

    return output


@digest(form=form)
def get_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@digest(form=form)
def get_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@digest(form=form)
def get_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@digest(form=form)
def get_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@digest(form=form)
def get_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


## From group


@digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False):

    target_index = get_group_index_from_atom(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_atom_id_from_group(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_atom_name_from_group(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_atom_type_from_group(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_index_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_groups_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['groups']['id'][:].astype('int64')
    else:
        output = item.file['topology']['groups']['id'][indices].astype('int64')

    return output.tolist()


@digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['groups']['name'][:].astype('str')
    else:
        output = item.file['topology']['groups']['name'][indices].astype('str')

    return output.tolist()


@digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['groups']['type'][:].astype('str')
    else:
        output = item.file['topology']['groups']['type'][indices].astype('str')

    return output.tolist()


@digest(form=form)
def get_component_index_from_group(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_component_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_index_from_group(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_index_from_group(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_index_from_group(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_bond_index_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_type_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_order_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bond_index_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_atoms_from_group(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_group(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_groups_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_components_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        output = get_component_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_molecules_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_entities_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_chains_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_bonds_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_inner_bonds_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_amino_acids_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@digest(form=form)
def get_n_nucleotides_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@digest(form=form)
def get_n_ions_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@digest(form=form)
def get_n_waters_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@digest(form=form)
def get_n_small_molecules_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@digest(form=form)
def get_n_lipids_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@digest(form=form)
def get_n_oligosaccharides_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'oligosaccharide').sum()

    return output


@digest(form=form)
def get_n_saccharides_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@digest(form=form)
def get_n_peptides_from_group(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@digest(form=form)
def get_n_proteins_from_group(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@digest(form=form)
def get_n_dnas_from_group(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@digest(form=form)
def get_n_rnas_from_group(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


## From component


@digest(form=form)
def get_atom_index_from_component(item, indices='all', skip_digestion=False):

    target_index = get_component_index_from_atom(item)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_atom_id_from_component(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_atom_name_from_component(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_atom_type_from_component(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_index_from_component(item, indices='all', skip_digestion=False):

    target_index = get_component_index_from_group(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_group_id_from_component(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_name_from_component(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_type_from_component(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_component_index_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_components_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['components']['id'][:].astype('int64')
    else:
        output = item.file['topology']['components']['id'][indices].astype('int64')

    return output.tolist()


@digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['components']['name'][:].astype('str')
    else:
        output = item.file['topology']['components']['name'][indices].astype('str')

    return output.tolist()


@digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['components']['type'][:].astype('str')
    else:
        output = item.file['topology']['components']['type'][indices].astype('str')

    return output.tolist()


@digest(form=form)
def get_molecule_index_from_component(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_molecule_id_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_name_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_type_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_index_from_component(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_entity_id_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_name_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_type_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_index_from_component(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_chain_id_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_name_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_type_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_bond_index_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_type_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_order_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bond_index_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_atoms_from_component(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_groups_from_component(item, indices='all', skip_digestion=False):

    output = get_group_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_components_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_molecules_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_chains_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_component(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_entities_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_bonds_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_amino_acids_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@digest(form=form)
def get_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output

@digest(form=form)
def get_n_ions_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@digest(form=form)
def get_n_waters_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@digest(form=form)
def get_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@digest(form=form)
def get_n_lipids_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@digest(form=form)
def get_n_oligosaccharides_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'oligosaccharide').sum()

    return output


@digest(form=form)
def get_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@digest(form=form)
def get_n_peptides_from_component(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@digest(form=form)
def get_n_proteins_from_component(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@digest(form=form)
def get_n_dnas_from_component(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@digest(form=form)
def get_n_rnas_from_component(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


## From molecule


@digest(form=form)
def get_atom_index_from_molecule(item, indices='all', skip_digestion=False):

    target_index = get_molecule_index_from_atom(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_atom_id_from_molecule(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_atom_name_from_molecule(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_atom_type_from_molecule(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_index_from_molecule(item, indices='all', skip_digestion=False):

    target_index = get_molecule_index_from_group(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_group_id_from_molecule(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_name_from_molecule(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_type_from_molecule(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_component_index_from_molecule(item, indices='all', skip_digestion=False):

    target_index = get_molecule_index_from_component(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_component_id_from_molecule(item, indices='all', skip_digestion=False):

    target_indices = get_component_index_from_molecule(item, indices=indices, skip_digestion=True)
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
def get_component_name_from_molecule(item, indices='all', skip_digestion=False):

    target_indices = get_component_index_from_molecule(item, indices=indices, skip_digestion=True)
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
def get_component_type_from_molecule(item, indices='all', skip_digestion=False):

    target_indices = get_component_index_from_molecule(item, indices=indices, skip_digestion=True)
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
def get_molecule_index_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_molecules_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['molecules']['id'][:].astype('int')
    else:
        output = item.file['topology']['molecules']['id'][indices].astype('int')

    return output.tolist()


@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['molecules']['name'][:].astype('str')
    else:
        output = item.file['topology']['molecules']['name'][indices].astype('str')

    return output.tolist()


@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['molecules']['type'][:].astype('str')
    else:
        output = item.file['topology']['molecules']['type'][indices].astype('str')

    return output.tolist()


@digest(form=form)
def get_entity_index_from_molecule(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_entity_id_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_name_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_type_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_index_from_molecule(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_chain_id_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_name_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_type_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_type_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_order_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_inner_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    output = get_group_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_components_from_molecule(item, indices='all', skip_digestion=False):

    output = get_component_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_molecules_from_system(item)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


digest(form=form)
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_molecule(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@digest(form=form)
def get_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@digest(form=form)
def get_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@digest(form=form)
def get_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output

@digest(form=form)
def get_n_oligosaccharides_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'oligosaccharide').sum()

    return output


@digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@digest(form=form)
def get_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'peptide').sum()

    return output


@digest(form=form)
def get_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'protein').sum()

    return output


@digest(form=form)
def get_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'dna').sum()

    return output


@digest(form=form)
def get_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'dna').sum()

    return output


## From entity


@digest(form=form)
def get_atom_index_from_entity(item, indices='all', skip_digestion=False):

    target_index = get_entity_index_from_atom(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_atom_id_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_atom_name_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_atom_type_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_index_from_entity(item, indices='all', skip_digestion=False):

    target_index = get_entity_index_from_group(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_group_id_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_name_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_type_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_molecule_index_from_entity(item, indices='all', skip_digestion=False):

    target_index = get_entity_index_from_molecule(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_molecule_id_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_molecule_name_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_molecule_type_from_entity(item, indices='all', skip_digestion=False):

    target_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
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
        output = item.file['topology']['entities']['id'][:].astype('int')
    else:
        output = item.file['topology']['entities']['id'][indices].astype('int')

    return output.tolist()


@digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['entities']['name'][:].astype('str')
    else:
        output = item.file['topology']['entities']['name'][indices].astype('str')

    return output.tolist()


@digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['entities']['type'][:].astype('str')
    else:
        output = item.file['topology']['entities']['type'][indices].astype('str')

    if not is_all(indices):
        output = output[indices]

    return output.tolist()


@digest(form=form)
def get_chain_index_from_entity(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_chain_id_from_entity(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_name_from_entity(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_type_from_entity(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


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

    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


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
def get_n_oligosaccharides_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'oligosaccharide').sum()

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


## From chain


@digest(form=form)
def get_atom_index_from_chain(item, indices='all', skip_digestion=False):

    target_index = get_chain_index_from_atom(item)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_atom_id_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_atom_name_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_atom_type_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_index_from_chain(item, indices='all', skip_digestion=False):

    target_index = get_chain_index_from_group(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_group_id_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_name_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_group_type_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_component_index_from_chain(item, indices='all', skip_digestion=False):

    target_index = get_chain_index_from_component(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_component_id_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_component_index_from_chain(item, indices=indices, skip_digestion=True)
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
def get_component_name_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_component_index_from_chain(item, indices=indices, skip_digestion=True)
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
def get_component_type_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_component_index_from_chain(item, indices=indices, skip_digestion=True)
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
def get_molecule_index_from_chain(item, indices='all', skip_digestion=False):

    target_index = get_chain_index_from_molecule(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_molecule_id_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_molecule_name_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_molecule_type_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_entity_index_from_chain(item, indices='all', skip_digestion=False):

    target_index = get_chain_index_from_entity(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_entity_id_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_entity_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_entity_name_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_entity_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
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
def get_entity_type_from_chain(item, indices='all', skip_digestion=False):

    target_indices = get_entity_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
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
        output = item.file['topology']['chains']['id'][:].astype('int')
    else:
        output = item.file['topology']['chains']['id'][indices].astype('int')

    return output.tolist()


@digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['chains']['name'][:].astype('str')
    else:
        output = item.file['topology']['chains']['name'][indices].astype('str')

    return output.tolist()


@digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.file['topology']['chains']['type'][:].astype('str')
    else:
        output = item.file['topology']['chains']['type'][indices].astype('str')

    return output.tolist()


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

    output = get_group_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_components_from_chain(item, indices='all', skip_digestion=False):

    output = get_component_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    output = get_molecule_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_entities_from_chain(item, indices='all', skip_digestion=False):

    output = get_entity_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

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

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


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
def get_n_oligosaccharides_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'oligosaccharide').sum()

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


## From system


@digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    output = item.file['topology'].attrs['n_atoms']

    if output==0:
        output = item.file['structures'].attrs['n_atoms']

    return output


@digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    output = item.file['topology'].attrs['n_groups']

    return output


@digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    output = item.file['topology'].attrs['n_components']

    return output


@digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    output = item.file['topology'].attrs['n_chains']

    return output


@digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    output = item.file['topology'].attrs['n_molecules']

    return output


@digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    output = item.file['topology'].attrs['n_entities']

    return output


@digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    output = item.file['topology'].attrs['n_bonds']

    return output


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
def get_n_oligosaccharides_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'oligosaccharide').sum()

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
    edges = get_bonded_atoms_pairs_from_bond(item, skip_digestion=True)
    
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

    output = get_bonded_atoms_pairs_from_bond(item, skip_digestion=True)
   
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
    edges = get_bonded_atoms_pairs_from_bond(item, skip_digestion=True)
    
    G.add_edges_from(edges)

    output = []
    for nodo in G.nodes():
        output.append(list(G.neighbors(nodo)))

    del G, edges

    return output


@digest(form=form)
def get_inner_bonded_atom_pairs_from_system(item, skip_digestion=False):

    output = get_bonded_atoms_pairs_from_bond(item)
   
    return output


## From bond


@digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_bonds_from_system(item)
        output = np.arange(n_aux, dtype=int).tolist()
    else:
        output = indices.tolist()

    return output


@digest(form=form)
def get_bond_id_from_bond(item, indices='all', skip_digestion=False):

    output = item.file['topology']['bonds']['id'][:].astype('int64')

    if not is_all(indices):
        output = output[indices]

    return output


@digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    output = item.file['topology']['bonds']['order'][:].astype('str')

    if not is_all(indices):
        output = output[indices]

    return output


@digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    output = item.file['topology']['bonds']['type'][:].astype('str')

    if not is_all(indices):
        output = output[indices]

    return output


@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    tmp_out = None

    if is_all(indices):

        atom1_index = item.file['topology']['bonds']['atom1_index'][:].astype('int64')
        atom2_index = item.file['topology']['bonds']['atom2_index'][:].astype('int64')

    else:

        atom1_index = item.file['topology']['bonds']['atom1_index'][indices].astype('int64')
        atom2_index = item.file['topology']['bonds']['atom2_index'][indices].astype('int64')

    tmp_out = np.array([atom1_index, atom2_index])
    tmp_out = np.sort(tmp_out)

    return tmp_out


@digest(form=form)
def get_bonded_atom_pairs_from_bond(item, indices='all', skip_digestion=False):

    return get_bonded_atoms_from_bond(item, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_bonds_from_bond(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_bonds_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output



# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

