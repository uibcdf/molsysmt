from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw



def digest_value(value, caller=None):

    # Atom

    if caller.endswith('_to_atom'):

        if caller.endswith('set_atom_index_to_atom'):
            from .atom_index import digest_atom_index
            return digest_atom_index(value, caller=caller)

        if caller.endswith('set_atom_name_to_atom'):
            from .atom_name import digest_atom_name
            return digest_atom_name(value, caller=caller)

        if caller.endswith('set_atom_id_to_atom'):
            from .atom_id import digest_atom_id
            return digest_atom_id(value, caller=caller)

        if caller.endswith('set_atom_type_to_atom'):
            from .atom_type import digest_atom_type
            return digest_atom_type(value, caller=caller)

        if caller.endswith('set_group_index_to_atom'):
            from .group_index import digest_group_index
            return digest_group_index(value, caller=caller)

        if caller.endswith('set_group_name_to_atom'):
            from .group_name import digest_group_name
            return digest_group_name(value, caller=caller)

        if caller.endswith('set_group_id_to_atom'):
            from .group_id import digest_group_id
            return digest_group_id(value, caller=caller)

        if caller.endswith('set_group_type_to_atom'):
            from .group_type import digest_group_type
            return digest_group_type(value, caller=caller)

        if caller.endswith('set_component_index_to_atom'):
            from .component_index import digest_component_index
            return digest_component_index(value, caller=caller)

        if caller.endswith('set_component_name_to_atom'):
            from .component_name import digest_component_name
            return digest_component_name(value, caller=caller)

        if caller.endswith('set_component_id_to_atom'):
            from .component_id import digest_component_id
            return digest_component_id(value, caller=caller)

        if caller.endswith('set_component_type_to_atom'):
            from .component_type import digest_component_type
            return digest_component_type(value, caller=caller)

        if caller.endswith('set_molecule_index_to_atom'):
            from .molecule_index import digest_molecule_index
            return digest_molecule_index(value, caller=caller)

        if caller.endswith('set_molecule_name_to_atom'):
            from .molecule_name import digest_molecule_name
            return digest_molecule_name(value, caller=caller)

        if caller.endswith('set_molecule_id_to_atom'):
            from .molecule_id import digest_molecule_id
            return digest_molecule_id(value, caller=caller)

        if caller.endswith('set_molecule_type_to_atom'):
            from .molecule_type import digest_molecule_type
            return digest_molecule_type(value, caller=caller)

        if caller.endswith('set_chain_index_to_atom'):
            from .chain_index import digest_chain_index
            return digest_chain_index(value, caller=caller)

        if caller.endswith('set_chain_name_to_atom'):
            from .chain_name import digest_chain_name
            return digest_chain_name(value, caller=caller)

        if caller.endswith('set_chain_id_to_atom'):
            from .chain_id import digest_chain_id
            return digest_chain_id(value, caller=caller)

        if caller.endswith('set_chain_type_to_atom'):
            from .chain_type import digest_chain_type
            return digest_chain_type(value, caller=caller)

        if caller.endswith('set_entity_index_to_atom'):
            from .entity_index import digest_entity_index
            return digest_entity_index(value, caller=caller)

        if caller.endswith('set_entity_name_to_atom'):
            from .entity_name import digest_entity_name
            return digest_entity_name(value, caller=caller)

        if caller.endswith('set_entity_id_to_atom'):
            from .entity_id import digest_entity_id
            return digest_entity_id(value, caller=caller)

        if caller.endswith('set_entity_type_to_atom'):
            from .entity_type import digest_entity_type
            return digest_entity_type(value, caller=caller)

        if caller.endswith('set_coordinates_to_atom'):
            from .coordinates import digest_coordinates
            return digest_coordinates(value, caller=caller)

        if caller.endswith('set_occupancy_to_atom'):
            from .occupancy import digest_occupancy
            return digest_occupancy(value, caller=caller)

        if caller.endswith('set_b_factor_to_atom'):
            from .b_factor import digest_b_factor
            return digest_b_factor(value, caller=caller)

    # Group

    if caller.endswith('_to_group'):

        if caller.endswith('set_group_index_to_group'):
            from .group_index import digest_group_index
            return digest_group_index(value, caller=caller)

        if caller.endswith('set_group_name_to_group'):
            from .group_name import digest_group_name
            return digest_group_name(value, caller=caller)

        if caller.endswith('set_group_id_to_group'):
            from .group_id import digest_group_id
            return digest_group_id(value, caller=caller)

        if caller.endswith('set_group_type_to_group'):
            from .group_type import digest_group_type
            return digest_group_type(value, caller=caller)

        if caller.endswith('set_component_index_to_group'):
            from .component_index import digest_component_index
            return digest_component_index(value, caller=caller)

        if caller.endswith('set_component_name_to_group'):
            from .component_name import digest_component_name
            return digest_component_name(value, caller=caller)

        if caller.endswith('set_component_id_to_group'):
            from .component_id import digest_component_id
            return digest_component_id(value, caller=caller)

        if caller.endswith('set_component_type_to_group'):
            from .component_type import digest_component_type
            return digest_component_type(value, caller=caller)

        if caller.endswith('set_molecule_index_to_group'):
            from .molecule_index import digest_molecule_index
            return digest_molecule_index(value, caller=caller)

        if caller.endswith('set_molecule_name_to_group'):
            from .molecule_name import digest_molecule_name
            return digest_molecule_name(value, caller=caller)

        if caller.endswith('set_molecule_id_to_group'):
            from .molecule_id import digest_molecule_id
            return digest_molecule_id(value, caller=caller)

        if caller.endswith('set_molecule_type_to_group'):
            from .molecule_type import digest_molecule_type
            return digest_molecule_type(value, caller=caller)

        if caller.endswith('set_chain_index_to_group'):
            from .chain_index import digest_chain_index
            return digest_chain_index(value, caller=caller)

        if caller.endswith('set_chain_name_to_group'):
            from .chain_name import digest_chain_name
            return digest_chain_name(value, caller=caller)

        if caller.endswith('set_chain_id_to_group'):
            from .chain_id import digest_chain_id
            return digest_chain_id(value, caller=caller)

        if caller.endswith('set_chain_type_to_group'):
            from .chain_type import digest_chain_type
            return digest_chain_type(value, caller=caller)

        if caller.endswith('set_entity_index_to_group'):
            from .entity_index import digest_entity_index
            return digest_entity_index(value, caller=caller)

        if caller.endswith('set_entity_name_to_group'):
            from .entity_name import digest_entity_name
            return digest_entity_name(value, caller=caller)

        if caller.endswith('set_entity_id_to_group'):
            from .entity_id import digest_entity_id
            return digest_entity_id(value, caller=caller)

        if caller.endswith('set_entity_type_to_group'):
            from .entity_type import digest_entity_type
            return digest_entity_type(value, caller=caller)

    # Component

    if caller.endswith('_to_component'):

        if caller.endswith('set_component_index_to_component'):
            from .component_index import digest_component_index
            return digest_component_index(value, caller=caller)

        if caller.endswith('set_component_name_to_component'):
            from .component_name import digest_component_name
            return digest_component_name(value, caller=caller)

        if caller.endswith('set_component_id_to_component'):
            from .component_id import digest_component_id
            return digest_component_id(value, caller=caller)

        if caller.endswith('set_component_type_to_component'):
            from .component_type import digest_component_type
            return digest_component_type(value, caller=caller)

        if caller.endswith('set_molecule_index_to_component'):
            from .molecule_index import digest_molecule_index
            return digest_molecule_index(value, caller=caller)

        if caller.endswith('set_molecule_name_to_component'):
            from .molecule_name import digest_molecule_name
            return digest_molecule_name(value, caller=caller)

        if caller.endswith('set_molecule_id_to_component'):
            from .molecule_id import digest_molecule_id
            return digest_molecule_id(value, caller=caller)

        if caller.endswith('set_molecule_type_to_component'):
            from .molecule_type import digest_molecule_type
            return digest_molecule_type(value, caller=caller)

        if caller.endswith('set_chain_index_to_component'):
            from .chain_index import digest_chain_index
            return digest_chain_index(value, caller=caller)

        if caller.endswith('set_chain_name_to_component'):
            from .chain_name import digest_chain_name
            return digest_chain_name(value, caller=caller)

        if caller.endswith('set_chain_id_to_component'):
            from .chain_id import digest_chain_id
            return digest_chain_id(value, caller=caller)

        if caller.endswith('set_chain_type_to_component'):
            from .chain_type import digest_chain_type
            return digest_chain_type(value, caller=caller)

        if caller.endswith('set_entity_index_to_component'):
            from .entity_index import digest_entity_index
            return digest_entity_index(value, caller=caller)

        if caller.endswith('set_entity_name_to_component'):
            from .entity_name import digest_entity_name
            return digest_entity_name(value, caller=caller)

        if caller.endswith('set_entity_id_to_component'):
            from .entity_id import digest_entity_id
            return digest_entity_id(value, caller=caller)

        if caller.endswith('set_entity_type_to_component'):
            from .entity_type import digest_entity_type
            return digest_entity_type(value, caller=caller)

    # Molecule

    if caller.endswith('_to_molecule'):

        if caller.endswith('set_molecule_index_to_molecule'):
            from .molecule_index import digest_molecule_index
            return digest_molecule_index(value, caller=caller)

        if caller.endswith('set_molecule_name_to_molecule'):
            from .molecule_name import digest_molecule_name
            return digest_molecule_name(value, caller=caller)

        if caller.endswith('set_molecule_id_to_molecule'):
            from .molecule_id import digest_molecule_id
            return digest_molecule_id(value, caller=caller)

        if caller.endswith('set_molecule_type_to_molecule'):
            from .molecule_type import digest_molecule_type
            return digest_molecule_type(value, caller=caller)

        if caller.endswith('set_chain_index_to_molecule'):
            from .chain_index import digest_chain_index
            return digest_chain_index(value, caller=caller)

        if caller.endswith('set_chain_name_to_molecule'):
            from .chain_name import digest_chain_name
            return digest_chain_name(value, caller=caller)

        if caller.endswith('set_chain_id_to_molecule'):
            from .chain_id import digest_chain_id
            return digest_chain_id(value, caller=caller)

        if caller.endswith('set_chain_type_to_molecule'):
            from .chain_type import digest_chain_type
            return digest_chain_type(value, caller=caller)

        if caller.endswith('set_entity_index_to_molecule'):
            from .entity_index import digest_entity_index
            return digest_entity_index(value, caller=caller)

        if caller.endswith('set_entity_name_to_molecule'):
            from .entity_name import digest_entity_name
            return digest_entity_name(value, caller=caller)

        if caller.endswith('set_entity_id_to_molecule'):
            from .entity_id import digest_entity_id
            return digest_entity_id(value, caller=caller)

        if caller.endswith('set_entity_type_to_molecule'):
            from .entity_type import digest_entity_type
            return digest_entity_type(value, caller=caller)

    # Chain

    if caller.endswith('_to_chain'):

        if caller.endswith('set_chain_index_to_chain'):
            from .chain_index import digest_chain_index
            return digest_chain_index(value, caller=caller)

        if caller.endswith('set_chain_name_to_chain'):
            from .chain_name import digest_chain_name
            return digest_chain_name(value, caller=caller)

        if caller.endswith('set_chain_id_to_chain'):
            from .chain_id import digest_chain_id
            return digest_chain_id(value, caller=caller)

        if caller.endswith('set_chain_type_to_chain'):
            from .chain_type import digest_chain_type
            return digest_chain_type(value, caller=caller)

        if caller.endswith('set_entity_index_to_chain'):
            from .entity_index import digest_entity_index
            return digest_entity_index(value, caller=caller)

        if caller.endswith('set_entity_name_to_chain'):
            from .entity_name import digest_entity_name
            return digest_entity_name(value, caller=caller)

        if caller.endswith('set_entity_id_to_chain'):
            from .entity_id import digest_entity_id
            return digest_entity_id(value, caller=caller)

        if caller.endswith('set_entity_type_to_chain'):
            from .entity_type import digest_entity_type
            return digest_entity_type(value, caller=caller)

    # Entity

    if caller.endswith('_to_entity'):

        if caller.endswith('set_entity_index_to_entity'):
            from .entity_index import digest_entity_index
            return digest_entity_index(value, caller=caller)

        if caller.endswith('set_entity_name_to_entity'):
            from .entity_name import digest_entity_name
            return digest_entity_name(value, caller=caller)

        if caller.endswith('set_entity_id_to_entity'):
            from .entity_id import digest_entity_id
            return digest_entity_id(value, caller=caller)

        if caller.endswith('set_entity_type_to_entity'):
            from .entity_type import digest_entity_type
            return digest_entity_type(value, caller=caller)


    # System

    if caller.endswith('_to_system'):

        if caller.endswith('set_structure_id_to_system'):
            from .structure_id import digest_structure_id
            return digest_structure_id(value, caller=caller)

        if caller.endswith('set_time_to_system'):
            from .time import digest_time
            return digest_time(value, caller=caller)

        if caller.endswith('set_box_to_system'):
            from .box import digest_box
            return digest_box(value, caller=caller)

        if caller.endswith('set_coordinates_to_system'):
            from .coordinates import digest_coordinates
            return digest_coordinates(value, caller=caller)

        if caller.endswith('set_forcefield_to_system'):
            from .forcefield import digest_forcefield
            return digest_forcefield(value, caller=caller)

        if caller.endswith('set_non_bonded_method_to_system'):
            from .non_bonded_method import digest_non_bonded_method
            return digest_non_bonded_method(value, caller=caller)

        if caller.endswith('set_cutoff_distance_to_system'):
            from .cutoff_distance import digest_cutoff_distance
            return digest_cutoff_distance(value, caller=caller)

        if caller.endswith('set_switch_distance_to_system'):
            from .switch_distance import digest_switch_distance
            return digest_switch_distance(value, caller=caller)

        if caller.endswith('set_dispersion_correction_to_system'):
            from .dispersion_correction import digest_dispersion_correction
            return digest_dispersion_correction(value, caller=caller)

        if caller.endswith('set_ewald_error_tolerance_to_system'):
            from .ewald_error_tolerance import digest_ewald_error_tolerance
            return digest_ewald_error_tolerance(value, caller=caller)

        if caller.endswith('set_hydrogen_mass_to_system'):
            from .hydrogen_mass import digest_hydrogen_mass
            return digest_hydrogen_mass(value, caller=caller)

        if caller.endswith('set_constraints_to_system'):
            from .constraints import digest_constraints
            return digest_constraints(value, caller=caller)

        if caller.endswith('set_flexible_constraints_to_system'):
            from .flexible_constraints import digest_flexible_constraints
            return digest_flexible_constraints(value, caller=caller)

        if caller.endswith('set_water_model_to_system'):
            from .water_model import digest_water_model
            return digest_water_model(value, caller=caller)

        if caller.endswith('set_rigid_water_to_system'):
            from .rigid_water import digest_rigid_water
            return digest_rigid_water(value, caller=caller)

        if caller.endswith('set_implicit_solvent_to_system'):
            from .implicit_solvent import digest_implicit_solvent
            return digest_implicit_solvent(value, caller=caller)

        if caller.endswith('set_solute_dielectric_to_system'):
            from .solute_dielectric import digest_solute_dielectric
            return digest_solute_dielectric(value, caller=caller)

        if caller.endswith('set_solvent_dielectric_to_system'):
            from .solvent_dielectric import digest_solvent_dielectric
            return digest_solvent_dielectric(value, caller=caller)

        if caller.endswith('set_salt_concentration_to_system'):
            from .salt_concentration import digest_salt_concentration
            return digest_salt_concentration(value, caller=caller)

        if caller.endswith('set_kappa_to_system'):
            from .kappa import digest_kappa
            return digest_kappa(value, caller=caller)



















    if caller.endswith('set_constraints_to_system'):
        from .coordinates import digest_constraints
        return digest_constraints(value, caller=caller)

    if value is not None:
        if puw.is_quantity(value):
            return puw.standardize(value)

    raise ArgumentError('value', value=value, caller=caller, message=None)
