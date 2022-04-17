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

_form='file:pdb'


## From atom

def get_atom_id_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_atom_id_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_atom_name_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_atom_name_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_atom_type_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_atom_type_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_group_index_from_atom (item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_group_index_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_component_index_from_atom (item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_component_index_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_chain_index_from_atom (item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_chain_index_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_molecule_index_from_atom (item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_molecule_index_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_entity_index_from_atom (item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_entity_index_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_inner_bonded_atoms_from_atom (item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_inner_bonded_atoms_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_n_inner_bonds_from_atom (item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_n_inner_bonds_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_coordinates_from_atom(item, indices='all', structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)
        structure_indices = _digest_structure_indices(structure_indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_coordinates_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

## group

def get_group_id_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_group_id_from_group as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_group_name_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_group_name_from_group as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_group_type_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_group_type_from_group as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

## component

def get_component_id_from_component (item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_component_id_from_component as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_component_name_from_component (item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_component_name_from_component as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_component_type_from_component (item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_component_type_from_component as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

## molecule

def get_molecule_id_from_molecule (item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_molecule_id_from_molecule as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, check=False)

    return output

def get_molecule_name_from_molecule (item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_molecule_name_from_molecule as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_molecule_type_from_molecule (item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_molecule_type_from_molecule as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

## chain

def get_chain_id_from_chain (item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_chain_id_from_chain as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_chain_name_from_chain (item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_chain_name_from_chain as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_chain_type_from_chain (item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_chain_type_from_chain as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

## entity

def get_entity_id_from_entity (item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_entity_id_from_entity as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_entity_name_from_entity (item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_entity_name_from_entity as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_entity_type_from_entity (item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_entity_type_from_entity as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

## system

def get_n_atoms_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_n_atoms_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_n_groups_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_n_groups_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_n_components_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_n_components_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_n_chains_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_n_chains_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_n_molecules_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_n_molecules_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_n_entities_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_n_entities_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_n_bonds_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_n_bonds_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_coordinates_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_coordinates_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_box_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_box_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_box_shape_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_box_shape_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_box_lengths_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_box_lengths_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_box_angles_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_box_angles_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_box_volume_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_box_volume_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_time_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_time_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_step_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_step_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_n_structures_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_n_structures_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_bonded_atoms_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

## bond

def get_bond_order_from_bond(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_bond_order_from_bond as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_bond_type_from_bond(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_bond_type_from_bond as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

def get_atom_index_from_bond(item, indices='all', structure_indices='all', check=True):

    _checking_form(item, check)

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import get_atom_index_from_bond as aux_get

    tmp_item = to_openmm_PDBFile(item, check=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check=False)

    return output

#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

