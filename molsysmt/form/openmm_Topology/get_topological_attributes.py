from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
from networkx import Graph
import numpy as np
import types
from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
import pandas as pd

form='openmm.Topology'


## From atom


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_atoms_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    atom=list(item.atoms())
    output=[str(atom[ii].id) for ii in tmp_indices]
    del(atom)

    return output


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    atom=list(item.atoms())
    output=[atom[ii].name for ii in tmp_indices]
    del(atom)

    return output


@arg_digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    atom=list(item.atoms())
    output=[atom[ii].element.symbol for ii in tmp_indices]
    del(atom)

    return output


@arg_digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    atom=list(item.atoms())
    output = [atom[ii].residue.index for ii in tmp_indices]
    del(atom)

    return output


@arg_digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    from molsysmt.element.component import get_component_index as _get

    output = _get(item, element='atom', selection=indices, redefine_indices=True, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_component_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_component_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    output = get_component_index_from_atom(item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()

@arg_digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    from molsysmt.element.entity import get_entity_index as _get
    return _get(item, element='atom', selection=indices,
            redefine_indices=True, skip_digestion=True)


@arg_digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    atom=list(item.atoms())
    output = [atom[ii].residue.chain.index for ii in tmp_indices]
    del(atom)

    return output


@arg_digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_name_from_atom(item, indices='all', skip_digestion=False):

    return None


@arg_digest(form=form)
def get_chain_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False):

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


@arg_digest(form=form)
def get_bond_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_bond_type_from_bond(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bond_order_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_bond_order_from_bond(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_n_groups_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        output = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_components_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        output = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_entities_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_chains_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        bond_indices = get_bond_index_from_atom(item, indices, skip_digestion=True)
        output = np.unique(np.concatenate(bond_indices)).shape[0]
        del bond_indices

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        bond_indices = get_inner_bond_index_from_atom(item, indices, skip_digestion=True)
        output = np.unique(np.concatenate(bond_indices)).shape[0]
        del bond_indices

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@arg_digest(form=form)
def get_n_ions_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@arg_digest(form=form)
def get_n_waters_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@arg_digest(form=form)
def get_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'olicosaccharide').sum()

    return output


@arg_digest(form=form)
def get_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@arg_digest(form=form)
def get_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@arg_digest(form=form)
def get_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@arg_digest(form=form)
def get_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@arg_digest(form=form)
def get_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


## From group


@arg_digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False):

    target_index = get_group_index_from_atom(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_group_index_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_groups_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_indices = get_n_groups_from_system(item, skip_digestion=True)
        indices = range(n_indices)

    group=list(item.residues())
    output = [str(group[ii].id) for ii in indices]
    del(group)

    return output

@arg_digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_indices = get_n_groups_from_system(item, skip_digestion=True)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].name for ii in indices]
    del(group)

    return output

@arg_digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    from molsysmt.element.group import get_group_type_from_group_name

    if is_all(indices):
        n_indices = get_n_groups_from_system(item, skip_digestion=True)
        indices = range(n_indices)

    group = list(item.residues())
    output = [get_group_type_from_group_name(group[ii].name, skip_digestion=True) for ii in indices]
    del(group)

    return output


@arg_digest(form=form)
def get_component_index_from_group(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_component_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_index_from_group(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_index_from_group(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_index_from_group(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False):

    return None


@arg_digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bond_index_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_type_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_order_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bond_index_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()



@arg_digest(form=form)
def get_n_atoms_from_group(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_group(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_groups_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_n_components_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        output = get_component_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_molecules_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_entities_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_chains_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_bonds_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_inner_bonds_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_amino_acids_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@arg_digest(form=form)
def get_n_ions_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@arg_digest(form=form)
def get_n_waters_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@arg_digest(form=form)
def get_n_lipids_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'polysaccharide').sum()

    return output


@arg_digest(form=form)
def get_n_saccharides_from_group(item, indices='all', skip_digestion=False):

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@arg_digest(form=form)
def get_n_peptides_from_group(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@arg_digest(form=form)
def get_n_proteins_from_group(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@arg_digest(form=form)
def get_n_dnas_from_group(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@arg_digest(form=form)
def get_n_rnas_from_group(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


## From component


@arg_digest(form=form)
def get_atom_index_from_component(item, indices='all', skip_digestion=False):

    target_index = get_component_index_from_atom(item)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_group_index_from_component(item, indices='all', skip_digestion=False):

    target_index = get_component_index_from_group(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_component_index_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_components_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output

@arg_digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False):

    output = get_component_index_from_component(item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    output = get_component_index_from_component(item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    from molsysmt.element.component import get_component_type as _get

    return _get(item, element='component', selection=indices, redefine_indices=True, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_index_from_component(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_molecule_id_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_name_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_type_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_index_from_component(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_entity_id_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_name_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_type_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_index_from_component(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_chain_id_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_name_from_component(item, indices='all', skip_digestion=False):

    return None


@arg_digest(form=form)
def get_chain_type_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bond_index_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_type_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_order_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bond_index_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_atoms_from_component(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_groups_from_component(item, indices='all', skip_digestion=False):

    output = get_group_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_components_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_n_molecules_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_chains_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_component(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_entities_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_bonds_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_amino_acids_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@arg_digest(form=form)
def get_n_ions_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@arg_digest(form=form)
def get_n_waters_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@arg_digest(form=form)
def get_n_lipids_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'polysaccharide').sum()

    return output


@arg_digest(form=form)
def get_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@arg_digest(form=form)
def get_n_peptides_from_component(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@arg_digest(form=form)
def get_n_proteins_from_component(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@arg_digest(form=form)
def get_n_dnas_from_component(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@arg_digest(form=form)
def get_n_rnas_from_component(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


## From molecule


@arg_digest(form=form)
def get_atom_index_from_molecule(item, indices='all', skip_digestion=False):

    target_index = get_molecule_index_from_atom(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_group_index_from_molecule(item, indices='all', skip_digestion=False):

    target_index = get_molecule_index_from_group(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_component_index_from_molecule(item, indices='all', skip_digestion=False):

    target_index = get_molecule_index_from_component(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_molecule_index_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_molecules_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False):

    from molsysmt.element.molecule import get_molecule_id as _get

    return _get(item, element='molecule', selection=indices, redefine_indices=True, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    from molsysmt.element.molecule import get_molecule_name as _get

    return _get(item, element='molecule', selection=indices, redefine_indices=True, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    from molsysmt.element.molecule import get_molecule_type as _get

    return _get(item, element='molecule', selection=indices, redefine_indices=True, skip_digestion=True)


@arg_digest(form=form)
def get_entity_index_from_molecule(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_entity_id_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_name_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_type_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_index_from_molecule(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_chain_id_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_name_from_molecule(item, indices='all', skip_digestion=False):

    return None


@arg_digest(form=form)
def get_chain_type_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_type_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_order_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    output = get_group_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_components_from_molecule(item, indices='all', skip_digestion=False):

    output = get_component_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_molecules_from_system(item)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_molecule(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@arg_digest(form=form)
def get_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@arg_digest(form=form)
def get_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@arg_digest(form=form)
def get_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'polysaccharide').sum()

    return output


@arg_digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@arg_digest(form=form)
def get_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'peptide').sum()

    return output


@arg_digest(form=form)
def get_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'protein').sum()

    return output


@arg_digest(form=form)
def get_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'dna').sum()

    return output


@arg_digest(form=form)
def get_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    group_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'dna').sum()

    return output


## From entity


@arg_digest(form=form)
def get_atom_index_from_entity(item, indices='all', skip_digestion=False):

    target_index = get_entity_index_from_atom(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_group_index_from_entity(item, indices='all', skip_digestion=False):

    target_index = get_entity_index_from_group(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_component_index_from_entity(item, indices='all', skip_digestion=False):

    target_index = get_entity_index_from_component(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_molecule_index_from_entity(item, indices='all', skip_digestion=False):

    target_index = get_entity_index_from_molecule(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_entity_index_from_entity(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_entities_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):

    from molsysmt.element.entity import get_entity_id as _get

    return _get(item, element='entity', selection=indices, redefine_indices=True, skip_digestion=True)


@arg_digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    from molsysmt.element.entity import get_entity_name as _get

    return _get(item, element='entity', selection=indices, redefine_indices=True, skip_digestion=True)


@arg_digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    from molsysmt.element.entity import get_entity_type as _get

    return _get(item, element='entity', selection=indices, redefine_types=True, skip_digestion=True)


@arg_digest(form=form)
def get_chain_index_from_entity(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_chain_id_from_entity(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_name_from_entity(item, indices='all', skip_digestion=False):

    return None


@arg_digest(form=form)
def get_chain_type_from_entity(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bond_index_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_type_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_order_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bond_index_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):

    output = get_group_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_components_from_entity(item, indices='all', skip_digestion=False):

    output = get_component_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    output = get_molecule_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_entities_from_entity(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_n_chains_from_entity(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@arg_digest(form=form)
def get_n_ions_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@arg_digest(form=form)
def get_n_waters_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@arg_digest(form=form)
def get_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'polysaccharide').sum()

    return output


@arg_digest(form=form)
def get_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@arg_digest(form=form)
def get_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(np.concatenate([np.array(ii) for ii in molecule_indices]))
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = int((np.array(molecule_types) == 'peptide').sum())

    return output


@arg_digest(form=form)
def get_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(np.concatenate([np.array(ii) for ii in molecule_indices]))
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = int((np.array(molecule_types) == 'protein').sum())

    return output


@arg_digest(form=form)
def get_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(np.concatenate([np.array(ii) for ii in molecule_indices]))
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = int((np.array(molecule_types) == 'dna').sum())

    return output


@arg_digest(form=form)
def get_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(np.concatenate([np.array(ii) for ii in molecule_indices]))
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = int((np.array(molecule_types) == 'rna').sum())

    return output


## From chain


@arg_digest(form=form)
def get_atom_index_from_chain(item, indices='all', skip_digestion=False):

    target_index = get_chain_index_from_atom(item)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_group_index_from_chain(item, indices='all', skip_digestion=False):

    target_index = get_chain_index_from_group(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_component_index_from_chain(item, indices='all', skip_digestion=False):

    target_index = get_chain_index_from_component(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_molecule_index_from_chain(item, indices='all', skip_digestion=False):

    target_index = get_chain_index_from_molecule(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_entity_index_from_chain(item, indices='all', skip_digestion=False):

    target_index = get_chain_index_from_entity(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_chain_index_from_chain(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_chains_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output

@arg_digest(form=form)
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):

    chains=list(item.chains())
    if is_all(indices):
        output = [chain.id for chain in chains]
    else:
        output = [chains[ii].id for ii in indices]
    del(chains)

    return output

@arg_digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    return None

@arg_digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    from molsysmt.element.chain import get_chain_type

    output = get_chain_type(item, element='chain', selection=indices, redefine_types=True)

    return output


@arg_digest(form=form)
def get_bond_index_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_type_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_order_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bond_index_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_groups_from_chain(item, indices='all', skip_digestion=False):

    output = get_group_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_components_from_chain(item, indices='all', skip_digestion=False):

    output = get_component_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    output = get_molecule_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_entities_from_chain(item, indices='all', skip_digestion=False):

    output = get_entity_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_chains_from_chain(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@arg_digest(form=form)
def get_n_ions_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@arg_digest(form=form)
def get_n_waters_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@arg_digest(form=form)
def get_n_lipids_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'polysaccharide').sum()

    return output


@arg_digest(form=form)
def get_n_saccharides_from_chain(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    group_indices=np.concatenate([np.array(ii) for ii in group_indices])
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@arg_digest(form=form)
def get_n_peptides_from_chain(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(np.concatenate([np.array(ii) for ii in molecule_indices]))
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = int((np.array(molecule_types) == 'peptide').sum())

    return output


@arg_digest(form=form)
def get_n_proteins_from_chain(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(np.concatenate([np.array(ii) for ii in molecule_indices]))
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = int((np.array(molecule_types) == 'protein').sum())

    return output


@arg_digest(form=form)
def get_n_dnas_from_chain(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(np.concatenate([np.array(ii) for ii in molecule_indices]))
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = int((np.array(molecule_types) == 'dna').sum())

    return output


@arg_digest(form=form)
def get_n_rnas_from_chain(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(np.concatenate([np.array(ii) for ii in molecule_indices]))
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = int((np.array(molecule_types) == 'rna').sum())

    return output


## From bond


@arg_digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_bonds_from_system(item, skip_digestion=True)
        output = np.arange(n_aux, dtype=int).tolist()
    else:
        output = indices.tolist()

    return output
## From bond

@arg_digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, skip_digestion=True)
    bond = list(item.bonds())
    output=[bond[ii].order for ii in tmp_indices]
    del(bond)

    return output

@arg_digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, skip_digestion=True)
    bond = list(item.bonds())
    output=[bond[ii].type for ii in tmp_indices]
    del(bond)

    return output

@arg_digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, skip_digestion=True)
    bond = list(item.bonds())
    atom_set = set()
    for ii in tmp_indices:
        atom_set.add(bond[ii].atom1.index)
        atom_set.add(bond[ii].atom2.index)
    del bond

    return sorted(atom_set)


@arg_digest(form=form)
def get_bonded_atom_pairs_from_bond(item, indices='all', skip_digestion=False):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, skip_digestion=True)
    bond = list(item.bonds())
    output = [sorted([bond[ii].atom1.index, bond[ii].atom2.index]) for ii in tmp_indices]
    del bond

    return output


@arg_digest(form=form)
def get_n_bonds_from_bond(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_aux = get_n_bonds_from_system(item, skip_digestion=True)
        output = n_aux
    else:
        output = len(indices)

    return output


## From system


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    return item.getNumAtoms()

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    return item.getNumResidues()

@arg_digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    component_index_from_atom = get_component_index_from_atom(item, indices='all', skip_digestion=True)

    if component_index_from_atom[0] is None:
        n_components = 0
    else:
        output = np.unique(component_index_from_atom)
        n_components = output.shape[0]

    return n_components


@arg_digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    molecule_index_from_atom = get_molecule_index_from_atom(item, skip_digestion=True)
    if molecule_index_from_atom[0] is None:
        n_molecules = 0
    else:
        output = np.unique(molecule_index_from_atom)
        n_molecules = output.shape[0]
    return n_molecules


@arg_digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    entity_index_from_atom = get_entity_index_from_atom(item, skip_digestion=True)
    if entity_index_from_atom[0] is None:
        n_entities = 0
    else:
        output = np.unique(entity_index_from_atom)
        n_entities = output.shape[0]
    return n_entities


@arg_digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    return item.getNumChains()


@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    return item.getNumBonds()


@arg_digest(form=form)
def get_n_amino_acids_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@arg_digest(form=form)
def get_n_ions_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@arg_digest(form=form)
def get_n_waters_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@arg_digest(form=form)
def get_n_lipids_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'polysaccharide').sum()

    return output


@arg_digest(form=form)
def get_n_saccharides_from_system(item, skip_digestion=False):

    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@arg_digest(form=form)
def get_n_peptides_from_system(item, skip_digestion=False):

    molecule_types = get_molecule_type_from_molecule(item, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@arg_digest(form=form)
def get_n_proteins_from_system(item, skip_digestion=False):

    molecule_types = get_molecule_type_from_molecule(item, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@arg_digest(form=form)
def get_n_dnas_from_system(item, skip_digestion=False):

    molecule_types = get_molecule_type_from_molecule(item, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@arg_digest(form=form)
def get_n_rnas_from_system(item, skip_digestion=False):

    molecule_types = get_molecule_type_from_molecule(item, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


@arg_digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):

    n_bonds = get_n_bonds_from_system(item, skip_digestion=True)
    output = list(range(n_bonds))

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_system(item, skip_digestion=False):

    return get_bonded_atoms_from_bond(item, skip_digestion=True)


@arg_digest(form=form)
def get_bonded_atom_pairs_from_system(item, skip_digestion=False):

    output = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
   
    return output


@arg_digest(form=form)
def get_inner_bond_index_from_system(item, skip_digestion=False):

    n_bonds = get_n_bonds_from_system(item, skip_digestion=True)
    output = list(range(n_bonds))

    return output


@arg_digest(form=form)
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


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_system(item, skip_digestion=False):

    output = get_bonded_atom_pairs_from_bond(item)
   
    return output


## get_total_n_* functions
## Return the total count within the scope defined by the queried indices.
## Each function delegates to the per-element getter and sums or counts
## appropriately depending on how the element hierarchy relates to Y.

# --- From atom ---

@arg_digest(form=form)
def get_total_n_atoms_from_atom(item, indices='all', skip_digestion=False):
    return get_n_atoms_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_groups_from_atom(item, indices='all', skip_digestion=False):
    return get_n_groups_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_components_from_atom(item, indices='all', skip_digestion=False):
    return get_n_components_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_molecules_from_atom(item, indices='all', skip_digestion=False):
    return get_n_molecules_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_entities_from_atom(item, indices='all', skip_digestion=False):
    return get_n_entities_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_chains_from_atom(item, indices='all', skip_digestion=False):
    return get_n_chains_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_bonds_from_atom(item, indices='all', skip_digestion=False):
    per_atom = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    unique_bonds = set()
    for bond_list in per_atom:
        unique_bonds.update(bond_list)
    return len(unique_bonds)

@arg_digest(form=form)
def get_total_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):
    per_atom = get_inner_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    unique_bonds = set()
    for bond_list in per_atom:
        unique_bonds.update(bond_list)
    return len(unique_bonds)

@arg_digest(form=form)
def get_total_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):
    return get_n_amino_acids_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):
    return get_n_nucleotides_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_ions_from_atom(item, indices='all', skip_digestion=False):
    return get_n_ions_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_waters_from_atom(item, indices='all', skip_digestion=False):
    return get_n_waters_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):
    return get_n_small_molecules_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_lipids_from_atom(item, indices='all', skip_digestion=False):
    return get_n_lipids_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_saccharides_from_atom(item, indices='all', skip_digestion=False):
    return get_n_saccharides_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_peptides_from_atom(item, indices='all', skip_digestion=False):
    return get_n_peptides_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_proteins_from_atom(item, indices='all', skip_digestion=False):
    return get_n_proteins_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False):
    return get_n_polysaccharides_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_dnas_from_atom(item, indices='all', skip_digestion=False):
    return get_n_dnas_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_rnas_from_atom(item, indices='all', skip_digestion=False):
    return get_n_rnas_from_atom(item, indices=indices, skip_digestion=True)


# --- From group ---
# Note: get_n_components_from_group and get_n_chains_from_group already return
# scalar unique counts in openmm.Topology, so total_ delegates directly.

@arg_digest(form=form)
def get_total_n_atoms_from_group(item, indices='all', skip_digestion=False):
    return int(sum(get_n_atoms_from_group(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_groups_from_group(item, indices='all', skip_digestion=False):
    return get_n_groups_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_components_from_group(item, indices='all', skip_digestion=False):
    return get_n_components_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_molecules_from_group(item, indices='all', skip_digestion=False):
    return get_n_molecules_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_entities_from_group(item, indices='all', skip_digestion=False):
    return get_n_entities_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_chains_from_group(item, indices='all', skip_digestion=False):
    return get_n_chains_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_amino_acids_from_group(item, indices='all', skip_digestion=False):
    return get_n_amino_acids_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_nucleotides_from_group(item, indices='all', skip_digestion=False):
    return get_n_nucleotides_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_ions_from_group(item, indices='all', skip_digestion=False):
    return get_n_ions_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_waters_from_group(item, indices='all', skip_digestion=False):
    return get_n_waters_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_small_molecules_from_group(item, indices='all', skip_digestion=False):
    return get_n_small_molecules_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_lipids_from_group(item, indices='all', skip_digestion=False):
    return get_n_lipids_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_saccharides_from_group(item, indices='all', skip_digestion=False):
    return get_n_saccharides_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_peptides_from_group(item, indices='all', skip_digestion=False):
    return get_n_peptides_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_proteins_from_group(item, indices='all', skip_digestion=False):
    return get_n_proteins_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_polysaccharides_from_group(item, indices='all', skip_digestion=False):
    return get_n_polysaccharides_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_dnas_from_group(item, indices='all', skip_digestion=False):
    return get_n_dnas_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_rnas_from_group(item, indices='all', skip_digestion=False):
    return get_n_rnas_from_group(item, indices=indices, skip_digestion=True)


# --- From molecule ---

@arg_digest(form=form)
def get_total_n_atoms_from_molecule(item, indices='all', skip_digestion=False):
    return int(sum(get_n_atoms_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_groups_from_molecule(item, indices='all', skip_digestion=False):
    return int(sum(get_n_groups_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_components_from_molecule(item, indices='all', skip_digestion=False):
    return int(sum(get_n_components_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_molecules_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_molecules_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_entities_from_molecule(item, indices='all', skip_digestion=False):
    # get_n_entities_from_molecule returns a scalar in openmm.Topology
    return int(get_n_entities_from_molecule(item, indices=indices, skip_digestion=True))

@arg_digest(form=form)
def get_total_n_chains_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_chains_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_amino_acids_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_nucleotides_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_ions_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_ions_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_waters_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_waters_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_lipids_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_lipids_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_saccharides_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_peptides_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_peptides_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_proteins_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_proteins_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_polysaccharides_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_dnas_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_dnas_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_rnas_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_rnas_from_molecule(item, indices=indices, skip_digestion=True)


# --- From entity ---

@arg_digest(form=form)
def get_total_n_atoms_from_entity(item, indices='all', skip_digestion=False):
    return int(sum(get_n_atoms_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_groups_from_entity(item, indices='all', skip_digestion=False):
    return int(sum(get_n_groups_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_components_from_entity(item, indices='all', skip_digestion=False):
    return int(sum(get_n_components_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_molecules_from_entity(item, indices='all', skip_digestion=False):
    return int(sum(get_n_molecules_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_entities_from_entity(item, indices='all', skip_digestion=False):
    return get_n_entities_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_chains_from_entity(item, indices='all', skip_digestion=False):
    return get_n_chains_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):
    return get_n_amino_acids_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):
    return get_n_nucleotides_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_ions_from_entity(item, indices='all', skip_digestion=False):
    return get_n_ions_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_waters_from_entity(item, indices='all', skip_digestion=False):
    return get_n_waters_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_lipids_from_entity(item, indices='all', skip_digestion=False):
    return get_n_lipids_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_saccharides_from_entity(item, indices='all', skip_digestion=False):
    return get_n_saccharides_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_peptides_from_entity(item, indices='all', skip_digestion=False):
    return get_n_peptides_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_proteins_from_entity(item, indices='all', skip_digestion=False):
    return get_n_proteins_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_polysaccharides_from_entity(item, indices='all', skip_digestion=False):
    return get_n_polysaccharides_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_dnas_from_entity(item, indices='all', skip_digestion=False):
    return get_n_dnas_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_rnas_from_entity(item, indices='all', skip_digestion=False):
    return get_n_rnas_from_entity(item, indices=indices, skip_digestion=True)


# --- From component ---

@arg_digest(form=form)
def get_total_n_atoms_from_component(item, indices='all', skip_digestion=False):
    return int(sum(get_n_atoms_from_component(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_groups_from_component(item, indices='all', skip_digestion=False):
    return int(sum(get_n_groups_from_component(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_components_from_component(item, indices='all', skip_digestion=False):
    return get_n_components_from_component(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_molecules_from_component(item, indices='all', skip_digestion=False):
    # get_n_molecules_from_component returns a scalar in openmm.Topology
    return int(get_n_molecules_from_component(item, indices=indices, skip_digestion=True))

@arg_digest(form=form)
def get_total_n_entities_from_component(item, indices='all', skip_digestion=False):
    # get_n_entities_from_component returns a scalar in openmm.Topology
    return int(get_n_entities_from_component(item, indices=indices, skip_digestion=True))

@arg_digest(form=form)
def get_total_n_chains_from_component(item, indices='all', skip_digestion=False):
    return get_n_chains_from_component(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_amino_acids_from_component(item, indices='all', skip_digestion=False):
    return get_n_amino_acids_from_component(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_nucleotides_from_component(item, indices='all', skip_digestion=False):
    return get_n_nucleotides_from_component(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_ions_from_component(item, indices='all', skip_digestion=False):
    return get_n_ions_from_component(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_waters_from_component(item, indices='all', skip_digestion=False):
    return get_n_waters_from_component(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_lipids_from_component(item, indices='all', skip_digestion=False):
    return get_n_lipids_from_component(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_saccharides_from_component(item, indices='all', skip_digestion=False):
    return get_n_saccharides_from_component(item, indices=indices, skip_digestion=True)


# --- From chain ---

@arg_digest(form=form)
def get_total_n_atoms_from_chain(item, indices='all', skip_digestion=False):
    return int(sum(get_n_atoms_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_groups_from_chain(item, indices='all', skip_digestion=False):
    return int(sum(get_n_groups_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_components_from_chain(item, indices='all', skip_digestion=False):
    return int(sum(get_n_components_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_molecules_from_chain(item, indices='all', skip_digestion=False):
    return int(sum(get_n_molecules_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_entities_from_chain(item, indices='all', skip_digestion=False):
    return int(sum(get_n_entities_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_chains_from_chain(item, indices='all', skip_digestion=False):
    return get_n_chains_from_chain(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):
    return get_n_amino_acids_from_chain(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):
    return get_n_nucleotides_from_chain(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_ions_from_chain(item, indices='all', skip_digestion=False):
    return get_n_ions_from_chain(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_waters_from_chain(item, indices='all', skip_digestion=False):
    return get_n_waters_from_chain(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_lipids_from_chain(item, indices='all', skip_digestion=False):
    return get_n_lipids_from_chain(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_saccharides_from_chain(item, indices='all', skip_digestion=False):
    return get_n_saccharides_from_chain(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_polysaccharides_from_chain(item, indices='all', skip_digestion=False):
    return get_n_polysaccharides_from_chain(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_dnas_from_chain(item, indices='all', skip_digestion=False):
    return get_n_dnas_from_chain(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_rnas_from_chain(item, indices='all', skip_digestion=False):
    return get_n_rnas_from_chain(item, indices=indices, skip_digestion=True)


# List of functions to be imported


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

