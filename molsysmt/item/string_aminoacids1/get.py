#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotWithThisFormError as _NotWithThisFormError
from molsysmt._private.exceptions import NotImplementedMethodError as _NotImplementedMethodError
from molsysmt._private.digestion import digest_item as _digest_item
from molsysmt._private.digestion import digest_indices as _digest_indices
from molsysmt._private.digestion import digest_structure_indices as _digest_structure_indices
from molsysmt import puw as _puw
import numpy as _np
from networkx import Graph as _Graph

_form='string:aminoacids1'

## From atom

## From group

def get_group_id_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise _NotImplementedMethodError()

def get_group_name_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise _NotImplementedMethodError()

def get_group_type_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise _NotImplementedMethodError()

## From component

## From molecule

## From chain

## From entity

## From system

def get_n_groups_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return len(item)

## From bond


#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)

#######################################################################################
########### REMOVE COMMON GET METHODS NOT DEFINED FOR THIS CURRENT FORM ###############
#######################################################################################

del(

    # From atom
    get_atom_index_from_atom,
    get_group_id_from_atom,
    get_group_name_from_atom,
    get_group_type_from_atom,
    get_component_id_from_atom,
    get_component_name_from_atom,
    get_component_type_from_atom,
    get_chain_id_from_atom,
    get_chain_name_from_atom,
    get_chain_type_from_atom,
    get_molecule_id_from_atom,
    get_molecule_name_from_atom,
    get_molecule_type_from_atom,
    get_entity_id_from_atom,
    get_entity_name_from_atom,
    get_entity_type_from_atom,
    get_n_atoms_from_atom,
    get_n_groups_from_atom,
    get_n_components_from_atom,
    get_n_molecules_from_atom,
    get_n_chains_from_atom,
    get_n_entities_from_atom,
    get_bonded_atoms_from_atom,
    get_bond_index_from_atom,
    get_n_bonds_from_atom,
    get_inner_bond_index_from_atom,

    # From group
    get_atom_index_from_group,
    get_atom_id_from_group,
    get_atom_name_from_group,
    get_atom_type_from_group,
    get_group_index_from_group,
    get_component_index_from_group,
    get_component_id_from_group,
    get_component_name_from_group,
    get_component_type_from_group,
    get_chain_index_from_group,
    get_chain_id_from_group,
    get_chain_name_from_group,
    get_chain_type_from_group,
    get_molecule_index_from_group,
    get_molecule_id_from_group,
    get_molecule_name_from_group,
    get_molecule_type_from_group,
    get_entity_index_from_group,
    get_entity_id_from_group,
    get_entity_name_from_group,
    get_entity_type_from_group,
    get_n_atoms_from_group,
    get_n_groups_from_group,
    get_n_components_from_group,
    get_n_molecules_from_group,
    get_n_chains_from_group,
    get_n_entities_from_group,

    # From component
    get_atom_index_from_component,
    get_atom_id_from_component,
    get_atom_name_from_component,
    get_atom_type_from_component,
    get_group_index_from_component,
    get_group_id_from_component,
    get_group_name_from_component,
    get_group_type_from_component,
    get_component_index_from_component,
    get_chain_index_from_component,
    get_chain_id_from_component,
    get_chain_name_from_component,
    get_chain_type_from_component,
    get_molecule_index_from_component,
    get_molecule_id_from_component,
    get_molecule_name_from_component,
    get_molecule_type_from_component,
    get_entity_index_from_component,
    get_entity_id_from_component,
    get_entity_name_from_component,
    get_entity_type_from_component,
    get_n_atoms_from_component,
    get_n_groups_from_component,
    get_n_components_from_component,
    get_n_molecules_from_component,
    get_n_chains_from_component,
    get_n_entities_from_component,

    # From molecule
    get_atom_index_from_molecule,
    get_atom_id_from_molecule,
    get_atom_name_from_molecule,
    get_atom_type_from_molecule,
    get_group_index_from_molecule,
    get_group_id_from_molecule,
    get_group_name_from_molecule,
    get_group_type_from_molecule,
    get_component_index_from_molecule,
    get_component_id_from_molecule,
    get_component_name_from_molecule,
    get_component_type_from_molecule,
    get_chain_index_from_molecule,
    get_chain_id_from_molecule,
    get_chain_name_from_molecule,
    get_chain_type_from_molecule,
    get_molecule_index_from_molecule,
    get_entity_index_from_molecule,
    get_entity_id_from_molecule,
    get_entity_name_from_molecule,
    get_entity_type_from_molecule,
    get_n_atoms_from_molecule,
    get_n_groups_from_molecule,
    get_n_components_from_molecule,
    get_n_molecules_from_molecule,
    get_n_chains_from_molecule,
    get_n_entities_from_molecule,

    # From chain
    get_atom_index_from_chain,
    get_atom_id_from_chain,
    get_atom_name_from_chain,
    get_atom_type_from_chain,
    get_group_index_from_chain,
    get_group_id_from_chain,
    get_group_name_from_chain,
    get_group_type_from_chain,
    get_component_index_from_chain,
    get_component_id_from_chain,
    get_component_name_from_chain,
    get_component_type_from_chain,
    get_chain_index_from_chain,
    get_molecule_index_from_chain,
    get_molecule_id_from_chain,
    get_molecule_name_from_chain,
    get_molecule_type_from_chain,
    get_entity_index_from_chain,
    get_entity_id_from_chain,
    get_entity_name_from_chain,
    get_entity_type_from_chain,
    get_n_atoms_from_chain,
    get_n_groups_from_chain,
    get_n_components_from_chain,
    get_n_molecules_from_chain,
    get_n_chains_from_chain,
    get_n_entities_from_chain,

    # From entity
    get_atom_index_from_entity,
    get_atom_id_from_entity,
    get_atom_name_from_entity,
    get_atom_type_from_entity,
    get_group_index_from_entity,
    get_group_id_from_entity,
    get_group_name_from_entity,
    get_group_type_from_entity,
    get_component_index_from_entity,
    get_component_id_from_entity,
    get_component_name_from_entity,
    get_component_type_from_entity,
    get_chain_index_from_entity,
    get_chain_id_from_entity,
    get_chain_name_from_entity,
    get_chain_type_from_entity,
    get_molecule_index_from_entity,
    get_molecule_id_from_entity,
    get_molecule_name_from_entity,
    get_molecule_type_from_entity,
    get_entity_index_from_entity,
    get_n_atoms_from_entity,
    get_n_groups_from_entity,
    get_n_components_from_entity,
    get_n_molecules_from_entity,
    get_n_chains_from_entity,
    get_n_entities_from_entity,

    # From system
    get_n_aminoacids_from_system,
    get_n_nucleotides_from_system,
    get_n_ions_from_system,
    get_n_waters_from_system,
    get_n_cosolutes_from_system,
    get_n_small_molecules_from_system,
    get_n_peptides_from_system,
    get_n_proteins_from_system,
    get_n_dnas_from_system,
    get_n_rnas_from_system,
    get_n_lipids_from_system,
    get_coordinates_from_system,
    get_box_shape_from_system,
    get_box_lengths_from_system,
    get_box_angles_from_system,
    get_box_volume_from_system,
    get_bonded_atoms_from_system,
    get_bond_index_from_system,
    get_inner_bonded_atoms_from_system,
    get_inner_bond_index_from_system,

    # From bond
    get_bond_index_from_bond,
    get_n_bonds_from_bond

    )

