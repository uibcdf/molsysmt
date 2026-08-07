from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='molsysmt.MolSys'

###### Set

## to atom

def _set_atom_state_attribute(item, attribute, indices, value):
    if attribute == 'formal_charge' and puw.is_quantity(value):
        value = puw.get_value(value, to_unit='elementary_charge')
    native_attribute = {
        'formal_charge': 'formal_charge',
        'atom_is_aromatic': 'is_aromatic',
        'n_unpaired_electrons': 'n_unpaired_electrons',
        'n_implicit_hydrogens': 'n_implicit_hydrogens',
        'allows_implicit_hydrogens': 'allows_implicit_hydrogens',
        'atom_stereochemistry': 'stereochemistry',
    }[attribute]
    atom_indices = None if is_all(indices) else indices
    item.topology._set_chemical_state_atom_attribute(
        native_attribute, value, atom_indices=atom_indices
    )
    if attribute == 'formal_charge':
        item.molecular_mechanics.formal_charge = None


@arg_digest(form=form)
def set_formal_charge_to_atom(item, indices='all', value=None, skip_digestion=False):
    return _set_atom_state_attribute(item, 'formal_charge', indices, value)


@arg_digest(form=form)
def set_atom_is_aromatic_to_atom(item, indices='all', value=None, skip_digestion=False):
    return _set_atom_state_attribute(item, 'atom_is_aromatic', indices, value)


@arg_digest(form=form)
def set_n_unpaired_electrons_to_atom(item, indices='all', value=None, skip_digestion=False):
    return _set_atom_state_attribute(item, 'n_unpaired_electrons', indices, value)


@arg_digest(form=form)
def set_n_implicit_hydrogens_to_atom(item, indices='all', value=None, skip_digestion=False):
    return _set_atom_state_attribute(item, 'n_implicit_hydrogens', indices, value)


@arg_digest(form=form)
def set_allows_implicit_hydrogens_to_atom(item, indices='all', value=None, skip_digestion=False):
    return _set_atom_state_attribute(item, 'allows_implicit_hydrogens', indices, value)


@arg_digest(form=form)
def set_atom_stereochemistry_to_atom(item, indices='all', value=None, skip_digestion=False):
    return _set_atom_state_attribute(item, 'atom_stereochemistry', indices, value)


def _set_bond_state_attribute(item, attribute, indices, value):
    """Delegate a canonical bond-state assignment to the native topology."""

    from importlib import import_module

    topology_set = import_module('molsysmt.form.molsysmt_Topology.set')
    function = getattr(topology_set, f'set_{attribute}_to_bond')
    return function(
        item.topology, indices=indices, value=value, skip_digestion=True
    )


@arg_digest(form=form)
def set_bond_id_to_bond(item, indices='all', value=None, skip_digestion=False):
    return _set_bond_state_attribute(item, 'bond_id', indices, value)


@arg_digest(form=form)
def set_bond_order_to_bond(item, indices='all', value=None, skip_digestion=False):
    return _set_bond_state_attribute(item, 'bond_order', indices, value)


@arg_digest(form=form)
def set_fractional_bond_order_to_bond(item, indices='all', value=None, skip_digestion=False):
    return _set_bond_state_attribute(item, 'fractional_bond_order', indices, value)


@arg_digest(form=form)
def set_bond_type_to_bond(item, indices='all', value=None, skip_digestion=False):
    return _set_bond_state_attribute(item, 'bond_type', indices, value)


@arg_digest(form=form)
def set_bond_is_aromatic_to_bond(item, indices='all', value=None, skip_digestion=False):
    return _set_bond_state_attribute(item, 'bond_is_aromatic', indices, value)


@arg_digest(form=form)
def set_bond_is_conjugated_to_bond(item, indices='all', value=None, skip_digestion=False):
    return _set_bond_state_attribute(item, 'bond_is_conjugated', indices, value)


@arg_digest(form=form)
def set_bond_stereochemistry_to_bond(item, indices='all', value=None, skip_digestion=False):
    return _set_bond_state_attribute(item, 'bond_stereochemistry', indices, value)


@arg_digest(form=form)
def set_bond_stereo_atom_indices_to_bond(item, indices='all', value=None, skip_digestion=False):
    return _set_bond_state_attribute(item, 'bond_stereo_atom_indices', indices, value)


@arg_digest(form=form)
def set_bond_donor_atom_index_to_bond(item, indices='all', value=None, skip_digestion=False):
    return _set_bond_state_attribute(item, 'bond_donor_atom_index', indices, value)


@arg_digest(form=form)
def set_bond_acceptor_atom_index_to_bond(item, indices='all', value=None, skip_digestion=False):
    return _set_bond_state_attribute(item, 'bond_acceptor_atom_index', indices, value)


@arg_digest(form=form)
def set_bond_joins_components_to_bond(item, indices='all', value=None, skip_digestion=False):
    return _set_bond_state_attribute(item, 'bond_joins_components', indices, value)


@arg_digest(form=form)
def set_bond_evidence_to_bond(item, indices='all', value=None, skip_digestion=False):
    return _set_bond_state_attribute(item, 'bond_evidence', indices, value)

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
def set_isotope_to_atom(item, indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Topology.set import set_isotope_to_atom as aux_set
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
            raise StructuralInconsistencyError("Coordinates mismatch with number of atoms", caller="molsysmt.form.molsysmt_MolSys.set")

    return aux_set(item.structures, indices=indices, structure_indices=structure_indices,
                value=value, skip_digestion=True)

@arg_digest(form=form)
def set_velocities_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    from molsysmt.form.molsysmt_Structures.set import set_velocities_to_atom as aux_set
    from molsysmt.form.molsysmt_Topology.get_topological_attributes import get_n_atoms_from_system as get_n_atoms_from_system

    if is_all(indices):
        n_atoms = get_n_atoms_from_system(item.topology, skip_digestion=True)
        if n_atoms!=value.shape[1]:
            raise StructuralInconsistencyError("Coordinates mismatch with number of atoms", caller="molsysmt.form.molsysmt_MolSys.set")

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

    from ..molsysmt_Structures.set import set_structure_id_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices,
                                                          value=value, skip_digestion=True)


@arg_digest(form=form)
def set_structure_chemical_state_index_to_system(
    item, structure_indices='all', value=None, skip_digestion=False
):
    """Setting nullable chemical-state indices aligned to structures."""

    return item._set_structure_chemical_state_indices(
        value, structure_indices=structure_indices
    )

@arg_digest(form=form)
def set_time_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Structures.set import set_time_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices,
                                                  value=value, skip_digestion=True)

@arg_digest(form=form)
def set_box_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    from ..molsysmt_Structures.set import set_box_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices,
                                                 value=value, skip_digestion=True)

@arg_digest(form=form)
def set_coordinates_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value, skip_digestion=True)

# Mechanical

@arg_digest(form=form)
def set_forcefield_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_forcefield_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_non_bonded_method_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_non_bonded_method_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_cutoff_distance_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_cutoff_distance_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_switch_distance_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_switch_distance_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_dispersion_correction_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_dispersion_correction_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_ewald_error_tolerance_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_ewald_error_tolerance_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_hydrogen_mass_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_hydrogen_mass_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_constraints_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_constraints_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_flexible_constraints_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_flexible_constraints_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_water_model_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_water_model_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_rigid_water_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_rigid_water_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_implicit_solvent_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_implicit_solvent_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_solute_dielectric_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_solute_dielectric_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_solvent_dielectric_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_solvent_dielectric_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_salt_concentration_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_salt_concentration_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)

@arg_digest(form=form)
def set_kappa_to_system(item, value=None, skip_digestion=False):

    from ..molsysmt_MolecularMechanics.set import set_kappa_to_system as aux_set

    return aux_set(item.molecular_mechanics, value=value, skip_digestion=True)
