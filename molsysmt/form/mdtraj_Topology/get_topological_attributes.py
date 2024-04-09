#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

form='mdtraj.Topology'


## From atom

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

    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    output=[item.atom(ii).serial for ii in tmp_indices]
    output=np.array(output, dtype=int)
    return output


@digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    output=[item.atom(ii).name for ii in tmp_indices]
    output=np.array(output, dtype=object)
    return output


@digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    output=[item.atom(ii).element.symbol for ii in tmp_indices]
    output=np.array(output, dtype=object)
    return output


@digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    output=[item.atom(ii).residue.index for ii in tmp_indices]
    output=np.array(output, dtype=int)
    return output


@digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_group_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_group_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_group_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    from molsysmt.element.component import get_component_index_from_atom

    output = get_component_index_from_atom(item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_component_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_component_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    from molsysmt.element.molecule import get_molecule_index_from_atom

    output = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_molecule_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    from molsysmt.element.entity import get_entity_index_from_atom

    output = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    output=[item.atom(ii).residue.chain.index for ii in tmp_indices]
    output=np.array(output, dtype=int)
    return output


@digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_name_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_type_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False):

    output = None

    G = Graph()
    edges = get_bonded_atoms_pairs_from_bond(item)
    n_bonds = len(edges)
    edge_indices = np.array([{'index': ii} for ii in range(n_bonds)]).reshape([n_bonds, 1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if is_all(indices):

        aux_get = getattr(module, 'get_atom_index_from_atom')
        indices = aux_get(item)

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

    aux_indices = get_bond_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_bond_type_from_bond(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_bond_order_from_atom(item, indices='all', skip_digestion=False):

    aux_indices = get_bond_index_from_atom(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_bond_order_from_bond(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    output = None

    G = Graph()
    edges = get_bonded_atoms_pairs_from_bond(item)
    
    G.add_edges_from(edges)

    if is_all(indices):

        indices = get_atom_index_from_atom(item)

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

        output = get_bonded_atom_pairs_from_bond(item)
   
    else:

        pairs = get_bonded_atom_pairs_from_bond(item)
        pairs = np.array(pairs)
        mask = np.isin(pairs[:,0], indices) | np.isin(pairs[:,1], indices)
        output = pairs[mask,:].tolist()

        del pairs, mask

    return output


@digest(form=form)
def get_inner_bond_index_from_atom(item, indices='all', skip_digestion=False):

    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item)
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
    edges = get_bonded_atom_pairs_from_bond(item)
    
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

        output = get_bonded_atom_pairs_from_bond(item)
   
    else:

        pairs = get_bonded_atom_pairs_from_bond(item)
        pairs = np.array(pairs)
        mask = np.isin(pairs[:,0], indices) * np.isin(pairs[:,1], indices)
        output = pairs[mask,:].tolist()

        del pairs, mask

    return output


@digest(form=form)
def get_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_atoms_from_system(item)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_groups_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_groups_from_system(item)
    else:
        output = get_group_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_components_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_components_from_system(item)
    else:
        output = get_component_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_molecules_from_system(item)
    else:
        output = get_molecule_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_chains_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item)
    else:
        output = get_chain_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_entities_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = get_entity_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):

        output = get_n_bonds_from_system(item)

    else:

        bond_indices = get_bond_index_from_atom(item, indices)
        output = np.unique(np.concatenate(bond_indices)).shape[0]
        del bond_indices

    return output


@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):

        output = get_n_bonds_from_system(item)

    else:

        bond_indices = get_inner_bond_index_from_atom(item, indices)
        output = np.unique(np.concatenate(bond_indices)).shape[0]
        del bond_indices

    return output


@digest(form=form)
def get_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@digest(form=form)
def get_n_ions_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices)
    output = (np.array(group_types) == 'ion').sum()

    return output


@digest(form=form)
def get_n_waters_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices)
    output = (np.array(group_types) == 'water').sum()

    return output


@digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@digest(form=form)
def get_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@digest(form=form)
def get_n_oligosaccharides_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices)
    output = (np.array(group_types) == 'olicosaccharide').sum()

    return output


@digest(form=form)
def get_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    group_indices = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@digest(form=form)
def get_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@digest(form=form)
def get_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@digest(form=form)
def get_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@digest(form=form)
def get_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


## From group


@digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False):

    target_index = get_group_index_from_atom(item)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_atom_id_from_group(item, indices='all', skip_digestion=False):

    target_indices = get_atom_index_from_group(item, indices=indices)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices)
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

    target_indices = get_atom_index_from_group(item, indices=indices)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices)
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

    target_indices = get_atom_index_from_group(item, indices=indices)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices)
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
        n_indices = get_n_groups_from_system(item, skip_digestion=True)
        indices = np.arange(n_indices)

    output = [item.residue(ii).resSeq for ii in indices]
    output = np.array(output, dtype=int)
    return output

@digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        n_indices = get_n_groups_from_system(item, skip_digestion=True)
        indices = np.arange(n_indices)

    output = [item.residue(ii).name for ii in indices]
    output = np.array(output, dtype=object)
    return output

@digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    from molsysmt.element.group import get_group_type_from_group_name as aux_get

    output = get_group_name_from_group(item, indices=indices, skip_digestion=True)
    output = [aux_get(ii) for ii in output]
    output = np.array(output, dtype=object)

    return output


@digest(form=form)
def get_component_index_from_group(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_group(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_component_index_from_atom(item, indices=first_atom_index_from_target)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_group(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_group(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_component_index_from_group(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_index_from_group(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_group(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_group(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_group(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_group(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_index_from_group(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_group(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_group(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_group(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_molecule_index_from_group(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_index_from_group(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_group(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_group(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_group(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_group(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_n_atoms_from_group(item, indices='all', skip_digestion=False):

    output = get_atom_index_from_group(item, indices)
    output = [len(ii) for ii in output]

    return output


@digest(form=form)
def get_n_groups_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_groups_from_system(item)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_components_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_components_from_system(item)
    else:
        output = get_component_index_from_group(item, indices=indices)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_molecules_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_molecules_from_system(item)
    else:
        output = get_molecule_index_from_group(item, indices=indices)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_chains_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item)
    else:
        output = get_chain_index_from_group(item, indices=indices)
        output = np.unique(output).shape[0]

    return output


@digest(form=form)
def get_n_entities_from_group(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = get_entity_index_from_group(item, indices=indices)
        output = np.unique(output).shape[0]

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

    target_indices = get_atom_index_from_component(item, indices=indices)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices)
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

    target_indices = get_atom_index_from_component(item, indices=indices)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices)
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

    target_indices = get_atom_index_from_component(item, indices=indices)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices)
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

    target_index = get_component_index_from_group(item)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_group_id_from_component(item, indices='all', skip_digestion=False):

    target_indices = get_group_index_from_component(item, indices=indices)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices)
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

    target_indices = get_group_index_from_component(item, indices=indices)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices)
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

    target_indices = get_group_index_from_component(item, indices=indices)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices)
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

    from molsysmt.element.component import get_component_id_from_component

    output = get_component_id_from_component(item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    from molsysmt.element.component import get_component_name_from_component

    output = get_component_name_from_component(item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    from molsysmt.element.component import get_component_type_from_component

    output = get_component_type_from_component(item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_chain_index_from_component(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_component(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_chain_id_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_component(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_name_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_component(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_type_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_component(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_index_from_component(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_component(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target)

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

    atom_index_from_target = get_atom_index_from_component(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_entity_id_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_component(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_name_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_component(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_entity_type_from_component(item, indices='all', skip_digestion=False):

    aux_indices = get_entity_index_from_component(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_n_atoms_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_groups_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_components_from_component(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_components_from_system(item)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_molecules_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_chains_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_entities_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_bonds_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_aminoacids_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_ions_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_waters_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_peptides_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_proteins_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_dnas_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_rnas_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_lipids_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_oligosaccharides_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


## From molecule


@digest(form=form)
def get_atom_index_from_molecule(item, indices='all', skip_digestion=False):

    target_index = get_molecule_index_from_atom(item)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_atom_id_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_atom_name_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_atom_type_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_group_index_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_group_id_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_group_name_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_group_type_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_component_index_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_component_id_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_component_name_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_component_type_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_chain_index_from_molecule(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_molecule(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_chain_id_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_molecule(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_name_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_molecule(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_type_from_molecule(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_molecule(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


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

    from molsysmt.element.molecule import get_molecule_id_from_molecule

    output = get_molecule_id_from_molecule(item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    from molsysmt.element.molecule import get_molecule_name_from_molecule

    output = get_molecule_name_from_molecule(item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    from molsysmt.element.molecule import get_molecule_type_from_molecule

    output = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_entity_index_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_entity_id_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_entity_name_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_entity_type_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_components_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_molecules_from_system(item)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_aminoacids_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_oligosaccharides_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()



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

    raise NotImplementedMethodError()


@digest(form=form)
def get_atom_name_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_atom_type_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_group_index_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_group_id_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_group_name_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_group_type_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_component_index_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_component_id_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_component_name_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_component_type_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


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

    raise NotImplementedMethodError()

@digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_molecule_index_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_molecule_id_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_molecule_name_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_molecule_type_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_entity_index_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_entity_id_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_entity_name_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_entity_type_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_groups_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_components_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_chains_from_chain(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_chains_from_system(item)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_entities_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_aminoacids_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_ions_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_waters_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_peptides_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_proteins_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_dnas_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_rnas_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_lipids_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_oligosaccharides_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_saccharides_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


## From entity


@digest(form=form)
def get_atom_index_from_entity(item, indices='all', skip_digestion=False):

    target_index = get_entity_index_from_atom(item)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@digest(form=form)
def get_atom_id_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_atom_name_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_atom_type_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_group_index_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_group_id_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_group_name_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_group_type_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_component_index_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_component_id_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_component_name_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_component_type_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_chain_index_from_entity(item, indices='all', skip_digestion=False):

    atom_index_from_target = get_atom_index_from_entity(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target)

    del atom_index_from_target, first_atom_index_from_target

    return output


@digest(form=form)
def get_chain_id_from_entity(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_entity(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_name_from_entity(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_entity(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_chain_type_from_entity(item, indices='all', skip_digestion=False):

    aux_indices = get_chain_index_from_entity(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@digest(form=form)
def get_molecule_index_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_molecule_id_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_molecule_name_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_molecule_type_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


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

    from molsysmt.element.entity import get_entity_id_from_entity

    output = get_entity_id_from_entity(item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    from molsysmt.element.entity import get_entity_name_from_entity

    output = get_entity_name_from_entity(item, indices=indices, skip_digestion=True)

    return output

@digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    from molsysmt.element.entity import get_entity_type_from_entity

    output = get_entity_type_from_entity(item, indices=indices, skip_digestion=True)

    return output


@digest(form=form)
def get_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_components_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_chains_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_entities_from_entity(item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = len(indices)

    return output


@digest(form=form)
def get_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_aminoacids_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_ions_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_waters_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_oligosaccharides_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


## From system

@digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    return item.n_atoms

@digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    return item.n_residues

@digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    from molsysmt.element.component import get_n_components_from_system

    output = get_n_components_from_system(item, skip_digestion=True)

    return output

@digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    return item.n_chains

@digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    from molsysmt.element.molecule import get_n_molecules_from_system

    output = get_n_molecules_from_system(item, skip_digestion=True)

    return output

@digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    from molsysmt.element.entity import get_n_entities_from_system

    output = get_n_entities_from_system(item, skip_digestion=True)

    return output

@digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    return item.n_bonds


@digest(form=form)
def get_n_aminoacids_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_nucleotides_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_ions_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_waters_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_small_molecules_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_peptides_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_proteins_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_dnas_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_rnas_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_lipids_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_oligosaccharides_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_n_saccharides_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bonded_atoms_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


@digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()


## From bond


@digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    tmp_indices = get_bond_index_from_bond(item, indices=indices)
    bond = list(item.bonds)
    output=[[bond[ii].atom1.index, bond[ii].atom2.index] for ii in tmp_indices]
    output=np.array(output)
    del(bond)
    return output


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

