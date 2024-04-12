from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
import types

form = 'molsysmt.Topology'


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
        output = item.atoms['atom_id'].to_list()
    else:
        output = item.atoms['atom_id'][indices].to_list()

    return output


@digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.atoms['atom_name'].to_list()
    else:
        output = item.atoms['atom_name'][indices].to_list()

    return output


@digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.atoms['atom_type'].to_list()
    else:
        output = item.atoms['atom_type'][indices].to_list()

    return output


@digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.atoms['group_index'].to_list()
    else:
        output = item.atoms['group_index'][indices].to_list()

    return output


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
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    output = item.groups['component_index'][group_indices].to_list()
    del group_indices

    return output


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

    component_indices = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
    output = item.components['molecule_index'][component_indices].to_list()
    del component_indices

    return output


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

    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    output = item.molecules['entity_index'][molecule_indices].to_list()
    del molecule_indices

    return output


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
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
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
        output = item.atoms['chain_index'][:].to_numpy()
    else:
        output = item.atoms['chain_index'][indices].to_list()

    return output


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
    output = (np.array(group_types) == 'oligosaccharide').sum()

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


# From group


@digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False):

    aux = item.atoms.groupby('group_index')

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux.groups.items()]
    else:
        output = [aux.groups[ii].tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_atom_id_from_group(item, indices='all', skip_digestion=False):

    aux = item.atoms.groupby('group_index')['atom_id']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_atom_name_from_group(item, indices='all', skip_digestion=False):

    aux = item.atoms.groupby('group_index')['atom_name']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_atom_type_from_group(item, indices='all', skip_digestion=False):

    aux = item.atoms.groupby('group_index')['atom_type']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

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
        output = item.groups['group_id'].to_list()
    else:
        output = item.groups['group_id'][indices].to_list()

    return output


@digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.groups['group_name'].to_list()
    else:
        output = item.groups['group_name'][indices].to_list()

    return output


@digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.groups['group_type'].to_list()
    else:
        output = item.groups['group_type'][indices].to_list()

    return output


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
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, skip_digestion=True)
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


# From component


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

    aux = item.groups.groupby('component_index')

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux.groups.items()]
    else:
        output = [aux.groups[ii].tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_group_id_from_component(item, indices='all', skip_digestion=False):

    aux = item.groups.groupby('component_index')['group_id']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_group_name_from_component(item, indices='all', skip_digestion=False):

    aux = item.groups.groupby('component_index')['group_name']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_group_type_from_component(item, indices='all', skip_digestion=False):

    aux = item.groups.groupby('component_index')['group_type']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

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
        output = item.components['component_id'].to_list()
    else:
        output = item.components['component_id'][indices].to_list()

    return output


@digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.components['component_name'].to_list()
    else:
        output = item.components['component_name'][indices].to_list()

    return output


@digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.components['component_type'].to_list()
    else:
        output = item.components['component_type'][indices].to_list()

    return output


@digest(form=form)
def get_molecule_index_from_component(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_molecule_id_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_component(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_name_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_component(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_type_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_component(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices)
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
def get_n_entities_from_component(item, indices='all', skip_digestion=False):


    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
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


# From molecule


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

    aux = item.components.groupby('molecule_index')

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux.groups.items()]
    else:
        output = [aux.groups[ii].tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_component_id_from_molecule(item, indices='all', skip_digestion=False):

    aux = item.components.groupby('molecule_index')['component_id']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_component_name_from_molecule(item, indices='all', skip_digestion=False):

    aux = item.components.groupby('molecule_index')['component_name']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

    return output


@digest(form=form)
def get_component_type_from_molecule(item, indices='all', skip_digestion=False):

    aux = item.components.groupby('molecule_index')['component_type']

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux]
    else:
        output = [aux.get_group(ii).tolist() for ii in indices]

    del aux

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
        output = item.molecules['molecule_id'].to_list()
    else:
        output = item.molecules['molecule_id'][indices].to_list()

    return output


@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.molecules['molecule_name'].to_list()
    else:
        output = item.molecules['molecule_name'][indices].to_list()

    return output


@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.molecules['molecule_type'].to_list()
    else:
        output = item.molecules['molecule_type'][indices].to_list()

    return output


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


@digest(form=form)
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_molecule(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    return _auxiliary_getter(get_n_bonds_from_molecule, item, indices)


@digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    return _auxiliary_getter(get_n_inner_bonds_from_molecule, item, indices)


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
    output = (np.array(group_types) == 'rna').sum()

    return output


# From entity


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

    aux = item.molecules.groupby('entity_index')

    if is_all(indices):
        output = [jj.tolist() for ii, jj in aux.groups.items()]
    else:
        output = [aux.groups[ii].tolist() for ii in indices]

    del aux

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
        output = item.entities['entity_name'].to_list()
    else:
        output = item.entities['entity_name'][indices].to_list()

    return output


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


# From bond


@digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_bonds_from_system(item)
        output = np.arange(n_aux, dtype=int).tolist()
    else:
        output = indices.tolist()

    return output


@digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    if 'order' in item.bonds:

        if is_all(indices):
            output = item.bonds['order'].to_list()
        else:
            output = item.bonds['order'][indices].to_list()

    else:

        output = None

    return output


@digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    if 'type' in item.bonds:

        if is_all(indices):
            output = item.bonds['type'].to_list()
        else:
            output = item.bonds['type'][indices].to_list()

    else:

        output = None

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
        n_aux = get_n_bonds_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

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


# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

