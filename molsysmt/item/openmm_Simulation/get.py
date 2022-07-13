#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotWithThisFormError as _NotWithThisFormError
from molsysmt._private.exceptions import NotImplementedMethodError as _NotImplementedMethodError
from molsysmt._private.digestion import digest_item as _digest_item
from molsysmt._private.digestion import digest_indices as _digest_indices
from molsysmt._private.digestion import digest_structure_indices as _digest_structure_indices
from molsysmt._private.variables import is_all as _is_all
from molsysmt import puw as _puw
import numpy as _np
from networkx import Graph as _Graph

_form='openmm.Simulation'

## From atom

def get_atom_id_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_atom_name_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_atom_type_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_group_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_component_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_chain_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_molecule_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_entity_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_inner_bonded_atoms_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_n_inner_bonds_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_coordinates_from_atom(item, indices='all', structure_indices='all', check=True):

    coordinates = item.context.getState(getPositions=True).getPositions(asNumpy=True)
    unit = puw.get_unit(coordinates)
    coordinates = puw.get_value(coordinates)
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])

    if not _is_all(structure_indices):
        coordinates = coordinates[structure_indices,:,:]

    if not _is_all(indices):
        coordinates = coordinates[:,indices,:]

    coordinates = coordinates * unit
    coordinates = puw.standardize(coordinates)

    return coordinates

## From group

def get_group_id_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_group_name_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_group_type_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

## From component

def get_component_id_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_component_name_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_component_type_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

## From molecule

def get_molecule_id_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_molecule_name_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_molecule_type_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

## From chain

def get_chain_id_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_chain_name_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_chain_type_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

## From entity

def get_entity_id_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_entity_name_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_entity_type_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

## From system

def get_n_atoms_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return item.getNumParticles()

def get_n_groups_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    raise NotWithThisFormError()

def get_n_components_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    raise NotWithThisFormError()

def get_n_chains_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    raise NotWithThisFormError()

def get_n_molecules_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    raise NotWithThisFormError()

def get_n_entities_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    raise NotWithThisFormError()

def get_n_bonds_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    raise NotWithThisFormError()

def get_box_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    box=item.context.getState().getPeriodicBoxVectors(asNumpy=True)

    if box is not None:
        box_unit = box.unit
        box = np.array(box._value)
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * box_unit

    output=None

    if box is not None:
        if _is_all(structure_indices):
            output=box
        else:
            output=box[structure_indices,:,:]

    return output

def get_time_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    output = item.context.getState().getTime()
    value = puw.get_value(output)
    unit = puw.get_unit(output)
    output = np.array([value])*unit
    output = puw.standardize(output)

    return output

def get_step_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    return None

def get_n_structures_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return 1

def get_bonded_atoms_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    raise NotWithThisFormError()

## From bond

def get_bond_order_from_bond(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_bond_type_from_bond(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

def get_atom_index_from_bond(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    raise NotWithThisFormError()

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
    #get_coordinates_from_system,
    #get_box_shape_from_system,
    #get_box_lengths_from_system,
    #get_box_angles_from_system,
    #get_box_volume_from_system,
    #get_bonded_atoms_from_system,
    #get_bond_index_from_system,
    #get_inner_bonded_atoms_from_system,
    #get_inner_bond_index_from_system,

    # From bond
    #get_bond_index_from_bond,
    #get_n_bonds_from_bond

    )

