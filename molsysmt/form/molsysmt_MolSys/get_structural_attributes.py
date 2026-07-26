from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
import types

form = 'molsysmt.MolSys'


#######################################################################
#                 To be customized for each form                      #
#######################################################################


# From atom


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_coordinates_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_velocities_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_occupancy_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_occupancy_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_alternate_location_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_alternate_location_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_b_factor_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_b_factor_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices, skip_digestion=True)


# From system


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_coordinates_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_velocities_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_velocities_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_box_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_box_shape_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_box_shape_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_box_lengths_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_box_angles_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_box_angles_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_box_volume_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_box_volume_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_time_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_temperature_from_system(item, structure_indices='all', skip_digestion=False):
    from molsysmt.form.molsysmt_Structures import get_temperature_from_system as aux_get

    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_potential_energy_from_system(item, structure_indices='all', skip_digestion=False):
    from molsysmt.form.molsysmt_Structures import get_potential_energy_from_system as aux_get

    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_kinetic_energy_from_system(item, structure_indices='all', skip_digestion=False):
    from molsysmt.form.molsysmt_Structures import get_kinetic_energy_from_system as aux_get

    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_total_energy_from_system(item, structure_indices='all', skip_digestion=False):
    from molsysmt.form.molsysmt_Structures import get_total_energy_from_system as aux_get

    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_structure_id_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_structure_index_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_structure_index_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_structure_chemical_state_index_from_system(
    item, structure_indices='all', skip_digestion=False
):
    """Getting resolved chemical-state indices aligned to structures."""

    return item._get_structure_chemical_state_indices(
        structure_indices=structure_indices, resolved=True
    ).tolist()

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_n_structures_from_system as aux_get
    return aux_get(item.structures, structure_indices='all', skip_digestion=True)

@arg_digest(form=form)
def get_occupancy_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_occupancy_from_system as aux_get
    return aux_get(item.structures, structure_indices='all', skip_digestion=True)

@arg_digest(form=form)
def get_b_factor_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_b_factor_from_system as aux_get
    return aux_get(item.structures, structure_indices='all', skip_digestion=True)

@arg_digest(form=form)
def get_alternate_location_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_alternate_location_from_system as aux_get
    return aux_get(item.structures, structure_indices='all', skip_digestion=True)

@arg_digest(form=form)
def get_bioassembly_from_system(item, skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_bioassembly_from_system as aux_get
    return aux_get(item.structures, skip_digestion=True)

@arg_digest(form=form)
def get_n_bioassemblies_from_system(item, skip_digestion=False):

    from molsysmt.form.molsysmt_Structures import get_n_bioassemblies_from_system as aux_get
    return aux_get(item.structures, skip_digestion=True)


# List of functions to be imported


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
