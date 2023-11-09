from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
from networkx import Graph

form='molsysmt.TopologyNEW'

## From atom

@digest(form=form)
def get_atom_index_from_atom(item, indices='all'):

    if is_all(indices):
        output = list(np.range(item.atoms.shape[0]))
    else:
        output = indices

    return output
    
@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    if is_all(indices):
        output = item.atoms['id'][:].to_numpy()
    else:
        output = item.atoms['id'][indices].to_numpy()

    return output

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    if is_all(indices):
        output = item.atoms['name'][:].astype('str')
    else:
        output = item.atoms['name'][indices].astype('str')

    return output

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    if is_all(indices):
        output = item.atoms['type'][:].astype('str')
    else:
        output = item.atoms['type'][indices].astype('str')

    return output

@digest(form=form)
def get_group_index_from_atom(item, indices='all'):

    if is_all(indices):
        output = item.atoms['group_index'][:].to_numpy()
    else:
        output = item.atoms['group_index'][indices].to_numpy()

    return output

@digest(form=form)
def get_group_id_from_atom(item, indices='all'):

    group_indices = get_group_index_from_atom(item, indices=indices)
    output = item.groups['group_id'][group_indices].to_numpy()
    del(group_indices)

    return output

@digest(form=form)
def get_group_name_from_atom(item, indices='all'):

    group_indices = get_group_index_from_atom(item, indices=indices)
    output = item.groups['group_name'][group_indices].to_numpy()
    del(group_indices)

    return output

@digest(form=form)
def get_group_type_from_atom(item, indices='all'):

    group_indices = get_group_index_from_atom(item, indices=indices)
    output = item.groups['group_name'][group_indices].to_numpy()
    del(group_indices)

    return output

@digest(form=form)
def get_component_index_from_atom(item, indices='all'):

    group_indices = get_group_index_from_atom(item, indices=indices)
    output = item.groups['component_index'][group_indices].to_numpy()
    del(group_indices)

    return output

@digest(form=form)
def get_component_id_from_atom(item, indices='all'):

    component_indices = get_component_index_from_atom(item, indices=indices)
    output = item.components['component_id'][component_indices].to_numpy()
    del(component_indices)

    return output

@digest(form=form)
def get_component_name_from_atom(item, indices='all'):

    component_indices = get_component_index_from_atom(item, indices=indices)
    output = item.components['component_name'][component_indices].to_numpy()
    del(component_indices)

    return output

@digest(form=form)
def get_component_type_from_atom(item, indices='all'):

    component_indices = get_component_index_from_atom(item, indices=indices)
    output = item.components['component_type'][component_indices].to_numpy()
    del(component_indices)

    return output

@digest(form=form)
def get_molecule_index_from_atom(item, indices='all'):

    component_indices = get_component_index_from_atom(item, indices=indices)
    output = item.components['molecule_index'][component_indices].to_numpy()
    del(component_indices)

    return output

@digest(form=form)
def get_molecule_id_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    output = item.molecules['molecule_id'][molecule_indices].to_numpy()
    del(molecule_indices)

    return output

@digest(form=form)
def get_molecule_name_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    output = item.molecules['molecule_name'][molecule_indices].to_numpy()
    del(molecule_indices)

    return output

@digest(form=form)
def get_molecule_type_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    output = item.molecules['molecule_type'][molecule_indices].to_numpy()
    del(molecule_indices)

    return output

@digest(form=form)
def get_entity_index_from_atom(item, indices='all'):

    molecule_indices = get_molecule_index_from_atom(item, indices=indices)
    output = item.molecules['entity_index'][molecule_indices].to_numpy()
    del(molecule_indices)

    return output

@digest(form=form)
def get_entity_id_from_atom(item, indices='all'):

    entity_indices = get_entity_index_from_atom(item, indices=indices)
    output = item.entity['entity_id'][entity_indices].to_numpy()
    del(entity_indices)

    return output

@digest(form=form)
def get_entity_name_from_atom(item, indices='all'):

    entity_indices = get_entity_index_from_atom(item, indices=indices)
    output = item.entity['entity_name'][entity_indices].to_numpy()
    del(entity_indices)

    return output

@digest(form=form)
def get_entity_type_from_atom(item, indices='all'):

    entity_indices = get_entity_index_from_atom(item, indices=indices)
    output = item.entity['entity_type'][entity_indices].to_numpy()
    del(entity_indices)

    return output

@digest(form=form)
def get_chain_index_from_atom(item, indices='all'):

    if is_all(indices):
        output = item.atoms['chain_index'][:].to_numpy()
    else:
        output = item.atoms['chain_index'][indices].to_numpy()

    return output

@digest(form=form)
def get_chain_id_from_atom(item, indices='all'):

    chain_indices = get_chain_index_from_atom(item, indices=indices)
    output = item.chains['chain_id'][chain_indices].to_numpy()
    del(group_indices)

    return output

@digest(form=form)
def get_chain_name_from_atom(item, indices='all'):

    chain_indices = get_chain_index_from_atom(item, indices=indices)
    output = item.chains['chain_name'][chain_indices].to_numpy()
    del(chain_indices)

    return output

@digest(form=form)
def get_chain_type_from_atom(item, indices='all'):

    chain_indices = get_chain_index_from_atom(item, indices=indices)
    output = item.chains['chain_name'][chain_indices].to_numpy()
    del(chain_indices)

    return output

@digest(form=form)
def get_n_atoms_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_atoms_from_system(item)
    else:
        return len(indices)

@digest(form=form)
def get_n_groups_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_groups_from_system(item)
    else:
        output = get_group_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]
        return output

@digest(form=form)
def get_n_components_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_components_from_system(item)
    else:
        output = get_component_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]
        return output

@digest(form=form)
def get_n_molecules_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_molecules_from_system(item)
    else:
        output = get_molecule_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]
        return output

@digest(form=form)
def get_n_entities_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_entities_from_system(item)
    else:
        output = get_entity_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]
        return output

@digest(form=form)
def get_n_chains_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_chains_from_system(item)
    else:
        output = get_chain_index_from_atom(item, indices=indices)
        output = np.unique(output).shape[0]
        return output

@digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all'):

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
            output.append(np.array([], dtype=int))

    output = np.array(output, dtype=object)

    for ii in range(output.shape[0]):
        output[ii] = np.sort(output[ii])

    del(G, edges)

    return output

@digest(form=form)
def get_bond_index_from_atom(item, indices='all'):

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
            output.append(np.array([], dtype=int))

    output = np.array(output, dtype=object)

    del(G, edges, edge_indices)

    return output

@digest(form=form)
def get_n_bonds_from_atom(item, indices='all'):

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

    output = None

    if is_all(indices):
        output = get_bond_index_from_bond(item)
    else:
        aux_list = list(indices)
        output = item.bonds.query('atom1_index==@aux_list and atom2_index==@aux_list').index.to_numpy(dtype=int, copy=True)

    return output

@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all'):

    if is_all(indices):

        output = get_bonded_atoms_from_bond(item, indices='all')

    else:

        bond_indices = get_inner_bond_index_from_atom (item, indices=indices)
        output = get_bonded_atoms_from_bond(item, indices=bond_indices)
        del(bond_indices)

    output = output[np.lexsort((output[:, 1], output[:, 0]))]

    return(output)

@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all'):

    bond_indices = get_inner_bond_index_from_atom(item, indices=indices)
    output = bond_indices.shape[0]
    del(bond_indices)
    return(output)

@digest(form=form)
def get_occupancy_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    output = item.atoms['occupancy'][tmp_indices].to_numpy()
    return output

@digest(form=form)
def get_alternate_location_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    output = item.atoms['alternate_location'][tmp_indices].to_numpy()
    return output

@digest(form=form)
def get_b_factor_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    output = item.atoms['b_factor'][tmp_indices].to_numpy()
    unit = puw.get_standard_units(dimensionality={'[L]':2})
    output = puw.quantity(output, unit, standardized=True)
    return output

@digest(form=form)
def get_formal_charge_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    output = item.atoms['formal_charge'][tmp_indices].to_numpy()
    unit = puw.get_standard_units(dimensionality={'[T]':1, '[A]':1})
    output = puw.quantity(output, unit, standardized=True)
    return output

@digest(form=form)
def get_partial_charge_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    output = item.atoms['partial_charge'][tmp_indices].to_numpy()
    unit = puw.get_standard_units(dimensionality={'[T]':1, '[A]':1})
    output = puw.quantity(output, unit, standardized=True)
    return output

@digest(form=form)
def get_n_aminoacids_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_aminoacids_from_system(item)
    else:
        group_indices = get_group_index_from_atom(item, indices=indices)
        group_indices = np.unique(group_indices)
        group_types = get_group_type_from_group(item, indices=group_indices)
        return (group_types=='amino acid').sum()

@digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_nucleotides_from_system (item)
    else:
        group_indices = get_group_index_from_atom(item, indices=indices)
        group_indices = np.unique(group_indices)
        group_types = get_group_type_from_group(item, indices=group_indices)
        return (group_types=='nucleotide').sum()

@digest(form=form)
def get_n_ions_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_ions_from_system (item)
    else:
        molecule_indices = get_molecule_index_from_atom(item, indices=indices)
        molecule_indices = np.unique(molecule_indices)
        molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
        return (molecule_types=='ion').sum()

@digest(form=form)
def get_n_waters_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_waters_from_system (item)
    else:
        molecule_indices = get_molecule_index_from_atom(item, indices=indices)
        molecule_indices = np.unique(molecule_indices)
        molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
        return (molecule_types=='water').sum()

@digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_small_molecules_from_system(item)
    else:
        molecule_indices = get_molecule_index_from_atom(item, indices=indices)
        molecule_indices = np.unique(molecule_indices)
        molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
        return (molecule_types=='small molecule').sum()

@digest(form=form)
def get_n_peptides_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_peptides_from_system (item)
    else:
        molecule_indices = get_molecule_index_from_atom (item, indices=indices)
        molecule_indices = np.unique(molecule_indices)
        molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
        return (molecule_types=='peptide').sum()

@digest(form=form)
def get_n_proteins_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_proteins_from_system (item)
    else:
        molecule_indices = get_molecule_index_from_atom (item, indices=indices)
        molecule_indices = np.unique(molecule_indices)
        molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
        return (molecule_types=='protein').sum()

@digest(form=form)
def get_n_dnas_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_dnas_from_system (item)
    else:
        molecule_indices = get_molecule_index_from_atom (item, indices=indices)
        molecule_indices = np.unique(molecule_indices)
        molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
        return (molecule_types=='dna').sum()

@digest(form=form)
def get_n_rnas_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_rnas_from_system (item)
    else:
        molecule_indices = get_molecule_index_from_atom (item, indices=indices)
        molecule_indices = np.unique(molecule_indices)
        molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
        return (molecule_types=='rna').sum()

@digest(form=form)
def get_n_lipids_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_lipids_from_system (item)
    else:
        molecule_indices = get_molecule_index_from_atom (item, indices=indices)
        molecule_indices = np.unique(molecule_indices)
        molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
        return (molecule_types=='lipid').sum()

@digest(form=form)
def get_n_oligosaccharides_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_oligosaccharides_from_system (item)
    else:
        molecule_indices = get_molecule_index_from_atom (item, indices=indices)
        molecule_indices = np.unique(molecule_indices)
        molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
        return (molecule_types=='oligosaccharide').sum()

@digest(form=form)
def get_n_saccharides_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_saccharides_from_system (item)
    else:
        molecule_indices = get_molecule_index_from_atom (item, indices=indices)
        molecule_indices = np.unique(molecule_indices)
        molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
        return (molecule_types=='saccharide').sum()


## group

@digest(form=form)
def get_atom_index_from_group(item, indices='all'):

    output = []

    if is_all(indices):
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        mask = (item.atoms['group_index']==ii)
        output.append(item.atoms['atom_index'][mask].to_numpy())

    return output

@digest(form=form)
def get_atom_id_from_group(item, indices='all'):

    output=[]

    tmp_indices = get_atom_index_from_group(item, indices=indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices))

    return output

@digest(form=form)
def get_atom_name_from_group(item, indices='all'):

    output=[]

    tmp_indices = get_atom_index_from_group(item, indices=indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices))

    return output

@digest(form=form)
def get_atom_type_from_group(item, indices='all'):

    output=[]

    tmp_indices = get_atom_index_from_group(item, indices=indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices))

    return output

@digest(form=form)
def get_group_index_from_group(item, indices='all'):

    if is_all(indices):
        n_groups = get_n_groups_from_system(item)
        output = list(np.arange(n_groups))
    else:
        output = indices

    return output

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    if is_all(indices):
        output = item.groups['group_id'].to_list()
    else:
        output = item.groups['group_id'][indices].to_list()

    return output

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    if is_all(indices):
        output = item.groups['group_name'].to_list()
    else:
        output = item.groups['group_name'][indices].to_list()

    return output

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    if is_all(indices):
        output = item.groups['group_type'].to_list()
    else:
        output = item.groups['group_type'][indices].to_list()

    return output

@digest(form=form)
def get_component_index_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_id_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_name_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_type_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_index_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_id_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_name_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_type_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_index_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_id_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_name_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_type_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_index_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_id_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_name_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_type_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_atoms_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_groups_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_components_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_molecules_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_chains_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_entities_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_bonds_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_inner_bonds_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_aminoacids_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_nucleotides_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_ions_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_waters_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_small_molecules_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_peptides_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_proteins_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_dnas_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_rnas_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_lipids_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_oligosaccharides_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_saccharides_from_group(item, indices='all'):

    raise NotImplementedError



## component

@digest(form=form)
def get_atom_index_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_atom_id_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_atom_name_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_atom_type_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_index_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_id_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_name_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_type_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_index_from_component(item, indices='all'):

    if is_all(indices):
        n_components = get_n_components_from_system(item)
        output = list(np.arange(n_components))
    else:
        output = indices

    return output

@digest(form=form)
def get_component_id_from_component(item, indices='all'):

    if is_all(indices):
        output = item.components['component_id'].to_list()
    else:
        output = item.components['component_id'][indices].to_list()

    return output

@digest(form=form)
def get_component_name_from_component(item, indices='all'):

    if is_all(indices):
        output = item.components['component_name'].to_list()
    else:
        output = item.components['component_name'][indices].to_list()

    return output

@digest(form=form)
def get_component_type_from_component(item, indices='all'):

    if is_all(indices):
        output = item.components['component_type'].to_list()
    else:
        output = item.components['component_type'][indices].to_list()

    return output

@digest(form=form)
def get_chain_index_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_id_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_name_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_type_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_index_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_id_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_name_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_type_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_index_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_id_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_name_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_type_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_atoms_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_groups_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_components_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_molecules_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_chains_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_entities_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_bonds_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_aminoacids_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_nucleotides_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_ions_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_waters_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_small_molecules_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_peptides_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_proteins_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_dnas_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_rnas_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_lipids_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_oligosaccharides_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_saccharides_from_component(item, indices='all'):

    raise NotImplementedError


## molecule

@digest(form=form)
def get_atom_index_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_atom_id_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_atom_name_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_atom_type_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_index_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_id_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_name_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_type_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_index_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_id_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_name_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_type_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_index_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_id_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_name_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_type_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_index_from_molecule(item, indices='all'):

    if is_all(indices):
        n_molecules = get_n_molecules_from_system(item)
        output = list(np.arange(n_components))
    else:
        output = indices

    return output

@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all'):

    if is_all(indices):
        output = item.molecules['molecule_id'].to_list()
    else:
        output = item.molecules['molecule_id'][indices].to_list()

    return output

@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all'):

    if is_all(indices):
        output = item.molecules['molecule_name'].to_list()
    else:
        output = item.molecules['molecule_name'][indices].to_list()

    return output

@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all'):

    if is_all(indices):
        output = item.molecules['molecule_type'].to_list()
    else:
        output = item.molecules['molecule_type'][indices].to_list()

    return output

@digest(form=form)
def get_entity_index_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_id_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_name_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_type_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_atoms_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_groups_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_components_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_molecules_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_chains_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_entities_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_bonds_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_aminoacids_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_ions_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_waters_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_peptides_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_proteins_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_dnas_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_rnas_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_lipids_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_oligosaccharides_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all'):

    raise NotImplementedError


## chain

@digest(form=form)
def get_atom_index_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_atom_id_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_atom_name_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_atom_type_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_index_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_id_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_name_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_type_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_index_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_id_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_name_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_type_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_index_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_id_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_name_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_type_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_index_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_id_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_name_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_type_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_index_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_id_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_name_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_type_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_atoms_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_groups_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_components_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_molecules_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_chains_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_entities_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_bonds_from_chain(item, indices='all'):

    raise NotImplementedError


@digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_aminoacids_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_ions_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_waters_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_peptides_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_proteins_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_dnas_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_rnas_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_lipids_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_oligosaccharides_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_saccharides_from_chain(item, indices='all'):

    raise NotImplementedError


## entity

@digest(form=form)
def get_atom_index_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_atom_id_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_atom_name_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_atom_type_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_index_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_id_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_name_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_type_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_index_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_id_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_name_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_type_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_index_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_id_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_name_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_type_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_index_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_id_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_name_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_type_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_index_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_id_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_name_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_type_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_atoms_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_groups_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_components_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_molecules_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_chains_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_entities_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_bonds_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_aminoacids_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_ions_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_waters_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_peptides_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_proteins_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_dnas_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_rnas_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_lipids_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_oligosaccharides_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_saccharides_from_entity(item, indices='all'):

    raise NotImplementedError


## system

@digest(form=form)
def get_n_atoms_from_system(item):

    return item.atoms.shape[0]

@digest(form=form)
def get_n_groups_from_system(item):

    return item.groups.shape[0]

@digest(form=form)
def get_n_components_from_system(item):

    return item.components.shape[0]

@digest(form=form)
def get_n_chains_from_system(item):

    return item.chains.shape[0]

@digest(form=form)
def get_n_molecules_from_system(item):

    return item.molecules.shape[0]

@digest(form=form)
def get_n_entities_from_system(item):

    return item.entities.shape[0]

@digest(form=form)
def get_n_bonds_from_system(item):

    return item.bonds.shape[0]

@digest(form=form)
def get_n_inner_bonds_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_aminoacids_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_nucleotides_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_ions_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_waters_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_small_molecules_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_peptides_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_proteins_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_dnas_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_rnas_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_lipids_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_oligosaccharides_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_saccharides_from_system(item):

    raise NotImplementedError

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all'):

    raise NotImplementedError

## bond

@digest(form=form)
def get_bond_index_from_bond(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_bond_order_from_bond(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_bond_type_from_bond(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_n_bonds_from_bond(item, indices='all'):

    raise NotImplementedError

