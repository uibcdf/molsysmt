#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.exceptions import NotWithThisFormError as _NotWithThisFormError
from molsysmt._private.exceptions import NotImplementedMethodError as _NotImplementedMethodError
from molsysmt._private.digestion import digest_item as _digest_item
from molsysmt._private.digestion import digest_indices as _digest_indices
from molsysmt._private.digestion import digest_structure_indices as _digest_structure_indices
from molsysmt import puw as _puw
import numpy as _np
from networkx import Graph as _Graph

_form='mdtraj.Topology'

## From atom

def get_atom_id_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices)
    output=[item.atom(ii).serial for ii in tmp_indices]
    output=np.array(output, dtype=int)
    return output

def get_atom_name_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices)
    output=[item.atom(ii).name for ii in tmp_indices]
    output=np.array(output, dtype=object)
    return output

def get_atom_type_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices)
    output=[item.atom(ii).element.symbol for ii in tmp_indices]
    output=np.array(output, dtype=object)
    return output

def get_group_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices)
    output=[item.atom(ii).residue.index for ii in tmp_indices]
    output=np.array(output, dtype=int)
    return output

def get_component_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.component import component_index_from_atom

    return component_index_from_atom(item, indices=indices)

def get_chain_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices)
    output=[item.atom(ii).residue.chain.index for ii in tmp_indices]
    output=np.array(output, dtype=int)
    return output

def get_molecule_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.molecule import molecule_index_from_atom as get
    return get(item, indices=indices)

def get_entity_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.entity import entity_index_from_atom as get
    return get(item, indices=indices)

def get_inner_bonded_atoms_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotImplementedError

def get_n_inner_bonds_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotImplementedError

## From group

def get_group_id_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = np.arange(n_indices)

    output = [item.residue(ii).resSeq for ii in indices]
    output = np.array(output, dtype=int)
    return output

def get_group_name_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = np.arange(n_indices)

    output = [item.residue(ii).name for ii in indices]
    output = np.array(output, dtype=object)
    return output

def get_group_type_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.group import group_type_from_group
    return group_type_from_group(item, indices=indices)

## From component

def get_component_id_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.component import component_id_from_component
    return component_id_from_component(item, indices=indices)

def get_component_name_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.component import component_name_from_component
    return component_name_from_component(item, indices=indices)

def get_component_type_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.component import component_type_from_component
    return component_type_from_component(item, indices=indices)

## From molecule

def get_molecule_id_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.molecule import molecule_id_from_molecule
    return molecule_id_from_molecule(item, indices=indices)

def get_molecule_name_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.molecule import molecule_name_from_molecule
    return molecule_name_from_molecule(item, indices=indices)

def get_molecule_type_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.molecule import molecule_type_from_molecule
    return molecule_type_from_molecule(item, indices=indices)

## From chain

def get_chain_id_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotImplementedError

def get_chain_name_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotImplementedError

def get_chain_type_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotImplementedError

## From entity

def get_entity_id_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.entity import entity_id_from_entity
    return entity_id_from_entity(item, indices=indices)

def get_entity_name_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.entity import entity_name_from_entity
    return entity_name_from_entity(item, indices=indices)

def get_entity_type_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.elements.entity import entity_type_from_entity
    return entity_type_from_entity(item, indices=indices)

## From system

def get_n_atoms_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return item.n_atoms

def get_n_groups_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return item.n_residues

def get_n_components_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    from molsysmt.elements.component import n_components_from_system as get
    return get(item)

def get_n_chains_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return item.n_chains

def get_n_molecules_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    from molsysmt.elements.molecule import n_molecules_from_system as get
    return get(item)

def get_n_entities_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    from molsysmt.elements.entity import n_entities_from_system as get
    return get(item)

def get_n_bonds_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return item.n_bonds

def get_bonded_atoms_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    raise NotImplementedError

## From bond

def get_bond_order_from_bond(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotImplementedError

def get_bond_type_from_bond(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotImplementedError

def get_atom_index_from_bond(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_bond_index_from_bond(item, indices=indices, structure_indices=structure_indices)
    bond = list(item.bonds)
    output=[[bond[ii].atom1.index, bond[ii].atom2.index] for ii in tmp_indices]
    output=np.array(output)
    del(bond)
    return output

#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)

#######################################################################################
############## REMOVE COMMON GET METHODS NOT DEFINED FOR THIS FORM ####################
#######################################################################################

del(

    # From atom
    #get_atom_index_from_atom,
    #get_group_id_from_atom,
    #get_group_name_from_atom,
    #get_group_type_from_atom,
    #get_component_id_from_atom,
    #get_component_name_from_atom,
    #get_component_type_from_atom,
    #get_chain_id_from_atom,
    #get_chain_name_from_atom,
    #get_chain_type_from_atom,
    #get_molecule_id_from_atom,
    #get_molecule_name_from_atom,
    #get_molecule_type_from_atom,
    #get_entity_id_from_atom,
    #get_entity_name_from_atom,
    #get_entity_type_from_atom,
    #get_n_atoms_from_atom,
    #get_n_groups_from_atom,
    #get_n_components_from_atom,
    #get_n_molecules_from_atom,
    #get_n_chains_from_atom,
    #get_n_entities_from_atom,
    #get_bonded_atoms_from_atom,
    #get_bond_index_from_atom,
    #get_n_bonds_from_atom,
    #get_inner_bond_index_from_atom,

    # From group
    #get_atom_index_from_group,
    #get_atom_id_from_group,
    #get_atom_name_from_group,
    #get_atom_type_from_group,
    #get_group_index_from_group,
    #get_component_index_from_group,
    #get_component_id_from_group,
    #get_component_name_from_group,
    #get_component_type_from_group,
    #get_chain_index_from_group,
    #get_chain_id_from_group,
    #get_chain_name_from_group,
    #get_chain_type_from_group,
    #get_molecule_index_from_group,
    #get_molecule_id_from_group,
    #get_molecule_name_from_group,
    #get_molecule_type_from_group,
    #get_entity_index_from_group,
    #get_entity_id_from_group,
    #get_entity_name_from_group,
    #get_entity_type_from_group,
    #get_n_atoms_from_group,
    #get_n_groups_from_group,
    #get_n_components_from_group,
    #get_n_molecules_from_group,
    #get_n_chains_from_group,
    #get_n_entities_from_group,

    # From component
    #get_atom_index_from_component,
    #get_atom_id_from_component,
    #get_atom_name_from_component,
    #get_atom_type_from_component,
    #get_group_index_from_component,
    #get_group_id_from_component,
    #get_group_name_from_component,
    #get_group_type_from_component,
    #get_component_index_from_component,
    #get_chain_index_from_component,
    #get_chain_id_from_component,
    #get_chain_name_from_component,
    #get_chain_type_from_component,
    #get_molecule_index_from_component,
    #get_molecule_id_from_component,
    #get_molecule_name_from_component,
    #get_molecule_type_from_component,
    #get_entity_index_from_component,
    #get_entity_id_from_component,
    #get_entity_name_from_component,
    #get_entity_type_from_component,
    #get_n_atoms_from_component,
    #get_n_groups_from_component,
    #get_n_components_from_component,
    #get_n_molecules_from_component,
    #get_n_chains_from_component,
    #get_n_entities_from_component,

    # From molecule
    #get_atom_index_from_molecule,
    #get_atom_id_from_molecule,
    #get_atom_name_from_molecule,
    #get_atom_type_from_molecule,
    #get_group_index_from_molecule,
    #get_group_id_from_molecule,
    #get_group_name_from_molecule,
    #get_group_type_from_molecule,
    #get_component_index_from_molecule,
    #get_component_id_from_molecule,
    #get_component_name_from_molecule,
    #get_component_type_from_molecule,
    #get_chain_index_from_molecule,
    #get_chain_id_from_molecule,
    #get_chain_name_from_molecule,
    #get_chain_type_from_molecule,
    #get_molecule_index_from_molecule,
    #get_entity_index_from_molecule,
    #get_entity_id_from_molecule,
    #get_entity_name_from_molecule,
    #get_entity_type_from_molecule,
    #get_n_atoms_from_molecule,
    #get_n_groups_from_molecule,
    #get_n_components_from_molecule,
    #get_n_molecules_from_molecule,
    #get_n_chains_from_molecule,
    #get_n_entities_from_molecule,

    # From chain
    #get_atom_index_from_chain,
    #get_atom_id_from_chain,
    #get_atom_name_from_chain,
    #get_atom_type_from_chain,
    #get_group_index_from_chain,
    #get_group_id_from_chain,
    #get_group_name_from_chain,
    #get_group_type_from_chain,
    #get_component_index_from_chain,
    #get_component_id_from_chain,
    #get_component_name_from_chain,
    #get_component_type_from_chain,
    #get_chain_index_from_chain,
    #get_molecule_index_from_chain,
    #get_molecule_id_from_chain,
    #get_molecule_name_from_chain,
    #get_molecule_type_from_chain,
    #get_entity_index_from_chain,
    #get_entity_id_from_chain,
    #get_entity_name_from_chain,
    #get_entity_type_from_chain,
    #get_n_atoms_from_chain,
    #get_n_groups_from_chain,
    #get_n_components_from_chain,
    #get_n_molecules_from_chain,
    #get_n_chains_from_chain,
    #get_n_entities_from_chain,

    # From entity
    #get_atom_index_from_entity,
    #get_atom_id_from_entity,
    #get_atom_name_from_entity,
    #get_atom_type_from_entity,
    #get_group_index_from_entity,
    #get_group_id_from_entity,
    #get_group_name_from_entity,
    #get_group_type_from_entity,
    #get_component_index_from_entity,
    #get_component_id_from_entity,
    #get_component_name_from_entity,
    #get_component_type_from_entity,
    #get_chain_index_from_entity,
    #get_chain_id_from_entity,
    #get_chain_name_from_entity,
    #get_chain_type_from_entity,
    #get_molecule_index_from_entity,
    #get_molecule_id_from_entity,
    #get_molecule_name_from_entity,
    #get_molecule_type_from_entity,
    #get_entity_index_from_entity,
    #get_n_atoms_from_entity,
    #get_n_groups_from_entity,
    #get_n_components_from_entity,
    #get_n_molecules_from_entity,
    #get_n_chains_from_entity,
    #get_n_entities_from_entity,

    # From system
    #get_n_aminoacids_from_system,
    #get_n_nucleotides_from_system,
    #get_n_ions_from_system,
    #get_n_waters_from_system,
    #get_n_cosolutes_from_system,
    #get_n_small_molecules_from_system,
    #get_n_peptides_from_system,
    #get_n_proteins_from_system,
    #get_n_dnas_from_system,
    #get_n_rnas_from_system,
    #get_n_lipids_from_system,
    get_coordinates_from_system,
    get_box_shape_from_system,
    get_box_lengths_from_system,
    get_box_angles_from_system,
    get_box_volume_from_system,
    #get_bonded_atoms_from_system,
    #get_bond_index_from_system,
    #get_inner_bonded_atoms_from_system,
    #get_inner_bond_index_from_system,

    # From bond
    #get_bond_index_from_bond,
    #get_n_bonds_from_bond

    )

