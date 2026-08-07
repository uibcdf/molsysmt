from copy import copy

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
import types

form = 'molsysmt.StructuresDict'


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    coordinates = copy(item['coordinates'])

    if not is_all(structure_indices):
        if not is_all(indices):
            coordinates = coordinates[np.ix_(structure_indices, indices)]
        else:
            coordinates = coordinates[structure_indices, :, :]
    elif not is_all(indices):
        coordinates = coordinates[:, indices, :]

    return coordinates


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    if is_all(structure_indices):
        return item['coordinates'].shape[0]
    return len(structure_indices)


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):
    coordinates = copy(item['coordinates'])
    if is_all(structure_indices):
        return coordinates
    return coordinates[structure_indices, :, :]


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    box = item.get('box', None)
    if box is None:
        return None

    box = copy(box)
    if is_all(structure_indices):
        return box
    return box[structure_indices, :, :]




@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):
    structure_id = item.get('structure_id', None)
    if structure_id is None:
        return None

    structure_id = copy(structure_id)
    if is_all(structure_indices):
        return structure_id
    return structure_id[structure_indices]


@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    velocities = item.get('velocities', None)
    if velocities is None or indices is None or structure_indices is None:
        return None

    velocities = copy(velocities)
    if not is_all(structure_indices):
        velocities = velocities[structure_indices, :, :]
    if not is_all(indices):
        velocities = velocities[:, indices, :]
    return velocities


@arg_digest(form=form)
def get_velocities_from_system(item, structure_indices='all', skip_digestion=False):
    return get_velocities_from_atom(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )


@arg_digest(form=form)
def get_b_factor_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    b_factor = item.get('b_factor', None)
    if b_factor is None:
        return None

    b_factor = copy(b_factor)
    if not is_all(structure_indices):
        b_factor = b_factor[structure_indices, :]
    if not is_all(indices):
        b_factor = b_factor[:, indices]
    return b_factor


@arg_digest(form=form)
def get_occupancy_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    occupancy = item.get('occupancy', None)
    if occupancy is None or indices is None or structure_indices is None:
        return None

    occupancy = copy(occupancy)
    if not is_all(structure_indices):
        occupancy = occupancy[structure_indices, :]
    if not is_all(indices):
        occupancy = occupancy[:, indices]
    return occupancy


@arg_digest(form=form)
def get_alternate_location_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    alternate_location = item.get('alternate_location', None)
    if alternate_location is None or indices is None or structure_indices is None:
        return None

    alternate_location = copy(alternate_location)
    if not is_all(indices):
        selected = []
        for locations in alternate_location:
            selected.append({index: locations[index] for index in indices if index in locations})
        alternate_location = selected
    if not is_all(structure_indices):
        alternate_location = [alternate_location[index] for index in structure_indices]
    return alternate_location


@arg_digest(form=form)
def get_b_factor_from_system(item, structure_indices='all', skip_digestion=False):
    return get_b_factor_from_atom(item, structure_indices=structure_indices, skip_digestion=True)


@arg_digest(form=form)
def get_alternate_location_from_system(item, structure_indices='all', skip_digestion=False):
    return get_alternate_location_from_atom(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
    time = item.get('time', None)
    if time is None:
        return None

    return _get_structure_series(time, structure_indices)


def _get_structure_series(value, structure_indices):
    if structure_indices is None or value is None:
        return None
    value = copy(value)
    if is_all(structure_indices):
        return value
    return value[structure_indices]


@arg_digest(form=form)
def get_temperature_from_system(item, structure_indices='all', skip_digestion=False):
    return _get_structure_series(item.get('temperature'), structure_indices)


@arg_digest(form=form)
def get_potential_energy_from_system(item, structure_indices='all', skip_digestion=False):
    return _get_structure_series(item.get('potential_energy'), structure_indices)


@arg_digest(form=form)
def get_kinetic_energy_from_system(item, structure_indices='all', skip_digestion=False):
    return _get_structure_series(item.get('kinetic_energy'), structure_indices)


@arg_digest(form=form)
def get_total_energy_from_system(item, structure_indices='all', skip_digestion=False):
    potential_energy = get_potential_energy_from_system(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    kinetic_energy = get_kinetic_energy_from_system(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    if potential_energy is None or kinetic_energy is None:
        return None
    return potential_energy + kinetic_energy


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
