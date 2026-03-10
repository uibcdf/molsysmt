from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='molsysmt.MolSys'

###### Set

## to atom

@arg_digest(form=form)
def set_atom_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_atom_index_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_atom_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_atom_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_atom_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_atom_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_atom_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_atom_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_group_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_group_index_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_group_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_group_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_group_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_group_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_group_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_group_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_component_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_component_index_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_component_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_component_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_component_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_component_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_component_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_component_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_index_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_index_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_index_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    from molsysmt.form.molsysmt_Structures.set import set_coordinates_to_atom as aux_set
    from molsysmt.form.molsysmt_Topology.get_topological_attributes import get_n_atoms_from_system as get_n_atoms_from_system

    if is_all(indices):
        n_atoms = get_n_atoms_from_system(item.topology, skip_digestion=True)
        if n_atoms!=value.shape[1]:
            raise ValueError('Coordinates has a different atoms number.')

    return aux_set(item.structures, indices=indices, structure_indices=structure_indices,
                value=value, skip_digestion=True)

@arg_digest(form=form)
def set_velocities_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    from molsysmt.form.molsysmt_Structures.set import set_velocities_to_atom as aux_set
    from molsysmt.form.molsysmt_Topology.get_topological_attributes import get_n_atoms_from_system as get_n_atoms_from_system

    if is_all(indices):
        n_atoms = get_n_atoms_from_system(item.topology, skip_digestion=True)
        if n_atoms!=value.shape[1]:
            raise ValueError('Coordinates has a different atoms number.')

    return aux_set(item.structures, indices=indices, structure_indices=structure_indices,
                value=value, skip_digestion=True)

@arg_digest(form=form)
def set_b_factor_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    from molsysmt.form.molsysmt_Structures.set import set_b_factor_to_atom as aux_set

    return aux_set(item.structures, indices=indices, structure_indices=structure_indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_occupancy_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    from molsysmt.form.molsysmt_Structures.set import set_occupancy_to_atom as aux_set

    return aux_set(item.structures, indices=indices, structure_indices=structure_indices, value=value, skip_digestion=True)

## Group

@arg_digest(form=form)
def set_group_index_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_group_index_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_group_name_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_group_name_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_group_id_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_group_id_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_group_type_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_group_type_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_component_index_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_component_index_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_component_name_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_component_name_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_component_id_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_component_id_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_component_type_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_component_type_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_index_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_index_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_name_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_name_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_id_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_id_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_type_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_type_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_index_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_index_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_name_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_name_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_id_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_id_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_type_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_type_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_index_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_index_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_name_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_name_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_id_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_id_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_type_to_group(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_type_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

## Component

@arg_digest(form=form)
def set_component_index_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_component_index_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_component_name_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_component_name_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_component_id_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_component_id_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_component_type_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_component_type_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_index_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_index_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_name_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_name_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_id_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_id_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_type_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_type_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_index_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_index_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_name_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_name_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_id_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_id_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_type_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_type_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_index_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_index_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_name_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_name_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_id_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_id_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_type_to_component(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_type_to_component as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

## Molecule

@arg_digest(form=form)
def set_molecule_index_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_index_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_name_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_name_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_id_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_id_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_type_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_type_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_index_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_index_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_name_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_name_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_id_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_id_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_type_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_type_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_index_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_index_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_name_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_name_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_id_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_id_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_type_to_molecule(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_type_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

## Chain

@arg_digest(form=form)
def set_molecule_index_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_index_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_name_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_name_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_id_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_id_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_molecule_type_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_molecule_type_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_index_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_index_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_name_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_name_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_id_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_id_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_chain_type_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_chain_type_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_index_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_index_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_name_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_name_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_id_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_id_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_type_to_chain(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_type_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

## Entity

@arg_digest(form=form)
def set_entity_index_to_entity(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_index_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_name_to_entity(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_name_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_id_to_entity(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_id_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_entity_type_to_entity(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_entity_type_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


###
### System
###

@arg_digest(form=form)
def set_structure_id_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Structures.set_structure_id_to_system import set_structure_id_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices,
                                                          value=value, skip_digestion=True)

@arg_digest(form=form)
def set_time_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Structures.set_time_to_system import set_time_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices,
                                                  value=value, skip_digestion=True)

@arg_digest(form=form)
def set_box_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Structures.set_box_to_system import set_box_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices,
                                                 value=value, skip_digestion=True)

@arg_digest(form=form)
def set_coordinates_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value, skip_digestion=True)

# Mechanical

@arg_digest(form=form)
def set_forcefield_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_forcefield_to_system import set_forcefield_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_non_bonded_method_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_non_bonded_method_to_system import set_non_bonded_method_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_cutoff_distance_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_cutoff_distance_to_system import set_cutoff_distance_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_switch_distance_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_switch_distance_to_system import set_switch_distance_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_dispersion_correction_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_dispersion_correction_to_system import set_dispersion_correction_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_ewald_error_tolerance_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_ewald_error_tolerance_to_system import set_ewald_error_tolerance_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_hydrogen_mass_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_hydrogen_mass_to_system import set_hydrogen_mass_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_constraints_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_constraints_to_system import set_constraints_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_flexible_constraints_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_flexible_constraints_to_system import set_flexible_constraints_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_water_model_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_water_model_to_system import set_water_model_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_rigid_water_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_rigid_water_to_system import set_rigid_water_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_implicit_solvent_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_implicit_solvent_to_system import set_implicit_solvent_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_solute_dielectric_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_solute_dielectric_to_system import set_solute_dielectric_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_solvent_dielectric_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_solvent_dielectric_to_system import set_solvent_dielectric_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_salt_concentration_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_salt_concentration_to_system import set_salt_concentration_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_kappa_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set_kappa_to_system import set_kappa_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)
