#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from .is_openmm_Topology import is_openmm_Topology
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np
from networkx import Graph

## From atom

def get_atom_id_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    atom=list(item.atoms())
    output=[atom[ii].id for ii in tmp_indices]
    output=np.array(output, dtype=int)
    del(atom)

    return output

def get_atom_name_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    atom=list(item.atoms())
    output=[atom[ii].name for ii in tmp_indices]
    output=np.array(output)
    del(atom)

    return output

def get_atom_type_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    atom=list(item.atoms())
    output=[atom[ii].element.symbol for ii in tmp_indices]
    output=np.array(output)
    del(atom)

    return output

def get_group_index_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()


    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    atom=list(item.atoms())
    output = [atom[ii].residue.index for ii in tmp_indices]
    output=np.array(output)
    del(atom)

    return output

def get_component_index_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()


    from molsysmt.element.component import component_index_from_atom as _get
    return _get(item, indices=indices, check=False)

def get_chain_index_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    atom=list(item.atoms())
    output = [atom[ii].residue.chain.index for ii in tmp_indices]
    del(atom)
    output =np.array(output)

    return output

def get_molecule_index_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    from molsysmt.element.molecule import molecule_index_from_atom as _get
    return _get(item, indices=indices, check=False)

def get_entity_index_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    from molsysmt.element.entity import entity_index_from_atom as _get
    return _get(item, indices=indices, check=False)

def get_inner_bonded_atoms_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output=[]

    if indices is 'all':

        for bond in item.bonds():
            output.append([bond.atom1.index, bond.atom2.index])

    else:

        set_indices = set(indices)

        for bond in item.bonds():
            if bond.atom1.index in set_indices:
                if bond.atom2.index in set_indices:
                    output.append([bond.atom1.index, bond.atom2.index])

    output = np.array(output, dtype=int)

    return(output)

def get_n_inner_bonds_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_bonds_from_system (item)
    else:
        inner_bonded_atoms = get_inner_bonded_atoms_from_atom(item, indices=indices,
                structure_indices=structure_indices)
        return inner_bonded_atoms.shape[0]


def get_coordinates_from_atom(item, indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    raise NotWithThisFormError()

## From group

def get_group_id_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_indices = get_n_groups_from_system(item, check=False)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].id for ii in indices]
    del(group)
    output = np.array(output, dtype=int)

    return output

def get_group_name_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_indices = get_n_groups_from_system(item, check=False)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].name for ii in indices]
    del(group)
    output =np.array(output, dtype=object)

    return output

def get_group_type_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    from molsysmt.element.group import name_to_type

    if indices is 'all':
        n_indices = get_n_groups_from_system(item, check=False)
        indices = range(n_indices)

    group=list(item.residues())
    output = [name_to_type(group[ii].name) for ii in indices]
    del(group)
    output = np.array(output, dtype=object)

    return output

## From component

def get_component_id_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    from molsysmt.element.component import get_component_index_from_atom as _get
    return _get(item, indices=indices, check=False)

def get_component_name_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    from molsysmt.element.component import get_component_name_from_atom as _get
    return _get(item, indices=indices, check=False)

def get_component_type_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    from molsysmt.element.component import get_component_type_from_atom as _get
    return _get(item, indices=indices)

## From molecule

def get_molecule_id_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    from molsysmt.element.molecule import molecule_id_from_molecule as _get
    return _get(item, indices)

def get_molecule_name_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    from molsysmt.element.molecule import molecule_name_from_molecule as _get
    return _get(item, indices, check=False)

def get_molecule_type_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    from molsysmt.element.molecule import molecule_type_from_molecule as _get
    return _get(item, indices, check=False)

## From chain

def get_chain_id_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_indices = get_n_chains_from_system(item, check=False)
        indices = range(n_indices)

    chain=list(item.chains())
    output = [chain[ii].id for ii in indices]
    del(chain)
    output = np.array(output)

    return output

def get_chain_name_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_indices = get_n_chains_from_system(item, check=False)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = np.array(output)
    return output

def get_chain_type_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_indices = get_n_chains_from_system(item, check=False)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = np.array(output)
    return output

## From entity

def get_entity_id_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    from molsysmt.element.entity import entity_id_from_entity as _get
    return _get(item, indices, check=False)

def get_entity_name_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    from molsysmt.element.entity import entity_name_from_entity as _get
    return _get(item, indices)

def get_entity_type_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    from molsysmt.element.entity import entity_type_from_entity as _get
    return _get(item, indices)

## From system

def get_n_atoms_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    return item.getNumAtoms()

def get_n_groups_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    return item.getNumResidues()

def get_n_components_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    from molsysmt.element.component import n_components_from_system as _get
    return _get(item, check=False)

def get_n_chains_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    return item.getNumChains()

def get_n_molecules_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    from molsysmt.element.molecule import n_molecules_from_system as _get
    return _get(item, check=False)

def get_n_entities_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    from molsysmt.element.entity import n_entities_from_system as _get
    return _get(item, check=False)

def get_n_bonds_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    return item.getNumBonds()

def get_box_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt import puw

    box = item.getPeriodicBoxVectors()

    output = None

    if box is not None:
        unit = puw.get_unit(box)
        box = np.array(puw.get_value(box))
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * unit
        output = puw.standardize(box)

    return output

def get_time_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    return None

def get_step_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    return None

def get_n_structures_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    return 0

def get_bonded_atoms_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    raise NotImplementedMethodError

## From bond

def get_bond_order_from_bond(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_bond_index_from_bond(item, indices=indices, check=False)
    bond = list(item.bonds())
    output=[bond[ii].order for ii in tmp_indices]
    output=np.array(output)
    del(bond)

    return output

def get_bond_type_from_bond(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    tmp_indices = get_bond_index_from_bond(item, indices=indices, check=False)
    bond = list(item.bonds())
    output=[bond[ii].type for ii in tmp_indices]
    output=np.array(output)
    del(bond)

    return output

def get_atom_index_from_bond(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_bonds = get_n_bonds_from_system(item, check=False)
        indices = np.arange(n_bonds)

    bond = list(item.bonds())
    output=[[bond[ii].atom1.index, bond[ii].atom2.index] for ii in indices]
    output=np.array(output)
    del(bond)

    return output

#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

## From atom

def get_atom_index_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_aux = get_n_atoms_from_system(item, check=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_group_id_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_group_name_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_group_type_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_component_id_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_component_name_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_component_type_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_id_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_name_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_type_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_id_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_name_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_type_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_id_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_name_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_type_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_atom(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_n_atoms_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_atoms_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

def get_n_groups_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_groups_from_system(item, check=False)
    else:
        output = get_group_index_from_atom(item, indices=indices, check=True)
        output = np.unique(output).shape[0]

    return output

def get_n_components_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_components_from_system(item, check=False)
    else:
        output = get_component_index_from_atom(item, indices=indices, check=True)
        output = np.unique(output).shape[0]

    return output

def get_n_molecules_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_molecules_from_system(item, check=False)
    else:
        output = get_molecule_index_from_atom(item, indices=indices, check=True)
        output = np.unique(output).shape[0]

    return output

def get_n_chains_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_chains_from_system(item, check=False)
    else:
        output = get_chain_index_from_atom(item, indices=indices, check=True)
        output = np.unique(output).shape[0]

    return output

def get_n_entities_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_entities_from_system(item, check=False)
    else:
        output = get_entity_index_from_atom(item, indices=indices, check=True)
        output = np.unique(output).shape[0]

    return output

def get_bonded_atoms_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

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

def get_bond_index_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

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

def get_n_bonds_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

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

def get_inner_bond_index_from_atom(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    raise NotImplementedError


## From group

def get_atom_index_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_group(item, indices=indices, check=False)
    aux_indices = get_group_index_from_atom(item, check=False)
    aux_vals = get_atom_index_from_atom(item, check=False)

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

def get_atom_id_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_group(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_group(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_group(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_aux = get_n_groups_from_system(item, check=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_component_index_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, check=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_component_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_component_id_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_component_name_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_component_type_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_chain_index_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, check=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_chain_id_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_chain_name_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_chain_type_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_molecule_index_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, check=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_molecule_id_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_molecule_name_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_molecule_type_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_entity_index_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, check=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_entity_id_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_entity_name_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_entity_type_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_group(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_n_atoms_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_atom_index_from_group(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_groups_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()


    if indices is 'all':
        output = get_n_groups_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

def get_n_components_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_components_from_system(item, check=False)
    else:
        output = get_component_index_from_group(item, indices=indices, check=False)
        output = np.unique(output).shape[0]

    return output

def get_n_molecules_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_molecules_from_system(item, check=False)
    else:
        output = get_molecule_index_from_group(item, indices=indices, check=False)
        output = np.unique(output).shape[0]

    return output

def get_n_chains_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_chains_from_system(item, check=False)
    else:
        output = get_chain_index_from_group(item, indices=indices, check=False)
        output = np.unique(output).shape[0]

    return output

def get_n_entities_from_group(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        return get_n_entities_from_system(item, check=False)
    else:
        output = get_entity_index_from_group(item, indices=indices, check=False)
        output = np.unique(output).shape[0]

    return output


## From component

def get_atom_index_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_component(item, indices=indices, check=False)
    aux_indices = get_component_index_from_atom(item, check=False)
    aux_vals = get_atom_index_from_atom(item, check=False)

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

def get_atom_id_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_component(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_component(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_component(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_component(item, indices=indices, check=False)
    aux_indices = get_component_index_from_atom(item, check=False)
    aux_vals = get_group_index_from_atom(item, check=False)

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

def get_group_id_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_component(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_name_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_component(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_type_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_component(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_index_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_aux = get_n_components_from_system(item, check=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_chain_index_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, check=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_chain_id_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_name_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_type_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_index_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, check=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_molecule_id_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_name_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_type_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_index_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, check=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_entity_id_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_name_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_type_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_component(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_n_atoms_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_atom_index_from_component(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_groups_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_group_index_from_component(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_components_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_components_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

def get_n_molecules_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_molecules_from_system(item, check=False)
    else:
        output = get_molecule_index_from_component(item, indices=indices, check=True)
        output = np.unique(output).shape[0]

    return output

def get_n_chains_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_chains_from_system(item, check=False)
    else:
        output = get_chain_index_from_component(item, indices=indices, check=True)
        output = np.unique(output).shape[0]

    return output

def get_n_entities_from_component(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_entities_from_system(item, check=False)
    else:
        output = get_entity_index_from_component(item, indices=indices, check=True)
        output = np.unique(output).shape[0]

    return output

## molecule

def get_atom_index_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_molecule(item, indices=indices, check=False)
    aux_indices = get_molecule_index_from_atom(item, check=False)
    aux_vals = get_atom_index_from_atom(item, check=False)

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

def get_atom_id_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_molecule(item, indices=indices, check=False)
    aux_indices = get_molecule_index_from_atom(item, check=False)
    aux_vals = get_group_index_from_atom(item, check=False)

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

def get_group_id_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_name_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_type_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_index_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_molecule(item, indices=indices, check=False)
    aux_indices = get_molecule_index_from_atom(item, check=False)
    aux_vals = get_component_index_from_atom(item, check=False)

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

def get_component_id_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_name_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_type_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_index_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_molecule(item, indices=indices, check=False)
    aux_indices = get_molecule_index_from_atom(item, check=False)
    aux_vals = get_chain_index_from_atom(item, check=False)

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

def get_chain_id_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_name_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_type_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_molecule(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_index_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_aux = get_n_molecules_from_system(item, check=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_entity_index_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    atom_index_from_target = get_atom_index_from_molecule(item, indices=indices, check=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, check=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_entity_id_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_molecule(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_name_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_molecule(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_type_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_molecule(item, indices=indices, check=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_n_atoms_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_atom_index_from_molecule(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_groups_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_group_index_from_molecule(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_components_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_component_index_from_molecule(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_molecules_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_molecules_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

def get_n_chains_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_chain_index_from_molecule(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_entities_from_molecule(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_entities_from_system(item, check=False)
    else:
        output = get_entity_index_from_molecule(item, indices=indices, check=True)
        output = np.unique(output).shape[0]

    return output

## chain

def get_atom_index_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, check=False)
    aux_indices = get_chain_index_from_atom(item, check=False)
    aux_vals = get_atom_index_from_atom(item, check=False)

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

def get_atom_id_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, check=False)
    aux_indices = get_chain_index_from_atom(item, check=False)
    aux_vals = get_group_index_from_atom(item, check=False)

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

def get_group_id_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_name_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_type_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_index_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, check=False)
    aux_indices = get_chain_index_from_atom(item, check=False)
    aux_vals = get_component_index_from_atom(item, check=False)

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

def get_component_id_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_name_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_type_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_index_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_aux = get_n_chains_from_system(item, check=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_molecule_index_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, check=False)
    aux_indices = get_chain_index_from_atom(item, check=False)
    aux_vals = get_molecule_index_from_atom(item, check=False)

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

def get_molecule_id_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_name_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_type_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_entity_index_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, check=False)
    aux_indices = get_chain_index_from_atom(item, check=False)
    aux_vals = get_entity_index_from_atom(item, check=False)

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

def get_entity_id_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_entity_name_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_entity_type_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_entity_index_from_chain(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_n_atoms_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_atom_index_from_chain(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_groups_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_group_index_from_chain(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_components_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_component_index_from_chain(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_molecules_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_molecule_index_from_chain(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_chains_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_chains_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

def get_n_entities_from_chain(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_entities_from_system(item, check=False)
    else:
        output = get_entity_index_from_chain(item, indices=indices, check=True)
        output = np.unique(output).shape[0]

    return output

## From entity

def get_atom_index_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices, check=False)
    aux_indices = get_entity_index_from_atom(item, check=False)
    aux_vals = get_atom_index_from_atom(item, check=False)

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

def get_atom_id_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_atom_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices, check=False)
    aux_indices = get_entity_index_from_atom(item, check=False)
    aux_vals = get_group_index_from_atom(item, check=False)

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

def get_group_id_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_name_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_type_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_group_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_index_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices, check=False)
    aux_indices = get_entity_index_from_atom(item, check=False)
    aux_vals = get_component_index_from_atom(item, check=False)

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

def get_component_id_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_name_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_type_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_component_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_index_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices, check=False)
    aux_indices = get_entity_index_from_atom(item, check=False)
    aux_vals = get_chain_index_from_atom(item, check=False)

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

def get_chain_id_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_name_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_type_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_chain_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_index_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices, check=False)
    aux_indices = get_entity_index_from_atom(item, check=False)
    aux_vals = get_molecule_index_from_atom(item, check=False)

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

def get_molecule_id_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_name_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_type_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    aux_indices = get_molecule_index_from_entity(item, indices=indices, check=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_entity_index_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_aux = get_n_entities_from_system(item, check=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_n_atoms_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_atom_index_from_entity(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_groups_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_group_index_from_entity(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_components_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_component_index_from_entity(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_molecules_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_molecule_index_from_entity(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_chains_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    output = get_chain_index_from_entity(item, indices=indices, check=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_entities_from_entity(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_entities_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

## system

def get_n_aminoacids_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    group_types = get_group_type_from_group(item, check=False)
    return (group_types=='aminoacid').sum()

def get_n_nucleotides_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    group_types = get_group_type_from_group(item, check=False)
    return (group_types=='nucleotide').sum()

def get_n_ions_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    molecule_types = get_group_type_from_group(item, check=False)
    return (molecule_types=='ion').sum()

def get_n_waters_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    molecule_types = get_group_type_from_group(item, check=False)
    return (molecule_types=='water').sum()

def get_n_cosolutes_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    molecule_types = get_group_type_from_group(item, check=False)
    return (molecule_types=='cosolute').sum()

def get_n_small_molecules_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    molecule_types = get_group_type_from_group(item, check=False)
    return (molecule_types=='small molecule').sum()

def get_n_peptides_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    molecule_types = get_molecule_type_from_molecule(item, check=False)
    return (molecule_types=='peptide').sum()

def get_n_proteins_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    molecule_types = get_molecule_type_from_molecule(item, check=False)
    return (molecule_types=='protein').sum()

def get_n_dnas_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    molecule_types = get_molecule_type_from_molecule(item, check=False)
    return (molecule_types=='dna').sum()

def get_n_rnas_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    molecule_types = get_molecule_type_from_molecule(item, check=False)
    return (molecule_types=='rna').sum()

def get_n_lipids_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    molecule_types = get_molecule_type_from_molecule(item, check=False)
    return (molecule_types=='lipid').sum()

def get_coordinates_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    return get_coordinates_from_atom(item, structure_indices=structure_indices, check=False)

def get_box_shape_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.pbc import box_shape_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    output = box_shape_from_box_vectors(tmp_box, check=False)

    return output

def get_box_lengths_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.pbc import box_lengths_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    output = box_lengths_from_box_vectors(tmp_box, check=False)

    return output

def get_box_angles_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.pbc import box_angles_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    output = box_angles_from_box_vectors(tmp_box, check=False)

    return output

def get_box_volume_from_system(item, structure_indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.pbc import box_volume_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    if tmp_box is None:
        output=None
    else:
        output = box_volume_from_box_vectors(tmp_box, check=False)

    return output

def get_bonded_atoms_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    return get_bonded_atoms_from_atom(item, check=False)

def get_bond_index_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')


    return get_bond_index_from_atom(item, check=False)

def get_inner_bonded_atoms_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    return get_inner_bonded_atoms_from_atom(item, check=False)

def get_inner_bond_index_from_system(item, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

    return get_inner_bond_index_from_atom(item, check=False)

## bond

def get_bond_index_from_bond(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        n_aux = get_n_bonds_from_system(item, check=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_n_bonds_from_bond(item, indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

    if indices is 'all':
        output = get_n_bonds_from_system(item, check=False)
    else:
        output = indices.shape[0]

    return output

