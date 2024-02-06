from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='molsysmt.MolSys'

###### Set

## to atom

@digest(form=form)
def set_atom_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_atom_index_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_atom_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_atom_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_atom_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_atom_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_atom_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_atom_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_group_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_group_index_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_group_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_group_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_group_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_group_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_group_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_group_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_component_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_component_index_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_component_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_component_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_component_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_component_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_component_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_component_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_index_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_index_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_index_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Structures import set_coordinates_to_atom as aux_set
    from ..molsysmt_Topology import get_n_atoms_from_system

    if is_all(indices):
        n_atoms = get_n_atoms_from_system(item.topology, skip_digestion=True)
        if n_atoms!=value.shape[1]:
            raise ValueError('Coordinates has a different atoms number.')

    return aux_set(item.structures, indices=indices, structure_indices=structure_indices,
                value=value, skip_digestion=True)

@digest(form=form)
def set_velocities_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Structures import set_velocities_to_atom as aux_set
    from ..molsysmt_Topology import get_n_atoms_from_system

    if is_all(indices):
        n_atoms = get_n_atoms_from_system(item.topology, skip_digestion=True)
        if n_atoms!=value.shape[1]:
            raise ValueError('Coordinates has a different atoms number.')

    return aux_set(item.structures, indices=indices, structure_indices=structure_indices,
                value=value, skip_digestion=True)

@digest(form=form)
def set_b_factor_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Structures import set_b_factor_to_atom as aux_set

    return aux_set(item.structures, indices=indices, structure_indices=structure_indices, value=value, skip_digestion=True)

@digest(form=form)
def set_occupancy_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Structures import set_occupancy_to_atom as aux_set

    return aux_set(item.structures, indices=indices, structure_indices=structure_indices, value=value, skip_digestion=True)

## Group

@digest(form=form)
def set_group_index_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_group_index_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_group_name_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_group_name_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_group_id_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_group_id_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_group_type_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_group_type_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_component_index_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_component_index_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_component_name_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_component_name_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_component_id_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_component_id_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_component_type_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_component_type_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_index_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_index_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_name_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_name_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_id_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_id_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_type_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_type_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_index_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_index_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_name_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_name_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_id_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_id_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_type_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_type_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_index_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_index_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_name_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_name_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_id_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_id_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_type_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_type_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

## Component

@digest(form=form)
def set_component_index_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_component_index_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_component_name_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_component_name_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_component_id_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_component_id_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_component_type_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_component_type_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_index_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_index_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_name_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_name_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_id_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_id_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_type_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_type_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_index_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_index_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_name_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_name_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_id_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_id_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_type_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_type_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_index_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_index_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_name_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_name_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_id_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_id_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_type_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_type_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

## Molecule

@digest(form=form)
def set_molecule_index_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_index_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_name_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_name_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_id_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_id_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_type_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_type_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_index_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_index_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_name_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_name_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_id_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_id_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_type_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_type_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_index_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_index_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_name_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_name_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_id_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_id_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_type_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_type_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

## Chain

@digest(form=form)
def set_molecule_index_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_index_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_name_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_name_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_id_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_id_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_molecule_type_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_molecule_type_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_index_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_index_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_name_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_name_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_id_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_id_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_chain_type_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_chain_type_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_index_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_index_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_name_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_name_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_id_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_id_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_type_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_type_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

## Entity

@digest(form=form)
def set_entity_index_to_entity(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_index_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_name_to_entity(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_name_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_id_to_entity(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_id_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@digest(form=form)
def set_entity_type_to_entity(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology import set_entity_type_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


###
### System
###

@digest(form=form)
def set_structure_id_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Structures import set_structure_id_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices,
                                                          value=value, skip_digestion=True)

@digest(form=form)
def set_time_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Structures import set_time_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices,
                                                  value=value, skip_digestion=True)

@digest(form=form)
def set_box_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Structures import set_box_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices,
                                                 value=value, skip_digestion=True)

@digest(form=form)
def set_coordinates_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value, skip_digestion=True)

# Mechanical

@digest(form=form)
def set_forcefield_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_forcefield_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_non_bonded_method_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_non_bonded_method_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_cutoff_distance_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_cutoff_distance_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_switch_distance_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_switch_distance_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_dispersion_correction_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_dispersion_correction_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_ewald_error_tolerance_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_ewald_error_tolerance_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_hydrogen_mass_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_hydrogen_mass_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_constraints_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_constraints_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_flexible_constraints_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_flexible_constraints_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_water_model_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_water_model_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_rigid_water_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_rigid_water_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_implicit_solvent_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_implicit_solvent_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_solute_dielectric_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_solute_dielectric_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_solvent_dielectric_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_solvent_dielectric_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_salt_concentration_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_salt_concentration_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@digest(form=form)
def set_kappa_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics import set_kappa_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

