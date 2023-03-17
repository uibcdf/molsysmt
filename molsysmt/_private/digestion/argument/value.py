from molsysmt._private.exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw



def digest_value(value, caller=None):

    if caller.endswith('set_coordinates_to_atom'):
        from .coordinates import digest_coordinates
        return digest_coordinates(value, caller=caller)

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
