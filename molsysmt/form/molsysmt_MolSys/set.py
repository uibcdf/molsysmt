from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

###### Set

## Atom

@digest(form='molsysmt.MolSys')
def set_atom_name_to_atom(item, indices='all', value=None):

    from ..molsysmt_Topology import set_atom_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, structure_indices=structure_indices, value=value)

@digest(form='molsysmt.MolSys')
def set_atom_id_to_atom(item, indices='all', value=None):

    from ..molsysmt_Topology import set_atom_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value)

@digest(form='molsysmt.MolSys')
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None):

    from ..molsysmt_Structures import set_coordinates_to_atom as molsysmt_Structures_set_coordinates_to_atom
    from ..molsysmt_Topology import get_n_atoms_from_system as molsysmt_Topology_get_n_atoms_from_system

    if is_all(indices):
        n_atoms = molsysmt_Topology_get_n_atoms_from_system(item.topology)
        if n_atoms!=value.shape[1]:
            raise ValueError('Coordinates has a different atoms number.')

    return molsysmt_Structures_set_coordinates_to_atom(item.structures, indices=indices, structure_indices=structure_indices,
                value=value)

@digest(form='molsysmt.MolSys')
def set_b_factor_to_atom(item, indices='all', structure_indices='all', value=None):

    from ..molsysmt_Structures import set_b_factor_to_atom as aux_set

    return aux_set(item.structures, indices=indices, structure_indices=structure_indices, value=value)

@digest(form='molsysmt.MolSys')
def set_occupancy_to_atom(item, indices='all', structure_indices='all', value=None):

    from ..molsysmt_Structures import set_occupancy_to_atom as aux_set

    return aux_set(item.structures, indices=indices, structure_indices=structure_indices, value=value)

###
### System
###

@digest(form='molsysmt.MolSys')
def set_structure_id_to_system(item, structure_indices='all', value=None):

    from ..molsysmt_Structures import set_structure_id_to_system as molsysmt_Structures_set_structure_id_to_system

    return molsysmt_Structures_set_structure_id_to_system(item.structures, structure_indices=structure_indices, value=value)

@digest(form='molsysmt.MolSys')
def set_time_to_system(item, structure_indices='all', value=None):

    from ..molsysmt_Structures import set_time_to_system as molsysmt_Structures_set_time_to_system

    return molsysmt_Structures_set_time_to_system(item.structures, structure_indices=structure_indices, value=value)

@digest(form='molsysmt.MolSys')
def set_box_to_system(item, structure_indices='all', value=None):

    from ..molsysmt_Structures import set_box_to_system as molsysmt_Structures_set_box_to_system

    return molsysmt_Structures_set_box_to_system(item.structures, structure_indices=structure_indices, value=value)

@digest(form='molsysmt.MolSys')
def set_coordinates_to_system(item, structure_indices='all', value=None):

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value)

# Mechanical

@digest(form='molsysmt.MolSys')
def set_forcefield_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_forcefield_to_system as molsysmt_MolecularMechanics_set_forcefield_to_system

    return molsysmt_MolecularMechanics_set_forcefield_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_non_bonded_method_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_non_bonded_method_to_system as molsysmt_MolecularMechanics_set_non_bonded_method_to_system

    return molsysmt_MolecularMechanics_set_non_bonded_method_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_cutoff_distance_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_cutoff_distance_to_system as molsysmt_MolecularMechanics_set_cutoff_distance_to_system

    return molsysmt_MolecularMechanics_set_cutoff_distance_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_switch_distance_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_switch_distance_to_system as molsysmt_MolecularMechanics_set_switch_distance_to_system

    return molsysmt_MolecularMechanics_set_switch_distance_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_dispersion_correction_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_dispersion_correction_to_system as molsysmt_MolecularMechanics_set_dispersion_correction_to_system

    return molsysmt_MolecularMechanics_set_dispersion_correction_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_ewald_error_tolerance_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_ewald_error_tolerance_to_system as molsysmt_MolecularMechanics_set_ewald_error_tolerance_to_system

    return molsysmt_MolecularMechanics_set_ewald_error_tolerance_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_hydrogen_mass_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_hydrogen_mass_to_system as molsysmt_MolecularMechanics_set_hydrogen_mass_to_system

    return molsysmt_MolecularMechanics_set_hydrogen_mass_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_constraints_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_constraints_to_system as molsysmt_MolecularMechanics_set_constraints_to_system

    return molsysmt_MolecularMechanics_set_constraints_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_flexible_constraints_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_flexible_constraints_to_system as molsysmt_MolecularMechanics_set_flexible_constraints_to_system

    return molsysmt_MolecularMechanics_set_flexible_constraints_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_water_model_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_water_model_to_system as molsysmt_MolecularMechanics_set_water_model_to_system

    return molsysmt_MolecularMechanics_set_water_model_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_rigid_water_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_rigid_water_to_system as molsysmt_MolecularMechanics_set_rigid_water_to_system

    return molsysmt_MolecularMechanics_set_rigid_water_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_implicit_solvent_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_implicit_solvent_to_system as molsysmt_MolecularMechanics_set_implicit_solvent_to_system

    return molsysmt_MolecularMechanics_set_implicit_solvent_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_solute_dielectric_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_solute_dielectric_to_system as molsysmt_MolecularMechanics_set_solute_dielectric_to_system

    return molsysmt_MolecularMechanics_set_solute_dielectric_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_solvent_dielectric_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_solvent_dielectric_to_system as molsysmt_MolecularMechanics_set_solvent_dielectric_to_system

    return molsysmt_MolecularMechanics_set_solvent_dielectric_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_salt_concentration_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_salt_concentration_to_system as molsysmt_MolecularMechanics_set_salt_concentration_to_system

    return molsysmt_MolecularMechanics_set_salt_concentration_to_system(item.molecular_mechanics, value=value)

@digest(form='molsysmt.MolSys')
def set_kappa_to_system(item, value=None):

    from ..molsysmt_MolecularMechanics import set_kappa_to_system as molsysmt_MolecularMechanics_set_kappa_to_system

    return molsysmt_MolecularMechanics_set_kappa_to_system(item.molecular_mechanics, value=value)

















